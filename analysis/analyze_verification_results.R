# Bibliography Verification Analysis Script for RStudio
# Load and analyze bibliography verification results
# Use this script to filter, summarize, and report on reference verification

# Install packages if needed (uncomment first time):
# install.packages("tidyverse")
# install.packages("knitr")

library(tidyverse)

# ============================================================================
# 1. LOAD DATA
# ============================================================================

# Load the R-compatible verification results
refs <- read_csv("verification_for_R.csv")

# View structure
glimpse(refs)

# Quick summary
cat("Total references:", nrow(refs), "\n")
cat("Verified:", sum(refs$Status == "VERIFIED"), "\n")
cat("Needs review:", sum(refs$Status == "NEEDS_REVIEW"), "\n")
cat("Ancient texts:", sum(refs$Status == "ANCIENT_TEXT"), "\n")

# ============================================================================
# 2. OVERALL STATISTICS
# ============================================================================

# Summary by status
status_summary <- refs %>%
  group_by(Status) %>%
  summarise(
    Count = n(),
    Percentage = round(100 * n() / nrow(refs), 1),
    Avg_Score = round(mean(CrossRef_Match_Score, na.rm = TRUE), 1),
    .groups = "drop"
  )

print("VERIFICATION STATUS SUMMARY:")
print(status_summary)

# Summary by reference type
type_summary <- refs %>%
  group_by(Reference_Type) %>%
  summarise(
    Count = n(),
    Verified = sum(Status == "VERIFIED"),
    Needs_Review = sum(Status == "NEEDS_REVIEW"),
    Pct_Verified = round(100 * sum(Status == "VERIFIED") / n(), 1),
    Avg_Score = round(mean(CrossRef_Match_Score, na.rm = TRUE), 1),
    .groups = "drop"
  )

print("\nREFERENCE TYPE BREAKDOWN:")
print(type_summary)

# Summary by confidence level
confidence_summary <- refs %>%
  group_by(Confidence_Level) %>%
  summarise(
    Count = n(),
    Percentage = round(100 * n() / nrow(refs), 1),
    .groups = "drop"
  ) %>%
  arrange(factor(Confidence_Level, levels = c("Excellent", "Good", "Fair", "Poor")))

print("\nCONFIDENCE LEVEL DISTRIBUTION:")
print(confidence_summary)

# ============================================================================
# 3. IDENTIFY HIGH-PRIORITY REVIEWS
# ============================================================================

# Critical issues (HIGH priority - don't publish without fixing)
critical_reviews <- refs %>%
  filter(
    Status == "NEEDS_REVIEW",
    Review_Priority == "HIGH"
  ) %>%
  select(
    Reference_Number,
    Reference_Type,
    Extracted_First_Author,
    Extracted_Year,
    CrossRef_Match_Score,
    Title_Similarity,
    Issues_Detected
  ) %>%
  arrange(CrossRef_Match_Score)

if (nrow(critical_reviews) > 0) {
  cat("\n⚠️  CRITICAL REVIEWS (HIGH Priority):\n")
  print(critical_reviews, n = nrow(critical_reviews))
} else {
  cat("\n✓ No critical issues found!\n")
}

# Medium priority (verify before publishing)
medium_reviews <- refs %>%
  filter(
    Status == "NEEDS_REVIEW",
    Review_Priority == "MEDIUM"
  ) %>%
  select(
    Reference_Number,
    Reference_Type,
    Extracted_First_Author,
    CrossRef_Match_Score,
    Issues_Detected
  )

if (nrow(medium_reviews) > 0) {
  cat("\n⚠️  MEDIUM PRIORITY REVIEWS:\n")
  print(medium_reviews, n = Inf)
}

# ============================================================================
# 4. SPECIAL CASES
# ============================================================================

# Classics and translations (have original year)
classics <- refs %>%
  filter(Is_Translation_or_Classic == TRUE) %>%
  select(
    Reference_Number,
    Extracted_First_Author,
    Extracted_Year,
    Extracted_Original_Year,
    Confidence_Level,
    Issues_Detected
  )

if (nrow(classics) > 0) {
  cat("\n📚 CLASSICS & TRANSLATIONS (Track Original Year):\n")
  print(classics, n = Inf)
} else {
  cat("\n📚 No classics or translations detected.\n")
}

# Ancient texts (skipped verification)
ancient <- refs %>%
  filter(Is_Ancient == TRUE) %>%
  select(
    Reference_Number,
    Extracted_First_Author,
    Extracted_Year,
    Status
  )

if (nrow(ancient) > 0) {
  cat("\n⌛ ANCIENT TEXTS (Verification Skipped, Pre-1800):\n")
  print(ancient, n = Inf)
}

# Books without DOI
books_no_doi <- refs %>%
  filter(Is_Book == TRUE, Has_DOI == FALSE) %>%
  select(
    Reference_Number,
    Extracted_First_Author,
    Extracted_Year,
    Confidence_Level,
    Status
  )

if (nrow(books_no_doi) > 0) {
  cat("\n📖 BOOKS WITHOUT DOI (Expected, Especially Older Works):\n")
  cat("Count:", nrow(books_no_doi), "\n")
  if (nrow(books_no_doi) <= 10) {
    print(books_no_doi, n = Inf)
  } else {
    print(books_no_doi, n = 10)
    cat("... and", nrow(books_no_doi) - 10, "more\n")
  }
}

# ============================================================================
# 5. DATA QUALITY METRICS
# ============================================================================

# DOI coverage
doi_coverage <- refs %>%
  summarise(
    Total = n(),
    With_DOI = sum(Has_DOI),
    DOI_Percentage = round(100 * sum(Has_DOI) / n(), 1),
    CrossRef_Found = sum(CrossRef_Found),
    CrossRef_Percentage = round(100 * sum(CrossRef_Found) / n(), 1)
  )

print("\nDATA QUALITY METRICS:")
print(doi_coverage)

# Title similarity statistics
title_sim_stats <- refs %>%
  filter(CrossRef_Found == TRUE) %>%
  summarise(
    Min_Similarity = round(min(Title_Similarity, na.rm = TRUE), 3),
    Mean_Similarity = round(mean(Title_Similarity, na.rm = TRUE), 3),
    Median_Similarity = round(median(Title_Similarity, na.rm = TRUE), 3),
    Max_Similarity = round(max(Title_Similarity, na.rm = TRUE), 3)
  )

print("\nTITLE SIMILARITY STATISTICS (for found references):")
print(title_sim_stats)

# Match score distribution
match_score_dist <- refs %>%
  filter(CrossRef_Found == TRUE) %>%
  summarise(
    Excellent_90_100 = sum(CrossRef_Match_Score >= 90),
    Good_75_89 = sum(CrossRef_Match_Score >= 75 & CrossRef_Match_Score < 90),
    Fair_50_74 = sum(CrossRef_Match_Score >= 50 & CrossRef_Match_Score < 75),
    Poor_Below_50 = sum(CrossRef_Match_Score < 50)
  )

print("\nMATCH SCORE DISTRIBUTION (for found references):")
print(match_score_dist)

# ============================================================================
# 6. EXPORT PUBLICATION-READY RESULTS
# ============================================================================

# Export verified references only (safe for publication)
verified_clean <- refs %>%
  filter(Status == "VERIFIED" | Status == "ANCIENT_TEXT") %>%
  select(
    Reference_Number,
    Reference_Type,
    Original_Text,
    Confidence_Level,
    CrossRef_Match_Score,
    Extracted_DOI,
    Verified_DOI
  ) %>%
  arrange(Reference_Number)

# Save for publication
write_csv(verified_clean, "bibliography_verified_final.csv")
cat("\n✓ Verified bibliography exported to: bibliography_verified_final.csv\n")

# Export review list (items needing attention)
review_list <- refs %>%
  filter(Status == "NEEDS_REVIEW") %>%
  select(
    Reference_Number,
    Reference_Type,
    Extracted_First_Author,
    Extracted_Year,
    Extracted_Title,
    CrossRef_Match_Score,
    Title_Similarity,
    Issues_Detected
  ) %>%
  arrange(CrossRef_Match_Score)

if (nrow(review_list) > 0) {
  write_csv(review_list, "bibliography_needs_review.csv")
  cat("✓ Items needing review exported to: bibliography_needs_review.csv\n")
}

# ============================================================================
# 7. SUMMARY TABLE FOR PUBLICATION
# ============================================================================

# Create publication-ready summary table
summary_for_paper <- refs %>%
  filter(Status == "VERIFIED" | Status == "ANCIENT_TEXT") %>%
  group_by(Reference_Type) %>%
  summarise(
    `Total References` = n(),
    `With DOI` = sum(Has_DOI),
    `High Confidence` = sum(High_Confidence, na.rm = TRUE),
    `Mean Match Score` = round(mean(CrossRef_Match_Score, na.rm = TRUE), 1),
    .groups = "drop"
  ) %>%
  mutate(
    `Reference Type` = case_when(
      Reference_Type == "journal_article" ~ "Journal Articles",
      Reference_Type == "book" ~ "Books",
      Reference_Type == "ancient_text" ~ "Ancient Texts",
      Reference_Type == "in_press" ~ "In Press",
      TRUE ~ Reference_Type
    )
  ) %>%
  select(`Reference Type`, everything(), -Reference_Type)

print("\nSUMMARY TABLE FOR PUBLICATION:")
print(summary_for_paper)

# ============================================================================
# 8. VISUALIZATIONS (Optional)
# ============================================================================

# Plot 1: Match score distribution
if (require(ggplot2, quietly = TRUE)) {
  
  p1 <- refs %>%
    filter(CrossRef_Found == TRUE) %>%
    ggplot(aes(x = CrossRef_Match_Score)) +
    geom_histogram(bins = 20, fill = "steelblue", color = "white") +
    facet_wrap(~Reference_Type) +
    labs(
      title = "Distribution of Match Scores by Reference Type",
      x = "CrossRef Match Score",
      y = "Count",
      subtitle = "Higher scores = stronger verification confidence"
    ) +
    theme_minimal() +
    theme(
      plot.title = element_text(face = "bold"),
      panel.grid.major.x = element_blank()
    )
  
  print(p1)
  ggsave("match_score_distribution.png", p1, width = 10, height = 6)
  
  # Plot 2: Status by type
  p2 <- refs %>%
    ggplot(aes(x = Reference_Type, fill = Status)) +
    geom_bar(position = "dodge") +
    labs(
      title = "Verification Status by Reference Type",
      x = "Reference Type",
      y = "Count",
      fill = "Status"
    ) +
    theme_minimal() +
    theme(
      plot.title = element_text(face = "bold"),
      axis.text.x = element_text(angle = 45, hjust = 1)
    )
  
  print(p2)
  ggsave("status_by_type.png", p2, width = 10, height = 6)
  
  cat("\n✓ Plots saved: match_score_distribution.png, status_by_type.png\n")
  
} else {
  cat("\nNote: Install ggplot2 for visualizations: install.packages('ggplot2')\n")
}

# ============================================================================
# 9. FINAL CHECKLIST
# ============================================================================

cat("\n" %+% strrep("=", 70) %+% "\n")
cat("PUBLICATION READINESS CHECKLIST\n")
cat(strrep("=", 70) %+% "\n\n")

verified_count <- sum(refs$Status %in% c("VERIFIED", "ANCIENT_TEXT"))
total_count <- nrow(refs)
verification_rate <- round(100 * verified_count / total_count, 1)

cat("✓ Total references:", total_count, "\n")
cat("✓ Verified or skipped:", verified_count, "(", verification_rate, "%)\n")
cat("⚠  Needs review:", sum(refs$Status == "NEEDS_REVIEW"), "\n")

if (sum(refs$Status == "NEEDS_REVIEW") == 0) {
  cat("\n🎉 ALL REFERENCES VERIFIED - READY FOR PUBLICATION\n")
} else {
  cat("\n⚠️  Address", sum(refs$Status == "NEEDS_REVIEW"), "items before publishing\n")
  cat("   See: bibliography_needs_review.csv\n")
}

cat("\n✓ Results exported:\n")
cat("   - bibliography_verified_final.csv (for publication)\n")
if (nrow(review_list) > 0) {
  cat("   - bibliography_needs_review.csv (for manual verification)\n")
}
if (require(ggplot2, quietly = TRUE)) {
  cat("   - match_score_distribution.png (visualization)\n")
  cat("   - status_by_type.png (visualization)\n")
}

cat("\n" %+% strrep("=", 70) %+% "\n")

# ============================================================================
# 10. OPTIONAL: MARKDOWN REPORT GENERATION
# ============================================================================

# Uncomment to generate a markdown report for your paper's supplement

# generate_report <- function(refs) {
#   report <- paste0(
#     "# Bibliography Verification Report\n\n",
#     "## Summary Statistics\n",
#     "- Total references verified: ", nrow(refs), "\n",
#     "- Verified: ", sum(refs$Status == "VERIFIED"), " (",
#     round(100 * sum(refs$Status == "VERIFIED") / nrow(refs), 1), "%)\n",
#     "- Needs review: ", sum(refs$Status == "NEEDS_REVIEW"), "\n",
#     "- Ancient texts: ", sum(refs$Status == "ANCIENT_TEXT"), "\n\n",
#     "## References Needing Review\n"
#   )
#   
#   review_items <- refs %>% filter(Status == "NEEDS_REVIEW")
#   for (i in 1:nrow(review_items)) {
#     report <- paste0(report,
#       "### Reference #", review_items$Reference_Number[i], "\n",
#       review_items$Original_Text[i], "\n",
#       "**Issues**: ", review_items$Issues_Detected[i], "\n\n"
#     )
#   }
#   
#   return(report)
# }
# 
# report_text <- generate_report(refs)
# writeLines(report_text, "bibliography_verification_report.md")

cat("\n✓ Analysis complete. Check bibliography_verified_final.csv for results.\n\n")
