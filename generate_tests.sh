#!/bin/bash

OUTDIR="test"
mkdir -p "$OUTDIR"

MAX_M=10      # max number of strings
MAX_LEN=10    # max length of each string

echo "Generating tests into $OUTDIR/..."

generate_binary_string() {
    local len=$1
    local s=""
    for ((i=0;i<len;i++)); do
        if (( RANDOM % 2 )); then
            s="${s}1"
        else
            s="${s}0"
        fi
    done
    echo "$s"
}

for k in $(seq 0 100); do
    filename="$OUTDIR/Test_k_${k}.in"
    echo -e "$k\n01\n11\n100010110010110001101011001011\n110110010110001101011\n0110010110001101011\n110010110001101011001011\n10110010110001101011001\n000000000000000000000000000001" > "$filename"
done
echo "Done!"
