# 📊 Project Progress Map
## Georgia Clinical Trial Navigator (GCTN)

> **Current Status:** 🟢 Complete — All features working and tested

---

## ✅ Completed

### Foundation
- [x] Project concept and scope defined — health equity focus for Georgia cancer patients
- [x] Python environment set up
- [x] tkinter chosen as GUI framework (standard library — no pip installs)
- [x] Project structure organized

### Core Features (v0.1 — Flagship Demo)
- [x] Patient information input form (name, age, cancer type, subtype, city)
- [x] Basic eligibility screening by age and cancer type
- [x] Cancer subtype lookup with plain-language definitions
- [x] Georgia region detection by city
- [x] Nearby cancer center recommendations by region
- [x] Plain-language medical dictionary (50+ terms across 5 cancer types)

### ClinicalTrials.gov API Integration (v0.2)
- [x] Connected to ClinicalTrials.gov v2 REST API
- [x] Live search for recruiting trials using `urllib.request`
- [x] JSON response parsing with `json.loads`
- [x] Results filtered by cancer type and subtype
- [x] Plain-language trial summaries generated
- [x] Age eligibility warning flags added
- [x] Direct links to full trial pages on ClinicalTrials.gov

### Claude AI Integration (v0.3)
- [x] Claude AI API connected via HTTP POST request
- [x] Plain-language narrative explanations replace dictionary definitions
- [x] Prompt engineering — "patient advocate" framing for warm, readable responses
- [x] Graceful fallback to dictionary definitions when API key not configured

### Separate Translator Window (v0.4)
- [x] Plain-language popup moved to its own `tk.Toplevel` window
- [x] Trial results panel never overwritten when explaining text
- [x] Popup is scrollable and resizable
- [x] Close button added to popup

### Visual Redesign (v0.5)
- [x] Full dark navy color theme applied throughout
- [x] Styled buttons with distinct colors (blue/red/green)
- [x] Status bar at bottom with real-time feedback messages
- [x] Header banner with app title and tagline
- [x] Results panel uses light background for readability
- [x] All fonts switched to Helvetica for clean Mac rendering
- [x] Minimum window size set to prevent layout breaking

### Georgia Location Fix (v0.6)
- [x] Replaced keyword search (`query.locn=Georgia`) with GPS geo-filter
- [x] GPS coordinates dictionary built for 17 Georgia cities
- [x] 200-mile radius filter covers entire state of Georgia
- [x] Trials with no confirmed Georgia locations excluded from results
- [x] Georgia city coordinates mapped to `filter.geo` API parameter

### Final Polish & Bug Fixes (v0.7)
- [x] Clear / New Search button added (resets all fields and results)
- [x] Button rendering fixed for macOS — switched from `tk.Button` to `tk.Label` with click bindings (macOS ignores custom colors on `tk.Button`)
- [x] Expanded Georgia cities and regions (17 cities, 6 regions)
- [x] Added North Georgia and Central Georgia regions
- [x] `.gitignore` added to protect API key from GitHub
- [x] Code thoroughly commented for readability
- [x] All functions defined before main program logic (professor's structure requirement)
- [x] Jupyter Notebook version created (`gctn.ipynb`) for Mac compatibility
- [x] `.py` version cleaned of Jupyter/cell references for clean standalone submission
- [x] API key embedded in submission version for grader convenience

### GitHub & Documentation
- [x] Repository created and published publicly on GitHub
- [x] README.md written and updated to reflect all current features
- [x] PROGRESS.md tracking all development milestones
- [x] `.gitignore` protecting `.env` API key file

---

## 🗓️ Version History

| Version | Milestone | Key Change |
|---|---|---|
| v0.1 | Flagship Demo | Basic GUI with static eligibility check and plain-language dictionary |
| v0.2 | Live Trial Search | Connected to ClinicalTrials.gov API v2 — real recruiting trials |
| v0.3 | Claude AI Engine | AI plain-language explanations replace dictionary definitions |
| v0.4 | Separate Popup | Translator moved to its own window — results never overwritten |
| v0.5 | Visual Redesign | Dark navy theme, styled buttons, status bar, header banner |
| v0.6 | Georgia Location Fix | GPS geo-filter replaces broken keyword search |
| v0.7 | Final Polish | Button fix for Mac, Clear button, comments, code structure |

---

## 🐛 Known Issues & Resolutions

| Issue | Status | Resolution |
|---|---|---|
| Python crashes in VS Code on Mac | Resolved | Run from Terminal or use Jupyter Notebook version |
| `tk.Button` colors ignored on macOS | Resolved | Switched to `tk.Label` with click bindings |
| Keyword Georgia search returned wrong results | Resolved | GPS geo-filter with 200-mile radius |
| `__file__` not defined in Jupyter | Resolved | `try/except NameError` falls back to `os.getcwd()` |
| `root.after()` TclError in Jupyter | Resolved | Removed threading — API calls run on main thread |

---

## 🏁 Definition of Done — All Complete ✅

- [x] All core features tested and working reliably
- [x] Plain-language summaries reviewed for clarity
- [x] README fully documents how to install and run the app
- [x] Code is thoroughly commented throughout
- [x] All functions defined before main program logic
- [x] Both `.py` and `.ipynb` versions submitted
- [x] Code pushed to GitHub with descriptive commit messages

---

*Last updated: May 2026*
