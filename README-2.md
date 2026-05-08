# 🔬 Georgia Clinical Trial Navigator (GCTN)

**A free Python desktop application that helps Georgia cancer patients find actively recruiting clinical trials near them — and understand them in plain language.**

> Built by NeCole Smith · Healthcare Info Systems Development · Kennesaw State University · Spring 2026

---

## 💡 About This Project

Navigating clinical trials can be overwhelming, especially when medical language is hard to understand. The Georgia Clinical Trial Navigator was built to close a real health equity gap — 1 in 5 Georgia cancer patients who could benefit from a clinical trial never learns one exists.

GCTN connects directly to ClinicalTrials.gov in real time, filters results to confirmed Georgia locations using GPS coordinates, and uses Claude AI to explain complex trial text in warm, plain conversational language that anyone can understand.

---

## ✨ Features

- **Live Trial Search** — Pulls actively recruiting trials directly from ClinicalTrials.gov in real time using the official v2 REST API
- **GPS-Based Georgia Filter** — Uses GPS coordinates and a 200-mile radius to surface only trials with confirmed Georgia locations
- **Claude AI Plain-Language Translator** — Paste any clinical trial text and receive a warm, narrative explanation in plain English
- **Eligibility Check** — Instantly checks age and cancer type and flags potential mismatches
- **Nearby Cancer Centers** — Maps the user's city to the nearest Georgia cancer treatment centers
- **Clear / New Search** — Resets all fields so a new patient can start fresh without restarting the app
- **Status Bar** — Real-time feedback showing what the app is doing at every step
- **Standard Library Only** — No pip installs required; uses only Python's built-in libraries

---

## 🖥️ How to Run

### Requirements
- Python 3.7 or higher
- `tkinter` (included with most Python installations)
- Internet connection (for live trial search and AI features)
- No external packages needed — standard library only

### Run as a .py file
```bash
python3 gctn.py
```

> **Mac users:** If Python crashes when running through VS Code, run from Terminal directly:
> ```bash
> cd /path/to/this/file
> python3 gctn.py
> ```
> This is a known macOS + tkinter + VS Code conflict. Running from Terminal resolves it.

### Run as a Jupyter Notebook
Open `gctn.ipynb` in VS Code or Jupyter and click **Run All**.

---

## 🔑 API Key Setup (Claude AI Feature)

The AI plain-language translator requires a free Claude API key from Anthropic.

1. Get a free key at **console.anthropic.com**
2. Create a file named `.env` in the same folder as `gctn.py`
3. Add this one line:
```
CLAUDE_API_KEY=sk-ant-your-key-here
```
4. Run the app — the status line will show **✅ Claude AI ready**

> Without a key the app still works fully. The AI translator falls back to a built-in plain-language dictionary automatically.

---

## 🗺️ How to Use

### Searching for Trials
1. Enter your **name**, **age**, **cancer type**, and **Georgia city**
2. Optionally enter a **cancer subtype** (e.g. NSCLC, HER2, TNBC, MSI)
3. Click **🔍 Search Clinical Trials**
4. Results show matching recruiting trials with confirmed Georgia locations, plain-language summaries, and direct links to ClinicalTrials.gov

**Supported cancer types:** Lung · Colon · Pancreatic · Prostate · Breast

### AI Plain-Language Translator
1. Copy any text from a clinical trial listing
2. Paste it into the **Translate Medical Terms** box
3. Click **💬 Explain in Plain Language**
4. Claude AI returns a warm, conversational explanation in a separate popup window — your trial results stay on screen

---

## 📍 Georgia Cancer Centers

| Region | Centers |
|---|---|
| East Georgia | Georgia Cancer Center (Augusta University) |
| Metro Atlanta | Emory Winship Cancer Institute · Northside Hospital Cancer Institute · Piedmont Atlanta · Wellstar Health System |
| South Georgia | St. Joseph's/Candler (Savannah) · Phoebe Putney Memorial Hospital (Albany) |
| West Georgia | Piedmont Columbus Regional |
| North Georgia | AdventHealth Rome · Northeast Georgia Medical Center (Gainesville) |
| Central Georgia | Navicent Health / Atrium Health (Macon) |

---

## 🛠️ Technical Stack

| Component | Technology |
|---|---|
| GUI | Python `tkinter` |
| API Calls | Python `urllib` + `json` |
| Trial Data | ClinicalTrials.gov v2 REST API |
| AI Explanations | Anthropic Claude API |
| Location Filtering | GPS geo-filter with 200-mile radius |
| File System | Python `os` |
| External Packages | **None** — standard library only |

---

## 📁 Repository Structure

```
Georgia-Clinical-Trial-Finder-/
├── gctn.py              # Main application — run with python3 gctn.py
├── gctn.ipynb           # Jupyter Notebook version
├── .gitignore           # Excludes .env from GitHub (keeps API key safe)
├── PROGRESS.md          # Development history and milestone tracker
└── README.md            # This file
```

---

## ⚠️ Disclaimer

This tool is for **informational and educational purposes only**. It is not a substitute for medical advice. Always consult a qualified healthcare provider or clinical research nurse before making decisions about clinical trial participation.

Trial data is retrieved live from ClinicalTrials.gov and may not reflect the most current enrollment status at every site.

---

## 🙏 Acknowledgments

- Trial data provided by the U.S. National Library of Medicine via the [ClinicalTrials.gov API v2](https://clinicaltrials.gov/data-api/api)
- AI explanations powered by [Anthropic Claude](https://www.anthropic.com)
- Built as a Healthcare Info Systems Development course project at Kennesaw State University

---

## 👩‍💻 Author

**NeCole Smith**
[github.com/NeColeMonet](https://github.com/NeColeMonet)
