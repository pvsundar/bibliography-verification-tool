# Bibliography Verification Tool v1.0

### Automated verification of APA-style references using CrossRef and PubMed

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg) ![License:
MIT](https://img.shields.io/badge/License-MIT-green.svg)
![DOI](https://img.shields.io/badge/DOI-pending-lightgrey.svg)

A production-grade Python tool for automatically verifying academic
bibliographies.\
Supports journal articles, books, translations, and ancient texts;
performs fuzzy title matching; retrieves DOIs; and generates detailed
verification reports for peer-review workflows.\
Tested and ready for publication requirements as of November 2025.

--------------------------------------------------------------------------

## 📌 Features

-   Verifies references against **CrossRef** and **PubMed**
-   Detects reference types:
    -   journal article
    -   book
    -   classic/translation
    -   ancient text
    -   in-press items\
-   Fuzzy title matching with type-specific thresholds:
    -   0.85 → journal articles
    -   0.75 → books\
-   Automated DOI lookup and metadata extraction
-   Unicode normalization for accented names
-   Year matching with ±2-year tolerance
-   Detects “Original work published…” for classics
-   Generates CSV, R-ready CSV, and human-readable logs
-   Graceful handling of API failures (exponential backoff)

--------------------------------------------------------------------------

## ⚙️ Installation

``` bash
pip install python-docx pandas requests urllib3
```

Clone the repository:

``` bash
git clone https://github.com/pvsundar/bibliography-verification-tool
cd bibliography-verification-tool
```

--------------------------------------------------------------------------

## 🚀 Quick Start

1.  Place **bibliography.docx** in your working directory.
2.  Configure your email (line 26 of the script):

``` python
EMAIL = "your.email@uw.edu"
```

3.  Run the tool:

``` bash
python verify_bibliography_production.py
```

4.  Review output files:
    -   `verification_report.csv`
    -   `verification_log.txt`
    -   `verification_for_R.csv`
    -   `extraction_failures.txt`

--------------------------------------------------------------------------

## 📝 What This Tool Does

-   Verifies bibliographies using CrossRef and PubMed APIs

-   Fuzzy matching, author verification, year comparison

-   Handles journal articles, books, translations, ancient texts

-   Tracks original publication years for classics

-   Produces multiple output formats for analysis and archiving

-   <div>

    --------------------------------------------------------------------------

    </div>

## 📊 Output File Overview

| File                      | Purpose                                    |
|---------------------------|--------------------------------------------|
| `verification_report.csv` | Full metadata for all processed references |
| `verification_log.txt`    | Human-readable summary and flagged items   |
| `verification_for_R.csv`  | R-ready results with boolean flags         |
| `extraction_failures.txt` | Debug log for extraction pattern failures  |

--------------------------------------------------------------------------

## 🛡️ Methods Text Example

> “References were verified against CrossRef and PubMed using the
> Bibliography Verification Tool v1.0 (Balakrishnan, 2025), implementing
> type-specific fuzzy title matching (thresholds: 0.85 for journal
> articles, 0.75 for books), Unicode-normalized author matching, and
> automated DOI lookup. Ancient texts (pre-1800) were excluded from
> automated verification.”

--------------------------------------------------------------------------

## 📚 Citation

**APA 7th Edition**

Balakrishnan, P. V. (Sundar). (2025). *Bibliography Verification Tool
v1.0: Automated reference verification against CrossRef and PubMed*
(Version 1.0.0) [Software]. GitHub.
<https://github.com/pvsundar/bibliography-verification-tool>\
ORCID: <https://orcid.org/0000-0002-2856-5543>

**BibTeX**

``` bibtex
@software{Balakrishnan2025_BVT,
  author       = {Balakrishnan, P. V. (Sundar)},
  title        = {Bibliography Verification Tool v1.0},
  subtitle     = {Automated reference verification against CrossRef and PubMed},
  year         = {2025},
  version      = {1.0.0},
  url          = {https://github.com/pvsundar/bibliography-verification-tool},
  orcid        = {https://orcid.org/0000-0002-2856-5543}
}
```

--------------------------------------------------------------------------

## 📄 Support & Documentation

Included in the repository: - `PRODUCTION_SETUP_GUIDE.md` -
`QUICK_REFERENCE.md` - `DEPLOYMENT_CHECKLIST.md` -
`CITATION_ATTRIBUTION_GUIDE.md` -
`analysis/analyze_verification_results.R`

--------------------------------------------------------------------------

## 📝 License

MIT License (see `LICENSE` file)

--------------------------------------------------------------------------

## ✉️ Contact

**P. V. (Sundar) Balakrishnan**\
Professor of Marketing Strategy & Analytics\
University of Washington Bothell\
ORCID: <https://orcid.org/0000-0002-2856-5543>
