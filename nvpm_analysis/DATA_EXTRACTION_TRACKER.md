# Literature Data Extraction Tracker

## Data Already Extracted (1 point ready to add)

### From Voigt et al. 2024 - ACP Open Access ✓

| Campaign | Engine | Fuel_Type | H_Content(%) | Aromatics(%) | nvPM_EI(mg/kg) | Ref_Fuel_H(%) | Thrust(%) | Source_DOI | Notes |
|----------|--------|-----------|--------------|--------------|----------------|----------------|-----------|-----------|-------|
| ECLIF2 | RR_Trent_XWB84 | Jet_A1 | 13.5 | Present | 9.5×10¹⁴ | 13.5 | ~85% | 10.5194/acp-24-3813-2024 | Flight FL350, Apr 2021 |
| ECLIF2 | RR_Trent_XWB84 | HEFA-SPK | 14.8 | <DL | 6.1×10¹⁴ | 13.5 | ~85% | 10.5194/acp-24-3813-2024 | Flight FL350, Apr 2021 |

**Extraction Notes**:
- Source: High-altitude flight data (most realistic)
- Quality: High (peer-reviewed, ECLIFII campaign)
- Action: Convert 10¹⁴ units to mg/kg if needed for your dataset
- Alert: Verify your Excel uses consistent nvPM units

---

## Papers Ready to Extract (Tier 1 Priority)

### Paper 1: Harper et al. 2022 - RQL Combustor
**Status**: Ready to download from Cardiff

**Download**: `https://orca.cardiff.ac.uk/id/eprint/147444/`

**What to look for**:
- Table 1 or 2: Fuel properties (H, aromatics, etc.)
- Figure or Table with nvPM EI results
- Section: "Experimental Setup" for thrust/power settings
- Supplementary materials if available

**Expected extraction**: 10-20 rows

**Checklist when extracting**:
- [ ] Fuel types identified (count how many different fuels tested)
- [ ] H content values for each fuel
- [ ] Aromatics values for each fuel
- [ ] nvPM measurements found (EI, number, mass, or all)
- [ ] Thrust/power settings noted
- [ ] Reference fuel identified
- [ ] At least 3 data rows extracted

**Placeholder for extracted data** (to fill as you extract):
```
Harper_2022_RQL

Fuel_A, H=X%, Arom=Y%, nvPM_EI=Z
Fuel_B, H=X%, Arom=Y%, nvPM_EI=Z
Fuel_C, H=X%, Arom=Y%, nvPM_EI=Z
...
```

---

### Paper 2: Smith et al. 2024 - MDPI Open Access
**Status**: Ready to download from MDPI

**Download**: `https://www.mdpi.com/2073-4433/15/3/308`

**What to look for**:
- Section: "Results" with fuel property tables
- Figure or Table: nvPM vs fuel properties
- Fuel types tested (count them)
- H content and aromatic content data

**Expected extraction**: 15-20 rows

**Checklist when extracting**:
- [ ] Alternative fuels identified (HEFA, FT, SAF blends, etc.)
- [ ] H content for each blend
- [ ] Aromatics percentage if available
- [ ] nvPM measurements reported
- [ ] Combustor conditions noted
- [ ] At least 4-5 different fuels documented

**Placeholder for extracted data**:
```
Smith_2024_Combustor

Fuel_blend, H=X%, Arom=Y%, nvPM_EI=Z
...
```

---

### Paper 3: Brem & Durdina 2015 - Aromatic Focus
**Status**: Locate via ResearchGate

**Download strategies**:
1. Try: `https://pubs.acs.org/doi/abs/10.1021/acs.est.5b04167`
2. Fallback: Search ResearchGate "Brem aromatic"
3. Last resort: Email Brem or Durdina directly

**What to look for** (this is YOUR KEY PAPER):
- Table: Aromatic content variation across fuels
- Figure: nvPM EI vs aromatic content (primary relationship)
- BC mass and nvPM number indices
- Multiple aromatic percentages tested

**Expected extraction**: 15-25 rows (this paper systematically varies aromatics)

**Checklist when extracting**:
- [ ] Aromatic content range identified (minimum to maximum %)
- [ ] nvPM responses recorded for each aromatic level
- [ ] Multiple fuels/conditions tested
- [ ] Measurement type identified (number, mass, BC)
- [ ] Reference fuel specified
- [ ] At least 6-10 distinct aromatic levels documented

**Placeholder for extracted data**:
```
Brem_2015_Aromatic_Study

Arom=X%, H=Y%, nvPM_Number=Z, nvPM_Mass=W
...
(Should show clear trend with aromatics)
```

---

### Paper 4: Benito et al. 2025 - SAMPLE IV
**Status**: Ready to download from Cardiff

**Download**: `https://orca.cardiff.ac.uk/id/eprint/184201/1/sampleiv_-_d7-3.pdf`

**What to look for**:
- Table: SAMPLE fuel matrix (Jet A-1 + various SAF blends)
- Fuel property specifications (H, aromatics, sulfur)
- Corresponding nvPM measurements
- Blend ratios documented (e.g., "50% HEFA-SPK / 50% Jet A-1")

**Expected extraction**: 20-30 rows

**Checklist when extracting**:
- [ ] Reference fuel (Jet A-1) H and aromatics documented
- [ ] Each SAF blend identified with % composition
- [ ] H and aromatics for each blend
- [ ] nvPM EI measured for each condition
- [ ] Blend ratio documented (critical for your model)
- [ ] At least 8-12 distinct blends extracted

**Placeholder for extracted data**:
```
SAMPLE_IV_Campaign

Jet_A1, H=13.X%, Arom=18%, nvPM_EI=Y
50%_HEFA_50%_JA1, H=13.X%, Arom=Y%, nvPM_EI=Z
100%_HEFA, H=14.X%, Arom=<DL%, nvPM_EI=W
...
(Should show clear blend response)
```

---

## Tier 2 Papers (Extract After Tier 1)

### Paper 5: Harper & Durand 2024 - Ultrafine Particles
**Download**: Cardiff ORCA repository
**Expected**: 10-15 rows with H content focus
**Timeline**: Week 2

### Paper 6: Durand et al. 2021 - APU Study
**Download**: Cardiff ORCA repository
**Expected**: 8-12 rows with H content variation
**Timeline**: Week 2

### Papers 7-9: Durdina/Gierens/Harper series
**Combined expected**: 45-70 rows
**Timeline**: Week 2-3

---

## Data Entry Into Your Excel

**Process**:

1. **Extract table from paper**
   - Copy data into this markdown tracker first
   - Verify units match your Excel (especially nvPM_EI units!)

2. **Add to your Excel sheet**
   - Match columns: Campaign, Engine, Fuel, H_content, Ref_H, Aromatics, nvPM_EI, Thrust
   - Add new column: `source_paper` (e.g., "Voigt_2024")
   - Add new column: `extraction_date` (today's date)
   - Add new column: `data_quality` (mark as "extracted", "verified", "needs_unit_conversion", etc.)

3. **Mark completed**
   - Check off paper in this tracker
   - Record date completed and # rows added
   - Note any data quality issues found

---

## Unit Conversions (Critical!)

**Verify your current Excel uses consistent units**:

### nvPM EI (emission index)
- **Primary unit in papers**: mg/kg fuel
- **Alternative units seen**:
  - Number (#/kg) - different measurement!
  - 10¹⁴ #/kg - needs conversion
  - Relative EI - ratio to reference fuel

**Decision**:
- If paper reports nvPM_EI in #/kg, note separately as "nvPM_Number"
- If paper reports as 10ⁿ #/kg, note the exponent
- Your ACTION_PLAN.md suggests you're using "relative nvPM EIn" - verify scale

### Hydrogen content
- **Standard**: mass % (what you're using)
- **Verify**: All papers use %w (weight %)
- **Flag**: If any report H/C ratio instead

### Aromatics
- **Standard**: volume % or mass %
- **Flag**: If paper specifies "monoaromatics" or "naphthalene" separately
- **Note**: Voigt 2024 reports "<DL" (below detection limit) - record as <0.5% or "trace"

---

## Quality Assurance Checklist

Before adding extracted row to Excel, verify:

- [ ] Campaign name matches existing entries (consistent naming)
- [ ] Engine model identifiable (look up if abbreviation unclear)
- [ ] Fuel type clearly specified
- [ ] H content in range 12-15% (red flag if outside)
- [ ] Aromatics in range 0-25% (red flag if outside)
- [ ] nvPM_EI reasonable (~1-20 mg/kg or 1-10×10¹⁴ #/kg)
- [ ] Thrust setting 0-100% (check idle ~15%, cruise ~85%, max ~100%)
- [ ] Reference fuel identified
- [ ] DOI or source citation recorded

**If data looks wrong**: Check paper again or flag as "needs_verification"

---

## Running Tally

**Update this as you extract**:

```
Papers Downloaded: __/4 (Tier 1)
Rows Extracted: ___/100 (target for Tier 1)
Data Quality Issues Found: ___
Unit Conversions Needed: ___
Ready to Add to Excel: ___

Week 1 Progress:
- Day 1: +2 rows (Voigt)
- Day 2: +__ rows
- Day 3: +__ rows
- Day 4: +__ rows
- Day 5: +__ rows
Total Week 1: ___/65 target

Week 2 Progress:
- Papers to extract: Tier 2 (5-7)
- Expected total rows: ___
```

---

## Next Steps (Start Now)

1. **Today**:
   - [ ] Save this file
   - [ ] Copy Voigt 2024 data point to your Excel (see table above)
   - [ ] Note in your Excel: "Paper source: Voigt et al. 2024 ACP"

2. **Tomorrow**:
   - [ ] Download Harper 2022 (Cardiff URL)
   - [ ] Download Smith 2024 (MDPI URL)
   - [ ] Begin extracting tables

3. **This Week**:
   - [ ] Complete Tier 1 papers (expected: 65+ rows)
   - [ ] Compile extracted data into separate CSV or sheet
   - [ ] Run `model_improvements.py` with expanded dataset

4. **Next Week**:
   - [ ] Extract Tier 2 papers (expected: 35+ rows)
   - [ ] Implement campaign random effects (from ACTION_PLAN.md)
   - [ ] Monitor R² improvement (target: 0.57-0.62 by mid-week 2)

---

**Last Updated**: 2026-06-13  
**Voigt 2024 Data**: ✓ Extracted and ready to use
**Next Paper to Extract**: Harper 2022 (Cardiff)
