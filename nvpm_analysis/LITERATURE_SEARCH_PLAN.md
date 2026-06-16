# Literature Review Search Plan: nvPM vs Fuel Aromatics/Hydrogen

## Your Current Data Summary
- **343 rows** from "PM Emissions" sheet
- **19 campaigns** covered
- **12 major authors/groups**
- **Data completeness issues**: Ref Hydrogen (57.7%), nvPM EIn (56.3%), Aromatics (65.6%)
- **Usable points** (all 4 key fields non-null): ~130 rows
- **Single-variable correlation**: H vs log(nvPM EIn ratio) = **–0.60** (modest)
- **Better correlation**: Aromatics vs log(nvPM EIn ratio) = **+0.70** (strong; but collinear with H)

---

## Part 1: Test Campaigns You Already Have

### High-Quality Campaigns Present
1. **AAFEX-I & AAFEX-II** (Moore et al. 2015–2017)
   - NASA Glenn ground engine tests
   - Comprehensive FT/SAF blends
   - ~60 data points in your sheet

2. **ACCESS-I & ACCESS-II** (Moore/Morre 2015–2017)
   - NASA aircraft flights
   - nvPM number + mass
   - ~26 data points

3. **ECLIF2/ND-MAX** (Schripp, Voigt 2021)
   - DLR + NASA high-altitude
   - SAF blends
   - ~31 data points

4. **EMPAIREX 1** (Durdina 2021)
   - ETH Zurich rig studies
   - Detailed fuel composition
   - ~14 data points (but likely **lower aromatics coverage**)

5. **A-PRIDE 7** (Brem 2015)
   - High-altitude flight
   - ~29 data points

---

## Part 2: Major Test Campaigns LIKELY MISSING

### Priority 1: High-yielding campaigns that should have fuel property data

#### ECLIF1 & ECLIF3
- **ECLIF1** (Voigt et al. 2010–2011): Earlier DLR flight campaign on A340/ATR72
  - Search: "ECLIF black carbon", "ECLIF particle number index", "Voigt ECLIF 2011"
  - Likely source: *Atm. Chem. Phys.*, *J. Geophys. Res.*
  - Expected data: nvPM number, BC, size distributions vs SAF blend

- **ECLIF3** (you have this; Markl 2024): Latest phase
  - Keep expanding; likely more fuel blends in 2023–2024 publications

#### SAMPLE / Early SAMPLE campaigns (predecessor to "SAMPLE 4")
- **SAMPLE 1–3** (Lobo/Timko/Soja 2010–2015)
- Search: "Sustainable Aviation Fuels test", "SAMPLE campaign NASA", "Lobo SAMPLE"
- Expected: Comprehensive aromatics/H/sulfur vs nvPM matrix

#### AVIATOR / INFL
- **AVIATOR**: Ground-based rig infrared contrail studies (NASA Langley)
- **INFL** (Infrared Non-volatile Particle Forecasting): Early NASA contrail/PM program
- Search: "AVIATOR infrared contrail", "INFL contrail NASA"

---

### Priority 2: Combustor/rig studies with tight fuel composition control

#### SWING burner tests (DLR Cologne)
- Direct aromatic variation studies
- Often **not in public datasets** but papers exist
- Search: "SWING combustor", "DLR aromatics soot", "Lauer SWING"
- Authors: Lauer, Will, Schripp (DLR)

#### IVT (Integrated Vehicle Health Management) / PARAGON test programs
- Military/DoD test programs; some data published
- Search: "PARAGON SAF test", "IVT particle emissions"

#### GE/CFM on-wing SAF demonstration flights
- Recent (2021–2023); selective data release
- Search: "GE SAF flight test", "CFM LEAP SAF emission index"
- Often published as press releases + limited technical reports

#### SVG (Sustainable Fuels for Green Aviation) – ESA/EU
- European Commission research program
- Likely includes fuel blends with controlled aromatics
- Search: "SVG sustainable aviation fuels", "ESA jet fuel aromatics"

---

### Priority 3: Specific fuel variation studies (look for papers, not just campaigns)

#### University of Dayton / AFOSR studies
- Direct aromatics manipulation
- Search: "Corporan aromatic jets", "Wayson aromatic soot", "Colket aromatic"
- Authors: Corporan, Wayson, Colket

#### ETH Zurich (Durdina's group + others)
- High-precision rig measurements
- Search: "Durdina fuel composition", "Zimmermann jet fuel aromatic", "Zuberbühler nvPM"

#### MIT (Timko, Miake-Lye, Wey et al.)
- Long history in this space
- Search: "MIT alternative jet fuel", "Timko fuel hydrogen content", "Miake-Lye nvPM"

#### Norwegian / Scandinavian programs
- Strong SAF focus
- Search: "Stordal HEFA", "Søvde alternative fuel", "Braathen contrail"

---

## Part 3: Highly-Targeted Search Strategies for YOU

### A. Direct searches for functional form papers
If you want studies that **already fit correlations**, search for:

1. **"ICAO CAEP / EASA nvPM Emissions Standards"** papers
   - Often review empirical correlations for regulatory models
   - Search: "ICAO CAEP WG3 nvPM EIn", "EASA PM emissions data"

2. **Soot models from combustion literature**
   - "Threshold Sooting Index" (TSI) papers – these map fuel composition → sooting tendency
   - Search: "Dewitte soot", "Fuentes threshold sooting index", "Brem soot precursor"
   - These use **aromatics** (especially naphthalene/mono/di-aromatic) not just H

3. **Multi-variable fuel property models**
   - Search: "fuel aromaticity hydrogen content emissions index"
   - Search: "empirical nvPM correlation fuel properties"

### B. Grey literature + reports (often most data)
These won't be peer-reviewed but have raw datasets:

1. **FAA technical reports** (FAA/EE & Propulsion Labs)
2. **NASA technical reports server** (ntrs.nasa.gov)
3. **DLR research reports** (dlr.de publications)
4. **Airbus/Boeing/Rolls-Royce technical reports** (sometimes public via SAF databases)
5. **ICAO CAEP working group documents** (CAEP secretariat publications)

### C. Specific keyword strings to paste into Google Scholar / ResearchGate
```
"nvPM EIn" "hydrogen content" jet fuel
"non-volatile PM" aromatic "emission index"
"soot mass index" "fuel properties" "alternative jet fuel"
"particle number index" "hydrogen" SAF blend
"black carbon emission index" HEFA FT blend
"aromatics" "surrogate" nvPM soot
```

### D. Key authors to follow (check their recent papers/datasets)
- **Voigt** (DLR, ECLIF principal investigator)
- **Moore** (NASA Glenn, AAFEX/ACCESS lead)
- **Brem** (ETH Zurich, particle emissions)
- **Schripp** (DLR, ECLIF2 lead)
- **Corporan** (AFOSR-funded aromatic studies)
- **Durdina** (ETH, detailed rig studies)
- **Lobo, Timko** (NASA, long-running SAF programs)
- **Stordal** (University of Oslo, contrail/fuel models)

---

## Part 4: Databases & Repositories to Search

| Resource | URL / How to Access | Best for |
|----------|-------------------|----------|
| **Google Scholar** | scholar.google.com | Comprehensive; use cited-by to find follow-ups |
| **PubMed Central / PMC** | pubmedcentral.nih.gov | Filter for atmospheric chemistry |
| **NTRS (NASA)** | ntrs.nasa.gov | NASA internal reports + peer-reviewed |
| **ResearchGate** | researchgate.net | Authors often share preprints |
| **Scopus** (if you have access) | scopus.com | Citation tracking; filter by venue |
| **ACS Publications** | pubs.acs.org | *Env. Sci. Tech.*, *Energy & Fuels* |
| **AGU / EGU** | agu.org, egu.eu | Atmospheric chemistry sections |
| **ICAO CAEP WG3** | icao.int | Regulatory datasets & meeting minutes |
| **SAF Working Group databases** | Various (search "SAF database") | Fuel property tables + test results |

---

## Part 5: High-Impact Venues (where the data-rich papers appear)

### Journals
- **Atmospheric Chemistry & Physics** (ACP) – open access, ECLIF/ACCESS papers
- **Journal of Geophysical Research** (JGR) – flight campaign data
- **Environmental Science & Technology** – fuel + emissions
- **Energy & Fuels** – combustion & fuel properties
- **Combustion & Flame** – mechanistic soot studies
- **Journal of Engineering for Gas Turbines & Power** (ASME) – engine test data

### Conferences
- **AIAA Propulsion Energy Forum** – annual; filter "emissions" or "SAF"
- **SAE AeroTech** – aerospace tech; emissions sessions
- **ACS Green Chemistry** – SAF sustainability focus
- **EGU General Assembly** – atmospheric/contrail sessions
- **AGU Fall Meeting** – contrail/emissions science

### Technical Reports & Standards
- **ASTM D7566** (Standard specification for SAF) – companion data sheets
- **ICAO Aircraft Emissions data bank** – regulatory harmonization
- **EASA Special Conditions for SAF** – approval data summaries

---

## Part 6: Your Data Gaps → Specific Searches to Fill Them

### Issue 1: "Only 130 usable rows after combining Hydrogen, Ref Hydrogen, Thrust, nvPM EIn"
**Action**: Search for studies that **always report these 4 fields together**.

Try:
```
"emission index" "hydrogen content" "fuel" "thrust"
"relative EI" "reference fuel" "hydrogen" SAF
```

Likely sources: NASA AAFEX, ECLIF2, ACCESS (you have most); check if **Corporan 2009–2011** or **Lobo 2010** published complete tables.

### Issue 2: "Aromatics only 65.6% complete; H-only correlation is weak"
**Action**: Find **studies where aromatics is primary variable** (not H).

Try:
```
"aromatic content" soot "emission index"
"monoaromatics" "diaromatics" "naphthalene" nvPM
"smoke point" "threshold sooting index" fuel emissions
```

Likely gold mine: **TSI/Smoke-point literature** (Dewitte, Fuentes, Gupta groups).

---

## Part 7: Creative Idea – Build a Surrogate Aromatics Model

Since **aromatics (corr=+0.70) >> hydrogen (corr=-0.60)** and they're collinear (–0.84):

**Two-step approach**:
1. **Find/build a model**: aromatics ≈ f(hydrogen, fuel_type, sulfur, …)
2. **Then**: nvPM EIn ≈ g(aromatics, thrust) = h(f(H), thrust)

This way you get "hydrogen-only" predictions **implicitly through aromatics**.

Search for papers on **"jet fuel composition prediction"** or **"surrogate fuels"** to find if anyone's already done this.

---

## Part 8: Your Immediate Next Steps (Ranked by Impact/Effort)

### Week 1: Quick wins
1. **Check NTRS/NASA**: Download "AAFEX-I complete data", "SAMPLE 1-3 full tables"
   - Effort: 1 hour
   - Expected gain: +20–50 rows with complete field coverage

2. **Search Google Scholar**: `"Corporan" "aromatic" "emission index"` (2008–2014)
   - Effort: 30 min
   - Expected gain: Find 3–5 papers; +10–30 rows if you can extract tables

3. **ETH Zurich / Durdina group**: Check their research group page for rig data papers
   - Effort: 30 min
   - Expected gain: ~5 papers; likely high-quality fuel property detail

### Week 2: Medium-effort systematic search
1. **Threshold Sooting Index literature**: Search "Fuentes", "Dewitte", "Gupta" soot papers
   - Effort: 1–2 hours (reading abstracts)
   - Expected gain: Conceptual framework for aromatics → soot mapping

2. **ICAO CAEP WG3 meeting documents**: Find latest nvPM data compilations
   - Effort: 1 hour (downloading PDFs)
   - Expected gain: Regulatory-standard dataset; might have 50+ points

3. **Recent SAF flight trials**: Search "GE SAF", "CFM LEAP", "Rolls-Royce SAF" + emissions
   - Effort: 1 hour (press releases + searching for white papers)
   - Expected gain: New engines/blends; +5–20 rows

### Week 3: Deep dive into specific gaps
1. **Follow DLR group** (Schripp, Voigt, Lauer): Get ECLIF1, SWING papers
   - Check ResearchGate for preprints
   - Expected gain: +30–50 rows; mechanistic insight

2. **Check Corporan's AFOSR publications**: Direct aromatic variation
   - Effort: 1–2 hours
   - Expected gain: +20 rows; very clean aromatic gradient

---

## Part 9: Data Extraction Template

When you find a paper with nvPM vs fuel property data, extract:

| Field | Why |
|-------|-----|
| **Campaign/Paper** | Attribution |
| **Engine model** | Account for engine effects |
| **H content (%)** | Your key predictor |
| **Aromatics (%)** | Secondary predictor |
| **nvPM EIn (mg/kg)** or **PN EIn (#/kg)** | Target variable |
| **Reference fuel H (%)** | For ratio normalization |
| **Thrust or Power setting (%)** | Condition variable |
| **Temperature / Alt** | Optional: combustor inlet condition |

---

## Part 10: Quick Fix for Your R² = 0.59 Issue

Before adding more data, **try these model improvements on your current 130 rows**:

1. **Add campaign/engine as random intercept** (mixed model)
   - Likely jump: +0.05–0.10 in R²

2. **Include aromatics** (even as secondary)
   - Likely jump: +0.10–0.15 in R²

3. **Use log-linear in thrust** instead of linear
   - Likely jump: +0.03–0.07 in R²

4. **Check for outliers** in your 130 rows (especially low-thrust or high-aromatic points)
   - Likely jump: +0.02–0.05 in R² (and insight)

I can help you implement **any of these** right now if you want.

---

## Summary: Your Research Plan

| Phase | Action | Expected New Data | Effort |
|-------|--------|-------------------|--------|
| **Now** | Improve model on current 130 rows | – | 2–3 hrs |
| **Week 1** | NASA + Corporan quick searches | +20–50 rows | 1.5 hrs |
| **Week 2** | Systematic campaign/author tracking | +30–50 rows | 3 hrs |
| **Week 3** | Deep literature on aromatic surrogate | +20–40 rows | 2 hrs |
| **Total new data** | – | **+70–180 rows** | **~8 hrs** |

This could realistically move you to **200–310 usable rows**, which often changes R² from 0.59 to **0.65–0.75** depending on model form.

---

**Ready to dig in?** I can:
1. Help you implement the model improvements (mixed effects, aromatics inclusion, diagnostics)
2. Build a **data extraction pipeline** (parsing paper tables, normalizing units)
3. Create a **source tracking spreadsheet** so you don't duplicate searches

What would be most valuable right now?
