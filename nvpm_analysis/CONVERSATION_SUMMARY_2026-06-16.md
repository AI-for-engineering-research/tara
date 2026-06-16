# Conversation Summary: Literature Review Strategy Pivot
**Date**: June 16, 2026  
**Topic**: Restructuring nvPM literature sources to prioritize engine thrust data

---

## Problem Identified

The literature sources in `QUICK_REFERENCE.md` include many **combustor rig studies** that lack real thrust values:

- **Lab combustor rigs** (RQL, combustor test stands) operate at power settings or equivalence ratios, NOT aircraft thrust percentages
- Without real thrust values (idle 15%, cruise 85%, max 100%), data cannot be properly normalized
- Current plan includes too many lab studies that cannot contribute usable data points

---

## Literature Classification

### ✅ KEEP - Papers with Real Engine/Flight Thrust Data

These should be prioritized:

1. **Voigt 2024** - ECLIF2 flight campaign
   - Aircraft: Airbus A350 (Rolls-Royce Trent XWB-84)
   - Thrust: 85% cruise ✓
   - Status: Data already extracted

2. **Durdina series 2019-2021** - Real engine/APU tests
   - Expected: 35-55 data points
   - Likely to have thrust settings documented

3. **AAFEX Campaign** (Moore et al.)
   - Real engines with documented thrust data
   - Expected: 20-40+ data points
   - Access: NASA NTRS (fully public)

4. **SAMPLE Campaign** (Benito et al. 2025)
   - Multi-year program with real engine testing
   - Likely has thrust documentation
   - Expected: 20-30 data points

5. **Flight Campaign Series**: ECLIF, A-PRIDE, ACCESS
   - All flight-based data with real thrust values
   - Lead authors: Voigt (ECLIF), Brem (A-PRIDE)

### ❌ DEPRIORITIZE - Lab Combustor Rigs Without Thrust Data

These should be moved to lower priority or skipped:

- **Harper 2022** - RQL combustor (no real thrust)
- **Harper 2024** - RQL combustor (no real thrust)
- **Smith 2024** - Combustor rig (no real thrust)
- **Brem 2015** - Lab-based (likely combustor, not flight)
- **Gierens 2024** - Literature review (may primarily cite rig data)

---

## Action Items

### Immediate (This Week)
1. **Reprioritize search strategy** - Focus on AAFEX, ECLIF, SAMPLE campaigns first
2. **Search NASA NTRS** - For AAFEX Moore et al. complete data
3. **Search DLR/ACP** - For ECLIF Voigt and Schripp papers with flight thrust data
4. **Check Cardiff ORCA** - For SAMPLE Benito 2025 deliverable (already in list, keep this one)

### Search Queries to Try
```
Google Scholar:
- "AAFEX" "Moore" nvPM hydrogen site:ntrs.nasa.gov
- site:acp.copernicus.org "Voigt" ECLIF nvPM fuel
- "SAMPLE campaign" hydrogen content site:ntrs.nasa.gov
- "A-PRIDE" Brem aromatic emissions

ResearchGate:
- Ulrich Voigt (ECLIF lead)
- Mark Moore (AAFEX lead)
```

### Deprioritization Tasks
- Move Harper 2022 & 2024 to "optional - rig data only" section
- Mark Smith 2024 as lower priority
- Audit Brem 2015 before extraction - verify if it has real thrust data

---

## Expected Data Yield (Revised Plan)

**High-confidence sources with real thrust values:**
- Voigt 2024: 1 point (done)
- Durdina 2019-2021: 35-55 points
- AAFEX campaign: 20-40 points
- SAMPLE campaign: 20-30 points
- ECLIF/A-PRIDE/ACCESS campaigns: 30-50 points

**Total realistic**: 106-176 points with real thrust values

---

## Next Steps

1. **Create revised literature priority list** focused on engine/flight campaigns
2. **Design project visualization** - Show how literature → data extraction → model improvement pieces fit together
3. **Begin AAFEX search** - Highest expected yield per hour of work
4. **Verify paper types** - Before extracting, confirm each paper has real thrust documentation

---

## Files to Update

- `QUICK_REFERENCE.md` - Reorder by data quality (flight/engine first, rigs last)
- `LITERATURE_SOURCES_FOUND.md` - Add notes on which papers have real thrust values
- Create new: `LITERATURE_PRIORITY_REVISED.md` - Reorganized by thrust value availability

---

## Notes

- **Lab rig data isn't useless** - Just not suitable for this model's thrust normalization needs
- **Combustor studies might be useful later** for different analysis (e.g., fuel composition trends without thrust normalization)
- **Flight campaign data is gold** - Real-world conditions + thrust documentation = cleanest data
