# Literature Search Action Checklist

## Quick Start This Week

### Day 1: Start with 3 Easy Wins (30 min each)

- [ ] **Paper 1**: Download Voigt 2024 from ACP
  - URL: `https://acp.copernicus.org/articles/24/3813/2024/acp-24-3813-2024.html`
  - Data already extracted above (1 point ready to add)
  - Time: 5 min (skip, already have data)
  - **Action**: Copy Voigt 2024 data point to your Excel now

- [ ] **Paper 2**: Access Harper 2022 on Cardiff
  - URL: `https://orca.cardiff.ac.uk/id/eprint/147444/`
  - Time: 15 min to download + scan for data tables
  - **Action**: Save PDF, find Tables 1-5 with H, aromatics, nvPM values
  - **Expected gain**: 10-15 data points

- [ ] **Paper 3**: Access Smith 2024 on MDPI
  - URL: `https://www.mdpi.com/2073-4433/15/3/308`
  - Time: 15 min to download + identify data sections
  - **Action**: Look for fuel composition tables and nvPM EI results
  - **Expected gain**: 15-20 data points

### Day 2-3: Medium Effort Papers (45 min each)

- [ ] **Paper 4**: Brem 2015 aromatic study
  - Try: ResearchGate search "Brem aromatic" for PDF
  - URL fallback: `https://pubs.acs.org/doi/abs/10.1021/acs.est.5b04167`
  - Time: 20 min to locate + 25 min to extract tables
  - **Expected gain**: 15-25 data points (aromatic is primary variable)

- [ ] **Paper 5**: Benito 2025 SAMPLE IV
  - URL: `https://orca.cardiff.ac.uk/id/eprint/184201/1/sampleiv_-_d7-3.pdf`
  - Time: 30 min to download + extract fuel property tables
  - **Expected gain**: 20-30 data points from SAMPLE campaign

### Week 2: Systematic Data Mining (2-3 hours)

- [ ] **Papers 6-8**: Durdina/Harper/Durand series (3 papers, 1-2 hours)
  - Check Cardiff ORCA for all Harper & Durand papers
  - Expected: 35-55 points combined
  - **Strategy**: Download all, batch extract tables

- [ ] **Paper 9**: Gierens 2024 literature review
  - URL: Manchester Metropolitan repository (`e-space.mmu.ac.uk`)
  - Expected: 10-15 compiled points from literature synthesis

---

## Data Extraction Template (Use for Each Paper)

When you open each paper, look for:

**Section to Find**: Results, Data Tables, or Supplementary Materials

**Extract These Columns**:
```
Campaign,Engine,Fuel Type,Hydrogen(%),Aromatics(%),nvPM_EI(mg/kg),Ref_Fuel_H(%),Thrust(%),Notes
```

**Example from Voigt 2024**:
```
ECLIF2,RR_Trent_XWB84,Jet_A1,13.5,Present,9.5E14,13.5,~85%,Flight_FL350
ECLIF2,RR_Trent_XWB84,HEFA_SPK,14.8,<DL,6.1E14,13.5,~85%,Flight_FL350
```

---

## Priority Order (by Data Yield per Hour)

### Tier 1: High Yield / Easy Access (Do First)
1. **Voigt 2024** - ✓ Already extracted
2. **Brem 2015** - 15-25 points, aromatic-focused (your strength)
3. **Benito 2025** - 20-30 points, SAMPLE campaign
4. **Smith 2024** - 15-20 points, direct MDPI access

**Tier 1 Total**: 60-95 points in ~2 hours

### Tier 2: Medium Yield / Moderate Effort (Do Second)
5. **Harper 2022** - 10-20 points
6. **Durand 2021** - 8-12 points
7. **Gierens 2024** - 10-15 points

**Tier 2 Total**: 28-47 points in ~2 hours

### Tier 3: Comprehensive (If Time Permits)
8. **Durdina 2019-2021** (3 papers) - 35-55 points
9. **Harper 2024** - 10-15 points

**Tier 3 Total**: 45-70 points in ~3 hours

**Grand Total: 133-212 points from 9 papers in 7 hours**

---

## Realistic Weekly Timeline

### Week 1
- **Monday-Tuesday** (2 hours): Tier 1 papers (#1-4)
  - Expected: 65 new data points
  - Model performance: R² → 0.53 → 0.55 (estimate)

- **Wednesday-Friday** (2 hours): Tier 2 papers (#5-7)
  - Expected: +35 new data points (total 100)
  - Model performance: R² → 0.57 (estimate)

### Week 2
- **Mon-Tue** (3 hours): Tier 3 papers (#8-9)
  - Expected: +55 new data points (total 155)
  - Model performance: R² → 0.60-0.62 (estimate)

- **Wed-Fri**: Additional campaign mining
  - Search: AAFEX, Corporan, DLR SWING (using keywords from SEARCH_KEYWORDS.txt)
  - Expected: +50-100 additional points (total 205-255)
  - Model performance: R² → 0.63-0.65 (estimate)

---

## While Waiting for Paper Downloads: Prep Work

While papers download, prepare your Excel sheet:

- [ ] Create new column: `paper_source_DOI`
- [ ] Create new column: `data_extracted_date`
- [ ] Create new column: `extraction_quality` (flag duplicates/unreliable values)
- [ ] Sort current data by `campaign` and `engine` to spot gaps
- [ ] Identify which rows need Arom_ref filled in (quick win per ACTION_PLAN.md)

---

## If PDF Download Fails

**Alternative access strategies**:

1. **If ResearchGate link fails**: 
   - Email author directly: [Find email from paper]
   - Message: "Hi [Author], I'm working on nvPM emissions vs fuel properties. Could you share the PDF of your [Paper]? I'm citing your work."
   - Success rate: ~60% get response in 24-48 hours

2. **If Cardiff ORCA fails**:
   - Try: `cardiff.ac.uk` direct search + author name
   - Try: Contacting Cardiff library with paper DOI

3. **If ACS Publications blocks access**:
   - Try: Google Scholar → Full Text PDF link
   - Try: ResearchGate author page
   - Try: University proxy if you have access

4. **If MDPI article is paywalled** (unlikely):
   - MDPI is usually open access; check "Download PDF" button
   - If blocked, email MDPI customer service (they're helpful)

---

## Success Criteria for Each Paper

Each paper extraction = complete when you have:
- [ ] Campaign name(s) identified
- [ ] Engine model(s) identified
- [ ] At least 2 rows with [H, nvPM_EI, Thrust] filled
- [ ] Aromatic data if available (even if partial)
- [ ] Source citation/DOI recorded

---

## Next Actions (Do These Now)

1. **Immediately**: Copy Voigt 2024 point to Excel (see data above)
2. **Today**: Download Harper 2022 from Cardiff (`https://orca.cardiff.ac.uk/id/eprint/147444/`)
3. **Today**: Download Smith 2024 from MDPI (`https://www.mdpi.com/2073-4433/15/3/308`)
4. **Tomorrow**: Extract tables from both + add to Excel

**Expected outcome by tomorrow**: +30-35 new data points added to your dataset

---

## File Structure to Organize

Create a new folder in your project:
```
nvpm_analysis/
  PAPERS_DOWNLOADED/
    voigt_2024_SAF_contrails.pdf          [✓ DATA EXTRACTED]
    harper_2022_RQL_combustor.pdf         [To download]
    smith_2024_alternative_fuels.pdf      [To download]
    brem_2015_aromatic_effects.pdf        [To download]
    benito_2025_SAMPLE_IV.pdf             [To download]
    ...
  EXTRACTED_DATA/
    AAFEX_extracted.csv
    ECLIF_extracted.csv
    SAMPLE_extracted.csv
    ...
```

---

**Last Updated**: 2026-06-13
**Status**: Ready to execute
**Expected Data Gain**: 120-150 points in 1-2 weeks
**Expected R² Improvement**: 0.53 → 0.60-0.65 (depending on model updates)
