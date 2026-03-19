# 🤖 LLM API Integration Pipeline

Python pipeline for integrating **OpenAI** and **Claude (Anthropic)** APIs into automated data workflows. Demonstrates real prompt engineering, structured response parsing, and batch processing — not just a raw API call.

Built as a customer feedback analysis system, but easily adaptable to any text processing use case.

---

## 📋 What It Does

1. **Loads** customer feedback records from CSV
2. **Builds** a structured prompt with custom instructions
3. **Calls** Claude or OpenAI API for each record
4. **Parses** the structured JSON response
5. **Exports** analyzed results to CSV + JSON summary

Each record gets: sentiment, score (1-5), topics, summary, and action flag.

---

## 📁 Project Structure

```
llm-api-integration-pipeline/
├── pipeline.py                    # Main pipeline script
├── requirements.txt               # Dependencies
├── data/
│   ├── input/
│   │   └── customer_feedback.csv  # Sample input data
│   └── output/                    # Analyzed results (generated)
├── logs/                          # JSON summaries (generated)
└── README.md
```

---

## ⚡ Quick Start

**1. Clone the repository**
```bash
git clone https://github.com/azahidgarcia/llm-api-integration-pipeline.git
cd llm-api-integration-pipeline
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set your API key**
```bash
# For Claude (Anthropic)
export ANTHROPIC_API_KEY="your-api-key-here"

# For OpenAI
export OPENAI_API_KEY="your-api-key-here"
```

**4. Choose your provider** in `pipeline.py`:
```python
PROVIDER = "claude"   # or "openai"
```

**5. Run the pipeline**
```bash
python pipeline.py
```

> 💡 **No API key?** The pipeline runs in demo mode with mock responses automatically.

---

## 📊 Example Output

```
=======================================================
  LLM API Integration Pipeline
  Provider : CLAUDE
  Started  : 2024-01-22 10:30:00
=======================================================
📂 Loaded 5 feedback record(s)

🤖 Running LLM analysis (CLAUDE)...
   [1/5] Analyzing record #1...
   [2/5] Analyzing record #2...
   [3/5] Analyzing record #3...
   [4/5] Analyzing record #4...
   [5/5] Analyzing record #5...

✅ Results saved to  : data/output/analyzed_feedback_20240122.csv
✅ Summary saved to  : logs/summary_20240122.json

📊 Analysis Summary:
   Records processed : 5
   Positive          : 3
   Neutral           : 1
   Negative          : 1
   Average score     : 3.8 / 5
   Actions required  : 1

🎉 Pipeline complete!
```

---

## 🧠 Prompt Engineering

The pipeline uses a structured system prompt + user prompt pattern:

```python
SYSTEM_PROMPT = """
You are a data analyst specialized in customer feedback analysis.
Always respond ONLY with valid JSON — no preamble, no explanation.
"""

# User prompt requests specific structured output:
{
  "sentiment": "positive | neutral | negative",
  "score": 1-5,
  "topics": ["topic1", "topic2"],
  "summary": "one sentence summary",
  "action_required": true | false
}
```

---

## 🔧 Adapting to Your Use Case

Change the prompt in `build_prompt()` to process any text:
- Document summarization
- Email classification
- Product description generation
- Data extraction from unstructured text
- Content moderation

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core language |
| Anthropic SDK | Claude API client |
| OpenAI SDK | GPT API client |

---

## 👤 Author

**Azahid García** — Python Automation & Data Engineer

- 🌐 [Fiverr Profile](https://fiverr.com)
- 💼 [Upwork Profile](https://upwork.com)
- 🐙 [GitHub](https://github.com/azahidgarcia)

---

## 📄 License

MIT License — free to use and modify.
