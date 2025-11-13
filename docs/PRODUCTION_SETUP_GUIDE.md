# Bibliography Verification Tool — Production Setup Guide

**Version**: 1.0 (Production Ready)  
**Last Updated**: November 2025

---

## Quick Start (3 steps)

```bash
# 1. Install dependencies
pip install python-docx pandas requests urllib3

# 2. Configure your email in the script
# Edit verify_bibliography_production.py, line 26:
EMAIL = "your.email@uw.edu"

# 3. Run verification
python verify_bibliography_production.py
```

---

## Installation

### Prerequisites
- Python 3.7+
- pip package manager
- Your bibliography in Word format (.docx)

### Step 1: Install Dependencies

```bash
pip install python-docx pandas requests urllib3
```

These packages provide:
- **python-docx**: Read Word documents
- **pandas**: Data manipulation and CSV export
- **requests**: HTTP API calls to CrossRef/PubMed
- **urllib3**: Automatic retry logic with exponential backoff

### Step 2: Configure the Script

Edit `verify_bibliography_production.py`:

```python
# Line 26 - REQUIRED: Your email for API politeness
EMAIL = "your.email@uw.edu"

# Line 19-22 - Optional: Change file names if needed
WORD_FILE = "bibliography.docx"
OUTPUT_FILE = "verification_report.csv"
DETAILED_LOG = "verification_log.txt"
R_OUTPUT_FILE = "verification_for_R.csv"
EXTRACTION_FAILURES_LOG = "extraction_failures.txt"

# Line 24 - Optional: Enable debug output
DEBUG_MODE = False  # Set to True for detailed extraction info
```

### Step 3: Prepare Your Bibliography

1. Open your Word document with APA-formatted references
2. Ensure each reference is a separate paragraph
3. Save as `.docx` (Microsoft Word format)
4. Place in the same directory as the Python script

---

## Running the Tool

### Basic Usage

```bash
python verify_bibliography_production.py
```

### With Debug Output (for testing)

Change `DEBUG_MODE = True` in the script to see detailed extraction info:

```python
DEBUG_MODE = True
```

This shows:
- Reference type detection
- Extracted metadata (authors, year, title, DOI)
- Title matching quality (STRONG/PARTIAL/WEAK)
- Author matching results
- CrossRef API responses

### Monitor Progress

The script prints real-time status for each reference:
- `✓` = VERIFIED (high confidence)
- `⚠` = NEEDS_REVIEW (requires manual check)
- `⌛` = ANCIENT_TEXT (pre-1800, skipped)

---

## Output Files

### 1. `verification_report.csv` (Main Results)

Spreadsheet with all extracted and verified metadata:

| Column | Description |
|--------|-------------|
| Reference_Number | Sequential ID |
| Reference_Type | book / journal_article / ancient_text / in_press |
| Original_Text | Complete citation from Word file |
| Extracted_First_Author | First author surname (accent-preserved) |
| Extracted_Year | Publication year from citation |
| Extracted_Original_Year | Original publication year (for classics/translations) |
| Extracted_Title | Article/book title extracted by regex |
| Extracted_DOI | DOI from citation |
| CrossRef_Found | Boolean: Found in CrossRef database |
| Title_Similarity | 0-1 score (0=no match, 1=perfect match) |
| CrossRef_Match_Score | 0-100 composite score |
| Verified_DOI | DOI from CrossRef |
| Verified_Title | Official title from CrossRef |
| Verified_Authors | Author names from CrossRef |
| Verified_Year | Publication year from CrossRef |
| Issues_Detected | Flags: YEAR_MISMATCH, NO_DOI_FOUND, etc. |
| Status | VERIFIED / NEEDS_REVIEW / ANCIENT_TEXT |

**Use Case**: Complete reference audit trail for publications. Archive with submitted paper.

---

### 2. `verification_log.txt` (Human-Readable Summary)

Key statistics and recommendations:

```
OVERALL STATISTICS:
  Total references checked: 30
  ✓ Verified: 21 (70.0%)
  ⚠  Needs review: 8 (26.7%)
  ⌛ Ancient texts (skipped): 1 (3.3%)
  References with DOI: 22 (73.3%)
  Classics/translations: 2 (6.7%)

MATCH SCORE INTERPRETATION:
  90-100: Excellent - Safe to publish as-is
  75-89:  Good - Verify DOI/year before publishing
  50-74:  Fair - Requires manual verification
  <50:    Poor - Do not use without manual verification

REFERENCES NEEDING REVIEW:
Reference #9 (book):
  Blanchard, K. H., Zigarmi, D., & Zigarmi, P. (2018)...
  Issues: LOW_MATCH_CONFIDENCE; NO_DOI_FOUND; YEAR_MISMATCH_31yrs
  Match Score: 25
  Title Similarity: 0.23
```

**Use Case**: Identify which references to manually verify before peer review.

---

### 3. `verification_for_R.csv` (R/RStudio Import)

Data frame with boolean flags and priority levels:

```r
library(tidyverse)

# Load results
refs <- read_csv("verification_for_R.csv")

# Filter to high-priority reviews
refs %>% 
  filter(Needs_Manual_Check, Review_Priority %in% c("HIGH", "MEDIUM")) %>%
  select(Reference_Number, Reference_Type, Confidence_Level, Issues_Detected) %>%
  view()

# Verify your published dataset
verified <- refs %>% 
  filter(Status == "VERIFIED", High_Confidence == TRUE)

cat("Safe to publish:", nrow(verified), "references\n")

# Breakdown by type
refs %>% 
  group_by(Reference_Type, Confidence_Level) %>% 
  summarise(count = n(), .groups = "drop")
```

**New Columns** (added in production version):
- `Needs_Manual_Check`: Boolean flag (TRUE = Status is NEEDS_REVIEW)
- `Has_DOI`: Boolean flag (TRUE = DOI present)
- `High_Confidence`: Boolean flag (Score ≥75 AND Similarity ≥0.85)
- `Is_Book`: Boolean flag (TRUE = Reference_Type is 'book')
- `Is_Ancient`: Boolean flag (TRUE = Reference_Type is 'ancient_text')
- `Is_Translation_or_Classic`: Boolean flag (TRUE = Original_Year present)
- `Confidence_Level`: Categorical (Excellent/Good/Fair/Poor)
- `Review_Priority`: Categorical (HIGH/MEDIUM/LOW)

---

### 4. `extraction_failures.txt` (Debugging)

References where metadata extraction failed:

```
REFERENCES WITH EXTRACTION FAILURES

Reference #1:
  Issues: Title extraction failed; Author extraction failed; Year extraction failed

Reference #14:
  Issues: Title extraction failed - pattern may need adjustment
```

**Use Case**: Improve extraction patterns for future runs. Typically indicates malformed citations.

---

## Verification Logic

### Reference Type Detection

| Type | Detection Rules | Verification |
|------|-----------------|---------------|
| **ancient_text** | Year < 1800 or contains "BCE" | Skipped (not in modern databases) |
| **in_press** | Year > current year or contains "in press" | Noted but verified if possible |
| **book** | Contains: publisher, press, edition, Prentice-Hall, Oxford UP, etc. | Lower title threshold (75% vs 85%) |
| **journal_article** | Default | Standard title threshold (85%) |

### Match Score Breakdown (0-100)

- **Title Match** (50 pts max)
  - ≥85% similarity = 50 pts (strong)
  - ≥70% similarity = 25 pts (partial)
  - <70% similarity = 0 pts (weak)
- **Year Match** (25 pts max)
  - Exact match = 25 pts
  - Within ±2 years = 15 pts (early online vs print)
  - >2 years apart = 0 pts + YEAR_MISMATCH flag
- **Author Match** (25 pts max)
  - First author found in verified authors = 25 pts
  - Not found = 0 pts

### Status Categories

| Status | Meaning | Action |
|--------|---------|--------|
| **VERIFIED** | Match score ≥50, reasonable confidence | Safe to publish |
| **NEEDS_REVIEW** | Low score, missing data, year mismatch, or not found | Manual verification required |
| **ANCIENT_TEXT** | Pre-1800 reference | No action needed (verification skipped) |

### Special Handling

#### Classics & Translations
When reference contains "(Original work published YYYY)":
- Example: Kant, I. (1993). *Grounding...* Hackett. (Original work published 1785)
- **Extracted year**: 1993 (modern edition)
- **Original year**: 1785 (tracked separately)
- **Flagged as**: CLASSIC_EDITION (not YEAR_MISMATCH)
- **Reason**: Year difference expected; verify content aligns with cited edition

#### Books vs Journal Articles
Books use **lower matching thresholds** because:
- Titles may have subtitles that differ slightly
- Edition information (3rd ed.) affects title
- Not all books have DOIs (common for pre-2010)

#### Ancient Texts
Pre-1800 references automatically skipped:
- CrossRef/PubMed don't index ancient philosophy
- Rely on manual verification (check against original)
- Flagged as `ANCIENT_TEXT` in status

---

## Production Workflow

### For Peer Review

1. **Run the tool** on complete bibliography:
   ```bash
   python verify_bibliography_production.py
   ```

2. **Review flagged items** in `verification_log.txt`:
   - Check each NEEDS_REVIEW entry
   - Verify year mismatches manually
   - Confirm DOIs are correct (especially if missing)

3. **Address issues**:
   - Update bibliography in Word
   - Re-run tool to verify fixes
   - Confirm all references now VERIFIED

4. **Archive results**:
   - Save CSV and log with manuscript
   - Include in supplementary materials if required
   - Reference in methods: "Bibliography verified using [tool name] v1.0"

### For R Analysis

```r
library(tidyverse)

# Load results
refs <- read_csv("verification_for_R.csv")

# Create publication-ready summary
summary_table <- refs %>%
  filter(Status == "VERIFIED" | Status == "ANCIENT_TEXT") %>%
  group_by(Reference_Type) %>%
  summarise(
    n_references = n(),
    with_doi = sum(Has_DOI),
    high_confidence = sum(High_Confidence, na.rm = TRUE),
    .groups = "drop"
  )

print(summary_table)

# Export clean bibliography (verified only)
verified_refs <- refs %>%
  filter(Status == "VERIFIED" | Status == "ANCIENT_TEXT") %>%
  select(Reference_Number, Original_Text, Status, Confidence_Level)

write_csv(verified_refs, "verified_bibliography_clean.csv")
```

---

## Configuration Options

### Year Matching Policy

Adjust in the script:

```python
# Allow ±N years for early online vs print publication
ALLOW_YEAR_DIFFERENCE = 2  # Default: 2 years

# Define cutoff for "ancient texts"
ANCIENT_TEXT_CUTOFF = 1800  # Default: pre-1800

# Example: Stricter year matching
ALLOW_YEAR_DIFFERENCE = 1  # Only allow ±1 year

# Example: More lenient for classics
ANCIENT_TEXT_CUTOFF = 1920  # Include early 20th century
```

### Title Matching Thresholds

```python
# Journal articles (stricter)
TITLE_SIMILARITY_HIGH = 0.85   # 85% must match
TITLE_SIMILARITY_LOW = 0.70    # 70% is partial

# Books (more lenient)
BOOK_TITLE_SIMILARITY_HIGH = 0.75  # 75% for books
BOOK_TITLE_SIMILARITY_LOW = 0.60   # 60% partial for books

# Example: More lenient (reduce false negatives)
TITLE_SIMILARITY_HIGH = 0.80
BOOK_TITLE_SIMILARITY_HIGH = 0.70

# Example: Stricter (reduce false positives)
TITLE_SIMILARITY_HIGH = 0.90
BOOK_TITLE_SIMILARITY_HIGH = 0.80
```

### Book Detection

Add publisher names to detect more books:

```python
BOOK_CUES = [
    'publisher', 'press', 'edition', 'ed.)', 'trans.)',
    'oxford university press', 'cambridge university press',
    'your_publisher_name_here'  # Add your specific publishers
]
```

---

## Troubleshooting

### Issue: "Could not find 'bibliography.docx'"

**Solution**: 
1. Check filename matches exactly (case-sensitive on Linux/Mac)
2. Ensure file is in same directory as script
3. File must be `.docx` format (not `.doc` or `.pdf`)

### Issue: Many references flagged as NOT_FOUND_IN_DATABASES

**Possible causes**:
- Very recent publications (CrossRef indexing lag ~2 weeks)
- Specialized/regional journals (not in CrossRef)
- Title extraction failed (check `extraction_failures.txt`)

**Solution**:
- Verify DOI manually via CrossRef.org
- Check PubMed.ncbi.nlm.nih.gov for biomedical articles
- Update title extraction patterns if systematically failing

### Issue: LOW_MATCH_CONFIDENCE on books

**Expected behavior**: Books often have lower title similarity due to subtitles.

**Solution**:
- Check match score (typically 50-75 is acceptable for books)
- Verify author matches
- Confirm DOI if available
- If everything else matches, reference is likely correct

### Issue: YEAR_MISMATCH on classics (Kant, Aristotle, etc.)

**Solution**: Should now be handled as `CLASSIC_EDITION` instead.

If still flagged:
- Check for "(Original work published YYYY)" in citation
- Verify format matches: `(Original work published 1785)`
- Re-run tool

### Issue: API Rate Limiting (429 errors)

**Cause**: Too many requests to CrossRef too quickly

**Solution** (automatic in production version):
- Script uses exponential backoff
- Automatic retry up to 5 times
- If still failing, wait 1-2 hours before re-running

### Issue: Unicode/Accent Problems (Treviño appears as TreviÃ±o)

**Solution**: Now handled automatically in production version
- Uses Unicode normalization
- Strips accents for comparison
- Displays properly in output

---

## API Rate Limits

**CrossRef**:
- Limit: Unlimited (but respectful)
- Current tool: ~1 sec/request (polite)
- Email header required (configured automatically)

**PubMed**:
- Limit: 3 requests/second
- Current tool: ~1 sec/request (well within limits)
- Email header required (configured automatically)

**For large bibliographies** (1000+ references):
- Expect ~30-60 minutes processing time
- Script handles rate limiting automatically
- Safe to run overnight

---

## Citation for Methods Section

If you publish using this tool:

> References were verified using Bibliography Verification Tool v1.0 (Balakrishnan, 2025; https://github.com/[your-repo]) incorporating fuzzy title matching, author verification, and automated DOI lookup. Reference-type-specific matching thresholds were applied (0.85 for journal articles, 0.75 for books). Ancient texts (pre-1800) were excluded from automated verification.

**Full Citation**:
Balakrishnan, P. V. S. (2025). Bibliography Verification Tool v1.0: Automated reference verification against CrossRef and PubMed. Available: [your repository URL]

---

## Support & Debugging

### Enable Debug Mode

For detailed diagnostic output:

```python
DEBUG_MODE = True
```

Output shows:
- Exact extraction for each reference
- CrossRef API responses
- Match calculations step-by-step

### Common Debug Patterns

```
DEBUG - Type: journal_article
DEBUG - Extracted:
  First Author: Smith
  Year: 2020
  Title: Example study
  DOI: 10.1234/example

DEBUG - Title match: STRONG (0.98)
DEBUG - Year match: EXACT
DEBUG - Author match: YES
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Nov 2025 | Production release. Session management, robust year extraction, classic edition handling, reference filtering, extraction logging |
| 0.9 | Oct 2025 | Beta: basic verification, ancient text detection, R export |

---

## License & Attribution

This tool is provided as-is for academic research use. 

**CrossRef & PubMed Data**:
- CrossRef: https://www.crossref.org/
- PubMed: https://pubmed.ncbi.nlm.nih.gov/

Maintain proper attribution when publishing with this tool.

---

## Next Steps

1. ✅ Install dependencies: `pip install python-docx pandas requests urllib3`
2. ✅ Configure email in script
3. ✅ Place bibliography.docx in working directory
4. ✅ Run: `python verify_bibliography_production.py`
5. ✅ Review `verification_log.txt` for flagged items
6. ✅ Address any NEEDS_REVIEW entries
7. ✅ Re-run to confirm fixes
8. ✅ Archive CSV with manuscript

---

**Questions?** Check `extraction_failures.txt` for debugging info or enable `DEBUG_MODE = True` for detailed diagnostics.
