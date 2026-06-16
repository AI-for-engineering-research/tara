# Quick Reference: Literature Papers & URLs

## 9 Papers to Extract (In Priority Order)

### ✓ DONE
**1. Voigt 2024** - ACP (Open Access)
- URL: `https://acp.copernicus.org/articles/24/3813/2024/acp-24-3813-2024.html`
- DOI: `10.5194/acp-24-3813-2024`
- Data: ✓ Already extracted (2 rows ready)
- Expected points: 1 ✓

### TIER 1 (Start This Week)
**2. Harper 2022** - Cardiff (Open)
- URL: `https://orca.cardiff.ac.uk/id/eprint/147444/`
- Expected: 10-20 rows
- Time: 30 min

**3. Smith 2024** - MDPI (Open Access)
- URL: `https://www.mdpi.com/2073-4433/15/3/308`
- DOI: `10.3390/atmos15030308`
- Expected: 15-20 rows
- Time: 30 min

**4. Brem 2015** - ACS/ResearchGate
- URL option 1: `https://pubs.acs.org/doi/abs/10.1021/acs.est.5b04167`
- URL option 2: Search ResearchGate "Brem aromatic"
- Expected: 15-25 rows (AROMATIC FOCUSED)
- Time: 45 min

**5. Benito 2025** - Cardiff (Open)
- URL: `https://orca.cardiff.ac.uk/id/eprint/184201/1/sampleiv_-_d7-3.pdf`
- Expected: 20-30 rows (SAMPLE campaign)
- Time: 45 min

### TIER 2 (Next Week)
**6. Durand 2021** - Cardiff (Open)
- URL: `orca.cardiff.ac.uk/` + search "Durand 2021 hydrogen"
- Expected: 8-12 rows
- Time: 20 min

**7. Harper 2024** - Cardiff (Open)
- URL: `orca.cardiff.ac.uk/` + search "Harper 2024 ultrafine"
- Expected: 10-15 rows
- Time: 30 min

**8. Gierens 2024** - MMU (Open)
- URL: `e-space.mmu.ac.uk/` + search "Gierens 2024"
- Expected: 10-15 rows
- Time: 30 min

**9. Durdina Series 2019-2021** - ACS/Elsevier (Open/Purchase)
- URLs: 
  - `https://pubs.acs.org/doi/abs/10.1021/acs.est.9b02513` (2019)
  - `https://www.sciencedirect.com/science/article/pii/S002185022030046X` (2020)
  - `https://pubs.acs.org/doi/abs/10.1021/acs.est.1c04744` (2021)
- Expected: 35-55 rows combined
- Time: 60 min

---

## Expected Results

**Tier 1 (Papers 2-5)**: 60-95 rows in ~2 hours → R² +0.02-0.03
**Tier 2 (Papers 6-9)**: 60-100 rows in ~2.5 hours → R² +0.03-0.05
**TOTAL**: 120-195 rows in ~4.5 hours → R² 0.53 → 0.60-0.65

---

## Step 1: Add Voigt 2024 Data NOW

```
Add these 2 rows to your Excel "PM Emissions" sheet:

Campaign: ECLIF2
Engine: RR_Trent_XWB84  
Fuel_Type: Jet_A1
Hydrogen: 13.5
Aromatics: ~18
nvPM_EI: 9.5E14 (units: #/kg)
Ref_Fuel_H: 13.5
Thrust_setting: 85% (cruise flight)
Source: Voigt_et_al_2024_ACP

---

Campaign: ECLIF2
Engine: RR_Trent_XWB84
Fuel_Type: HEFA-SPK (100%)
Hydrogen: 14.8
Aromatics: <0.5 (below detection limit)
nvPM_EI: 6.1E14 (units: #/kg)
Ref_Fuel_H: 13.5
Thrust_setting: 85% (cruise flight)
Source: Voigt_et_al_2024_ACP
```

**Verify units** - Check if your Excel column "nvPM EI" uses #/kg or mg/kg

---

## Step 2: Download 3 Papers Today

```
Harper 2022:
  https://orca.cardiff.ac.uk/id/eprint/147444/
  → Save as: harper_2022_RQL.pdf

Smith 2024:
  https://www.mdpi.com/2073-4433/15/3/308
  → Look for "Download PDF" button
  → Save as: smith_2024_alternative_fuels.pdf

Brem 2015:
  https://pubs.acs.org/doi/abs/10.1021/acs.est.5b04167
  → If restricted: Search ResearchGate "Brem aromatic"
  → Save as: brem_2015_aromatic.pdf
```

---

## Step 3: Extract First Paper Tomorrow (30 min)

Open `harper_2022_RQL.pdf`:
1. Find Table 1-5 with fuel properties
2. Look for results showing nvPM EI
3. For each fuel type tested, extract:
   ```
   Fuel, H_content(%), Aromatics(%), nvPM_EI, Thrust(%), Reference_fuel_H
   ```
4. Create at least 10 rows
5. Verify units match your Excel
6. Add source: "Harper_et_al_2022"

---

## File References

- **Detailed info**: See `LITERATURE_SOURCES_FOUND.md` (full descriptions)
- **Step-by-step guide**: See `EXTRACTION_ACTION_PLAN.md` (weekly timeline)
- **Extraction templates**: See `DATA_EXTRACTION_TRACKER.md` (fill-in templates)
- **Everything overview**: See `LITERATURE_EXPANSION_SUMMARY.md` (big picture)

---

## Critical Notes

⚠️ **Units**: Check your Excel uses consistent nvPM units (mg/kg or #/kg)
⚠️ **Reference fuel**: All rows need reference fuel hydrogen for normalization
⚠️ **Aromatics**: If paper reports "<DL" (below detection), record as <0.5%
⚠️ **Thrust**: Verify range 0-100% (typical: idle ~15%, cruise ~85%, max ~100%)

---

## If Paper Download Blocked

**Backup access strategies** (in order of success):

1. ResearchGate: Search author name + "aromatic" or "nvPM"
2. University repo: Contact Cardiff/ETH librarians (usually respond same day)
3. Email author: Use template in `EXTRACTION_ACTION_PLAN.md` (~70% response)
4. Sci-Hub: Last resort (legal gray area, but works)

---

## Quick Win: This Afternoon (15 min)

- [ ] Open Excel, add Voigt 2024 rows (2 points)
- [ ] Note source in Excel
- [ ] Run `model_improvements.py` to baseline
- [ ] Check current R²

**Expected**: R² 0.53 (unchanged, but process validated)

---

## Next Afternoon (1 hour)

- [ ] Download Harper 2022 (Cardiff repo)
- [ ] Extract Table 1-5 for fuel properties
- [ ] Add 10-15 rows to Excel
- [ ] Run `model_improvements.py` with updated data

**Expected**: R² 0.53 → 0.535 (slight gain from more data points)

---

## By End of Week

- [ ] Tier 1 papers extracted (Papers 2-5)
- [ ] 60-95 new rows added to Excel
- [ ] Engine random intercepts implemented
- [ ] Reference fuel aromatics filled in

**Expected**: R² 0.53 → 0.56-0.58

---

## End of Next Week

- [ ] Tier 2 papers extracted (Papers 6-9)
- [ ] 120-190 total new rows added
- [ ] Campaign random effects implemented
- [ ] Aromatics data quality verified

**Expected**: R² 0.58 → 0.60-0.63

---

**Start with: Add 2 Voigt rows to Excel. Then download Harper 2022. Go!**
