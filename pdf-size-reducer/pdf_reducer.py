#!/usr/bin/env python3
"""
PDF Compression Script - Target: Under 30 MB
Applies multiple compression strategies to reduce PDF file size
"""

import os
import sys
import subprocess
from pathlib import Path

def get_file_size_mb(filepath):
    """Get file size in MB"""
    size_bytes = os.path.getsize(filepath)
    size_mb = size_bytes / (1024 * 1024)
    return size_mb

def compress_with_ghostscript(input_path, output_path, quality='ebook'):
    """
    Compress PDF using Ghostscript
    Quality options: screen (72dpi), ebook (150dpi), printer (300dpi), prepress (300+dpi)
    """
    quality_settings = {
        'screen': '/screen',      # Lowest quality, smallest size (72 DPI)
        'ebook': '/ebook',        # Medium quality (150 DPI)
        'printer': '/printer',    # High quality (300 DPI)
        'prepress': '/prepress'   # Highest quality (300+ DPI)
    }
    
    setting = quality_settings.get(quality, '/ebook')
    
    cmd = [
        'gs',
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.4',
        f'-dPDFSETTINGS={setting}',
        '-dNOPAUSE',
        '-dQUIET',
        '-dBATCH',
        '-dCompressFonts=true',
        '-dDetectDuplicateImages=true',
        '-dDownsampleColorImages=true',
        '-dDownsampleGrayImages=true',
        '-dDownsampleMonoImages=true',
        f'-sOutputFile={output_path}',
        input_path
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Ghostscript error: {e.stderr.decode()}")
        return False
    except FileNotFoundError:
        print("Ghostscript not found. Installing...")
        subprocess.run(['apt-get', 'update'], capture_output=True)
        subprocess.run(['apt-get', 'install', '-y', 'ghostscript'], capture_output=True)
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except:
            return False

def compress_with_qpdf(input_path, output_path):
    """Compress PDF using qpdf with maximum optimization"""
    cmd = [
        'qpdf',
        '--compress-streams=y',
        '--object-streams=generate',
        '--optimize-images',
        '--remove-unreferenced-resources=yes',
        input_path,
        output_path
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        print("qpdf not found. Installing...")
        subprocess.run(['apt-get', 'update'], capture_output=True)
        subprocess.run(['apt-get', 'install', '-y', 'qpdf'], capture_output=True)
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except:
            return False

def compress_pdf_to_target(input_path, output_path, target_mb=30):
    """
    Compress PDF to under target size using progressive strategies
    """
    input_path = Path(input_path)
    output_path = Path(output_path)
    
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' not found")
        return False
    
    original_size = get_file_size_mb(input_path)
    print(f"\n{'='*60}")
    print(f"Original file: {input_path.name}")
    print(f"Original size: {original_size:.2f} MB")
    print(f"Target size: Under {target_mb} MB")
    print(f"{'='*60}\n")
    
    if original_size <= target_mb:
        print(f"✓ File is already under {target_mb} MB. No compression needed.")
        # Still copy to output location
        import shutil
        shutil.copy(input_path, output_path)
        return True
    
    # Strategy 1: Try qpdf first (fast, lossless)
    print("Strategy 1: Trying qpdf optimization (lossless)...")
    temp_output = output_path.parent / f"temp_qpdf_{output_path.name}"
    
    if compress_with_qpdf(str(input_path), str(temp_output)):
        size_after = get_file_size_mb(temp_output)
        print(f"  → Size after qpdf: {size_after:.2f} MB (reduced by {original_size - size_after:.2f} MB)")
        
        if size_after <= target_mb:
            temp_output.rename(output_path)
            print(f"\n✓ SUCCESS! File compressed to {size_after:.2f} MB")
            print(f"  Compression ratio: {(1 - size_after/original_size)*100:.1f}%")
            return True
        else:
            # Use qpdf output as input for next strategy
            input_path = temp_output
            original_size = size_after
    
    # Strategy 2: Ghostscript with ebook quality
    print("\nStrategy 2: Trying Ghostscript with 'ebook' quality (150 DPI)...")
    temp_output2 = output_path.parent / f"temp_ebook_{output_path.name}"
    
    if compress_with_ghostscript(str(input_path), str(temp_output2), 'ebook'):
        size_after = get_file_size_mb(temp_output2)
        print(f"  → Size after ebook compression: {size_after:.2f} MB")
        
        if size_after <= target_mb:
            temp_output2.rename(output_path)
            # Clean up temp files
            if temp_output.exists():
                temp_output.unlink()
            print(f"\n✓ SUCCESS! File compressed to {size_after:.2f} MB")
            print(f"  Compression ratio: {(1 - size_after/get_file_size_mb(sys.argv[1]))*100:.1f}%")
            return True
        else:
            input_path = temp_output2
            original_size = size_after
    
    # Strategy 3: Ghostscript with screen quality (aggressive)
    print("\nStrategy 3: Trying Ghostscript with 'screen' quality (72 DPI - aggressive)...")
    
    if compress_with_ghostscript(str(input_path), str(output_path), 'screen'):
        size_after = get_file_size_mb(output_path)
        print(f"  → Size after screen compression: {size_after:.2f} MB")
        
        # Clean up temp files
        if temp_output.exists():
            temp_output.unlink()
        if temp_output2.exists():
            temp_output2.unlink()
        
        if size_after <= target_mb:
            print(f"\n✓ SUCCESS! File compressed to {size_after:.2f} MB")
            print(f"  Compression ratio: {(1 - size_after/get_file_size_mb(sys.argv[1]))*100:.1f}%")
            print(f"\n  Note: 'screen' quality was used - image quality may be reduced")
            return True
        else:
            print(f"\n⚠ WARNING: Could not compress below {target_mb} MB")
            print(f"  Final size: {size_after:.2f} MB")
            print(f"  You may need to:")
            print(f"    - Remove pages")
            print(f"    - Extract and compress images separately")
            print(f"    - Split the PDF into multiple files")
            return False
    
    # Clean up temp files
    if temp_output.exists():
        temp_output.unlink()
    if temp_output2.exists():
        temp_output2.unlink()
    
    print("\n✗ FAILED: Could not compress the file")
    return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python compress_pdf_to_30mb.py <input.pdf> [output.pdf] [target_mb]")
        print("\nExample:")
        print("  python compress_pdf_to_30mb.py large_file.pdf")
        print("  python compress_pdf_to_30mb.py large_file.pdf compressed.pdf")
        print("  python compress_pdf_to_30mb.py large_file.pdf compressed.pdf 25")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Determine output filename
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        input_path = Path(input_file)
        output_file = input_path.parent / f"compressed_{input_path.name}"
    
    # Determine target size
    target_mb = 30
    if len(sys.argv) >= 4:
        try:
            target_mb = float(sys.argv[3])
        except ValueError:
            print(f"Warning: Invalid target size '{sys.argv[3]}', using default 30 MB")
    
    success = compress_pdf_to_target(input_file, output_file, target_mb)
    
    if success:
        print(f"\n✓ Compressed file saved to: {output_file}")
    else:
        print(f"\n✗ Compression failed or target not reached")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()