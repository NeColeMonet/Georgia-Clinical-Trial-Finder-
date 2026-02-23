# 🔬 Georgia Clinical Trial Navigator (GCTN)

A Python desktop application that helps Georgia cancer patients and their caregivers find actively recruiting clinical trials — and understand them in plain language.

---

## 💡 About This Project

Navigating clinical trials can be overwhelming, especially when medical language is hard to understand. The Georgia Clinical Trial Navigator was built to make that process a little easier.

This tool was developed as a Python course project with a real-world purpose: helping patients in Georgia find cancer clinical trials that may be right for them, without needing a medical background to understand the results.

---

## ✨ Features

- **Live Trial Search** — Pulls actively recruiting trials directly from [ClinicalTrials.gov](https://clinicaltrials.gov) in real time
- **Georgia-Focused Results** — Filters results to trials with locations in Georgia and maps them to nearby cancer centers
- **Plain-Language Summaries** — Converts complex trial descriptions into easy-to-read summaries
- **Medical Term Translator** — Paste any clinical trial text and get plain-language definitions for medical terms
- **Age Eligibility Check** — Flags trials where the patient may not meet the minimum age requirement
- **No internet dependency for basic use** — Eligibility screening and term translation work offline

---

## 🖥️ How to Run

### Requirements
- Python 3.7 or higher
- `tkinter` (included with most Python installations)
- No additional packages needed — uses only Python standard libraries

### Steps
1. Clone or download this repository
2. Open a terminal and navigate to the project folder
3. Run the app:

```bash
python gctn.py
```

---

## 🗺️ How to Use

### Finding Clinical Trials
1. Enter your **name**, **age**, **cancer type**, and **Georgia city**
2. Optionally enter a **cancer subtype** (e.g. NSCLC, HER2, TNBC)
3. Click **Search Clinical Trials**
4. Results will show matching recruiting trials in Georgia with plain-language summaries and direct links

**Supported cancer types:** Lung, Breast, Colon, Pancreatic, Prostate

### Translating Medical Terms
1. Copy and paste any clinical trial text into the **Translate Medical Terms** box
2. Click **Translate**
3. Any recognized medical terms will be explained in plain language

---

## 📍 Georgia Cancer Centers Included

| Region | Centers |
|---|---|
| East Georgia | Georgia Cancer Center (Augusta University) |
| Metro Atlanta | Emory Winship Cancer Institute, Northside Hospital Cancer Institute, Piedmont Atlanta |
| South Georgia | St. Joseph's/Candler (Savannah), Phoebe Putney Memorial Hospital (Albany) |
| West Georgia | Piedmont Columbus Regional |

---

## ⚠️ Disclaimer

This tool is for **informational and educational purposes only**. It is not a substitute for medical advice. Always consult a qualified healthcare provider or clinical research nurse before making decisions about clinical trial participation.

Trial data is retrieved live from ClinicalTrials.gov and may not reflect the most current enrollment status at every site.

---

## 🙏 Acknowledgments

- Trial data provided by the U.S. National Library of Medicine via the [ClinicalTrials.gov API v2](https://clinicaltrials.gov/data-api/api)
- Built as a course project with the goal of improving health information accessibility in Georgia

---

## 👩‍💻 Author

Made with 💙 by NeCole Monet Smith 
