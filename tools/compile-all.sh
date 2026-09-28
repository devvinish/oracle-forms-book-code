#!/bin/bash
# Compiles every module of an application in the order Forms needs (Chapter 38):
# libraries (.pll -> .plx), then menus (.mmb -> .mmx), then forms (.fmb -> .fmx).
# A library that attaches another compiles only after it: libraries are compiled in passes,
# until a pass compiles nothing new.
#   compile-all.sh <directory> <userid>
# The directory must be in FORMS_PATH, so that attached libraries are found.
dir=${1:?directory}; userid=${2:?userid}
cd "$dir" || exit 1
declare -a failed
compile() {                          # compile <file> <type>: 0 if the compiled file was written
  local out
  case $2 in LIBRARY) out=${1%.*}.plx;; MENU) out=${1%.*}.mmx;; FORM) out=${1%.*}.fmx;; esac
  rm -f "$out" "${1%.*}.err"
  frmcmp_batch module="$1" userid="$userid" module_type=$2 compile_all=yes batch=yes > /dev/null 2>&1
  [ -f "$out" ]
}

# libraries, in passes
todo=( $(ls *.pll 2>/dev/null) )
while [ ${#todo[@]} -gt 0 ]; do
  left=()
  for f in "${todo[@]}"; do compile "$f" LIBRARY || left+=("$f"); done
  [ ${#left[@]} -eq ${#todo[@]} ] && break            # no progress: the rest fail
  todo=("${left[@]}")
done
failed+=("${left[@]}")

for f in $(ls *.mmb 2>/dev/null); do compile "$f" MENU || failed+=("$f"); done
for f in $(ls *.fmb 2>/dev/null); do compile "$f" FORM || failed+=("$f"); done

total=$(ls *.pll *.mmb *.fmb 2>/dev/null | wc -l)
echo "compiled $((total - ${#failed[@]})) of $total modules"
for f in "${failed[@]}"; do
  echo "FAILED $f: $(grep -m1 -E 'FRM-[0-9]+|PL/SQL ERROR|PDE-' "${f%.*}.err" 2>/dev/null)"
done
[ ${#failed[@]} -eq 0 ]
