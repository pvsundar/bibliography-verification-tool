"""
Bibliography Verification Script - PRODUCTION VERSION
Comprehensive reference verification for academic peer-reviewed publications

Key Features:
- Detects and handles books, journal articles, ancient texts, in-press items
- Distinguishes between original publication year and modern edition year
- Robust CrossRef API with exponential backoff and session management
- Accented name handling (Unicode normalization)
- Lower matching thresholds for books and classics
- Flexible year matching (±2 years for early online vs print)
- Professional API etiquette (User-Agent, rate limiting, timeouts)
- Comprehensive extraction failure logging
- R-compatible CSV output with boolean flags
- Detailed verification reports for peer review

Requirements: pip install python-docx pandas requests urllib3
"""

import requests
import pandas as pd
from docx import Document
import re
from time import sleep
import unicodedata
from difflib import SequenceMatcher
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ============================================================================
# CONFIGURATION
# ============================================================================
WORD_FILE = "bibliography.docx"  # Your Word file with References
OUTPUT_FILE = "verification_report.csv"
DETAILED_LOG = "verification_log.txt"
R_OUTPUT_FILE = "verification_for_R.csv"
EXTRACTION_FAILURES_LOG = "extraction_failures.txt"

# DEBUG MODE - Set to False after testing
DEBUG_MODE = False

# Your email for polite API usage (CrossRef/PubMed require this)
EMAIL = "your.email@uw.edu"  # Replace with your actual email

# API endpoints
CROSSREF_API = "https://api.crossref.org/works"
PUBMED_API = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

# Matching thresholds for JOURNAL ARTICLES
TITLE_SIMILARITY_HIGH = 0.85  # 85% match = strong confidence
TITLE_SIMILARITY_LOW = 0.70   # 70% match = partial confidence

# Matching thresholds for BOOKS (more lenient)
BOOK_TITLE_SIMILARITY_HIGH = 0.75  # 75% match for books
BOOK_TITLE_SIMILARITY_LOW = 0.60   # 60% match for books

# Year matching
ALLOW_YEAR_DIFFERENCE = 2  # Allow ±2 years for early online vs print
ANCIENT_TEXT_CUTOFF = 1800  # References before this are "ancient texts"

# Book detection cues (expanded list)
BOOK_CUES = [
    'publisher', 'press', 'edition', 'ed.)', 'trans.)', 'pp.',
    'original work published', 'hackett', 'oxford university press',
    'prentice-hall', 'sage', 'wiley', 'routledge', 'praeger', 'ft press',
    'pearson', 'mcgraw-hill', 'cambridge university press',
    'harvard business review press', 'springer', 'emerald', 'palgrave',
    'taylor & francis', 'john wiley & sons', 'dissertation', 'thesis'
]

# ============================================================================
# CONFIGURE REQUESTS SESSION WITH BACKOFF & RETRY LOGIC
# ============================================================================
session = requests.Session()
session.headers.update({
    "User-Agent": f"UW-AcademicBibliographyVerifier/1.0 (mailto:{EMAIL})"
})

retries = Retry(
    total=5,
    backoff_factor=1.0,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET", "HEAD"]
)
session.mount("https://", HTTPAdapter(max_retries=retries))

def get_with_backoff(url, params=None):
    """Make HTTP GET request with automatic backoff and timeout"""
    if params is None:
        params = {}
    params.setdefault("mailto", EMAIL)
    try:
        response = session.get(url, params=params, timeout=20)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        return None

# ============================================================================
# UNICODE & TEXT PROCESSING FUNCTIONS
# ============================================================================

def normalize_text(text):
    """Normalize Unicode to NFC form"""
    return unicodedata.normalize('NFC', text) if text else text

def strip_accents(text):
    """Remove accents: Treviño -> Trevino, García -> Garcia"""
    if not text:
        return text
    return ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn')

def title_similarity(t1, t2):
    """Calculate title similarity score using SequenceMatcher (0-1)"""
    if not t1 or not t2:
        return 0
    t1_clean = strip_accents(t1).lower().strip()
    t2_clean = strip_accents(t2).lower().strip()
    return SequenceMatcher(None, t1_clean, t2_clean).ratio()

# ============================================================================
# REFERENCE TYPE DETECTION
# ============================================================================

def detect_reference_type(text):
    """Detect if reference is a book, journal article, ancient text, or in-press"""
    text_lower = text.lower()
    
    # Check for ancient text indicators (BCE)
    if re.search(r'\((\d+)\s*bce', text_lower):
        return 'ancient_text'
    
    # Check for very old dates (pre-1800)
    year_match = re.search(r'\((\d{4})\)', text)
    if year_match:
        year = int(year_match.group(1))
        if year < ANCIENT_TEXT_CUTOFF:
            return 'ancient_text'
    
    # Check for book indicators
    if any(indicator in text_lower for indicator in BOOK_CUES):
        return 'book'
    
    # Check for "in press" or future dates
    current_year = datetime.now().year
    if year_match and int(year_match.group(1)) > current_year:
        return 'in_press'
    
    if 'in press' in text_lower:
        return 'in_press'
    
    # Default to journal article
    return 'journal_article'

# ============================================================================
# APA CITATION EXTRACTION FUNCTIONS
# ============================================================================

def extract_doi_from_text(text):
    """Extract DOI from reference text"""
    doi_pattern = r'10\.\d{4,9}/[-._;()/:A-Z0-9]+'
    match = re.search(doi_pattern, text, re.IGNORECASE)
    return match.group(0) if match else None

def extract_year_from_text(text):
    """Extract publication year from reference text"""
    year_pattern = r'\((\d{4})\)'
    match = re.search(year_pattern, text)
    return match.group(1) if match else None

def extract_original_year_from_text(text):
    """Extract original publication year for classics/translations"""
    original_pub_pattern = r'\(Original work published\s+(\d{3,4})\)'
    match = re.search(original_pub_pattern, text, re.IGNORECASE)
    return match.group(1) if match else None

def extract_first_author_from_apa(text):
    """Extract first author surname - handles accented characters"""
    text = normalize_text(text)
    # \w matches Unicode word characters with re.UNICODE flag
    pattern = r'^([\w\-\']+),\s+[A-Z]'
    match = re.search(pattern, text, re.UNICODE)
    return match.group(1) if match else None

def extract_all_authors_from_apa(text):
    """Extract all authors from APA citation"""
    text = normalize_text(text)
    # Match everything before (YEAR)
    author_block_pattern = r'^(.+?)\s*\(\d{4}\)'
    match = re.search(author_block_pattern, text)
    if match:
        authors_text = match.group(1)
        
        # Handle "et al."
        if 'et al' in authors_text.lower():
            first = re.search(r'^([\w\-\']+),\s+[A-Z]\.', authors_text, re.UNICODE)
            return [first.group(1)] if first else []
        
        # Split on ", &" or " & " for multiple authors
        author_parts = re.split(r',\s*&\s*|\s+&\s+', authors_text)
        authors = []
        for part in author_parts:
            surname_match = re.search(r'([\w\-\']+),\s+[A-Z]\.', part, re.UNICODE)
            if surname_match:
                authors.append(surname_match.group(1))
        return authors
    return []

def extract_title_from_apa(text):
    """Extract article/book title from APA citation"""
    # Multiple patterns to handle variations
    patterns = [
        r'\(\d{4}\)\.\s*(.+?)[.?!]\s+(?=[A-Z])',
        r'\(\d{4}\)\.\s*(.+?)(?=\s+[A-Z][A-Za-z&\-\s]+[,\(])',
        r'\(\d{4}\)\.\s*(.+?)\.\s*[A-Z]'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            title = match.group(1).strip()
            if len(title) > 10:  # Filter out very short matches
                return title
    return None

def extract_crossref_year(metadata):
    """Extract year from CrossRef metadata, checking multiple fields"""
    if not isinstance(metadata, dict):
        return ""
    
    for key in ("published-print", "published-online", "issued", "created"):
        date_part = metadata.get(key, {})
        if isinstance(date_part, dict) and "date-parts" in date_part:
            try:
                return str(date_part["date-parts"][0][0])
            except (IndexError, TypeError):
                continue
    return ""

def is_probable_reference(line):
    """Filter to identify probable bibliography entries (skip headers)"""
    if not line or line.strip().isdigit():
        return False
    if re.match(r'^\s*\d+\s*\|\s*Page\s*$', line):
        return False
    if line.lower().strip() == 'references':
        return False
    if '(' not in line or ')' not in line:
        return False
    if not re.search(r'\(\d{4}\)', line) and 'BCE' not in line.upper():
        return False
    return True

# ============================================================================
# API CHECKING FUNCTIONS
# ============================================================================

def check_crossref(title, author=None, year=None, doi=None):
    """Check reference against CrossRef database with improved session handling"""
    try:
        if doi:
            url = f"https://api.crossref.org/works/{doi}"
            response = get_with_backoff(url)
            if response is None:
                return False, None
            data = response.json()
            return True, data.get("message", {})
        else:
            params = {"rows": 3}
            if title:
                params["query.title"] = title
            if author:
                params["query.author"] = author
            
            response = get_with_backoff(CROSSREF_API, params=params)
            if response is None:
                return False, None
            
            data = response.json()
            items = data.get("message", {}).get("items", [])
            if items:
                return True, items[0]
        
        return False, None
    except Exception as e:
        return False, str(e)

def check_pubmed(title, author=None):
    """Check reference against PubMed (primarily for journal articles)"""
    try:
        # Use quoted title for better precision
        query = f'"{title}"[Title]'
        if author:
            query += f' AND {author}[Author]'
        
        params = {
            'db': 'pubmed',
            'term': query,
            'retmode': 'json',
            'retmax': 1,
            'tool': 'UWAcademicVerifier',
            'email': EMAIL
        }
        
        response = get_with_backoff(PUBMED_API, params=params)
        if response is None:
            return False, None
        
        data = response.json()
        count = int(data.get('esearchresult', {}).get('count', 0))
        return count > 0, data
    except Exception as e:
        return False, str(e)

# ============================================================================
# MAIN VERIFICATION FUNCTION
# ============================================================================

def verify_bibliography(word_file):
    """Main function to verify all references"""
    
    print(f"Reading bibliography from {word_file}...")
    
    # Read Word document
    doc = Document(word_file)
    references = []
    
    # Extract all paragraphs, filtering for probable references
    for para in doc.paragraphs:
        text = para.text.strip()
        if is_probable_reference(text):
            references.append(text)
    
    print(f"Found {len(references)} reference entries (headers filtered)")
    if DEBUG_MODE:
        print(f"\n{'='*70}")
        print("DEBUG MODE: ON - Showing detailed extraction info")
        print(f"{'='*70}\n")
    
    # Initialize results list and extraction failure tracking
    results = []
    extraction_failures = {}
    
    # Process each reference
    for idx, ref_text in enumerate(references, 1):
        print(f"\nProcessing reference {idx}/{len(references)}...")
        print(f"  {ref_text[:80]}...")
        
        # Detect reference type
        ref_type = detect_reference_type(ref_text)
        
        # Extract metadata
        doi = extract_doi_from_text(ref_text)
        year = extract_year_from_text(ref_text)
        original_year = extract_original_year_from_text(ref_text)
        first_author = extract_first_author_from_apa(ref_text)
        all_authors = extract_all_authors_from_apa(ref_text)
        title = extract_title_from_apa(ref_text)
        
        if DEBUG_MODE:
            print(f"  DEBUG - Type: {ref_type}")
            print(f"  DEBUG - Extracted:")
            print(f"    First Author: {first_author}")
            print(f"    All Authors: {all_authors}")
            print(f"    Year: {year} | Original: {original_year}")
            print(f"    Title: {title}")
            print(f"    DOI: {doi}")
        
        # Initialize result dictionary
        result = {
            'Reference_Number': idx,
            'Reference_Type': ref_type,
            'Original_Text': ref_text,
            'Extracted_First_Author': first_author,
            'Extracted_All_Authors': ', '.join(all_authors) if all_authors else '',
            'Extracted_Year': year,
            'Extracted_Original_Year': original_year,
            'Extracted_Title': title,
            'Extracted_DOI': doi,
            'CrossRef_Found': False,
            'Title_Similarity': 0.0,
            'CrossRef_Match_Score': 0,
            'PubMed_Found': False,
            'Verified_DOI': '',
            'Verified_Title': '',
            'Verified_Authors': '',
            'Verified_Year': '',
            'Issues_Detected': [],
            'Status': 'PENDING'
        }
        
        # Handle ancient texts separately (skip verification)
        if ref_type == 'ancient_text':
            result['Status'] = 'ANCIENT_TEXT'
            result['Issues_Detected'] = f'Ancient text (pre-{ANCIENT_TEXT_CUTOFF}) - verification not applicable'
            results.append(result)
            print(f"  ⌛ Status: ANCIENT_TEXT (pre-{ANCIENT_TEXT_CUTOFF})")
            continue
        
        # Handle in-press items
        if ref_type == 'in_press':
            result['Issues_Detected'] = 'In press or future publication'
        
        # Track extraction failures
        if not title:
            extraction_failures[idx] = "Title extraction failed - pattern may need adjustment"
        if not first_author:
            extraction_failures[idx] = extraction_failures.get(idx, "") + "; Author extraction failed"
        if not year:
            extraction_failures[idx] = extraction_failures.get(idx, "") + "; Year extraction failed"
        
        # Check CrossRef
        if doi or title:
            crossref_found, crossref_data = check_crossref(title, first_author, year, doi)
            result['CrossRef_Found'] = crossref_found
            
            if crossref_found and crossref_data:
                result['Verified_DOI'] = crossref_data.get('DOI', '')
                result['Verified_Title'] = crossref_data.get('title', [''])[0]
                
                # Extract authors from CrossRef
                authors_list = crossref_data.get('author', [])
                if authors_list:
                    verified_authors = ', '.join([
                        f"{normalize_text(a.get('family', ''))} {normalize_text(a.get('given', ''))}" 
                        for a in authors_list[:3]
                    ])
                    result['Verified_Authors'] = verified_authors
                
                # Extract year from CrossRef (robust extraction)
                result['Verified_Year'] = extract_crossref_year(crossref_data)
                
                # Determine thresholds based on reference type
                if ref_type == 'book':
                    high_threshold = BOOK_TITLE_SIMILARITY_HIGH
                    low_threshold = BOOK_TITLE_SIMILARITY_LOW
                else:
                    high_threshold = TITLE_SIMILARITY_HIGH
                    low_threshold = TITLE_SIMILARITY_LOW
                
                # Calculate match score
                match_score = 0
                issues = []
                
                # Title similarity (using SequenceMatcher)
                if title and result['Verified_Title']:
                    sim = title_similarity(title, result['Verified_Title'])
                    result['Title_Similarity'] = round(sim, 3)
                    
                    if sim >= high_threshold:
                        match_score += 50
                        if DEBUG_MODE:
                            print(f"  DEBUG - Title match: STRONG ({sim:.2f})")
                    elif sim >= low_threshold:
                        match_score += 25
                        if DEBUG_MODE:
                            print(f"  DEBUG - Title match: PARTIAL ({sim:.2f})")
                    else:
                        if DEBUG_MODE:
                            print(f"  DEBUG - Title match: WEAK ({sim:.2f})")
                
                # Year match (with special handling for classics/editions)
                if year and result['Verified_Year']:
                    try:
                        year_diff = abs(int(year) - int(result['Verified_Year']))
                        
                        if original_year is None:
                            # Modern source - strict checking
                            if year_diff == 0:
                                match_score += 25
                                if DEBUG_MODE:
                                    print(f"  DEBUG - Year match: EXACT")
                            elif year_diff <= ALLOW_YEAR_DIFFERENCE:
                                match_score += 15
                                if DEBUG_MODE:
                                    print(f"  DEBUG - Year match: CLOSE (±{year_diff} years)")
                            else:
                                issues.append(f"YEAR_MISMATCH_{year_diff}yrs")
                                if DEBUG_MODE:
                                    print(f"  DEBUG - Year match: MISMATCH ({year_diff} years apart)")
                        else:
                            # Classic/translation - lenient checking
                            issues.append(f"CLASSIC_EDITION_(orig_{original_year}_edit_{year}_verified_{result['Verified_Year']})")
                            match_score += 20  # Still give credit for finding it
                            if DEBUG_MODE:
                                print(f"  DEBUG - Year match: CLASSIC_TRANSLATION (original {original_year})")
                    except ValueError:
                        pass
                
                # Author match (using accent-stripped comparison)
                if first_author and result['Verified_Authors']:
                    author_stripped = strip_accents(first_author.lower())
                    verified_stripped = strip_accents(result['Verified_Authors'].lower())
                    
                    if author_stripped in verified_stripped:
                        match_score += 25
                        if DEBUG_MODE:
                            print(f"  DEBUG - Author match: YES")
                    else:
                        if DEBUG_MODE:
                            print(f"  DEBUG - Author match: NO")
                
                result['CrossRef_Match_Score'] = match_score
        
        # Check PubMed (only for journal articles, not books)
        if title and first_author and ref_type == 'journal_article':
            pubmed_found, _ = check_pubmed(title, first_author)
            result['PubMed_Found'] = pubmed_found
        
        # Determine status and issues
        if not result.get('Issues_Detected'):
            issues = []
        else:
            issues = result['Issues_Detected'] if isinstance(result['Issues_Detected'], list) else [result['Issues_Detected']]
        
        if not result['CrossRef_Found'] and not result['PubMed_Found']:
            if 'NOT_FOUND_IN_DATABASES' not in issues:
                issues.append("NOT_FOUND_IN_DATABASES")
            result['Status'] = 'NEEDS_REVIEW'
        elif result['CrossRef_Match_Score'] < 50:
            if 'LOW_MATCH_CONFIDENCE' not in issues:
                issues.append("LOW_MATCH_CONFIDENCE")
            result['Status'] = 'NEEDS_REVIEW'
        else:
            result['Status'] = 'VERIFIED'
        
        if not doi:
            if 'NO_DOI_FOUND' not in issues:
                issues.append("NO_DOI_FOUND")
        
        if not title:
            if 'TITLE_NOT_EXTRACTED' not in issues:
                issues.append("TITLE_NOT_EXTRACTED")
            result['Status'] = 'NEEDS_REVIEW'
        
        result['Issues_Detected'] = '; '.join(issues) if issues else 'None'
        
        results.append(result)
        
        # Print status
        if result['Status'] == 'ANCIENT_TEXT':
            status_symbol = '⌛'
        elif result['Status'] == 'VERIFIED':
            status_symbol = '✓'
        else:
            status_symbol = '⚠'
        
        print(f"  {status_symbol} Status: {result['Status']} | Score: {result['CrossRef_Match_Score']} | "
              f"Sim: {result['Title_Similarity']:.2f} | Type: {ref_type}")
    
    return pd.DataFrame(results), extraction_failures

# ============================================================================
# GENERATE REPORTS
# ============================================================================

def generate_report(df, output_file, log_file, extraction_failures_file):
    """Generate comprehensive verification reports"""
    
    # Save detailed CSV
    df.to_csv(output_file, index=False)
    print(f"\n✓ Detailed report saved to: {output_file}")
    
    # Generate summary statistics
    total = len(df)
    verified = len(df[df['Status'] == 'VERIFIED'])
    needs_review = len(df[df['Status'] == 'NEEDS_REVIEW'])
    ancient = len(df[df['Status'] == 'ANCIENT_TEXT'])
    with_doi = len(df[df['Extracted_DOI'].notna() & (df['Extracted_DOI'] != '')])
    with_original_year = len(df[df['Extracted_Original_Year'].notna() & (df['Extracted_Original_Year'] != '')])
    crossref_found = len(df[df['CrossRef_Found'] == True])
    high_similarity = len(df[df['Title_Similarity'] >= TITLE_SIMILARITY_HIGH])
    
    # Count by reference type
    type_counts = df['Reference_Type'].value_counts().to_dict()
    
    # Count by status and type
    status_by_type = pd.crosstab(df['Reference_Type'], df['Status'])
    
    # Write summary log
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("BIBLIOGRAPHY VERIFICATION SUMMARY\n")
        f.write("="*70 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*70 + "\n\n")
        
        f.write("OVERALL STATISTICS:\n")
        f.write("-"*70 + "\n")
        f.write(f"Total references checked: {total}\n")
        f.write(f"✓ Verified: {verified} ({verified/total*100:.1f}%)\n")
        f.write(f"⚠  Needs review: {needs_review} ({needs_review/total*100:.1f}%)\n")
        f.write(f"⌛ Ancient texts (skipped): {ancient} ({ancient/total*100:.1f}%)\n")
        f.write(f"References with DOI: {with_doi} ({with_doi/total*100:.1f}%)\n")
        f.write(f"Classics/translations (original year): {with_original_year} ({with_original_year/total*100:.1f}%)\n")
        f.write(f"Found in CrossRef: {crossref_found} ({crossref_found/total*100:.1f}%)\n")
        f.write(f"High title similarity (≥{TITLE_SIMILARITY_HIGH}): {high_similarity} ({high_similarity/total*100:.1f}%)\n\n")
        
        f.write("REFERENCE TYPES:\n")
        f.write("-"*70 + "\n")
        for ref_type, count in type_counts.items():
            f.write(f"  {ref_type}: {count} ({count/total*100:.1f}%)\n")
        
        f.write("\nVERIFICATION STATUS BY REFERENCE TYPE:\n")
        f.write("-"*70 + "\n")
        f.write(status_by_type.to_string())
        f.write("\n\n")
        
        f.write("MATCH SCORE INTERPRETATION FOR PEER REVIEW:\n")
        f.write("-"*70 + "\n")
        f.write("  90-100: Excellent - Safe to publish as-is\n")
        f.write("  75-89:  Good - Verify DOI/year before publishing\n")
        f.write("  50-74:  Fair - Requires manual verification\n")
        f.write("  <50:    Poor - Do not use without manual verification\n\n")
        
        f.write("YEAR MATCHING POLICY:\n")
        f.write("-"*70 + "\n")
        f.write(f"  Modern sources: ±{ALLOW_YEAR_DIFFERENCE} years allowed (early online vs print)\n")
        f.write(f"  Classics/translations: Original year tracked separately\n")
        f.write(f"  Ancient texts: <{ANCIENT_TEXT_CUTOFF} (verification skipped)\n\n")
        
        f.write("="*70 + "\n")
        f.write("REFERENCES NEEDING REVIEW:\n")
        f.write("="*70 + "\n\n")
        
        needs_review_refs = df[df['Status'] == 'NEEDS_REVIEW']
        if len(needs_review_refs) > 0:
            for _, row in needs_review_refs.iterrows():
                f.write(f"Reference #{row['Reference_Number']} ({row['Reference_Type']}):\n")
                f.write(f"  {row['Original_Text'][:100]}...\n")
                f.write(f"  Issues: {row['Issues_Detected']}\n")
                f.write(f"  Match Score: {row['CrossRef_Match_Score']}\n")
                f.write(f"  Title Similarity: {row['Title_Similarity']:.2f}\n")
                if row['Extracted_Original_Year']:
                    f.write(f"  Original Year: {row['Extracted_Original_Year']}\n")
                f.write("\n")
        else:
            f.write("None - all references verified!\n\n")
        
        f.write("="*70 + "\n")
        f.write("QUICK DECISION RULES:\n")
        f.write("="*70 + "\n")
        f.write("If YEAR_MISMATCH ≤ 2 years AND title similarity > 0.75: Likely OK\n")
        f.write("If NOT_FOUND_IN_DATABASES but has DOI: Verify DOI is correct\n")
        f.write("If LOW_MATCH_CONFIDENCE but Is_Book=TRUE: Expected (lower thresholds for books)\n")
        f.write("If CLASSIC_EDITION: Check that original year aligns with content cited\n")
    
    print(f"✓ Summary log saved to: {log_file}")

def export_for_r(df, filename):
    """Export with R-friendly column names and format"""
    df_r = df.copy()
    
    # Convert to R-friendly column names (no spaces, underscores)
    df_r.columns = (df_r.columns
                    .str.replace(' ', '_', regex=False)
                    .str.replace('#', 'Num', regex=False))
    
    # Add simple boolean columns for R filtering
    df_r['Needs_Manual_Check'] = df_r['Status'] == 'NEEDS_REVIEW'
    df_r['Has_DOI'] = df_r['Extracted_DOI'].notna() & (df_r['Extracted_DOI'] != '')
    df_r['High_Confidence'] = (df_r['CrossRef_Match_Score'] >= 75) & (df_r['Title_Similarity'] >= TITLE_SIMILARITY_HIGH)
    df_r['Is_Book'] = df_r['Reference_Type'] == 'book'
    df_r['Is_Ancient'] = df_r['Reference_Type'] == 'ancient_text'
    df_r['Is_Translation_or_Classic'] = df_r['Extracted_Original_Year'].notna() & (df_r['Extracted_Original_Year'] != '')
    
    # Confidence level categories
    df_r['Confidence_Level'] = df_r['CrossRef_Match_Score'].apply(
        lambda x: 'Excellent' if x >= 90 else 
                  'Good' if x >= 75 else
                  'Fair' if x >= 50 else 'Poor'
    )
    
    # Review priority
    df_r['Review_Priority'] = df_r.apply(lambda row: 
        'HIGH' if row['Status'] == 'NEEDS_REVIEW' and row['CrossRef_Match_Score'] < 50 
        else 'MEDIUM' if row['Status'] == 'NEEDS_REVIEW' 
        else 'LOW', axis=1)
    
    df_r.to_csv(filename, index=False)
    print(f"✓ R-compatible file saved to: {filename}")

def export_extraction_failures(extraction_failures, filename):
    """Export extraction failures for debugging"""
    if not extraction_failures:
        return
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("REFERENCES WITH EXTRACTION FAILURES\n")
        f.write("="*70 + "\n\n")
        f.write("These references have incomplete or problematic metadata extraction.\n")
        f.write("Review the original citations and consider adjusting extraction patterns.\n\n")
        
        for ref_num in sorted(extraction_failures.keys()):
            issues = extraction_failures[ref_num]
            f.write(f"Reference #{ref_num}:\n")
            f.write(f"  Issues: {issues}\n\n")
    
    print(f"✓ Extraction failures logged to: {filename}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("BIBLIOGRAPHY VERIFICATION TOOL - PRODUCTION VERSION")
    print("="*70)
    print(f"\nConfiguration:")
    print(f"  • Year difference allowed: ±{ALLOW_YEAR_DIFFERENCE} years")
    print(f"  • Ancient text cutoff: <{ANCIENT_TEXT_CUTOFF}")
    print(f"  • Book title threshold: {BOOK_TITLE_SIMILARITY_HIGH}")
    print(f"  • Article title threshold: {TITLE_SIMILARITY_HIGH}")
    print(f"  • CrossRef session: Enabled with exponential backoff")
    print(f"  • Reference filtering: Enabled (headers removed)")
    print()
    
    

    try:
        # Run verification
        df_results, extraction_failures = verify_bibliography(WORD_FILE)
        
        # Generate reports
        generate_report(df_results, OUTPUT_FILE, DETAILED_LOG, EXTRACTION_FAILURES_LOG)
        export_for_r(df_results, R_OUTPUT_FILE)
        export_extraction_failures(extraction_failures, EXTRACTION_FAILURES_LOG)

        # === PRINT ONLY KEY SUMMARY SECTIONS TO CONSOLE ===
        try:
            with open(DETAILED_LOG, "r", encoding="utf-8") as f:
                lines = f.readlines()

            sections_to_print = []
            capture = False
            wanted_headers = [
                "OVERALL STATISTICS:",
                "REFERENCE TYPES:",
                "VERIFICATION STATUS BY REFERENCE TYPE:"
            ]

            for line in lines:
                if any(h in line for h in wanted_headers):
                    capture = True
                    sections_to_print.append("\n" + line.rstrip())
                    continue
                if capture:
                    # Stop capturing when we hit another all-caps header
                    if line.strip().isupper() and line.strip().endswith(":") and line.strip() not in wanted_headers:
                        capture = False
                    else:
                        sections_to_print.append(line.rstrip())

            print("\n" + "="*70)
            print("SUMMARY (Key Metrics Only)")
            print("="*70)
            for ln in sections_to_print:
                print(ln)
            print("="*70)
        except Exception as e_summary:
            print(f"(Could not print summary sections: {e_summary})")



        
        print("\n" + "="*70)
        print("✓ VERIFICATION COMPLETE!")
        print("="*70)
        print(f"\nGenerated files:")
        print(f"  1. {OUTPUT_FILE}")
        print(f"     → Detailed results with all extracted and verified metadata")
        print(f"  2. {DETAILED_LOG}")
        print(f"     → Human-readable summary and items needing review")
        print(f"  3. {R_OUTPUT_FILE}")
        print(f"     → R-compatible format with boolean flags and priority ratings")
        if extraction_failures:
            print(f"  4. {EXTRACTION_FAILURES_LOG}")
            print(f"     → References with extraction issues for debugging")
        
        print(f"\nNext steps for peer review:")
        print(f"  • Review items marked 'NEEDS_REVIEW' in {DETAILED_LOG}")
        print(f"  • Classics/translations show original publication year")
        print(f"  • Books use more lenient matching thresholds (expected)")
        print(f"  • Import {R_OUTPUT_FILE} into RStudio for filtering:")
        print(f"    library(tidyverse)")
        print(f"    refs <- read_csv('{R_OUTPUT_FILE}')")
        print(f"    refs %>% filter(Needs_Manual_Check) %>% view()")
        print("="*70 + "\n")
        
    except FileNotFoundError:
        print(f"\n✗ Error: Could not find '{WORD_FILE}'")
        print("  Please ensure the Word file is in the same directory as this script")
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
