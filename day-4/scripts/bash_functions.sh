#!/bin/bash

# ===================
# Bash Functions Demo
# ===================

# Simple function
say_hello() {
    echo "Hello, World!"
}

# Function with parameter
greet() {
    local name=$1
    echo "Hello, $name!"
}

# Function with multiple parameters
add_numbers() {
    local a=$1
    local b=$2
    local sum=$((a + b))
    echo $sum
}

# Function with return value (via echo)
get_timestamp() {
    echo $(date +%Y%m%d_%H%M%S)
}

# Function that checks something
file_exists() {
    local filepath=$1
    if [ -f "$filepath" ]; then
        return 0  # true in bash
    else
        return 1  # false in bash
    fi
}

# ===================
# Using the functions
# ===================

echo "=== Basic function ==="
say_hello

echo ""
echo "=== Function with parameter ==="
greet "Phoebe"
greet "Data Engineer"

echo ""
echo "=== Function with math ==="
result=$(add_numbers 5 10)
echo "5 + 10 = $result"

echo ""
echo "=== Function returning value ==="
timestamp=$(get_timestamp)
echo "Current timestamp: $timestamp"

echo ""
echo "=== Function with conditional return ==="
if file_exists "cities.txt"; then
    echo "cities.txt exists!"
else
    echo "cities.txt not found"
fi

if file_exists "nonexistent.txt"; then
    echo "Found it!"
else
    echo "nonexistent.txt not found (expected)"
fi