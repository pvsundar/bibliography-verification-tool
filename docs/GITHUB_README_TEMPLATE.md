# Bibliography Verification Tool v1.0

**Author**: P. V. Sundar Balakrishnan  
**Language**: Python 3.7+  
**License**: [Choose: MIT / GPL / Apache 2.0]  

Automated reference verification for academic publishing using CrossRef and PubMed databases.

---

## Quick Start

```bash
pip install python-docx pandas requests urllib3
python verify_bibliography_production.py
```

---

## Features

- ✅ Verify references against CrossRef and PubMed
- ✅ Handles journal articles, books, classics, ancient texts
- ✅ Fuzzy title matching (type-specific thresholds)
- ✅ Automated DOI lookup
- ✅ Unicode support for international author names
- ✅ CSV + R-compatible output
- ✅ Production-grade error handling

---

## Citation

If you use this tool in your research, please cite as:

```bibtex
@software{Balakrishnan2025,
  author = {Balakrishnan, P. V. Sundar},
  title = {Bibliography Verification Tool v1.0: Automated reference verification against CrossRef and PubMed},
  year = {2025},
  url = {https://github.com/[your-username]/bibliography-verification-tool}
}
```

**APA Format:**
```
Balakrishnan, P. V. S. (2025). Bibliography Verification Tool v1.0: 
Automated reference verification against CrossRef and PubMed. 
Retrieved from https://github.com/[your-username]/bibliography-verification-tool
```

---

## Installation

### Requirements
- Python 3.7 or higher
- pip package manager
- Internet connection (for API access)

### Setup

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install python-docx pandas requests urllib3
   ```

3. Configure your email (line 26 in script):
   ```python
   EMAIL = "your.email@uw.edu"  # Required for API politeness
   ```

4. Place your APA-formatted bibliography as `bibliography.docx`

5. Run:
   ```bash
   python verify_bibliography_production.py
   ```

---

## Usage

### Basic Workflow

```bash
python verify_bibliography_production.py
```

**Outputs**:
- `verification_report.csv` — Complete metadata for all references
- `verification_log.txt` — Human-readable summary with flagged items
- `verification_for_R.csv` — R-compatible format with boolean filters
- `extraction_failures.txt` — Debug information (if any extraction issues)

### Configuration

Edit `verify_bibliography_production.py`:

```python
# Required
EMAIL = "your.email@uw.edu"

# Optional
WORD_FILE = "bibliography.docx"
OUTPUT_FILE = "verification_report.csv"
DEBUG_MODE = False  # Set True for detailed output
ALLOW_YEAR_DIFFERENCE = 2  # ±2 years for early online vs print
```

---

## Documentation

See included guides:
- `PRODUCTION_SETUP_GUIDE.md` — Comprehensive setup and usage guide
- `QUICK_REFERENCE.md` — One-page quick reference card
- `DEPLOYMENT_CHECKLIST.md` — Pre-deployment verification
- `analyze_verification_results.R` — RStudio analysis template

---

## Example Output

```
Processing reference 1/30...
  ✓ Status: VERIFIED | Score: 100 | Sim: 1.00 | Type: journal_article

Processing reference 2/30...
  ⚠ Status: NEEDS_REVIEW | Score: 25 | Sim: 0.23 | Type: book

Processing reference 3/30...
  ⌛ Status: ANCIENT_TEXT (pre-1800)

VERIFICATION SUMMARY
================================================================================
Total references: 30
✓ Verified: 21 (70.0%)
⚠ Needs review: 8 (26.7%)
⌛ Ancient texts: 1 (3.3%)
```

---

## How It Works

1. **Extract**: Reads bibliography.docx and extracts metadata using APA regex patterns
2. **Query**: Searches CrossRef and PubMed for each reference
3. **Match**: Calculates confidence scores (title, year, author matching)
4. **Report**: Generates detailed results and flags issues for review

### Match Scoring

- **Title Similarity**: 50 points (journal article 85%, book 75% threshold)
- **Year Match**: 25 points (exact or within ±2 years)
- **Author Match**: 25 points (first author found in verified authors)

**Status Categories**:
- `VERIFIED` (Score ≥50): Publish as-is
- `NEEDS_REVIEW` (Score <50 or issues): Manual verification required
- `ANCIENT_TEXT` (pre-1800): Verification skipped

---

## R Analysis

Load results in RStudio:

```r
library(tidyverse)

refs <- read_csv("verification_for_R.csv")

# Summary by status
refs %>% group_by(Status) %>% count()

# Find critical issues
refs %>% 
  filter(Needs_Manual_Check, Review_Priority == "HIGH")

# Export verified references only
refs %>% 
  filter(Status %in% c("VERIFIED", "ANCIENT_TEXT")) %>%
  write_csv("bibliography_final.csv")
```

See `analyze_verification_results.R` for 10+ pre-built analysis functions.

---

## Features by Reference Type

| Type | Handling | Verification |
|------|----------|--------------|
| Journal Articles | Standard title matching (85%) | CrossRef + PubMed |
| Books | Lenient matching (75%) | CrossRef (often no DOI) |
| Classics/Translations | Tracks original year separately | Based on modern edition |
| Ancient Texts | Pre-1800 detected | Skipped (not in modern DBs) |

---

## API Limitations

- **CrossRef**: Unlimited (rate-limited by script to 1 req/sec)
- **PubMed**: 3 requests/second (script stays well within limits)
- **Large bibliographies**: 100+ refs takes 20-60 minutes (by design for API politeness)

---

## Troubleshooting

### Issue: "FileNotFoundError: bibliography.docx"
- Ensure file is in working directory with exact name
- File must be `.docx` format (not `.doc`)

### Issue: "LOW_MATCH_CONFIDENCE" on books
- Expected behavior (books have subtitles)
- Check if author + DOI match
- Score 50-75 is acceptable for books

### Issue: Many "NOT_FOUND_IN_DATABASES"
- Very recent papers (CrossRef lag ~2 weeks)
- Specialized journals (not in CrossRef)
- Check `extraction_failures.txt` for extraction issues

### Enable Debug Mode

Set `DEBUG_MODE = True` for detailed output showing:
- Reference type detection
- Extracted metadata
- Match calculations
- API responses

---

## Manual Verification Resources

For references flagged as NOT_FOUND_IN_DATABASES:
- **CrossRef**: https://www.crossref.org/
- **PubMed**: https://pubmed.ncbi.nlm.nih.gov/
- **Google Scholar**: https://scholar.google.com/

---

## Performance

| Bibliography Size | Time | Speed |
|-------------------|------|-------|
| 10-30 references | 1-5 min | ~0.3 ref/sec |
| 30-100 references | 5-20 min | ~0.3 ref/sec |
| 100-300 references | 20-90 min | ~0.3 ref/sec |

(Rate limited to 1 sec/reference for API politeness)

---

## Methods Section Example

> "References were verified using Bibliography Verification Tool v1.0 (Balakrishnan, 2025), which incorporates fuzzy title matching, author verification, and automated DOI lookup against CrossRef and PubMed databases. Reference-type-specific matching thresholds were applied (0.85 for journal articles, 0.75 for books) to accommodate format variations. Ancient texts (pre-1800) were excluded from automated verification."

---

## Contributing

Found an issue? Have an improvement?
- Open an Issue
- Submit a Pull Request
- Contact: [your-email@uw.edu]

---

## License

[Choose: MIT, GPL, Apache 2.0, etc.]

This tool is provided as-is for academic research use.

---

## Citation Files

For proper attribution in different formats:
- `CITATION.cff` — Citation File Format (for GitHub)
- See README.md for BibTeX and APA formats

---

## Acknowledgments

- **CrossRef API**: https://www.crossref.org/
- **PubMed API**: https://pubmed.ncbi.nlm.nih.gov/
- **Python libraries**: python-docx, pandas, requests, urllib3

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Nov 2025 | Production release. Session management, robust year extraction, classic edition handling, reference filtering, extraction logging |

---

**Questions or Issues?** Please open an Issue on GitHub or contact [your-email].

---

**Get Started**: `python verify_bibliography_production.py`

**Happy verifying!** 📚✅
