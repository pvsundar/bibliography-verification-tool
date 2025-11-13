# Bibliography Verification Tool — Deployment Checklist

**Version**: 1.0 Production Ready  
**Deployment Date**: [Your Date Here]  
**Status**: ☐ Ready for Deployment

---

## ✅ Pre-Deployment Checklist

### System Requirements
- [ ] Python 3.7+ installed
  - Verify: `python --version`
- [ ] pip package manager available
  - Verify: `pip --version`
- [ ] Internet connection (for CrossRef/PubMed APIs)
- [ ] Write permissions in working directory

### Dependencies Installed
- [ ] `python-docx` → `pip install python-docx`
- [ ] `pandas` → `pip install pandas`
- [ ] `requests` → `pip install requests`
- [ ] `urllib3` → `pip install urllib3`
- [ ] All installed: `pip list | grep -E "python-docx|pandas|requests|urllib3"`

### Files Ready
- [ ] `verify_bibliography_production.py` (main script)
- [ ] `bibliography.docx` (your APA-formatted references)
  - [ ] Format: Microsoft Word 2007+ (.docx)
  - [ ] Each reference is separate paragraph
  - [ ] All references have (YEAR) in citation
- [ ] Working directory accessible from terminal

### Configuration Done
- [ ] Email address set (line 26 in script)
  ```python
  EMAIL = "your.email@uw.edu"  # ← UPDATE THIS
  ```
- [ ] File names match (if using custom names):
  ```python
  WORD_FILE = "bibliography.docx"
  OUTPUT_FILE = "verification_report.csv"
  DETAILED_LOG = "verification_log.txt"
  R_OUTPUT_FILE = "verification_for_R.csv"
  EXTRACTION_FAILURES_LOG = "extraction_failures.txt"
  ```
- [ ] DEBUG_MODE set appropriately:
  ```python
  DEBUG_MODE = False  # Set True for first run if testing
  ```

---

## 🎯 Test Run Checklist

### First Execution
```bash
# From command line in working directory:
python verify_bibliography_production.py
```

- [ ] Script starts without errors
- [ ] Processes bibliography entries
- [ ] Shows progress for each reference
- [ ] Completes without exceptions

### Output Files Created
After run completes, verify these files exist:
- [ ] `verification_report.csv` (main results)
- [ ] `verification_log.txt` (summary)
- [ ] `verification_for_R.csv` (R-ready)
- [ ] `extraction_failures.txt` (if any extraction issues)

### Output Content Verification
- [ ] CSV files contain data (not empty)
- [ ] Log file shows statistics
- [ ] Status symbols present (✓, ⚠, ⌛)
- [ ] Match scores populated (0-100 range)

### Data Quality Checks
- [ ] At least 50% of references VERIFIED
- [ ] DOI extraction working (if present in citations)
- [ ] Title extraction working (if present in citations)
- [ ] Author extraction working

**Note**: If <50% verified on first run, enable DEBUG_MODE and check:
- Title extraction patterns matching your format
- Author name formats (accents/hyphens handled?)
- Year formats (all in parentheses?)

---

## 📋 Documentation Verification

All documentation files present:
- [ ] `PRODUCTION_SETUP_GUIDE.md` (detailed setup)
- [ ] `QUICK_REFERENCE.md` (quick reference card)
- [ ] `analyze_verification_results.R` (RStudio template)
- [ ] `DEPLOYMENT_CHECKLIST.md` (this file)

All documentation reviewed:
- [ ] Setup guide matches your environment
- [ ] Quick reference bookmarked
- [ ] R script compatible with your RStudio version

---

## 🔒 Data Integrity Checks

- [ ] Word file NOT modified by script
- [ ] Original bibliography backed up
- [ ] Output files properly formatted
- [ ] No data truncation in CSV exports
- [ ] Unicode characters (accents) preserved in output

---

## 🌐 API Connectivity

Before deploying to production:
- [ ] Internet connection stable
- [ ] CrossRef API reachable
  ```bash
  curl -I https://api.crossref.org/works/10.1234/example
  # Should return: HTTP/1.1 200 OK
  ```
- [ ] PubMed API reachable
  ```bash
  curl -I "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=test"
  # Should return: HTTP/1.1 200 OK
  ```

---

## 📊 Performance Baseline

First run metrics (capture for reference):
- [ ] Total references: ____
- [ ] References verified: ____
- [ ] Verification rate: ____ %
- [ ] Execution time: ____ minutes
- [ ] Average time per reference: ____ seconds
- [ ] Critical issues: ____
- [ ] Needs review: ____

**Expected performance**:
- Small bibliography (10-30 refs): 1-5 minutes
- Medium bibliography (30-100 refs): 5-20 minutes
- Large bibliography (100+ refs): 20-60 minutes

---

## ✓ Final Verification

### Pre-Production Testing
- [ ] Tested on sample of 10+ references
- [ ] Tested on each reference type (journal, book, ancient, in-press)
- [ ] Tested on references with/without DOI
- [ ] Tested on references with accented names
- [ ] Tested on classics (original year) if present

### Error Handling
- [ ] Script handles missing years gracefully
- [ ] Script handles special characters in titles
- [ ] Script recovers from API timeouts
- [ ] Script logs extraction failures

### Results Review
- [ ] VERIFIED references checked manually (spot check 5+)
- [ ] NEEDS_REVIEW items match expected issues
- [ ] Match scores reasonable for reference type
- [ ] Title similarity scores make sense

---

## 📤 Deployment Sign-Off

### Team/Advisor Review
- [ ] Code reviewed for correctness
- [ ] Configuration reviewed for accuracy
- [ ] Output format approved
- [ ] Documentation complete and accurate

### Publication Readiness
- [ ] Bibliography verified at >70% confidence
- [ ] All NEEDS_REVIEW items addressed
- [ ] All CRITICAL priority items resolved
- [ ] Ready to archive results with manuscript

---

## 🚀 Production Deployment

### Go-Live Steps
1. [ ] Final backup of bibliography.docx
2. [ ] Confirm all dependencies installed
3. [ ] Confirm EMAIL configured
4. [ ] Run full bibliography verification
5. [ ] Review verification_log.txt output
6. [ ] Address any NEEDS_REVIEW items
7. [ ] Generate final verification_for_R.csv
8. [ ] Archive all output files with manuscript

### Documentation Handover
- [ ] Setup guide provided to team
- [ ] Quick reference card available
- [ ] R analysis script available for team
- [ ] Emergency contacts/support identified

---

## 📁 File Organization (Post-Deployment)

```
manuscript_project/
├── Paper_Submission/
│   ├── manuscript.docx
│   ├── supplementary_materials/
│   │   ├── bibliography_verification/
│   │   │   ├── verify_bibliography_production.py
│   │   │   ├── bibliography_original.docx
│   │   │   ├── verification_report.csv
│   │   │   ├── verification_log.txt
│   │   │   ├── verification_for_R.csv
│   │   │   └── verification_methods.txt
│   │   └── [other supplementary]
│   └── [other manuscript files]
└── Archive/
    ├── PRODUCTION_SETUP_GUIDE.md
    ├── QUICK_REFERENCE.md
    └── DEPLOYMENT_CHECKLIST.md (this file)
```

---

## ⚠️ Known Limitations & Workarounds

| Issue | Limitation | Workaround |
|-------|-----------|-----------|
| Title extraction | Regex may miss atypical formats | Enable DEBUG_MODE, adjust pattern |
| Ancient texts | Pre-1800 not in CrossRef/PubMed | Manual verification only |
| Books without DOI | Expected but unverifiable via API | Trust title/author match |
| Regional journals | May not be in major databases | Manual spot-check |
| Very recent papers | CrossRef indexing lag (~2 weeks) | Wait or manually verify DOI |

---

## 🔄 Maintenance Plan

### Regular Maintenance
- [ ] Run tool quarterly on active bibliographies
- [ ] Update EMAIL if organizational changes
- [ ] Monitor API availability
- [ ] Archive results for historical reference

### Updates & Improvements
- [ ] Monitor CrossRef API changelog
- [ ] Check for python-docx updates
- [ ] Review GitHub/community issues
- [ ] Collect feedback from team

### Troubleshooting Resources
- [ ] Bookmark: https://www.crossref.org/documentation/
- [ ] Bookmark: https://pubmed.ncbi.nlm.nih.gov/
- [ ] Save: extraction_failures.txt for debugging
- [ ] Enable: DEBUG_MODE for detailed diagnostics

---

## 📝 Deployment Sign-Off Form

**Production Deployment Checklist Completed By:**
- Name: ____________________________
- Date: ____________________________
- Organization: ____________________________
- Role: ____________________________

**Status**: 
- [ ] ✅ READY FOR PRODUCTION
- [ ] ⏸️ CONDITIONAL (see notes below)
- [ ] ❌ NOT READY (see notes below)

**Notes/Issues**:
```
[Add any notes, issues, or conditional items here]
```

---

## 🎓 Best Practices for Production

### Before Each Run
1. Backup bibliography.docx
2. Verify EMAIL is current
3. Confirm dependencies (`pip list`)
4. Check internet connectivity

### During Run
1. Don't interrupt script (let it complete)
2. Monitor first 5 references for errors
3. Note any API timeouts (automatic retry)

### After Run
1. Review verification_log.txt immediately
2. Check extraction_failures.txt if any
3. Address CRITICAL priority items
4. Archive all output files

### For Team Usage
1. Create shared template with configured EMAIL
2. Document any organization-specific settings
3. Maintain changelog of runs
4. Collect feedback for improvements

---

## ✨ Success Criteria

✅ Deployment is successful when:
- All output files created without errors
- >70% of references achieve VERIFIED status
- Bibliography can be re-verified anytime
- Results reproducible across runs
- Team understands how to use tool
- Documentation is complete and clear

---

## 📞 Support & Escalation

**Issue Categories & Response**:

| Category | Response Time | Action |
|----------|---------------|--------|
| Script won't run | Immediate | Check dependencies, EMAIL config |
| Low verification rate | 1 hour | Enable DEBUG_MODE, check formats |
| API errors | 2-4 hours | Check connectivity, try later |
| Result accuracy | 1 day | Manual spot-check, adjust thresholds |

---

## 🎉 Ready for Deployment!

When ALL checkboxes above are completed:

✅ **THIS TOOL IS PRODUCTION-READY**

Archive this checklist with:
- Final bibliography
- Configuration settings
- Output files
- Any customizations made

---

**Document Version**: 1.0  
**Created**: November 2025  
**Tool Version**: verify_bibliography_production.py v1.0  

**Print and attach to manuscript supplementary materials**

---
