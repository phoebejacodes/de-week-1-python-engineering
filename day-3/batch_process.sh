#!/bin/bash

# Process multiple city files

CITIES_DIR="./data/city_lists"
OUTPUT_DIR="./output"

# Create test city files
mkdir -p "$CITIES_DIR"
echo -e "Kingston\nHavana" > "$CITIES_DIR/caribbean.txt"
echo -e "London\nParis" > "$CITIES_DIR/europe.txt"
echo -e "Tokyo\nSeoul" > "$CITIES_DIR/asia.txt"
echo -e "New York\nChicago" > "$CITIES_DIR/usa.txt"

echo "Processing city lists..."

# Loop through all .txt files in directory
for file in "$CITIES_DIR"/*.txt; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        echo "Processing: $filename"
        
        # Count cities
        city_count=$(wc -l < "$file")
        echo "  Cities: $city_count"
        
        # Show cities
        while read -r city; do
            echo "    - $city"
        done < "$file"
    fi
done

echo "Done processing all files"