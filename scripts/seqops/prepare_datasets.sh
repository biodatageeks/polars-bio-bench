#!/usr/bin/env bash
# Download the short-read datasets from ENA, verify their MD5, and write the two
# input variants every tool reads: the original gzip (plain, single stream) and
# a BGZF re-encoding with its .gzi index (splittable by polars-bio). Prints the
# SHA-256 of every input for provenance.
#
# usage: prepare_datasets.sh DATA_DIR      (needs curl, bgzip, md5sum or md5)
set -euo pipefail
DATA=${1:?usage: prepare_datasets.sh DATA_DIR}
mkdir -p "$DATA"
cd "$DATA"

# name | ENA paths (;-separated, concatenated in order) | MD5s (;-separated)
DATASETS=(
  "DRR609229_1|vol1/fastq/DRR609/DRR609229/DRR609229_1.fastq.gz|e705fdba0b1fca34244958bece7949b2"
  "ERR5897746_1|vol1/fastq/ERR589/006/ERR5897746/ERR5897746_1.fastq.gz|e2f3ac312a75a96e5c32c97654bb73b5"
  "DRR013000_1|vol1/fastq/DRR013/DRR013000/DRR013000_1.fastq.gz|3ad6d4d388dc202dfe4e42f85245e3f0"
  "SRR39421268|vol1/fastq/SRR394/068/SRR39421268/SRR39421268_1.fastq.gz;vol1/fastq/SRR394/068/SRR39421268/SRR39421268_2.fastq.gz|f56f939741213e0c68c4af3a1ff48966;f569e37ca0987487fbbd1c4d571d72f6"
)

md5() { if command -v md5sum >/dev/null; then md5sum "$1" | cut -d' ' -f1; else md5 -q "$1"; fi; }
sha256() { if command -v sha256sum >/dev/null; then sha256sum "$1" | cut -d' ' -f1; else shasum -a 256 "$1" | cut -d' ' -f1; fi; }

for entry in "${DATASETS[@]}"; do
  IFS='|' read -r name paths md5s <<<"$entry"
  IFS=';' read -ra P <<<"$paths"
  IFS=';' read -ra M <<<"$md5s"
  parts=()
  for i in "${!P[@]}"; do
    f=$(basename "${P[$i]}")
    if [ ! -s "$f" ] || [ "$(md5 "$f")" != "${M[$i]}" ]; then
      curl -fsSL --retry 5 -C - -o "$f" "https://ftp.sra.ebi.ac.uk/${P[$i]}"
    fi
    [ "$(md5 "$f")" = "${M[$i]}" ] || { echo "MD5 mismatch: $f" >&2; exit 1; }
    parts+=("$f")
  done
  # Plain gzip variant: a single member, as ENA serves it (concatenated for
  # paired runs, which gives a multi-member gzip that every tool reads).
  if [ ! -s "$name.fastq.gz" ]; then
    if [ "${#parts[@]}" -eq 1 ]; then ln -sf "${parts[0]}" "$name.fastq.gz"; else cat "${parts[@]}" > "$name.fastq.gz"; fi
  fi
  # BGZF variant with a .gzi index.
  if [ ! -s "$name.fastq.bgz.gzi" ]; then
    gzip -dc "$name.fastq.gz" | bgzip -@ 8 -c > "$name.fastq.bgz"
    bgzip -r "$name.fastq.bgz"
  fi
  printf '%s\t%s\t%s\n' "$name" "$(sha256 "$name.fastq.gz")" "$(sha256 "$name.fastq.bgz")"
done

# Translation input: Ensembl GRCh38 CDS (protein-coding transcripts' coding
# sequences), as gzip and BGZF. "current_fasta" moves with Ensembl releases;
# the SHA-256 printed below pins the exact file used.
CDS=Homo_sapiens.GRCh38.cds.all
if [ ! -s "$CDS.fa.gz" ]; then
  curl -fsSL --retry 5 -o "$CDS.fa.gz" "https://ftp.ensembl.org/pub/current_fasta/homo_sapiens/cds/$CDS.fa.gz"
fi
if [ ! -s "$CDS.fa.bgz.gzi" ]; then
  gzip -dc "$CDS.fa.gz" | bgzip -@ 8 -c > "$CDS.fa.bgz"
  bgzip -r "$CDS.fa.bgz"
fi
printf '%s\t%s\t%s\n' "$CDS" "$(sha256 "$CDS.fa.gz")" "$(sha256 "$CDS.fa.bgz")"
