#!/usr/bin/env python3
"""
Batch PDF Compression Script
Processes all PDF files in a specified directory
"""

import os
import sys
from pathlib import Path
from pdf_reducer import compress_pdf_to_target, get_file_size_mb

def batch_compress_pdfs(input_dir, output_dir=None, target_mb=30):
    """
    Compress all PDF files in a directory

    Args:
        input_dir: Directory containing PDF files to compress
        output_dir: Directory to save compressed PDFs (default: same as input_dir with '_compressed' suffix)
        target_mb: Target file size in MB (default: 30)
    """
    input_path = Path(input_dir)

    if not input_path.exists():
        print(f"Error: Directory '{input_dir}' not found")
        return False

    if not input_path.is_dir():
        print(f"Error: '{input_dir}' is not a directory")
        return False

    # Set output directory
    if output_dir is None:
        output_path = input_path / "compressed"
    else:
        output_path = Path(output_dir)

    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)

    # Find all PDF files
    pdf_files = list(input_path.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in '{input_dir}'")
        return False

    print(f"\n{'='*70}")
    print(f"Batch PDF Compression")
    print(f"{'='*70}")
    print(f"Input directory:  {input_path}")
    print(f"Output directory: {output_path}")
    print(f"Target size:      {target_mb} MB")
    print(f"Files found:      {len(pdf_files)}")
    print(f"{'='*70}\n")

    # Process each PDF
    results = []
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n{'#'*70}")
        print(f"Processing file {i}/{len(pdf_files)}: {pdf_file.name}")
        print(f"{'#'*70}")

        output_file = output_path / pdf_file.name

        try:
            success = compress_pdf_to_target(str(pdf_file), str(output_file), target_mb)
            results.append({
                'file': pdf_file.name,
                'success': success,
                'original_size': get_file_size_mb(pdf_file),
                'final_size': get_file_size_mb(output_file) if output_file.exists() else None
            })
        except Exception as e:
            print(f"Error processing {pdf_file.name}: {e}")
            results.append({
                'file': pdf_file.name,
                'success': False,
                'original_size': get_file_size_mb(pdf_file),
                'final_size': None,
                'error': str(e)
            })

    # Print summary
    print(f"\n\n{'='*70}")
    print(f"BATCH PROCESSING SUMMARY")
    print(f"{'='*70}\n")

    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]

    print(f"Total files:     {len(results)}")
    print(f"Successful:      {len(successful)}")
    print(f"Failed:          {len(failed)}")

    if successful:
        total_original = sum(r['original_size'] for r in successful)
        total_compressed = sum(r['final_size'] for r in successful if r['final_size'])
        total_saved = total_original - total_compressed

        print(f"\nCompression Results:")
        print(f"  Original total:    {total_original:.2f} MB")
        print(f"  Compressed total:  {total_compressed:.2f} MB")
        print(f"  Space saved:       {total_saved:.2f} MB ({(total_saved/total_original)*100:.1f}%)")

        print(f"\nSuccessful files:")
        for r in successful:
            reduction = r['original_size'] - r['final_size'] if r['final_size'] else 0
            print(f"  ✓ {r['file']}")
            print(f"    {r['original_size']:.2f} MB → {r['final_size']:.2f} MB (saved {reduction:.2f} MB)")

    if failed:
        print(f"\nFailed files:")
        for r in failed:
            error_msg = f" - {r.get('error', 'Unknown error')}" if 'error' in r else ""
            print(f"  ✗ {r['file']}{error_msg}")

    print(f"\n{'='*70}")
    print(f"Compressed files saved to: {output_path}")
    print(f"{'='*70}\n")

    return len(failed) == 0

def main():
    if len(sys.argv) < 2:
        print("Usage: python batch-reduce.py <input_directory> [output_directory] [target_mb]")
        print("\nExamples:")
        print("  python batch-reduce.py /path/to/pdfs")
        print("  python batch-reduce.py /path/to/pdfs /path/to/output")
        print("  python batch-reduce.py /path/to/pdfs /path/to/output 25")
        print("\nNotes:")
        print("  - If output_directory is not specified, a 'compressed' subfolder will be created")
        print("  - Default target size is 30 MB")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) >= 3 else None

    # Determine target size
    target_mb = 30
    if len(sys.argv) >= 4:
        try:
            target_mb = float(sys.argv[3])
        except ValueError:
            print(f"Warning: Invalid target size '{sys.argv[3]}', using default 30 MB")

    success = batch_compress_pdfs(input_dir, output_dir, target_mb)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
