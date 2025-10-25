# Study-Tools

A collection of Python utilities and scripts for study and productivity tasks.

## Tools

### PDF Size Reducer

A PDF compression tool that uses `Ghostscript` to reduce PDF file sizes while maintaining acceptable quality. Perfect for compressing large PDFs to meet upload size limits.

**Features:**
- Multiple compression quality levels (screen, ebook, printer, prepress)
- Automatic compression strategy selection to meet target file size
- Batch processing support for multiple PDFs
- Progress tracking and detailed statistics
- Preserves PDF quality while reducing file size

**Scripts:**
- `pdf_reducer.py` - Single PDF compression with customizable quality settings
- `batch-reduce.py` - Batch process multiple PDFs in a directory

## Installation

### Prerequisites

This project requires Python 3.6+ and Ghostscript.

**Install Ghostscript:**

macOS:
```bash
brew install ghostscript
```

Linux (Ubuntu/Debian):
```bash
sudo apt-get install ghostscript
```

Linux (Fedora/RHEL):
```bash
sudo dnf install ghostscript
```

Windows:
Download and install from [Ghostscript official website](https://www.ghostscript.com/download/gsdnload.html)

### Clone the Repository

```bash
git clone https://github.com/Yen-Coder/Study-Tools
cd Study-Tools
```

## Usage

### PDF Size Reducer

**Single PDF Compression:**

```bash
cd pdf-size-reducer
python3 pdf_reducer.py input.pdf output.pdf --target 30
```

Options:
- `--target`: Target file size in MB (default: 30)
- `--quality`: Initial quality level (screen/ebook/printer/prepress)

**Batch PDF Compression:**

```bash
cd pdf-size-reducer
python3 batch-reduce.py /path/to/pdf/folder --target 30
```

Options:
- `--output`: Output directory for compressed PDFs (default: input_dir/compressed)
- `--target`: Target file size in MB (default: 30)

**Examples:**

Compress a single PDF to under 30 MB:
```bash
python3 pdf_reducer.py large_document.pdf compressed_document.pdf
```

Compress all PDFs in a directory:
```bash
python3 batch-reduce.py ~/Documents/PDFs --output ~/Documents/Compressed_PDFs --target 25
```

## Project Structure

```
Study-Tools/
├── pdf-size-reducer/
│   ├── pdf_reducer.py      # Single PDF compression script
│   └── batch-reduce.py     # Batch PDF compression script
├── .gitignore
├── .gitattributes
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Future Tools

This repository is designed to grow with additional study and productivity tools. Stay tuned for more utilities!

