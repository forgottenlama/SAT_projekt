#!/bin/bash

# zavislost na pocte stringov

N_of_tests=50
OUTDIR="test"

mkdir -p "$OUTDIR"

generate_binary() {
    local length=$1
    local str=""
    for q in $(seq 1 $length); do
        if (( RANDOM % 2 )); then
            str="${str}1"
        else
            str="${str}0"
        fi
    done
    echo "$str"
}

# i je počet reťazcov
for i in $(seq 1 $N_of_tests); do
    filename="$OUTDIR/Test_i_${i}.in"
    : > "$filename"   # vytvorí/čistí súbor
    echo "$((10*i))" >> "$filename"
    for j in $(seq 1 $i); do 
        len=10 # dĺžka reťazca je 10
        generate_binary "$len" >> "$filename"
    done
done
