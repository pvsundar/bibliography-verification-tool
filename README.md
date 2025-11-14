# Bibliography Verification Tool v1.0

**Automated verification of APA-style references using CrossRef and PubMed**

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![DOI](https://img.shields.io/badge/DOI-pending-lightgrey.svg)

A production-grade Python tool for automatically verifying academic bibliographies. Supports journal articles, books, translations, and ancient texts; performs fuzzy title matching; retrieves DOIs; and generates detailed verification reports for peer-review workflows.

---

##  Quick Start

### Prerequisites
```bash
pip install python-docx pandas requests urllib3
```

### Basic Usage

1. **Prepare your folder**
```
   MyManuscript/
   ├── bibliography.docx
   └── verify_bibliography_production.py
```

2. **Configure email** (line 26 in script)
```python
EMAIL = "your.email@uw.edu"
```

3. **Run verification**
```bash
   cd MyManuscript
   python verify_bibliography_production.py
```

4. **Review outputs**
   - `verification_log.txt` → Start here (human-readable summary)
   - `verification_report.csv` → Full metadata for archiving
   - `verification_for_R.csv` → Statistical analysis in R
   - `extraction_failures.txt` → Debug log (if needed)

5. **Fix and re-run**
   - Edit `bibliography.docx` to correct flagged references
   - Re-run script (outputs overwrite automatically)

**Requirements for `bibliography.docx`:**
- APA format
- Each reference as separate paragraph
- Must be `.docx` format (not `.doc`)

---

## 📌 Features

- ✅ Verifies references against **CrossRef** and **PubMed**
- ✅ Detects reference types: journal articles, books, classics/translations, ancient texts, in-press items
- ✅ Fuzzy title matching with type-specific thresholds (0.85 for journals, 0.75 for books)
- ✅ Automated DOI lookup and metadata extraction
- ✅ Unicode normalization for accented names
- ✅ Year matching with ±2-year tolerance
- ✅ Handles classic editions with "(Original work published...)" notation
- ✅ Generates CSV, R-ready CSV, and human-readable logs
- ✅ Graceful API failure handling with exponential backoff

---

## 📄 Statement of Need

Accurate bibliographic references are crucial for scientific integrity and discoverability. The Bibliography Verification Tool automates reference validation against authoritative databases (CrossRef, PubMed), minimizing manual errors and streamlining the workflow for researchers, reviewers, and editors.

---

## 📊 Output Files Explained

| File | Purpose |
|------|---------|
| `verification_log.txt` | Human-readable summary with flagged items requiring attention |
| `verification_report.csv` | Complete metadata for all processed references (archival) |
| `verification_for_R.csv` | Boolean flags optimized for statistical analysis in R |
| `extraction_failures.txt` | Debug log for extraction pattern failures (if any) |

---

## 🛡️ Methods Section Example

Use this text in your manuscript's methods section:

> References were verified against CrossRef and PubMed using the Bibliography Verification Tool v1.0 (Balakrishnan, 2025), implementing type-specific fuzzy title matching (thresholds: 0.85 for journal articles, 0.75 for books), Unicode-normalized author matching, and automated DOI lookup. Ancient texts (pre-1800) were excluded from automated verification.

---

## ⚙️ Installation

**Clone the repository:**
```bash
git clone https://github.com/pvsundar/bibliography-verification-tool
cd bibliography-verification-tool
```

**Install dependencies:**
```bash
pip install python-docx pandas requests urllib3
```

Or use requirements.txt:
```bash
pip install -r requirements.txt
```

---

## 📚 Documentation

Comprehensive guides included in the repository:
- `PRODUCTION_SETUP_GUIDE.md` → Detailed setup and configuration
- `QUICK_REFERENCE.md` → Fast lookup for common tasks
- `DEPLOYMENT_CHECKLIST.md` → Pre-publication verification steps
- `CITATION_ATTRIBUTION_GUIDE.md` → How to cite this tool
- `analysis/analyze_verification_results.R` → 10+ pre-built R analysis functions

---

## 🎓 Citation

If you use this tool in your research, please cite:

**APA 7th Edition:**
```
Balakrishnan, P. V. (Sundar). (2025). Bibliography Verification Tool v1.0: 
Automated reference verification against CrossRef and PubMed (Version 1.0.0) 
[Software]. GitHub. https://github.com/pvsundar/bibliography-verification-tool
```

**BibTeX:**
```bibtex
@software{Balakrishnan2025_BVT,
  author       = {Balakrishnan, P. V. (Sundar)},
  title        = {Bibliography Verification Tool v1.0},
  subtitle     = {Automated reference verification against CrossRef and PubMed},
  year         = {2025},
  version      = {1.0.0},
  url          = {https://github.com/pvsundar/bibliography-verification-tool}
}
```

**In methods sections:**
```
References were verified using Bibliography Verification Tool v1.0 
(Balakrishnan, 2025), which implements fuzzy title matching (thresholds: 
0.85 for journal articles, 0.75 for books), author verification with 
Unicode normalization, and automated DOI lookup against CrossRef and 
PubMed databases.
```

---

## 📋 For JOSS Reviewers

This software paper describes:

- **Statement of Need**: Addressed above and expanded in the JOSS paper
- **Software Architecture**: Four-stage pipeline (extraction, query, matching, reporting)
- **State of the Field**: Comparison with citation managers, API libraries, and manual methods
- **Target Audience**: Academic authors, journal editors, meta-researchers
- **Novelty**: First turnkey solution integrating extraction, validation, and reproducible reporting for reference verification

**Repository completeness checklist:**
- ✅ Working code with comprehensive error handling
- ✅ Installation instructions (requirements.txt)
- ✅ Usage examples with sample data
- ✅ Documentation folder with user guides
- ✅ R analysis integration
- ✅ MIT License
- ✅ CITATION.cff with ORCID
- ✅ Community standards (README, documentation)

**JOSS submission information will be added upon submission**

---

## 🔧 Troubleshooting

### Common Issues

**Issue: "FileNotFoundError: bibliography.docx"**
- Ensure file is in the same directory as the script
- Check filename matches exactly (case-sensitive on Linux/Mac)
- Verify file format is `.docx` (not `.doc`)

**Issue: Many references flagged as "NOT_FOUND_IN_DATABASES"**
- Very recent publications (CrossRef indexing lag ~2 weeks)
- Specialized/regional journals not indexed in CrossRef
- Check `extraction_failures.txt` for extraction issues

**Issue: "LOW_MATCH_CONFIDENCE" on books**
- Expected behavior (books often have subtitle variations)
- Verify author and year match
- Scores 50-75 are typically acceptable for books

**Issue: API rate limiting (429 errors)**
- Script uses exponential backoff (automatic retry)
- Wait 1-2 hours if issue persists
- For large bibliographies (100+ refs), expect 20-60 minutes runtime

### Debug Mode

Enable detailed diagnostics:
```python
DEBUG_MODE = True  # In verify_bibliography_production.py
```

This outputs:
- Extraction details for each reference
- API responses
- Step-by-step match calculations

---

## 🌐 API Information

**CrossRef API:**
- Rate limit: Polite (1 request/second)
- Coverage: 130M+ scholarly publications
- Documentation: https://www.crossref.org/documentation/retrieve-metadata/rest-api/

**PubMed API:**
- Rate limit: 3 requests/second
- Coverage: 35M+ biomedical citations
- Documentation: https://www.ncbi.nlm.nih.gov/books/NBK25501/

Both APIs are free for academic use. Proper email headers are configured automatically.

---

## 📈 Performance

| Bibliography Size | Expected Runtime | Processing Rate |
|-------------------|------------------|-----------------|
| 10-30 references  | 1-5 minutes      | ~0.3 ref/sec    |
| 30-100 references | 5-20 minutes     | ~0.3 ref/sec    |
| 100-300 references| 20-90 minutes    | ~0.3 ref/sec    |

Rate limited to respect API guidelines. For very large bibliographies (300+ refs), consider running overnight.

---

## 🧪 Testing

Sample bibliography included:
```bash
python verify_bibliography_production.py --test
```

This verifies a test bibliography with known edge cases:
- Journal articles with and without DOIs
- Books with subtitle variations
- Classic editions with original publication years
- Ancient texts (pre-1800)
- In-press items

---

## 🔐 Privacy & Data

**What the tool accesses:**
- Local `.docx` file only
- Public CrossRef and PubMed APIs

**What the tool does NOT do:**
- Does not upload your bibliography to external servers
- Does not store data beyond local output files
- Does not require authentication or login

**Your data stays on your machine.** API queries contain only titles/authors for matching, not your full manuscript.

---

## 📝 License

MIT License

Copyright (c) 2025 P. V. (Sundar) Balakrishnan

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## ✉️ Contact

**P. V. (Sundar) Balakrishnan**  
Professor of Marketing Strategy & Analytics  
University of Washington Bothell  
📧 Email: [sundar@uw.edu](mailto:sundar@uw.edu)  
🔗 ORCID: [0000-0002-2856-5543](https://orcid.org/0000-0002-2856-5543)  
🐙 GitHub: [@pvsundar](https://github.com/pvsundar)

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report bugs**: Open an issue with reproduction steps
2. **Suggest features**: Open an issue describing the enhancement
3. **Submit fixes**: Fork the repo, make changes, submit a pull request
4. **Improve documentation**: Help make guides clearer

Please ensure:
- Code follows existing style
- Tests pass (if applicable)
- Documentation is updated
- Commit messages are descriptive

---

## 🙏 Acknowledgments

This tool builds upon:
- **CrossRef** REST API for scholarly metadata
- **PubMed** E-utilities for biomedical literature
- **python-docx** for Word document parsing
- **pandas** for data manipulation
- **R tidyverse** for statistical analysis

Special thanks to the open-source community for these foundational tools.

---

## 📌 Version History

**v1.0.0** (November 2025)
- Production release
- Full CrossRef and PubMed integration
- Reference-type-specific matching thresholds
- Unicode normalization
- Classic edition handling
- R analysis integration
- Comprehensive documentation

---

## ⭐ Star This Repository

If you find this tool useful, please star the repository to help others discover it!

---

**Repository**: https://github.com/pvsundar/bibliography-verification-tool  
**Version**: 1.0.0  
**Status**: Production Ready ✅  
**Last Updated**: November 2025  
**Maintained**: Yes, actively maintained

---

*Built with ❤️ for the academic research community*
