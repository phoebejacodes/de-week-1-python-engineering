#!/bin/bash

CSV_FILE="user_posts.csv"
JSON_FILE="user_posts.json"

echo "=============================="
echo "      DATA OUTPUT SUMMARY     "
echo "=============================="
echo ""

# ---- CSV SECTION ----
echo "=== CSV FILE CHECKS ==="
echo ""

echo "Total rows in CSV:"
wc -l "$CSV_FILE"
echo ""

echo "CSV headers:"
head -1 "$CSV_FILE"
echo ""

echo "Sample CSV rows:"
head -6 "$CSV_FILE"
echo ""

echo "Posts by Leanne Graham (CSV):"
grep "Leanne Graham" "$CSV_FILE" | wc -l
echo ""

# ---- JSON SECTION ----
echo "=== JSON FILE CHECKS ==="
echo ""

echo "Total records in JSON:"
jq length "$JSON_FILE"
echo ""

echo "Keys in JSON record:"
jq '.[0] | keys' "$JSON_FILE"
echo ""

echo "Sample JSON records:"
jq '.[0:3]' "$JSON_FILE"
echo ""

echo "Posts by Leanne Graham (JSON):"
jq '[.[] | select(.user_name == "Leanne Graham")] | length' "$JSON_FILE"
echo ""
