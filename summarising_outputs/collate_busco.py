#!/usr/bin/env python3

import argparse
import json
from pathlib import Path
import pandas as pd
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        description="Summarise BUSCO JSON results into a single CSV file"
    )
    parser.add_argument(
        "-i", "--input_dir",
        required=True,
        type=Path,
        help="Input directory containing BUSCO output (searched recursively)"
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        type=Path,
        help="Output CSV filename"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    input_dir = args.input_dir
    output_file = args.output

    if not input_dir.exists() or not input_dir.is_dir():
        sys.exit(f"ERROR: input_dir does not exist or is not a directory: {input_dir}")

    data = []

    # Iterate through all JSON files recursively
    for json_file in input_dir.rglob("*.json"):
        try:
            with open(json_file, "r") as f:
                content = json.load(f)
        except json.JSONDecodeError:
            print(f"WARNING: Could not parse JSON file: {json_file}", file=sys.stderr)
            continue

        results = content.get("results", {})
        if results:
            results["filename"] = json_file.name
            results["path"] = str(json_file.parent)
            data.append(results)

    if not data:
        sys.exit("ERROR: No valid BUSCO JSON results found.")

    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)

    print(f"Saved BUSCO summary to: {output_file}")
    print(df.head())


if __name__ == "__main__":
    main()
