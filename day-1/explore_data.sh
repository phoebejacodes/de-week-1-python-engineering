#!/bin/bash

echo "=== Data Summary ==="
echo ""
echo "Total records in CSV:"
wc -l user_posts.csv
echo ""
echo "Column headers:"
head -1 user_posts.csv
echo ""
echo "Sample data (first 5 rows):"
head -6 user_posts.csv
echo ""
echo "Unique users (by email column):"
cut -d',' -f3 user_posts.csv | sort | uniq | head -10