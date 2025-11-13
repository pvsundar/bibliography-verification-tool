# GitHub Deployment — PRINTABLE CHECKLIST

**Print this page and check off as you complete each step**

---

## 📥 STEP 1: DOWNLOAD FILES (10 files from /outputs/)

### CORE FILES (Must Have)
```
☐ verify_bibliography_production.py
☐ README.md
☐ CITATION.cff
☐ QUICK_REFERENCE.md
☐ analyze_verification_results.R
```

### DOCUMENTATION FILES (Recommended)
```
☐ PRODUCTION_SETUP_GUIDE.md
☐ DEPLOYMENT_CHECKLIST.md
☐ CITATION_ATTRIBUTION_GUIDE.md
☐ GITHUB_README_TEMPLATE.md
☐ GITHUB_DEPLOYMENT_BUNDLE.md (this guide)
```

---

## ✏️ STEP 2: CREATE NEW FILES (3 files)

### Create in your project folder:

#### File 1: LICENSE
```
☐ Copy MIT License template (below)
☐ Save as: LICENSE
☐ No file extension
```

#### File 2: requirements.txt
```
☐ Copy requirements template (below)
☐ Save as: requirements.txt
```

#### File 3: .gitignore
```
☐ Copy gitignore template (below)
☐ Save as: .gitignore
☐ Note the leading dot (.)
```

---

## 🔧 STEP 3: CUSTOMIZE EXISTING FILES (3 files)

### File 1: verify_bibliography_production.py
```
FIND:  EMAIL = "your.email@uw.edu"
REPLACE: EMAIL = "YOUR-EMAIL@YOUR-DOMAIN.COM"
Line: 26
☐ Updated
```

### File 2: README.md
```
FIND: [your-username]
REPLACE: YOUR-GITHUB-USERNAME
Locations: 3+ places (search for [your-username])
☐ Updated all occurrences
```

### File 3: CITATION.cff
```
FIND: [your-username]
REPLACE: YOUR-GITHUB-USERNAME
Line: ~9 and ~14
☐ Updated
```

---

## 📁 STEP 4: ORGANIZE FOLDER STRUCTURE

```
Create folders and move files:

☐ Create: docs/
   ☐ Move: QUICK_REFERENCE.md
   ☐ Move: PRODUCTION_SETUP_GUIDE.md
   ☐ Move: DEPLOYMENT_CHECKLIST.md
   ☐ Move: CITATION_ATTRIBUTION_GUIDE.md

☐ Create: analysis/
   ☐ Move: analyze_verification_results.R

Root folder should have:
   ☐ verify_bibliography_production.py
   ☐ README.md
   ☐ LICENSE
   ☐ CITATION.cff
   ☐ requirements.txt
   ☐ .gitignore
   ☐ docs/ (folder)
   ☐ analysis/ (folder)
```

---

## 🔍 STEP 5: PRE-FLIGHT CHECKS

Run these checks in terminal:

```bash
# Check 1: Email updated
grep "your.email@uw.edu" verify_bibliography_production.py
Result: Should show NOTHING (✓ if empty)
☐ PASS

# Check 2: No placeholder usernames
grep "\[your-username\]" README.md CITATION.cff
Result: Should show NOTHING (✓ if empty)
☐ PASS

# Check 3: LICENSE exists
ls LICENSE
Result: LICENSE (✓)
☐ PASS

# Check 4: requirements.txt exists
ls requirements.txt
Result: requirements.txt (✓)
☐ PASS

# Check 5: No test output files
ls *.csv *.txt 2>/dev/null | grep -v requirements.txt
Result: Should show NOTHING (✓ if empty)
☐ PASS
```

---

## 🚀 STEP 6: GITHUB SETUP

### On GitHub.com:
```
☐ Go to: https://github.com/new
☐ Repository name: bibliography-verification-tool
☐ Description: Automated reference verification against CrossRef and PubMed
☐ Visibility: PUBLIC
☐ Click: Create repository
☐ Copy the commands shown
```

### On Your Computer (Terminal):
```bash
# Navigate to your project
cd /path/to/bibliography-verification-tool

# Initialize git
☐ git init

# Add all files
☐ git add .

# First commit
☐ git commit -m "Initial commit: Bibliography Verification Tool v1.0"

# Add remote (copy from GitHub)
☐ git remote add origin https://github.com/YOUR-USERNAME/bibliography-verification-tool.git

# Set branch name
☐ git branch -M main

# Push to GitHub
☐ git push -u origin main
```

---

## ✅ STEP 7: VERIFY ON GITHUB

Go to: `https://github.com/YOUR-USERNAME/bibliography-verification-tool`

```
☐ README.md displays on main page
☐ All files appear in file list
☐ "Cite this repository" button visible (CITATION.cff working)
☐ docs/ folder visible with 4 markdown files
☐ analysis/ folder visible with R script
☐ LICENSE file visible
☐ requirements.txt visible
```

---

## 🎉 DONE!

```
Your GitHub repository is live!

Share your repository URL:
https://github.com/YOUR-USERNAME/bibliography-verification-tool

Next steps:
☐ Share link with academic community
☐ Add topics: python, bibliography, crossref, academic-publishing
☐ Monitor for stars and forks
☐ Create releases for version tracking
```

---

# 📋 TEMPLATES - COPY & PASTE BELOW

## Template 1: LICENSE (MIT)

```
MIT License

Copyright (c) 2025 P. V. Sundar Balakrishnan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Template 2: requirements.txt

```
python-docx>=0.8.10
pandas>=1.1.0
requests>=2.25.0
urllib3>=1.26.0
```

---

## Template 3: .gitignore

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/

# Project outputs (don't commit)
*.csv
*.txt
*.docx
*.xlsx

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Temp files
*.tmp
*.temp
~*
```

---

# 🎯 MY GITHUB SETUP INFO

**Fill in these details:**

```
My GitHub Username: _____________________________

My Email (for script): _____________________________

My GitHub Repository URL: 
https://github.com/___________________________/bibliography-verification-tool

License Choice (circle one):   MIT    /    GPL v3    /    Apache 2.0
(Recommended: MIT)

Commands I'll use:
git init
git add .
git commit -m "Initial commit: Bibliography Verification Tool v1.0"
git remote add origin https://github.com/___________/bibliography-verification-tool.git
git branch -M main
git push -u origin main
```

---

# 📝 QUICK REFERENCE

| Task | Command | Status |
|------|---------|--------|
| Download files | Go to `/mnt/user-data/outputs/` | ☐ |
| Create LICENSE | Copy MIT template | ☐ |
| Create requirements.txt | Copy template | ☐ |
| Create .gitignore | Copy template | ☐ |
| Update EMAIL | Line 26 in .py | ☐ |
| Update README | Replace [your-username] | ☐ |
| Update CITATION.cff | Replace [your-username] | ☐ |
| Organize folders | Create docs/ analysis/ | ☐ |
| Git init | `git init` | ☐ |
| Git add | `git add .` | ☐ |
| Git commit | `git commit -m "..."` | ☐ |
| Git remote | `git remote add origin ...` | ☐ |
| Git branch | `git branch -M main` | ☐ |
| Git push | `git push -u origin main` | ☐ |
| Verify GitHub | Check repository | ☐ |

---

# ⏱️ TIME ESTIMATE

```
Download files:           5 min  ☐
Create new files:         5 min  ☐
Customize existing:       10 min ☐
Organize folders:         5 min  ☐
Pre-flight checks:        5 min  ☐
GitHub setup:             10 min ☐
Git commands:             5 min  ☐
Verify on GitHub:         5 min  ☐
─────────────────────────────────
TOTAL:                    ~55 min ☐ DONE!
```

---

# 🆘 TROUBLESHOOTING

**If you see this error:**

```
error: failed to push some refs to 'origin'
```
**Solution**: Run `git pull origin main --allow-unrelated-histories` first

---

**If files don't show on GitHub:**

```
Check 1: ☐ All files git add'd
Check 2: ☐ All files git commit'd
Check 3: ☐ git push completed (watch for errors)
Check 4: ☐ Refresh GitHub page
Check 5: ☐ Check branch name (should be 'main')
```

---

**If "Cite this repository" button doesn't appear:**

```
Check 1: ☐ CITATION.cff file exists
Check 2: ☐ CITATION.cff in root folder (not in docs/)
Check 3: ☐ Wait 5 minutes (GitHub needs to index it)
Check 4: ☐ Refresh page
```

---

# 🎉 SUCCESS INDICATORS

When complete, you should see:

✅ Repository exists at github.com/YOUR-USERNAME/bibliography-verification-tool  
✅ README.md displays beautifully on main page  
✅ All 10 files visible in file browser  
✅ "Cite this repository" button present  
✅ docs/ and analysis/ folders visible  
✅ LICENSE file visible  
✅ GREEN checkmark on first commit  

---

**PRINT THIS PAGE AND USE IT AS YOUR DEPLOYMENT CHECKLIST!**

---

Generated: November 2025  
Tool: Bibliography Verification Tool v1.0  
Author: P. V. Sundar Balakrishnan
