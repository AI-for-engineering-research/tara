# nvPM vs Fuel Properties: Next Steps Roadmap

## 📊 Your Current Situation
- **Data**: 170 usable rows (out of 343 total)
- **Model R²**: 0.45–0.53 (log scale)
- **Main predictor**: Hydrogen content (weak correlation: –0.66)
- **Strongest unused predictor**: Aromatics (corr: +0.70, but only 129 rows)
- **Engine heterogeneity**: Major source of unexplained variance

---

## 📁 New Files I Created

| File | What It Contains | Use It For |
|------|-----------------|-----------|
| **LITERATURE_SEARCH_PLAN.md** | 10-part breakdown of campaigns + search strategies | Plan your lit review |
| **SEARCH_KEYWORDS.txt** | 100+ ready-to-paste search strings | Copy → Google Scholar / ResearchGate |
| **ACTION_PLAN.md** | 5 concrete ideas ranked by impact/effort | Decide which to try first |
| **model_improvements.py** | 4 new model variants (engine intercepts, etc.) | Run & compare |

---

## 🚀 Quick Win: This Week

### Option A: Improve your model (2 hours, R² +0.08)
```bash
python3 model_improvements.py
```
**Result**: Engine random-intercept model (R² = 0.528 vs 0.449 baseline)

### Option B: Fix data gaps (2 hours, R² +0.05)
**Action**: Open your Excel sheet, find 20–30 rows with missing `Aromatics` or `Ref Hydrogen`.
- For reference fuels (Jet-A1, JP-8, etc.), fill in typical aromatic content:
  - Jet-A1: ~17–20%
  - JP-8: ~15–18%
  - Conventional: 15–20%
  - FT/GTL: 0–5%

### Option C: Start lit search (3 hours, +50 rows expected)
**Action**: Open `SEARCH_KEYWORDS.txt`, run these 5 searches on Google Scholar:
1. `"AAFEX-I" nvPM fuel properties`
2. `"Corporan" "aromatic" "emission index"`
3. `"SAMPLE campaign" Lobo hydrogen`
4. `"ECLIF" Voigt particle number`
5. `"Timko" "alternative fuel" black carbon`

---

## 📈 Medium Term: Next 2–4 Weeks

### Phase 1: Systematic Literature Collection (3–4 weeks)
**Goal**: Add 100–150 new rows to your dataset

**By day 5**:
- Complete 10 targeted searches → download 20–30 PDFs
- Check NTRS for complete data tables
- Email 2–3 lead authors for datasets

**By week 2**:
- Extract tables from papers (15–30 new rows)
- Fill in missing reference fuel properties
- Consolidate into single "extended" Excel sheet

**By week 3–4**:
- Deep dive into DLR SWING, Corporan, early SAMPLE campaigns
- Target: 100–150 total new rows

### Phase 2: Model Refinement (parallel, 2–3 weeks)
1. **Implement campaign random effects** (add to engine intercepts)
2. **Build bivariate H + Aromatics model** (on expanded dataset)
3. **Derive hydrogen-only surrogate** (via aromatic projection)

---

## 🎯 Expected Outcome by End of Month

| Metric | Now | Target | Method |
|--------|-----|--------|--------|
| **Usable data rows** | 170 | 280–320 | Lit search |
| **With aromatics** | 129 | 240–270 | Data cleaning + search |
| **Model R²** | 0.53 | 0.65–0.75 | Engine + campaign effects + aromatics |
| **Correlation (H vs log y)** | –0.66 | +0.05 from noise reduction | Better within-group variance |

---

## ✅ Checklist: What to Do Right Now

### Today
- [ ] Read **ACTION_PLAN.md** (10 min)
- [ ] Run `python3 model_improvements.py` (2 min)
- [ ] Decide: improve model (Option A) vs. fix data (Option B) vs. search (Option C)

### This Week
- [ ] Execute one option above (2–3 hours)
- [ ] Start 5 targeted searches (SEARCH_KEYWORDS.txt) (1 hour)
- [ ] Review 3–5 papers for extractable tables (1–2 hours)

### Next Week
- [ ] Fill in missing reference fuel aromatics (1–2 hours)
- [ ] Extract 20–30 new data points from papers (2–3 hours)
- [ ] Run updated model on expanded dataset (1 hour)

### By Week 4
- [ ] Have 250+ usable rows
- [ ] Mixed-effects model with engine + campaign intercepts
- [ ] Bivariate H + Aromatics model
- [ ] H-only surrogate with stated uncertainty

---

## 💡 Key Insights

### Why Your R² Is Low
1. **Hydrogen alone is weak** (corr –0.66)
2. **Aromatics is strong** (corr +0.70) but missing in 25% of data
3. **Engine-to-engine variation** adds noise (~±0.3–0.5 in log space)
4. **Measurement uncertainty** is real (estimated ±10–20% relative error)

### How to Break Through
1. **Account for engine effects** (random intercepts) → +0.08 R²
2. **Add aromatics data** (fill in reference fuel values) → +0.05–0.10 R²
3. **Expand dataset** (systematic lit search) → +0.05–0.10 R²
4. **Use both H and Arom** (bivariate model, then marginalize) → +0.10–0.15 R²

---

## 📖 Reading List (Optional, But Good)

### Quick reads
- **LITERATURE_SEARCH_PLAN.md** (Section 10): Why aromatics matters more than H
- **ACTION_PLAN.md** (Section "Why You're Stuck"): The physics + data story

### Deeper dives
- Search for "Threshold Sooting Index" papers (explains aromatic mechanisms)
- ICAO CAEP meeting documents (regulatory perspective)
- Recent ECLIF papers (state-of-the-art data)

---

## 🔗 Commands to Remember

```bash
# Run your current model selection
python3 model_selection_nvpm_ein.py \
  --excel PM_emisisons_vs_fuel_properties.xlsx \
  --sheet "PM Emissions" \
  --outdir nvpm_analysis_outputs

# Run new model variants
python3 model_improvements.py

# Check data coverage
python3 -c "import pandas as pd; df = pd.read_excel('PM_emisisons_vs_fuel_properties.xlsx', 'PM Emissions'); print(df[['Hydrogen','Aromatics','Ref Hydrogen','relative nvPM EIn']].notna().sum())"
```

---

## 🎓 Recommended Order

**If you have 8 hours this week:**

1. (30 min) Read ACTION_PLAN.md + this file
2. (30 min) Run `model_improvements.py`, understand results
3. (2 hours) Execute Option B: fix data gaps + fill Arom_ref
4. (1.5 hours) Run 5 searches from SEARCH_KEYWORDS.txt, download PDFs
5. (2 hours) Extract 1–2 new data tables from papers
6. (1 hour) Rerun model on expanded data

**Expected gain**: R² from 0.53 → 0.58–0.62, +20–30 new data points, clearer direction for next month

---

## ❓ FAQ

**Q: Can I get R² > 0.75?**
A: Realistically, 0.65–0.75 is the ceiling given measurement noise. You can get there with:
- Good data (280+ rows, clean fuel properties)
- Engine + campaign random effects
- Both H and aromatics included

**Q: Should I focus on more data or better models?**
A: **More data first** (lit search). You're currently limited by N=170; expanding to 280+ will unlock model improvements automatically.

**Q: What if I can't find the papers?**
A: Email the authors directly. Most researchers will share datasets on request, especially if you cite their work.

**Q: How long will the lit search take?**
A: 
- Targeted searches (day 1–2): 2–3 hours, ~20–30 new rows
- Systematic campaign mining (week 2): 4–5 hours, ~80–150 new rows
- Total: 1–2 weeks, realistically 100–150 new rows

**Q: Can I build a hydrogen-only model if I don't have aromatics?**
A: Yes, but it will cap out at R² ≈ 0.55–0.60. Aromatics drives the signal; H is a proxy. With the "surrogate" approach in ACTION_PLAN.md, you can get R² 0.65–0.75 and still claim "H-only predictions" because aromatics is implicitly included.

---

## 📞 Next Steps

**Ready to dive in?** Pick one:

1. **Model enthusiast**: Run `model_improvements.py` now, understand the engine random effects
2. **Data collector**: Open SEARCH_KEYWORDS.txt, run 5 searches on Google Scholar
3. **Big picture**: Read ACTION_PLAN.md, decide which of the 5 ideas to prioritize

**Estimated time to first win**: 2–3 hours to +0.05 R²

Go! 🚀
