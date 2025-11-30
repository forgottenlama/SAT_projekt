#!/bin/bash

TESTDIR="test"
SOLVER="python3 superstring.py"   # príkaz pre spustenie solvera

if [ ! -d "$TESTDIR" ]; then
    echo "Directory $TESTDIR not found!"
    exit 1
fi

echo "Running tests in $TESTDIR/"
echo "-------------------------------------------"
printf "%-25s %10s\n" "Test file" "Time (ms)"
echo "-------------------------------------------"

total_ms=0
count=0

for f in "$TESTDIR"/*.in; do
    start=$(date +%s%3N)

    # spustenie solvera so správnym argumentom
    $SOLVER -i "$f" >/dev/null 2>&1

    end=$(date +%s%3N)
    ms=$(( end - start ))
    total_ms=$(( total_ms + ms ))
    count=$(( count + 1 ))

    printf "%-25s %10d\n" "$(basename "$f")" "$ms"
done

echo "-------------------------------------------"
echo "Total time: ${total_ms} ms"
if [ $count -gt 0 ]; then
    echo "Average: $(( total_ms / count )) ms/test"
fi
