"""
LLM API Integration Pipeline
Integrates OpenAI and Claude APIs for automated text processing workflows.
Author: Azahid García | github.com/azahidgarcia
"""

import os
import json
import csv
from datetime import datetime
from pathlib import Path


# ── Configuration ──────────────────────────────────────────────
INPUT_FILE    = "data/input/customer_feedback.csv"
OUTPUT_FOLDER = "data/output"
LOG_FOLDER    = "logs"

# Set your API key as environment variable:
# export ANTHROPIC_API_KEY="your-key-here"
# export OPENAI_API_KEY="your-key-here"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY    = os.getenv("OPENAI_API_KEY", "")

# Choose provider: "claude" or "openai"
PROVIDER = "claude"


# ── Prompt Engineering ─────────────────────────────────────────
SYSTEM_PROMPT = """
You are a data analyst specialized in customer feedback analysis.
Your job is to analyze customer feedback and return structured JSON.
Always respond ONLY with valid JSON — no preamble, no explanation.
"""

def build_prompt(feedback_text: str) -> str:
    """Build a structured prompt for feedback analysis."""
    return f"""
Analyze the following customer feedback and return a JSON object with:
- sentiment: "positive", "neutral", or "negative"
- score: integer from 1 (very negative) to 5 (very positive)
- topics: list of main topics mentioned (max 3)
- summary: one sentence summary (max 20 words)
- action_required: true or false

Customer feedback:
\"\"\"{feedback_text}\"\"\"

Respond with valid JSON only.
"""


# ── API Clients ────────────────────────────────────────────────
def call_claude(prompt: str) -> dict:
    """Call Anthropic Claude API."""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=512,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = message.content[0].text.strip()
        return json.loads(raw)
    except ImportError:
        print("   ⚠ anthropic package not installed. Run: pip install anthropic")
        return mock_response()
    except Exception as e:
        print(f"   ⚠ Claude API error: {e}")
        return mock_response()


def call_openai(prompt: str) -> dict:
    """Call OpenAI GPT API."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": prompt}
            ],
            max_tokens=512,
            temperature=0.2,
        )
        raw = response.choices[0].message.content.strip()
        return json.loads(raw)
    except ImportError:
        print("   ⚠ openai package not installed. Run: pip install openai")
        return mock_response()
    except Exception as e:
        print(f"   ⚠ OpenAI API error: {e}")
        return mock_response()


def mock_response() -> dict:
    """Return a mock response for demo purposes (no API key needed)."""
    return {
        "sentiment":        "positive",
        "score":            4,
        "topics":           ["product quality", "delivery", "customer service"],
        "summary":          "Customer is satisfied with product quality and fast delivery.",
        "action_required":  False,
        "_mock":            True
    }


def analyze_feedback(feedback_text: str) -> dict:
    """Route to the correct LLM provider."""
    prompt = build_prompt(feedback_text)
    if PROVIDER == "claude":
        return call_claude(prompt)
    elif PROVIDER == "openai":
        return call_openai(prompt)
    else:
        raise ValueError(f"Unknown provider: {PROVIDER}")


# ── Data Processing ────────────────────────────────────────────
def load_feedback(filepath: str) -> list[dict]:
    """Load feedback CSV file."""
    rows = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    print(f"📂 Loaded {len(rows)} feedback record(s) from {filepath}")
    return rows


def process_all(records: list[dict]) -> list[dict]:
    """Run LLM analysis on each feedback record."""
    results = []
    for i, record in enumerate(records, 1):
        feedback_id   = record.get("id", i)
        feedback_text = record.get("feedback", "")
        print(f"   [{i}/{len(records)}] Analyzing record #{feedback_id}...")

        analysis = analyze_feedback(feedback_text)

        results.append({
            "id":              feedback_id,
            "feedback":        feedback_text,
            "sentiment":       analysis.get("sentiment"),
            "score":           analysis.get("score"),
            "topics":          ", ".join(analysis.get("topics", [])),
            "summary":         analysis.get("summary"),
            "action_required": analysis.get("action_required"),
            "mock":            analysis.get("_mock", False),
            "processed_at":    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })

    return results


# ── Export ─────────────────────────────────────────────────────
def export_results(results: list[dict]) -> None:
    """Save results to CSV and summary to JSON."""
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(LOG_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # CSV output
    csv_path = os.path.join(OUTPUT_FOLDER, f"analyzed_feedback_{timestamp}.csv")
    if results:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        print(f"\n✅ Results saved to  : {csv_path}")

    # Summary JSON
    sentiments = [r["sentiment"] for r in results]
    scores     = [r["score"] for r in results if r["score"] is not None]
    summary = {
        "generated_at":     datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "provider":         PROVIDER,
        "records_processed": len(results),
        "sentiment_counts": {
            "positive": sentiments.count("positive"),
            "neutral":  sentiments.count("neutral"),
            "negative": sentiments.count("negative"),
        },
        "average_score":    round(sum(scores) / len(scores), 2) if scores else None,
        "actions_required": sum(1 for r in results if r["action_required"]),
    }
    log_path = os.path.join(LOG_FOLDER, f"summary_{timestamp}.json")
    with open(log_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"✅ Summary saved to  : {log_path}")

    # Print summary
    print(f"\n📊 Analysis Summary:")
    print(f"   Records processed : {summary['records_processed']}")
    print(f"   Positive          : {summary['sentiment_counts']['positive']}")
    print(f"   Neutral           : {summary['sentiment_counts']['neutral']}")
    print(f"   Negative          : {summary['sentiment_counts']['negative']}")
    print(f"   Average score     : {summary['average_score']} / 5")
    print(f"   Actions required  : {summary['actions_required']}")


# ── Main ───────────────────────────────────────────────────────
def main():
    print("=" * 55)
    print("  LLM API Integration Pipeline")
    print(f"  Provider : {PROVIDER.upper()}")
    print(f"  Started  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 55)

    records = load_feedback(INPUT_FILE)
    print(f"\n🤖 Running LLM analysis ({PROVIDER.upper()})...")
    results = process_all(records)
    export_results(results)

    print("\n🎉 Pipeline complete!")
    print("=" * 55)


if __name__ == "__main__":
    main()
