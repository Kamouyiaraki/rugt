#!/usr/bin/env python3

import os
import sys
import csv
import logging
import argparse
import subprocess
from pathlib import Path
from shutil import which

import pandas as pd

# Logging setup
LOG_PATH = Path("logs/get_taxids.log")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("get_taxids")
logger.setLevel(logging.INFO)

logger.addHandler(logging.StreamHandler(sys.stdout))
logger.addHandler(logging.FileHandler(LOG_PATH))

# Main functions
def detect_delimiter(file_path: Path) -> str:
    with open(file_path, "r", newline="") as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        return dialect.delimiter


def read_file(file_path: Path) -> pd.DataFrame:
    if not file_path.is_file():
        logger.error(f"Input file does not exist: {file_path}")
        sys.exit(1)

    if file_path.suffix == ".xlsx":
        df = pd.read_excel(file_path)
    else:
        delimiter = detect_delimiter(file_path)
        df = pd.read_csv(file_path, delimiter=delimiter)

    df.dropna(how="all", inplace=True)
    return df


def get_taxids(df, column_name, file_path, taxonkit_path):
    if column_name not in df.columns:
        logger.error(f"Column '{column_name}' not found in input file")
        logger.error(f"Available columns: {list(df.columns)}")
        sys.exit(1)

    taxonkit_path = Path(taxonkit_path)

    ids = df[column_name].astype(str).tolist()

    ids_file = Path("ids.txt")
    ids_file.write_text("\n".join(ids))

    stem = file_path.stem
    outdir = file_path.parent
    taxoutfile = outdir / f"{stem}_taxids_only.out"

    command = (
        f"cat {ids_file} | "
        f"{taxonkit_path} name2taxid"
        f"--data-dir $HOME/.taxonkit/ > {taxoutfile}"
    )

    logger.info("Running TaxonKit name2taxid")
    subprocess.run(command, shell=True, check=True)

    taxids_df = pd.read_csv(
        taxoutfile,
        sep="\t",
        header=None,
        names=["Taxonomic_name", "TaxID"],
    )

    null_rows = taxids_df[taxids_df.isnull().any(axis=1)]
    if not null_rows.empty:
        null_outfile = outdir / f"{stem}_null_taxids.csv"
        null_rows.to_csv(null_outfile, index=False)
        logger.info(f"Null TaxIDs written to {null_outfile}")

    return taxids_df


def merge_df(df: pd.DataFrame, file_path: Path) -> Path:
    stem = file_path.stem
    outdir = file_path.parent

    taxoutfile = outdir / f"{stem}_taxids_only.out"
    lin = pd.read_csv(taxoutfile, sep="\t", header=None)
    lin.columns = ["Taxonomic_name", "TaxID"]

    merged_df = pd.concat([df.reset_index(drop=True), lin], axis=1)

    outfile = outdir / f"{stem}_taxids.csv"
    merged_df.to_csv(outfile, index=False)

    return outfile


def main():
    parser = argparse.ArgumentParser(
        description="Map taxonomic names to TaxIDs using TaxonKit"
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        type=Path,
        help="Input CSV or XLSX file"
    )
    parser.add_argument(
        "-c", "--column",
        required=True,
        help="Column containing taxonomic names"
    )

    parser.add_argument(
        "--taxonkit_path",
        help="Path to taxonkit executable (if not provided, resolved from $PATH)"
    )
    
    args = parser.parse_args()
    
    if args.taxonkit:
        taxonkit_path = Path(args.taxonkit)
        if not taxonkit_path.is_file():
            logger.error(f"TaxonKit executable not found: {taxonkit_path}")
            sys.exit(1)
    else:
        resolved = which("taxonkit")
        if not resolved:
            logger.error(
                "TaxonKit executable not found. "
                "Provide --taxonkit or ensure taxonkit is in $PATH."
            )
            sys.exit(1)
        taxonkit_path = Path(resolved)

    logger.info(f"Reading input file: {args.input}")
    df = read_file(args.input)

    taxids_df = get_taxids(df, args.column, args.input)
    logger.info(f"Extracted {len(taxids_df)} TaxIDs")

    outfile = merge_df(df, args.input)
    logger.info(f"Final output written to: {outfile}")


if __name__ == "__main__":
    main()
    
## Example useage: 
## python get_taxids.py -i taxids2check.csv -c Current_Name 
##
## Output: 
## (1) csv of Taxonomic_name and taxID only 
## (2) csv of null taxIDs (i.e., taxonomic_name with no tax IDs)
## (3) csv of original input spreadsheet with taxIDs (where found) added as a new column. 