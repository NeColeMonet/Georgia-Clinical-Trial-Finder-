#!/usr/bin/env python3
"""
============================================================
Georgia Clinical Trial Navigator (GCTN)
============================================================
Author:      NeCole Smith
Course:      Healthcare Info Systems Development
Institution: Kennesaw State University
Semester:    Spring 2026

Description:
    A desktop application that helps Georgia cancer patients
    find actively recruiting clinical trials near them and
    understand them in plain language. Connects to the
    ClinicalTrials.gov API in real time, filters results to
    confirmed Georgia locations using GPS coordinates, and
    uses Claude AI to explain complex trial language in
    plain, conversational terms.

How to Run:
    python3 gctn.py
    Or from Terminal on Mac:
    cd /path/to/this/file && python3 gctn.py

Requirements:
    - Python 3.7 or higher
    - tkinter (included with most Python installations)
    - Internet connection (for live trial search and AI)
    - No pip installs needed — standard library only

API Key Setup (enables the AI plain-language feature):
    1. Get a free key at console.anthropic.com
    2. Create a file named .env in the same folder as gctn.py
    3. Add this line:  CLAUDE_API_KEY=sk-ant-your-key-here
    4. Run the app — status bar will show "Claude AI ready"
    NOTE: Without a key the app still works fully.
          The AI translator falls back to the built-in
          plain-language dictionary automatically.

NOTE FOR MAC USERS:
    If Python crashes when running this file through VS Code,
    run it directly from Terminal instead:
        cd /path/to/this/file
        python3 gctn.py
    This is a known macOS + tkinter + VS Code conflict.
    Running from Terminal resolves it completely.
============================================================
"""


# 🔬 Georgia Clinical Trial Navigator (GCTN)
#
# **Author:** NeCole Smith
# **Course:** Healthcare Info Systems Development — Spring 2026
# **Institution:** Kennesaw State University
#
# ---
#
# Project Overview
# This application helps Georgia cancer patients find actively recruiting clinical trials
# near them and understand them in plain language. It connects to the ClinicalTrials.gov
# API in real time, filters results to confirmed Georgia locations using GPS coordinates,
# and uses Claude AI to explain complex trial language in simple, conversational terms.
#
# How to Run
#


#
# PURPOSE: Import all required Python libraries and load the Claude API key.
#
# LIBRARIES USED (all from Python standard library — no pip install needed):
#   tkinter     — builds the desktop GUI window, buttons, and input fields
#   messagebox  — shows popup alert dialogs for errors and warnings
#   urllib      — sends HTTP requests to external APIs over the internet
#   json        — parses JSON responses returned by the APIs
#   os          — interacts with the file system to locate the .env file
# --------------------------------------------------------------------------

import tkinter as tk
from tkinter import messagebox
import urllib.request
import urllib.parse
import json
import os


def load_api_key():
    """
    Load the Claude API key from a .env file stored on the user's computer.

    The .env file should be in the same folder as this notebook and contain:
        CLAUDE_API_KEY=sk-ant-your-key-here

    This approach keeps the API key out of the source code so it is never
    accidentally uploaded to GitHub or shared publicly.

    Returns:
        str: The API key string if found, or an empty string if not found.
    """
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        base_dir = os.getcwd()  # Fallback if __file__ is not defined

    # Build the full path to the .env file
    env_path = os.path.join(base_dir, '.env')

    # If the file exists, read it line by line and look for the key
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                # Only process lines that start with our expected key name
                if line.startswith('CLAUDE_API_KEY='):
                    # Split on the first '=' only, return everything after it
                    return line.split('=', 1)[1].strip()

    # Return empty string if .env file not found — app still works without AI feature
    return ''


# Load the key at startup so all cells can access it as a global variable
CLAUDE_API_KEY = load_api_key()

# Print confirmation so the user knows immediately whether the key loaded
print(f'API Key loaded: {"Yes ✅" if CLAUDE_API_KEY else "No ⚠ — .env file not found in: " + os.getcwd()}')


#
# PURPOSE: Define all colors and fonts used throughout the application.
#
# DESIGN APPROACH:
#   All visual constants are defined here in one place so that the look
#   of the app can be updated by changing values in this single cell
#   rather than hunting through hundreds of lines of GUI code.
#
#   The color scheme uses a deep navy blue palette to give the app a
#   professional, healthcare-appropriate appearance rather than the
#   default gray tkinter look.
# --------------------------------------------------------------------------

# ── Background colors ────────────────────────────────────────────
CLR_BG         = '#1e2a3a'   # Main window background (deep navy)
CLR_PANEL      = '#253447'   # Section frame backgrounds (slightly lighter navy)

# ── Input field colors ────────────────────────────────────────────
CLR_ENTRY_BG   = '#f0f4f8'   # Text input field background (light blue-white)
CLR_ENTRY_FG   = '#1a1a2e'   # Text input field text color (near black)

# ── Label and text colors ─────────────────────────────────────────
CLR_LABEL_FG   = '#d0dce8'   # Main label text (soft white-blue)
CLR_HINT_FG    = '#6a8fa8'   # Hint/helper text (muted blue-gray)

# ── Results panel colors ──────────────────────────────────────────
CLR_RESULT_BG  = '#f8fafc'   # Results text area background (near white)
CLR_RESULT_FG  = '#1a2533'   # Results text color (dark navy)

# ── Button colors (each button has a distinct color for clarity) ──
CLR_BTN_SEARCH = '#0a4a8f'   # Search button (deep navy blue — high contrast)
CLR_BTN_CLEAR  = '#8b1a0f'   # Clear button (dark crimson — high contrast)
CLR_BTN_AI     = '#0a6640'   # AI Explain button (deep forest green — high contrast)
CLR_BTN_CLOSE  = '#4a5568'   # Close button (charcoal gray)
CLR_BTN_FG     = '#ffffff'   # All button text (white — high contrast against dark buttons)

# ── Status bar colors ─────────────────────────────────────────────
CLR_STATUS_BG  = '#141e2b'   # Status bar background (darkest navy)
CLR_STATUS_FG  = '#7fa8c4'   # Status bar default text (steel blue)

# ── Feedback colors (used for status messages) ────────────────────
CLR_OK         = '#2ecc71'   # Success messages (bright green)
CLR_WARN       = '#e67e22'   # Warning messages (orange)
CLR_ERR        = '#e74c3c'   # Error messages (red)

# ── Font definitions ──────────────────────────────────────────────
# Each font is a tuple of (font family, size) or (font family, size, style)
# Helvetica is used throughout for clean rendering on Mac
FONT_LABEL      = ('Helvetica', 11)           # Standard label text
FONT_LABEL_BOLD = ('Helvetica', 11, 'bold')   # Bold label text (section headers)
FONT_HINT       = ('Helvetica', 9)            # Small hint text under inputs
FONT_BTN        = ('Helvetica', 11, 'bold')   # Button labels
FONT_ENTRY      = ('Helvetica', 11)           # Text inside input fields
FONT_RESULT     = ('Helvetica', 10)           # Trial results display text
FONT_STATUS     = ('Helvetica', 9)            # Status bar text
FONT_TITLE      = ('Helvetica', 13, 'bold')   # Popup window titles

print('Theme loaded. ✅')


#
# PURPOSE: Map medical/clinical trial terms to plain-language definitions.
#
# HOW IT IS USED:
#   1. As a FALLBACK when Claude AI is unavailable — the app searches
#      pasted text for any matching keys and displays the definitions.
#   2. To explain cancer subtypes entered by the user in the search form.
#
# STRUCTURE:
#   A Python dictionary where:
#     key   = the medical term (lowercase string, for case-insensitive matching)
#     value = a plain-language explanation a patient can understand
#
# COVERAGE:
#   - Lung cancer subtypes and biomarkers
#   - Breast cancer subtypes and receptors
#   - Colon cancer markers
#   - Pancreatic cancer staging terms
#   - Prostate cancer terms
#   - General clinical trial terminology
# --------------------------------------------------------------------------

plain_language_terms = {

    # ── Lung cancer terms ────────────────────────────────────────
    'nsclc': 'Non-small cell lung cancer, the most common type of lung cancer.',
    'sclc': 'Small cell lung cancer, a faster-growing type of lung cancer.',
    'egfr': 'A gene change in lung cancer that may respond to targeted therapy.',
    'alk': 'A gene change in lung cancer that can be treated with targeted drugs.',
    'kras': 'A common gene change found in lung cancer.',
    'pd-1': 'A protein on immune cells. Some cancers block PD-1 to avoid attack.',
    'pd-l1': 'A protein on cancer cells that helps them hide from the immune system.',

    # ── Breast cancer terms ──────────────────────────────────────
    'her2': 'HER2-positive breast cancer, which may respond to targeted therapy.',
    'er': 'Estrogen receptor-positive breast cancer.',
    'pr': 'Progesterone receptor-positive breast cancer.',
    'tnbc': 'Triple-negative breast cancer, which does not have hormone receptors.',
    'hormone receptor': 'A feature that affects how breast cancer grows and is treated.',

    # ── Colon cancer terms ───────────────────────────────────────
    'msi': 'MSI-high colon cancer, which may respond to immunotherapy.',
    'ras': 'A gene change that affects colon cancer treatment options.',
    'braf': 'A gene change that affects colon cancer growth and treatment.',
    'metastatic': 'The cancer has spread to other parts of the body.',

    # ── Pancreatic cancer terms ──────────────────────────────────
    'resectable': 'The tumor can be removed with surgery.',
    'unresectable': 'The tumor cannot be removed with surgery.',
    'locally advanced': 'The cancer has grown nearby but has not spread far away.',
    'brca': 'A gene change linked to some pancreatic and breast cancers.',

    # ── Prostate cancer terms ────────────────────────────────────
    'gleason': 'A score that describes how aggressive prostate cancer is.',
    'psa': 'A blood test used to help detect prostate cancer.',
    'androgen': 'Male hormones that can help prostate cancer grow.',
    'castration-resistant': 'Cancer that grows even when testosterone is low.',

    # ── General clinical trial terminology ───────────────────────
    'investigational': 'A new drug or treatment that is still being studied.',
    'efficacy': 'How well a treatment works.',
    'tolerability': 'How well a person can handle the side effects.',
    'monotherapy': 'Using one drug alone.',
    'combination therapy': 'Using more than one drug together.',
    'randomized': 'Participants are assigned to groups by chance.',
    'double-blind': 'Neither the patient nor the doctor knows which treatment is given.',
    'open-label': 'Everyone knows which treatment is being given.',
    'placebo': 'A treatment with no active drug.',
    'inclusion criteria': 'Requirements a person must meet to join a study.',
    'exclusion criteria': 'Reasons a person cannot join a study.',
    'phase 1': 'A study phase that tests safety and dose.',
    'phase 2': 'A study phase that tests whether the treatment works.',
    'phase 3': 'A study phase that compares treatments.',
    'phase 4': 'A study phase that looks at long-term effects.',
    'primary endpoint': 'The main result the study is measuring.',
    'secondary endpoint': 'Extra results the study is also tracking.',
    'cohort': 'A group of patients in a study.',
    'arm': 'A treatment group in a clinical trial.',
    'adverse event': 'A side effect or unwanted reaction during the study.',
    'biomarker': 'A measurable sign in the body used to track disease or treatment response.',
}

print(f'Dictionary loaded: {len(plain_language_terms)} terms. ✅')


#
# PURPOSE: Map Georgia cities to geographic regions, and map regions
#          to nearby cancer treatment centers.
#
# HOW IT IS USED:
#   When the user enters their city, the app:
#     1. Looks up the city in the 'regions' dictionary to find the region name
#     2. Uses that region name to look up cancer centers in the 'centers' dictionary
#     3. Displays the nearest centers in the results panel
#
# DESIGN DECISION:
#   Two separate dictionaries are used rather than one nested structure
#   so that each can be updated independently. Adding a new city only
#   requires one line in 'regions'. Adding a new center only requires
#   one line in 'centers'.
# --------------------------------------------------------------------------

# Maps city names (lowercase) to their Georgia region label.
# The app checks if the user's city input CONTAINS any of these keys
# (not exact match) so partial city names still work.
regions = {
    'augusta':       'East Georgia',
    'atlanta':       'Metro Atlanta',
    'decatur':       'Metro Atlanta',
    'marietta':      'Metro Atlanta',
    'alpharetta':    'Metro Atlanta',
    'roswell':       'Metro Atlanta',
    'sandy springs': 'Metro Atlanta',
    'savannah':      'South Georgia',
    'albany':        'South Georgia',
    'valdosta':      'South Georgia',
    'brunswick':     'South Georgia',
    'columbus':      'West Georgia',
    'lagrange':      'West Georgia',
    'rome':          'North Georgia',
    'gainesville':   'North Georgia',
    'macon':         'Central Georgia',
    'warner robins': 'Central Georgia',
}

# Maps each region label to a list of major cancer treatment centers.
# These are displayed as recommended nearby facilities for the user.
centers = {
    'East Georgia': [
        'Georgia Cancer Center (Augusta University)'
    ],
    'Metro Atlanta': [
        'Emory Winship Cancer Institute',
        'Northside Hospital Cancer Institute',
        'Piedmont Atlanta',
        'Wellstar Health System',
    ],
    'South Georgia': [
        "St. Joseph's/Candler (Savannah)",
        'Phoebe Putney Memorial Hospital (Albany)',
    ],
    'West Georgia': [
        'Piedmont Columbus Regional'
    ],
    'North Georgia': [
        'AdventHealth Rome',
        'Northeast Georgia Medical Center (Gainesville)'
    ],
    'Central Georgia': [
        'Navicent Health / Atrium Health (Macon)'
    ],
}

print('Regions loaded. ✅')


#
# PURPOSE: Define reusable utility functions used across the application.
#
# FUNCTIONS:
#   find_region()          — looks up a user's city in the regions dictionary
#   check_eligibility()    — validates age and cancer type for trial eligibility
#   explain_subtype()      — looks up a cancer subtype in the plain-language dictionary
#   explain_terms_in_text()— scans pasted text for known medical terms and returns definitions
#   set_status()           — updates the status bar at the bottom of the window
#   make_button()          — creates a consistently styled tkinter button
# --------------------------------------------------------------------------


def find_region(city):
    """
    Look up a Georgia city and return its region name.

    Converts the input to lowercase and checks whether any known city key
    is contained within the input string. This allows partial matches
    (e.g. 'East Atlanta' still matches 'atlanta').

    Args:
        city (str): The city name entered by the user.

    Returns:
        str or None: The region name if found, or None if the city
                     is not in the known cities dictionary.
    """
    city = city.lower().strip()
    for key in regions:
        if key in city:
            return regions[key]
    return None  # City not found — app will show statewide results instead


def check_eligibility(age, cancer_type):
    """
    Perform a basic eligibility check based on age and cancer type.

    Note: This is a simplified screen only. Full eligibility for any
    specific trial requires review by a medical professional.

    Args:
        age (int): The patient's age.
        cancer_type (str): The cancer type entered by the user.

    Returns:
        str: A plain-language eligibility message to display to the user.
    """
    cancer_type = cancer_type.lower()

    # Most clinical trials have a minimum age of 18
    if age < 18:
        return 'Most clinical trials require participants to be 18 or older.'

    # The app currently supports these five cancer types specifically
    valid_types = ['lung', 'colon', 'pancreatic', 'prostate', 'breast']
    if cancer_type not in valid_types:
        # Other types may still have trials — show statewide results
        return 'This tool checks lung, colon, pancreatic, prostate, and breast cancer. Your cancer type may still have trials — results shown are statewide Georgia.'

    return f'You may be eligible for trials related to {cancer_type} cancer.'


def explain_subtype(subtype):
    """
    Look up a cancer subtype in the plain-language dictionary.

    Used to explain the optional subtype field the user enters
    (e.g. 'NSCLC', 'HER2', 'TNBC') in simple terms.

    Args:
        subtype (str): The cancer subtype entered by the user.

    Returns:
        str: A plain-language explanation, or a helpful fallback message.
    """
    subtype = subtype.lower().strip()

    # Check if the subtype exists in our medical dictionary
    if subtype in plain_language_terms:
        return plain_language_terms[subtype]

    # Handle empty subtype field gracefully
    if subtype == '':
        return 'No specific subtype entered.'

    # Subtype not in dictionary — give helpful guidance
    return 'This subtype is not in the dictionary, but some trials are subtype-specific. Ask your doctor for more details.'


def explain_terms_in_text(text):
    """
    Scan a block of text for recognized medical terms and return definitions.

    This is the FALLBACK for the AI translator — used when Claude AI
    is unavailable. It searches the entire pasted text for any terms
    that exist as keys in the plain_language_terms dictionary.

    Args:
        text (str): The clinical trial text pasted by the user.

    Returns:
        list: A list of 'TERM: definition' strings for all recognized terms.
              Returns a single 'not recognized' message if nothing is found.
    """
    text_lower = text.lower()
    explanations = []

    # Check every term in the dictionary against the pasted text
    for term, definition in plain_language_terms.items():
        if term in text_lower:
            explanations.append(f'{term.upper()}: {definition}')

    # If no terms matched, return a helpful fallback message
    if not explanations:
        explanations.append('No specific medical terms recognized.')

    return explanations


def set_status(message, color=None):
    """
    Update the status bar message at the bottom of the main window.

    The status bar gives the user real-time feedback about what the app
    is doing (e.g. 'Searching...', 'Done — 10 trials found', 'Error').

    Args:
        message (str): The message to display.
        color (str, optional): Hex color code for the text. Defaults to CLR_STATUS_FG.
    """
    if color is None:
        color = CLR_STATUS_FG
    status_label.config(text=f'  {message}', fg=color)
    root.update_idletasks()  # Force the GUI to refresh immediately


def make_button(parent, text, command, color, **kwargs):
    """
    Create a consistently styled button using tk.Label instead of tk.Button.

    On macOS, tkinter ignores bg/fg color settings on tk.Button widgets —
    the OS overrides them with the native system button style, making custom
    colors invisible. Using tk.Label with click bindings solves this because
    Labels fully respect custom background and foreground colors on all platforms.

    The label is given a hand cursor and click/hover bindings to mimic
    the feel of a real button.

    Args:
        parent: The tkinter parent widget to attach the button to.
        text (str): The button label.
        command (callable): The function to call when the button is clicked.
        color (str): The background color hex code.
        **kwargs: Any additional tkinter Label options.

    Returns:
        tk.Label: A label widget styled and bound to behave like a button.
    """
    btn = tk.Label(
        parent,
        text=text,
        bg=color,               # Background color — works on Mac unlike tk.Button
        fg=CLR_BTN_FG,          # White text for contrast
        font=FONT_BTN,          # Bold Helvetica 11
        relief=tk.FLAT,         # Flat style
        cursor='hand2',         # Pointer cursor on hover
        padx=16,
        pady=7,
        **kwargs,
    )

    # Bind left-click to trigger the command
    btn.bind('<Button-1>', lambda e: command())

    # Hover effect — slightly lighten on mouse enter, restore on leave
    def on_enter(e):
        btn.config(bg=color)

    def on_leave(e):
        btn.config(bg=color)

    btn.bind('<Enter>', on_enter)
    btn.bind('<Leave>', on_leave)

    return btn

print('Helper functions loaded. ✅')


#
# PURPOSE: Connect to ClinicalTrials.gov, fetch recruiting trials,
#          and format them into readable plain-language summaries.
#
# HOW THE API CONNECTION WORKS:
#   1. build_query()    — constructs the API request URL with all search filters
#   2. fetch_trials()   — sends the HTTP request and parses the JSON response
#   3. summarize_trial()— formats a single trial dict into a readable text block
#
# KEY DESIGN DECISION — GPS-BASED FILTERING:
#   Earlier versions used 'query.locn=Georgia' (keyword search), which
#   returned trials that merely mentioned Georgia in their text — even if
#   they had no actual Georgia locations. The fix was to switch to
#   'filter.geo' with GPS coordinates and a 200-mile radius. This ensures
#   every result has a confirmed Georgia site.
# --------------------------------------------------------------------------

# Base URL for the ClinicalTrials.gov v2 REST API
CTGOV_API = 'https://clinicaltrials.gov/api/v2/studies'

# GPS coordinates for each supported Georgia city.
# Used to build the geographic filter in build_query().
# Format: 'city name': (latitude, longitude)
CITY_COORDS = {
    'atlanta':       (33.7490, -84.3880),
    'decatur':       (33.7748, -84.2963),
    'marietta':      (33.9526, -84.5499),
    'alpharetta':    (34.0754, -84.2941),
    'roswell':       (34.0232, -84.3616),
    'sandy springs': (33.9304, -84.3733),
    'augusta':       (33.4735, -82.0105),
    'savannah':      (32.0835, -81.0998),
    'albany':        (31.5785, -84.1557),
    'valdosta':      (30.8327, -83.2785),
    'brunswick':     (31.1499, -81.4915),
    'columbus':      (32.4610, -84.9877),
    'lagrange':      (33.0398, -85.0311),
    'rome':          (34.2570, -85.1647),
    'gainesville':   (34.2979, -83.8241),
    'macon':         (32.8407, -83.6324),
    'warner robins': (32.6130, -83.5996),
}

# If the user's city is not in CITY_COORDS, default to Atlanta's coordinates.
# A 200-mile radius from Atlanta covers the entire state of Georgia.
DEFAULT_COORDS = (33.7490, -84.3880)


def build_query(cancer_type, subtype, city):
    """
    Build the ClinicalTrials.gov API request URL with all search filters.

    Uses urllib.parse.urlencode to safely encode all parameters into
    a properly formatted query string appended to the base API URL.

    Args:
        cancer_type (str): The cancer type (e.g. 'colon', 'lung').
        subtype (str): Optional cancer subtype (e.g. 'NSCLC', 'HER2').
        city (str): The user's Georgia city for geographic filtering.

    Returns:
        str: The complete API request URL ready to be sent.
    """
    # Build the condition search string (e.g. 'colon cancer KRAS')
    condition = cancer_type + ' cancer'
    if subtype:
        condition += ' ' + subtype  # Append subtype if provided

    # Look up GPS coordinates for the user's city
    city_lower = city.lower().strip()
    coords = DEFAULT_COORDS  # Start with Atlanta as fallback
    for key, val in CITY_COORDS.items():
        if key in city_lower:
            coords = val
            break  # Stop as soon as a matching city is found

    # Define all API query parameters
    params = {
        'query.cond':          condition,         # Search by condition/disease
        'filter.overallStatus': 'RECRUITING',     # Only actively recruiting trials
        'aggFilters':          'studyType:int',   # Interventional studies only
        'filter.geo':          f'distance({coords[0]},{coords[1]},200mi)',  # GPS filter
        'pageSize':            15,                # Return up to 15 results
        'format':              'json',            # Response format
        # Request only the specific data fields we need (reduces response size)
        'fields': 'NCTId,BriefTitle,BriefSummary,Phase,MinimumAge,MaximumAge,LocationFacility,LocationCity,LocationState,LocationStatus',
    }

    # Encode parameters and append to base URL
    return CTGOV_API + '?' + urllib.parse.urlencode(params)


def fetch_trials(cancer_type, subtype, city):
    """
    Send the API request to ClinicalTrials.gov and return parsed trial data.

    Sends an HTTP GET request using urllib.request, reads the JSON response,
    and loops through each study to extract the fields we care about.
    Only trials with confirmed Georgia locations are included in results.

    Args:
        cancer_type (str): The cancer type to search for.
        subtype (str): Optional cancer subtype.
        city (str): The user's Georgia city.

    Returns:
        tuple: (list of trial dicts, error string or None)
               Returns (None, error_message) if the request fails.
               Returns ([], None) if no trials are found.
    """
    url = build_query(cancer_type, subtype, city)

    # Send the HTTP GET request with a custom User-Agent header
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'GCTN/1.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            # Read the response bytes and decode to a string, then parse as JSON
            data = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        # Catch any network or parsing errors and return a user-friendly message
        return None, f'Could not connect to ClinicalTrials.gov: {e}'

    # Extract the list of studies from the response
    studies = data.get('studies', [])
    if not studies:
        return [], None  # No results found — not an error

    results = []

    # Loop through each study and extract the relevant fields
    for study in studies:
        # The API response is deeply nested — navigate to each module
        proto        = study.get('protocolSection', {})
        id_mod       = proto.get('identificationModule', {})    # Trial ID and title
        desc_mod     = proto.get('descriptionModule', {})       # Summary text
        design_mod   = proto.get('designModule', {})            # Phase info
        elig_mod     = proto.get('eligibilityModule', {})       # Age requirements
        contacts_mod = proto.get('contactsLocationsModule', {}) # Location data

        # Extract individual fields with safe fallback defaults
        nct_id    = id_mod.get('nctId', 'N/A')
        title     = id_mod.get('briefTitle', 'No title available')
        summary   = desc_mod.get('briefSummary', 'No summary available.')
        phases    = design_mod.get('phases', [])
        phase_str = ', '.join(phases) if phases else 'Not listed'
        min_age   = elig_mod.get('minimumAge', 'Not specified')
        max_age   = elig_mod.get('maximumAge', 'Not specified')

        # Filter locations to only include confirmed Georgia sites
        locations    = contacts_mod.get('locations', [])
        ga_locations = []

        for loc in locations:
            state = loc.get('state', '')
            # Check for both 'Georgia' and 'GA' to be safe
            if state.lower() in ('georgia', 'ga'):
                facility   = loc.get('facility', '')
                loc_city   = loc.get('city', '')
                status     = loc.get('recruitingStatus', '')

                # Build a readable location label
                label = f'{facility} — {loc_city}' if facility else loc_city

                # Append recruiting status if available
                if status and status.lower() == 'recruiting':
                    label += ' (Recruiting)'

                if label.strip():
                    ga_locations.append(label)

        # IMPORTANT: Skip this trial entirely if it has no Georgia locations.
        # This is the core fix that prevents 'no confirmed Georgia locations' results.
        if not ga_locations:
            continue

        # Add the cleaned trial data to our results list
        results.append({
            'nct_id':       nct_id,
            'title':        title,
            'summary':      summary,
            'phase':        phase_str,
            'min_age':      min_age,
            'max_age':      max_age,
            'ga_locations': ga_locations,
        })

    return results, None


def summarize_trial(trial, age):
    """
    Format a single trial dictionary into a readable multi-line text block.

    Extracts the first 3 sentences of the summary for a brief plain-language
    overview, checks whether the user's age meets the minimum requirement,
    and lists confirmed Georgia locations.

    Args:
        trial (dict): A trial dictionary returned by fetch_trials().
        age (int): The patient's age for eligibility checking.

    Returns:
        str: A formatted multi-line string ready to display in the results panel.
    """
    lines = [
        f"Trial ID : {trial['nct_id']}",
        f"Title    : {trial['title']}",
        f"Phase    : {trial['phase']}",
        f"Ages     : {trial['min_age']} to {trial['max_age']}",
    ]

    # Age eligibility warning — extract numeric age from strings like '18 Years'
    if trial['min_age'] != 'Not specified':
        try:
            # Use filter to extract only digit characters, then convert to int
            min_yr = int(''.join(filter(str.isdigit, trial['min_age'])))
            if age < min_yr:
                lines.append(f"  ⚠  You may not meet the minimum age ({trial['min_age']}) for this trial.")
        except ValueError:
            pass  # If parsing fails, skip the age warning silently

    # Shorten the summary to the first 3 sentences for readability
    sentences    = trial['summary'].replace('\n', ' ').split('. ')
    short_summary = '. '.join(sentences[:3]).strip()
    if short_summary and not short_summary.endswith('.'):
        short_summary += '.'  # Ensure the summary ends with a period

    lines.append(f'\nWhat this trial is about:\n  {short_summary}')

    # List Georgia locations with checkmark icons
    lines.append('\nGeorgia locations accepting patients:')
    for loc in trial['ga_locations'][:5]:  # Show max 5 locations
        lines.append(f'  ✅ {loc}')

    # Direct link to the full trial on ClinicalTrials.gov
    lines.append(f"\n  More info: https://clinicaltrials.gov/study/{trial['nct_id']}")

    # Visual separator between trials
    lines.append('─' * 70)

    return '\n'.join(lines)

print('ClinicalTrials.gov functions loaded. ✅')


#
# PURPOSE: Define all functions that respond to user actions in the GUI.
#
# EVENT HANDLERS (called when the user clicks a button):
#   on_check()       — triggered by the Search button; validates input,
#                      fetches trials, and displays results
#   display_trials() — called after fetch_trials() completes; populates
#                      the results panel with trial summaries
#   on_clear()       — triggered by the Clear button; resets all fields
#   call_claude_api()— sends pasted text to the Claude AI API and returns
#                      a plain-language narrative explanation
#   on_translate()   — triggered by the Explain button; opens the AI
#                      popup window and calls Claude
# --------------------------------------------------------------------------


def on_check():
    """
    Handle the Search Clinical Trials button click.

    Validates all required input fields, performs a basic eligibility check,
    looks up the user's region, displays preliminary results, then calls
    the ClinicalTrials.gov API and displays the full trial listings.

    Note: The API call is made directly on the main thread (no background
    root.after() callback from background threads — it causes a TclError.
    root.update() is called before the API request to keep the GUI responsive.
    """
    # Retrieve and clean all input field values
    name        = entry_name.get().strip()
    age_text    = entry_age.get().strip()
    cancer_type = entry_cancer.get().strip().lower()
    subtype     = entry_subtype.get().strip()
    city        = entry_city.get().strip()

    # Validate that all required fields are filled in
    if not name or not age_text or not cancer_type or not city:
        messagebox.showinfo('Missing Information', 'Please fill in all required fields.')
        return

    # Validate that age is a number
    if not age_text.isdigit():
        messagebox.showinfo('Invalid Age', 'Please enter a number for age.')
        return

    age = int(age_text)

    # Run the basic eligibility and subtype checks
    eligibility_message = check_eligibility(age, cancer_type)
    subtype_message     = explain_subtype(subtype)
    region              = find_region(city)

    # Build the initial results text to show while the API call runs
    result_lines = [
        f'Results for {name}  |  Age: {age}  |  Cancer Type: {cancer_type.title()}\n',
        f'Eligibility Check:\n  {eligibility_message}\n',
        f'Subtype Information:\n  {subtype_message}\n',
    ]

    # Add nearby cancer center info if the city was recognized
    if region:
        result_lines.append(f'Nearest Georgia Region: {region}')
        result_lines.append('Nearby Cancer Centers:')
        for c in centers[region]:
            result_lines.append(f'  - {c}')
        result_lines.append('')
    else:
        # City not in our directory — still search statewide
        result_lines.append(f"City '{city}' not found. Showing statewide Georgia results.\n")

    # Display the initial results and searching message
    text_result.config(state=tk.NORMAL)
    text_result.delete('1.0', tk.END)
    text_result.insert(tk.END, '\n'.join(result_lines))
    text_result.insert(tk.END, '\nSearching ClinicalTrials.gov — please wait...\n')
    set_status('Searching ClinicalTrials.gov — please wait...', CLR_BTN_SEARCH)

    # Force the GUI to repaint so the user sees the 'please wait' message
    root.update()

    trials, error = fetch_trials(cancer_type, subtype, city)

    # Display the trial results
    display_trials(trials, error, age)


def display_trials(trials, error, age):
    """
    Populate the results panel with trial summaries after the API call.

    Called by on_check() after fetch_trials() returns. Handles three cases:
    1. An error occurred (network failure, timeout, etc.)
    2. No trials were found for the given search
    3. Trials were found — display each one using summarize_trial()

    Args:
        trials (list or None): List of trial dicts, or None if error occurred.
        error (str or None): Error message string, or None if successful.
        age (int): The patient's age, passed to summarize_trial() for age checks.
    """
    # Case 1: API call failed
    if error:
        text_result.insert(tk.END, f'\n⚠  {error}\n')
        text_result.insert(tk.END, 'Search manually at: https://clinicaltrials.gov\n')
        set_status('Search failed — check your internet connection.', CLR_ERR)
        text_result.config(state=tk.DISABLED)
        return

    # Case 2: No results found
    if not trials:
        text_result.insert(tk.END, '\nNo recruiting trials found in Georgia for this cancer type.\n')
        text_result.insert(tk.END, 'Try adjusting your search or visiting https://clinicaltrials.gov\n')
        set_status('No trials found. Try a different search.', CLR_WARN)
        text_result.config(state=tk.DISABLED)
        return

    # Case 3: Display all found trials
    text_result.insert(tk.END, f"\n{'=' * 70}\n")
    text_result.insert(tk.END, f'  RECRUITING CLINICAL TRIALS IN GEORGIA  ({len(trials)} found)\n')
    text_result.insert(tk.END, f"{'=' * 70}\n\n")

    # Loop through each trial and append its formatted summary
    for trial in trials:
        text_result.insert(tk.END, summarize_trial(trial, age) + '\n')

    # Append next-steps guidance at the bottom of the results
    text_result.insert(tk.END, '\nNext Steps:\n')
    text_result.insert(tk.END, '  - Talk to your doctor or research nurse about these trials.\n')
    text_result.insert(tk.END, '  - Visit https://clinicaltrials.gov for full eligibility details.\n')

    # Make results read-only so the user cannot accidentally edit them
    text_result.config(state=tk.DISABLED)
    set_status(f'Done — {len(trials)} recruiting trials found in Georgia.', CLR_OK)


def on_clear():
    """
    Handle the Clear / New Search button click.

    Resets every input field and the results panel to their empty default
    state so a new patient can begin a fresh search without restarting
    the app or re-running any cells.
    """
    # Clear all text entry fields
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_cancer.delete(0, tk.END)
    entry_subtype.delete(0, tk.END)
    entry_city.delete(0, tk.END)

    # Clear the medical text translator box
    text_medical.delete('1.0', tk.END)

    # Clear the results panel (must enable first, then disable after clearing)
    text_result.config(state=tk.NORMAL)
    text_result.delete('1.0', tk.END)
    text_result.config(state=tk.DISABLED)

    # Reset status bar to default ready message
    set_status('Ready — enter patient information to search.')

    # Move keyboard focus back to the first input field for convenience
    entry_name.focus()


def call_claude_api(medical_text):
    """
    Send clinical trial text to the Claude AI API and return a plain-language explanation.

    Constructs a prompt that instructs Claude to act as a patient advocate
    and explain the text in warm, conversational language. Makes an HTTP POST
    request to Anthropic's API endpoint with the prompt and the user's text.

    Args:
        medical_text (str): The clinical trial text pasted by the user.

    Returns:
        tuple: (narrative_string, None) on success,
               or (None, error_message) on failure.
               If no API key is configured, returns setup instructions.
    """
    # Check that the API key was loaded — show setup instructions if not
    if not CLAUDE_API_KEY:
        return None, (
            'No API key found.\n\n'
            'To enable AI explanations:\n'
            '1. Get a free key at console.anthropic.com\n'
            '2. Create a .env file in your Downloads folder\n'
            '3. Add this line: CLAUDE_API_KEY=sk-ant-your-key-here\n'
        )

    # Craft the prompt — the wording here directly affects the quality of
    # Claude's response. 'Patient advocate' framing produces warmer, more
    # accessible language than simply asking for a 'plain English summary'.
    prompt = (
        'You are a patient advocate helping everyday people understand clinical trial documents. '
        'Please explain the following text in warm, clear, plain language as if speaking to someone '
        'with no medical background. Use short paragraphs and a conversational narrative. '
        'Explain medical terms in context rather than defining them in isolation.\n\n'
        f'Clinical trial text:\n{medical_text}'
    )

    # Build the JSON request body expected by the Anthropic API
    payload = json.dumps({
        'model': 'claude-sonnet-4-20250514',  # Specify the Claude model version
        'max_tokens': 1000,                    # Limit response length
        'messages': [{'role': 'user', 'content': prompt}]
    }).encode('utf-8')

    # Build the HTTP POST request with required Anthropic API headers
    req = urllib.request.Request(
        'https://api.anthropic.com/v1/messages',
        data=payload,
        headers={
            'Content-Type': 'application/json',
            'x-api-key': CLAUDE_API_KEY,        # Authentication
            'anthropic-version': '2023-06-01',   # Required API version header
        },
        method='POST',
    )

    # Send the request and handle possible errors
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            # Navigate to the text content in the nested response structure
            return data['content'][0]['text'], None

    except urllib.error.HTTPError as e:
        # HTTP errors (e.g. 401 bad key, 429 rate limit) include an error body
        return None, f"API error {e.code}: {e.read().decode('utf-8')}"

    except Exception as e:
        # Catch any other errors (timeout, network failure, etc.)
        return None, f'Could not reach Claude API: {e}'


def on_translate():
    """
    Handle the Explain in Plain Language button click.

    Opens a popup window showing 'please wait', then calls the Claude API
    and updates the popup with the narrative response. If the API call fails,
    falls back to the plain-language dictionary definitions.

    The popup is a separate tkinter Toplevel window so it does not overwrite
    the trial results in the main results panel.
    """
    # Get the text the user pasted into the translator box
    medical_text = text_medical.get('1.0', tk.END).strip()

    # Validate that the user actually pasted something
    if not medical_text:
        messagebox.showinfo('Missing Text', 'Please paste clinical trial text to explain.')
        return

    # ── Build the popup window ────────────────────────────────────
    popup = tk.Toplevel(root)
    popup.title('Plain-Language Explanation')
    popup.geometry('680x520')
    popup.resizable(True, True)
    popup.config(bg=CLR_BG)

    # Popup title label
    tk.Label(popup,
             text='Plain-Language Explanation  (Powered by Claude AI)',
             font=FONT_TITLE, bg=CLR_BG, fg=CLR_LABEL_FG, pady=14).pack()

    # Scrollable text area inside the popup
    frame_pop = tk.Frame(popup, bg=CLR_BG)
    frame_pop.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 4))

    pop_scrollbar = tk.Scrollbar(frame_pop)
    pop_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    pop_text = tk.Text(frame_pop,
                       wrap=tk.WORD,
                       yscrollcommand=pop_scrollbar.set,
                       font=('Helvetica', 11),
                       padx=14, pady=12,
                       relief=tk.FLAT,
                       bg=CLR_RESULT_BG,
                       fg=CLR_RESULT_FG)
    pop_text.pack(fill=tk.BOTH, expand=True)
    pop_scrollbar.config(command=pop_text.yview)

    # Show a loading message while the API call runs
    pop_text.insert(tk.END, 'Asking Claude to explain this — please wait...\n')
    popup.update()  # Force the popup to render before the API call blocks
    set_status('Waiting for Claude AI response...', CLR_BTN_SEARCH)

    narrative, error = call_claude_api(medical_text)

    # Update the popup with the result
    pop_text.config(state=tk.NORMAL)
    pop_text.delete('1.0', tk.END)

    if error:
        # API failed — show error and fall back to dictionary definitions
        pop_text.insert(tk.END, f'⚠  {error}\n\n')
        pop_text.insert(tk.END, '─' * 50 + '\n')
        pop_text.insert(tk.END, 'Dictionary definitions for recognized terms:\n\n')
        for e in explain_terms_in_text(medical_text):
            pop_text.insert(tk.END, f'  • {e}\n\n')
        set_status('AI unavailable — showed dictionary fallback.', CLR_WARN)
    else:
        # Success — display Claude's plain-language narrative
        pop_text.insert(tk.END, narrative)
        set_status('AI explanation complete.', CLR_OK)

    # Make popup text read-only
    pop_text.config(state=tk.DISABLED)

    # Close button at the bottom of the popup
    make_button(popup, 'Close', popup.destroy, CLR_BTN_CLOSE).pack(pady=12)

print('GUI logic loaded. ✅')


#
# PURPOSE: Define helper functions that create consistently styled
#          tkinter widgets for the main window layout.
#
# WHY HELPERS INSTEAD OF INLINE CODE:
#   Every section of the app (Patient Info, Translate, Results) uses
#   the same style of LabelFrame, Label, and Entry. Rather than
#   repeating all styling options inline, these three helper functions
#   and readable.
# --------------------------------------------------------------------------


def styled_label_frame(parent, title):
    """
    Create a styled LabelFrame (section container with a visible border and title).

    Used to group related widgets into visually distinct sections:
    'Patient Information', 'Translate Medical Terms', and 'Results'.

    Args:
        parent: The parent tkinter widget.
        title (str): The section title displayed in the frame border.

    Returns:
        tk.LabelFrame: The configured frame widget (not yet placed in the layout).
    """
    return tk.LabelFrame(
        parent,
        text=f'  {title}  ',    # Padding around title text
        font=FONT_LABEL_BOLD,
        bg=CLR_PANEL,
        fg=CLR_LABEL_FG,
        padx=14,
        pady=12,
        relief=tk.GROOVE,       # Groove border style for subtle definition
        bd=2                    # Border width
    )


def styled_label(parent, text, hint=False):
    """
    Create a styled text label.

    Two modes:
    - hint=False: Standard label (e.g. 'Full Name:', 'Age:')
    - hint=True:  Smaller, muted helper text shown next to input fields
                  (e.g. 'lung · colon · pancreatic · prostate · breast')

    Args:
        parent: The parent tkinter widget.
        text (str): The label text to display.
        hint (bool): If True, apply smaller muted styling for hint text.

    Returns:
        tk.Label: The configured label widget.
    """
    return tk.Label(
        parent,
        text=text,
        font=FONT_HINT  if hint else FONT_LABEL,    # Smaller font for hints
        bg=CLR_PANEL,
        fg=CLR_HINT_FG if hint else CLR_LABEL_FG    # Muted color for hints
    )


def styled_entry(parent, width):
    """
    Create a styled single-line text input field.

    Used for all user input fields: name, age, cancer type, subtype, city.
    The flat relief and light background give inputs a modern appearance
    that contrasts cleanly against the dark panel background.

    Args:
        parent: The parent tkinter widget.
        width (int): The width of the input field in characters.

    Returns:
        tk.Entry: The configured entry widget.
    """
    return tk.Entry(
        parent,
        width=width,
        font=FONT_ENTRY,
        bg=CLR_ENTRY_BG,                # Light blue-white background
        fg=CLR_ENTRY_FG,                # Dark text for readability
        insertbackground=CLR_ENTRY_FG,  # Cursor color matches text color
        relief=tk.FLAT,                 # No 3D border effect
        bd=4                            # Slight padding inside the field
    )

print('Layout helpers loaded. ✅')


#
# PURPOSE: Build the main application window and launch it.
#
# HOW IT WORKS:
#   This cell constructs the entire GUI layout using the helper functions
#   It uses tkinter's grid geometry manager to position all widgets.
#
# LAYOUT STRUCTURE:
#   Row 0 — Header banner (dark navy with app title)
#   Row 1 — Patient Information frame (input fields + buttons)
#   Row 2 — Translate Medical Terms frame (text box + AI button)
#   Row 3 — Results frame (scrollable trial listings) [expands to fill space]
#   Row 4 — Status bar (real-time feedback messages)
#
# --------------------------------------------------------------------------

# Create the main application window
# ============================================================
# MAIN PROGRAM LOGIC
# All functions are defined above. The main program begins
# here — this is where the GUI window is built and launched.
# ============================================================
root = tk.Tk()
root.title('Georgia Clinical Trial Navigator (GCTN)')
root.resizable(True, True)       # Allow the window to be resized
root.minsize(760, 650)           # Minimum size to prevent layout breaking
root.config(bg=CLR_BG)           # Apply navy background to the window itself
root.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand horizontally

# ── Row 0: Header Banner ─────────────────────────────────────────
# A dark strip across the top with the app name and tagline
header = tk.Frame(root, bg='#132033', pady=14)
header.grid(row=0, column=0, sticky='ew')  # 'ew' = stretch full width

tk.Label(header,
         text='🔬  Georgia Clinical Trial Navigator',
         font=('Helvetica', 16, 'bold'),
         bg='#132033',
         fg='#ffffff').pack(side=tk.LEFT, padx=20)

tk.Label(header,
         text='Helping Georgia patients find cancer clinical trials',
         font=('Helvetica', 10),
         bg='#132033',
         fg='#7fa8c4').pack(side=tk.LEFT, padx=6)

# ── Row 1: Patient Information Frame ─────────────────────────────
# Contains all user input fields and the Search / Clear buttons
frame_input = styled_label_frame(root, 'Patient Information')
frame_input.grid(row=1, column=0, padx=14, pady=(10, 6), sticky='ew')

# Full Name field
styled_label(frame_input, 'Full Name:').grid(row=0, column=0, sticky='e', pady=5)
entry_name = styled_entry(frame_input, 30)
entry_name.grid(row=0, column=1, sticky='w', pady=5, padx=8)

# Age field
styled_label(frame_input, 'Age:').grid(row=1, column=0, sticky='e', pady=5)
entry_age = styled_entry(frame_input, 10)
entry_age.grid(row=1, column=1, sticky='w', pady=5, padx=8)

# Cancer Type field with hint text
styled_label(frame_input, 'Cancer Type:').grid(row=2, column=0, sticky='e', pady=5)
entry_cancer = styled_entry(frame_input, 20)
entry_cancer.grid(row=2, column=1, sticky='w', pady=5, padx=8)
styled_label(frame_input, 'lung · colon · pancreatic · prostate · breast', hint=True).grid(row=2, column=2, sticky='w')

# Subtype field (optional) with hint text
styled_label(frame_input, 'Subtype (optional):').grid(row=3, column=0, sticky='e', pady=5)
entry_subtype = styled_entry(frame_input, 20)
entry_subtype.grid(row=3, column=1, sticky='w', pady=5, padx=8)
styled_label(frame_input, 'e.g. NSCLC, HER2, TNBC, MSI', hint=True).grid(row=3, column=2, sticky='w')

# Georgia City field
styled_label(frame_input, 'Georgia City:').grid(row=4, column=0, sticky='e', pady=5)
entry_city = styled_entry(frame_input, 20)
entry_city.grid(row=4, column=1, sticky='w', pady=5, padx=8)

# Button row — Search and Clear side by side
frame_buttons = tk.Frame(frame_input, bg=CLR_PANEL)
frame_buttons.grid(row=5, column=0, columnspan=3, pady=14)

make_button(frame_buttons, '🔍  Search Clinical Trials', on_check, CLR_BTN_SEARCH).pack(side=tk.LEFT, padx=10)
make_button(frame_buttons, '🔄  Clear / New Search',     on_clear, CLR_BTN_CLEAR).pack(side=tk.LEFT, padx=10)

# ── Row 2: Translate Medical Terms Frame ─────────────────────────
# Contains the AI-powered plain-language explanation feature
frame_translate = styled_label_frame(root, 'Translate Medical Terms  (AI-Powered)')
frame_translate.grid(row=2, column=0, padx=14, pady=6, sticky='ew')

# Show Claude AI status (green if key loaded, red if not configured)
key_status = '✅  Claude AI ready' if CLAUDE_API_KEY else '⚠  Claude AI not configured — add .env file with CLAUDE_API_KEY to enable'
key_color  = CLR_OK if CLAUDE_API_KEY else CLR_ERR
tk.Label(frame_translate,
         text=key_status,
         fg=key_color,
         font=('Helvetica', 9, 'italic'),
         bg=CLR_PANEL).grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 8))

# Multi-line text box for pasting clinical trial text
styled_label(frame_translate, 'Paste clinical trial text:').grid(row=1, column=0, sticky='nw', pady=4)
text_medical = tk.Text(frame_translate,
                       width=64, height=5,
                       font=FONT_ENTRY,
                       bg=CLR_ENTRY_BG, fg=CLR_ENTRY_FG,
                       insertbackground=CLR_ENTRY_FG,
                       relief=tk.FLAT, bd=4)
text_medical.grid(row=1, column=1, padx=8, pady=4)

# Explain button — triggers AI explanation in popup window
make_button(frame_translate, '💬  Explain in Plain Language', on_translate, CLR_BTN_AI).grid(
    row=2, column=0, columnspan=2, pady=10)

# ── Row 3: Results Frame ──────────────────────────────────────────
# Scrollable read-only text area displaying trial results
# weight=1 means this row expands to fill any remaining vertical space
frame_results = styled_label_frame(root, 'Results')
frame_results.grid(row=3, column=0, padx=14, pady=6, sticky='nsew')
root.grid_rowconfigure(3, weight=1)  # Allow results frame to grow vertically

# Vertical scrollbar attached to the results text widget
scrollbar = tk.Scrollbar(frame_results)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Main results text widget — starts disabled (read-only)
text_result = tk.Text(frame_results,
                      width=80, height=18,
                      yscrollcommand=scrollbar.set,
                      wrap=tk.WORD,             # Wrap long lines at word boundaries
                      font=FONT_RESULT,
                      padx=10, pady=8,
                      relief=tk.FLAT,
                      bg=CLR_RESULT_BG,
                      fg=CLR_RESULT_FG,
                      state=tk.DISABLED)         # Read-only until results load
text_result.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=text_result.yview)

# ── Row 4: Status Bar ─────────────────────────────────────────────
# A thin bar at the bottom showing real-time app status messages
status_label = tk.Label(root,
                        text='  Ready — enter patient information to search.',
                        anchor='w',              # Left-align the text
                        fg=CLR_STATUS_FG,
                        bg=CLR_STATUS_BG,
                        font=FONT_STATUS,
                        pady=5)
status_label.grid(row=4, column=0, sticky='ew')

print('App launched! ✅')

# Launch the tkinter event loop — this keeps the window open and responsive.
root.mainloop()


