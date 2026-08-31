#!/bin/bash
# Resizes the 2 real product box photos per product into assets/img/products/<slug>/
# Source: numbered folders (1-15) containing raw WhatsApp exports.
set -e

cd "$(dirname "$0")/.."

declare -a MAP=(
  "1:sayomax"
  "2:doxophil-a"
  "3:nuvinor"
  "4:loxwin-200"
  "5:zydec"
  "6:easily-pm"
  "7:simtol"
  "8:vogmix-0-3"
  "9:pcop-2"
  "10:doronec-150"
  "11:mynox-4k"
  "12:betop"
  "13:hylovision"
  "14:polycool"
  "15:solomax"
)

for entry in "${MAP[@]}"; do
  folder="${entry%%:*}"
  slug="${entry##*:}"
  outdir="public/assets/img/products/$slug"
  mkdir -p "$outdir"

  files=()
  while IFS= read -r f; do
    files+=("$f")
  done < <(find "source-photos/$folder" -type f -iname "*.jpeg" | sort)

  i=1
  for f in "${files[@]:0:2}"; do
    sips -Z 900 "$f" --out "$outdir/$i.jpg" >/dev/null 2>&1
    cwebp -q 78 "$outdir/$i.jpg" -o "$outdir/$i.webp" >/dev/null 2>&1
    echo "$slug/$i <- $f"
    i=$((i+1))
  done
done
