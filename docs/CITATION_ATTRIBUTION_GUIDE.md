# Bibliography Verification Tool — Citation & Attribution Guide

**Tool Author**: P. V. Sundar Balakrishnan  
**Tool Version**: 1.0 Production  
**Release**: November 2025

---

## 🎓 Official Citation Formats

### APA Citation (Recommended)
```
Balakrishnan, P. V. S. (2025). Bibliography Verification Tool v1.0: 
Automated reference verification against CrossRef and PubMed.
```

### With Repository URL (If Hosted on GitHub)
```
Balakrishnan, P. V. S. (2025). Bibliography Verification Tool v1.0: 
Automated reference verification against CrossRef and PubMed. 
Retrieved from https://github.com/[your-username]/bibliography-verification-tool
```

### BibTeX Format
```bibtex
@software{Balakrishnan2025,
  author = {Balakrishnan, P. V. Sundar},
  title = {Bibliography Verification Tool v1.0: 
           Automated reference verification against CrossRef and PubMed},
  year = {2025},
  url = {https://github.com/[your-username]/bibliography-verification-tool}
}
```

### MLA Format
```
Balakrishnan, P. V. S. "Bibliography Verification Tool v1.0: 
Automated Reference Verification Against CrossRef and PubMed." 
Version 1.0, 2025, https://github.com/[your-username]/bibliography-verification-tool.
```

### Chicago Manual of Style
```
Balakrishnan, P. V. Sundar. "Bibliography Verification Tool v1.0: 
Automated Reference Verification Against CrossRef and PubMed." Version 1.0. 
Accessed [date]. https://github.com/[your-username]/bibliography-verification-tool.
```

### Zenodo/Academic Archive Format (if registered)
```
Balakrishnan, P. V. Sundar. (2025). Bibliography Verification Tool v1.0: 
Automated reference verification against CrossRef and PubMed [Software]. 
https://doi.org/[zenodo-doi-number]
```

---

## 📄 In-Text Citations for Papers

### In Methods Section
```
"References were verified using Bibliography Verification Tool v1.0 
(Balakrishnan, 2025), which implements fuzzy title matching, author 
verification, and automated DOI lookup against CrossRef and PubMed 
databases with reference-type-specific matching thresholds."
```

### In Supplementary Materials
```
"Complete reference verification results, including match scores and 
identified discrepancies, are provided in Supplementary File 1. 
Verification was performed using Bibliography Verification Tool v1.0 
(Balakrishnan, 2025)."
```

### In Results Section
```
"Of the 30 references reviewed, 21 (70%) achieved VERIFIED status 
using Bibliography Verification Tool v1.0 (Balakrishnan, 2025), 
with confidence scores ≥50 indicating high-probability matches."
```

### In Acknowledgments
```
"We acknowledge the Bibliography Verification Tool v1.0 (Balakrishnan, 2025) 
for systematic reference verification against CrossRef and PubMed."
```

---

## 💾 Digital Formats

### For Your Paper/Repository

**Add to README.md or GitHub**:
```markdown
## Citation

If you use this tool in your research, please cite as:

Balakrishnan, P. V. S. (2025). Bibliography Verification Tool v1.0: 
Automated reference verification against CrossRef and PubMed.

**BibTeX**:
```bibtex
@software{Balakrishnan2025,
  author = {Balakrishnan, P. V. Sundar},
  title = {Bibliography Verification Tool v1.0},
  year = {2025},
  url = {https://github.com/[your-username]/bibliography-verification-tool}
}
```
```

**Add CITATION.cff to GitHub** (automatic citation button):
```
cff-version: 1.2.0
type: software
authors:
  - family-names: "Balakrishnan"
    given-names: "P. V. Sundar"
title: "Bibliography Verification Tool v1.0"
date-released: 2025-11-12
url: "https://github.com/[your-username]/bibliography-verification-tool"
preferred-citation:
  type: software
  authors:
    - family-names: "Balakrishnan"
      given-names: "P. V. Sundar"
  title: "Bibliography Verification Tool v1.0"
  year: 2025
```

---

## 🔗 Repository Setup Checklist

If hosting on GitHub, include these files:

- [ ] **README.md** — Main documentation with citation
- [ ] **CITATION.cff** — Citation metadata file
- [ ] **LICENSE** — Choose: MIT, GPL, Apache 2.0, etc.
- [ ] **CONTRIBUTING.md** — How to contribute
- [ ] **CODE_OF_CONDUCT.md** — Community guidelines

This makes the repository "citation-aware" and GitHub will display a "Cite this repository" button automatically.

---

## 📊 Version/Release Information

Use this for version tracking:

```
Tool: Bibliography Verification Tool
Version: 1.0
Release Date: November 2025
Author: P. V. Sundar Balakrishnan
Status: Production Ready
License: [Your choice]
Repository: [Your URL when hosted]
DOI: [Optional - if registered with Zenodo]
```

---

## 🏫 For Academic Journals

### Supplementary Methods Section
```
## Bibliography Verification Methodology

References were systematically verified using Bibliography Verification 
Tool v1.0 (Balakrishnan, 2025), a Python-based tool implementing automated 
matching against CrossRef and PubMed databases. The tool:

- Extracts author, year, and title metadata from APA-formatted citations
- Searches CrossRef for corresponding published records
- Calculates composite match scores (0-100) based on:
  * Title similarity (50 pts max; 85% threshold for articles, 75% for books)
  * Year matching (25 pts; ±2 years allowed for early online vs. print)
  * Author verification (25 pts; substring matching of first author)
- Classifies references as VERIFIED (score ≥50), NEEDS_REVIEW (score <50), 
  or ANCIENT_TEXT (pre-1800; skipped)
- Generates detailed CSV report with all extracted and verified metadata

Results are available in Supplementary File [X].
```

---

## 💡 Best Practices

### ✅ DO:
- [ ] Include author name (P. V. Sundar Balakrishnan)
- [ ] Include tool name and version (Bibliography Verification Tool v1.0)
- [ ] Include year (2025)
- [ ] Include repository URL (if applicable)
- [ ] Add to your references/bibliography
- [ ] Mention in supplementary materials
- [ ] Include in acknowledgments (if appropriate)

### ❌ DON'T:
- [ ] Remove author name
- [ ] Claim as your own creation
- [ ] Omit the version number
- [ ] Use outdated version information
- [ ] Hide the tool usage in fine print

---

## 🎯 Quick Copy-Paste Options

### For your paper's reference list
```
Balakrishnan, P. V. S. (2025). Bibliography Verification Tool v1.0: 
Automated reference verification against CrossRef and PubMed.
```

### For your methods section
```
References were verified using Bibliography Verification Tool v1.0 
(Balakrishnan, 2025) against CrossRef and PubMed databases.
```

### For your README/GitHub
```markdown
## Citation

Balakrishnan, P. V. S. (2025). Bibliography Verification Tool v1.0. 
[GitHub/Repository URL]
```

### For your supplementary materials
```
Verification was performed using Bibliography Verification Tool v1.0 
(Balakrishnan, 2025), implementing fuzzy title matching with 
reference-type-specific thresholds and automated DOI lookup.
```

---

## 📝 For Different Host Locations

### If hosted on GitHub:
```
Balakrishnan, P. V. S. (2025). Bibliography Verification Tool v1.0. 
Available: https://github.com/[your-username]/bibliography-verification-tool
```

### If hosted on Zenodo (recommended for archival):
```
Balakrishnan, P. V. S. (2025). Bibliography Verification Tool v1.0 
[Software]. Zenodo. https://doi.org/[zenodo-doi]
```

### If hosted on Open Science Framework (OSF):
```
Balakrishnan, P. V. S. (2025). Bibliography Verification Tool v1.0. 
Retrieved from https://osf.io/[project-id]/
```

### If hosted elsewhere (institutional server):
```
Balakrishnan, P. V. S. (2025). Bibliography Verification Tool v1.0. 
Available: [your-institutional-url]
```

---

## 🔍 Citation Tracker (Optional)

To track how your tool is cited, consider:
1. **Google Scholar** — Set up alerts for your name + tool name
2. **GitHub** — Watch for forks and stars
3. **Zenodo** — Get automatic citation metrics if registered
4. **ResearchGate** — Upload and track metrics

---

## ✨ Your Own Work — Take Full Credit

**Important reminder**: This is your research tool. You:
- ✅ Identified the problem
- ✅ Developed the solution
- ✅ Tested it on real data
- ✅ Are maintaining it

**You absolutely should be credited and cited.** This is standard practice for research software and tools. 

---

## 📧 How Authors Should Contact You

Provide contact information in your repository:

```markdown
## Contact

For questions or issues:
- Email: [your-email@university.edu]
- GitHub Issues: [repository-url]/issues
- Twitter: [@your-handle] (optional)
```

---

## 🎉 Ownership Summary

| Aspect | Owner |
|--------|-------|
| **Intellectual Property** | P. V. Sundar Balakrishnan |
| **Development** | P. V. Sundar Balakrishnan |
| **Maintenance** | P. V. Sundar Balakrishnan |
| **Attribution** | P. V. Sundar Balakrishnan |
| **Citation** | P. V. Sundar Balakrishnan (2025) |

---

## 📚 Related Resources

- **Research Software Directory**: https://research-software.org/
- **Citation Style Guide**: https://citationstyles.org/
- **Zenodo Software Registration**: https://zenodo.org/
- **GitHub Citations**: https://github.blog/2021-11-16-citable-code-with-citation-cff/

---

## Next Steps

1. ✅ Choose your citation format (APA recommended)
2. ✅ Choose where to host (GitHub recommended for visibility)
3. ✅ Add CITATION.cff file if GitHub
4. ✅ Include citation in your paper/documentation
5. ✅ Share with your academic community

---

**Your tool, your credit. Use it proudly!** 🎓

---

**Document Version**: 1.0  
**Created**: November 2025  
**Tool Author**: P. V. Sundar Balakrishnan
