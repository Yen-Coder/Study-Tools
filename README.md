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
1. Download the Windows installer from [Ghostscript official website](https://www.ghostscript.com/download/gsdnload.html)
2. Run the installer and follow the installation wizard
3. Make sure to check "Add to PATH" during installation
4. Verify installation by opening Command Prompt and running:
   ```cmd
   gswin64c -version
   ```
   or
   ```cmd
   gswin32c -version
   ```

**Note for Windows users:** If Ghostscript is not in your PATH, you may need to add it manually:
- Default installation path: `C:\Program Files\gs\gs[version]\bin`
- Add this path to your System Environment Variables

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

Linux/macOS:
```bash
python3 pdf_reducer.py large_document.pdf compressed_document.pdf
```

Windows (Command Prompt):
```cmd
python pdf_reducer.py large_document.pdf compressed_document.pdf
```

Windows (PowerShell):
```powershell
python pdf_reducer.py large_document.pdf compressed_document.pdf
```

Compress all PDFs in a directory:

Linux/macOS:
```bash
python3 batch-reduce.py ~/Documents/PDFs --output ~/Documents/Compressed_PDFs --target 25
```

Windows (Command Prompt):
```cmd
python batch-reduce.py C:\Users\YourName\Documents\PDFs --output C:\Users\YourName\Documents\Compressed_PDFs --target 25
```

Windows (PowerShell):
```powershell
python batch-reduce.py C:\Users\$env:USERNAME\Documents\PDFs --output C:\Users\$env:USERNAME\Documents\Compressed_PDFs --target 25
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

