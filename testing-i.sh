#!/bin/bash

INDIR="test"
SOLVER="python3 superstring.py"
OUTCSV="results.csv"

# Hlavička CSV
echo "subor,cas_s,klauzuly" > "$OUTCSV"

for i in $(seq 1 50); do
    file="$INDIR/Test_i_$i.in"
    # Meranie času v nanosekundách
    start=$(date +%s%N)

    # Spustenie solvera, výstup si odchytíme
    output=$($SOLVER -i "$file")

    end=$(date +%s%N)
    runtime_ns=$(( end - start ))
    runtime_s=$(awk "BEGIN {printf \"%.6f\", $runtime_ns / 1000000000}")

    # Počet klauzúl
    clauses=$(echo "$output" | grep -Eo "CLAUSES: [0-9]+" | awk '{print $2}')
    if [ -z "$clauses" ]; then
        clauses="0"
    fi

    # Pridanie riadku do CSV
    echo "$(basename "$file"),$runtime_s,$clauses" >> "$OUTCSV"
done

echo "Výsledky uložené v $OUTCSV"
