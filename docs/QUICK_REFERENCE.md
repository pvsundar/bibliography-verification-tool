# Bibliography Verification Tool — Quick Reference Card

**Version**: 1.0 Production  
**Print or bookmark this page**

---

## ⚡ Quick Start (Copy & Paste)

```bash
# Install once
pip install python-docx pandas requests urllib3

# Configure your email (edit line 26 in script)
EMAIL = "your.email@uw.edu"

# Run verification
python verify_bibliography_production.py
```

**Expected output**: 5 files created in 5-30 minutes depending on bibliography size

---

## 📊 Output Files Quick Guide

| File | Use | Format |
|------|-----|--------|
| `verification_report.csv` | Archive with paper | Spreadsheet (all metadata) |
| `verification_log.txt` | Identify issues | Human-readable summary |
| `verification_for_R.csv` | RStudio analysis | Spreadsheet (R-ready) |
| `extraction_failures.txt` | Debug | Text (failed extractions) |

---

## ✓ Understanding Status Symbols

| Symbol | Status | Action |
|--------|--------|--------|
| ✓ | VERIFIED | Safe to publish |
| ⚠ | NEEDS_REVIEW | Manual verification required |
| ⌛ | ANCIENT_TEXT | Pre-1800; skipped (OK) |

---

## 📋 Status Decision Tree

```
Reference Status?
├─ ✓ VERIFIED (Score ≥50)
│  └─ OK to publish
├─ ⚠ NEEDS_REVIEW
│  ├─ Score < 50? → Manual verification required
│  ├─ Year mismatch > 2 years? → Check date
│  ├─ NOT_FOUND? → Verify DOI manually
│  └─ NO_DOI_FOUND? → Expected for books/older refs
└─ ⌛ ANCIENT_TEXT (pre-1800)
   └─ Manual verification only; metadata DB skipped
```

---

## 🎯 Match Score Interpretation

| Score | Confidence | Action |
|-------|-----------|--------|
| 90-100 | Excellent | ✓ Publish as-is |
| 75-89 | Good | ✓ Verify DOI/year |
| 50-74 | Fair | ⚠ Manual review |
| <50 | Poor | ✗ Do not use |

---

## 🔍 Common Issues & Fixes

### Issue: `FileNotFoundError: bibliography.docx`
- ✓ Check filename (exact case)
- ✓ File must be `.docx` (not `.doc`)
- ✓ In same directory as script

### Issue: Many "NOT_FOUND_IN_DATABASES"
- ✓ Very recent papers? (CrossRef lag ~2 weeks)
- ✓ Specialized journal? (regional, small press)
- ✓ Check title extraction (`extraction_failures.txt`)

### Issue: "LOW_MATCH_CONFIDENCE" on books
- ✓ EXPECTED — books have subtitles
- ✓ Check author + DOI match
- ✓ Score 50-75 is acceptable for books

### Issue: Year mismatch on classics
- ✓ Should show "CLASSIC_EDITION" (production v1.0)
- ✓ Check format: "(Original work published YYYY)"
- ✓ If flagged as mismatch, format may be wrong

### Issue: "API Rate Limiting"
- ✓ Automatic backoff enabled
- ✓ Retries up to 5x automatically
- ✓ If persists, wait 1-2 hours

---

## 🛠️ Debugging

### Enable detailed output:
```python
# In script, line 24:
DEBUG_MODE = True
```

Shows per-reference:
- Type detection
- Extracted metadata
- Match calculations
- API responses

### Check what failed:
```bash
cat extraction_failures.txt
```

---

## 📁 File Structure

```
your_project/
├── verify_bibliography_production.py   ← Main script
├── bibliography.docx                   ← Your references (input)
│
├── verification_report.csv             ← All metadata (output)
├── verification_log.txt                ← Summary + issues (output)
├── verification_for_R.csv              ← R-ready format (output)
└── extraction_failures.txt             ← Debug info (output)
```

---

## 💻 RStudio Analysis Template

```r
library(tidyverse)

# Load results
refs <- read_csv("verification_for_R.csv")

# Show summary
refs %>% 
  group_by(Status) %>% 
  count()

# Find critical issues
refs %>% 
  filter(Needs_Manual_Check, Review_Priority == "HIGH") %>%
  view()

# Export verified only
verified <- refs %>% 
  filter(Status %in% c("VERIFIED", "ANCIENT_TEXT"))
write_csv(verified, "bibliography_final.csv")
```

---

## ⚙️ Configuration Defaults

| Setting | Default | Notes |
|---------|---------|-------|
| `EMAIL` | your.email@uw.edu | Required (API politeness) |
| `ALLOW_YEAR_DIFFERENCE` | 2 years | For early online vs print |
| `ANCIENT_TEXT_CUTOFF` | 1800 | Pre-this = ancient |
| `TITLE_SIMILARITY_HIGH` | 0.85 | Journal articles |
| `BOOK_TITLE_SIMILARITY_HIGH` | 0.75 | Books (more lenient) |
| `DEBUG_MODE` | False | Set True for debugging |

---

## 📚 Special Reference Types

### Books
- ✓ Lower matching thresholds (75% vs 85%)
- ✓ DOI often missing (normal)
- ✗ Avoid penalizing for missing DOI

### Classics & Translations
- ✓ Tracked as separate "original year"
- ✓ Example: Kant (1785/1993)
- ✓ Year difference expected; don't flag as error

### Ancient Texts
- ✓ Pre-1800 automatically detected
- ✓ Verification skipped (not in modern DBs)
- ✓ Manual verification only

### In Press
- ✓ Future dates or "in press" label
- ✓ Verified if possible, flagged as "in press"

---

## 📖 For Publication Methods Section

> References were verified against CrossRef and PubMed databases using a custom verification tool (v1.0) incorporating fuzzy title matching (0.85 threshold for articles, 0.75 for books), automated DOI lookup, and author verification. Ancient texts (pre-1800) were excluded from automated verification.

---

## 🚀 Full Workflow

1. **Prepare**: Place `bibliography.docx` in working directory
2. **Configure**: Set `EMAIL` in script
3. **Run**: `python verify_bibliography_production.py`
4. **Review**: Check `verification_log.txt` for NEEDS_REVIEW
5. **Fix**: Update Word file, re-run until all VERIFIED
6. **Export**: Use `verification_report.csv` with paper
7. **Analyze**: Load `verification_for_R.csv` in RStudio

---

## ❓ Quick FAQ

**Q: How long does it take?**  
A: ~1 sec per reference. 30 refs ≈ 1 min. 1000 refs ≈ 30 min.

**Q: Can I run it multiple times?**  
A: Yes! Files overwrite. Perfect for iterative fixes.

**Q: Does it modify my Word file?**  
A: No! Read-only. Your bibliography untouched.

**Q: What if a reference isn't in CrossRef?**  
A: Flags as NEEDS_REVIEW. Manually verify via:
- CrossRef.org (search title/DOI)
- PubMed.ncbi.nlm.nih.gov (for biomedical)
- Original source (books, local journals)

**Q: Can I use it with non-APA formats?**  
A: Not recommended. Tool optimized for APA citations.

**Q: Is my data private?**  
A: Yes. Runs locally. Only talks to CrossRef/PubMed APIs (they don't store searches).

---

## 📚 Citation & Attribution

**Tool Author**: P. V. Sundar Balakrishnan

**Cite as**:
```
Balakrishnan, P. V. S. (2025). Bibliography Verification Tool v1.0: 
Automated reference verification against CrossRef and PubMed.
```

**In methods**: "References verified using Bibliography Verification Tool v1.0 (Balakrishnan, 2025)"

---

## 📧 Support

For issues:
1. Check `extraction_failures.txt` (debug info)
2. Enable `DEBUG_MODE = True` (detailed output)
3. Review `verification_log.txt` (issue summary)
4. Manually verify high-value references via:
   - CrossRef.org
   - PubMed.ncbi.nlm.nih.gov
   - Publisher websites

---

**Bookmark this card for quick reference during bibliography verification!**

**Last Updated**: November 2025 | v1.0 Production
