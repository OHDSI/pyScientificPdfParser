# How to Use pyScientificPdfParser

This guide provides a detailed walkthrough of how to install, set up, and use the `pyScientificPdfParser` package to process scientific PDF documents.

## 1. Installation

### Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies.

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate
```

### Installing the Package

The package is available on PyPI and can be installed with pip. It offers different installation options depending on your needs.

#### A) Standard Installation
This installs the core package with basic functionality.

```bash
pip install pyscientificpdfparser
```

#### B) Installation with Machine Learning Extras
This is the **recommended** option for most users. It includes the necessary libraries for Document Layout Analysis (DLA) and Table Structure Recognition (TSR).

```bash
pip install pyscientificpdfparser[ml]
```

#### C) Full Installation with LLM Refinement
This option includes all dependencies, including those for the optional LLM-based refinement features.

```bash
pip install pyscientificpdfparser[ml,llm]
```

### System Dependencies
This package relies on Tesseract for Optical Character Recognition (OCR). You must install it on your system.

- **On Debian/Ubuntu:**
  ```bash
  sudo apt-get install tesseract-ocr
  ```
- **On macOS (using Homebrew):**
  ```bash

  brew install tesseract
  ```
- **On Windows:**
  Download and run the installer from the [official Tesseract documentation](https://tesseract-ocr.github.io/tessdoc/Installation.html).

## 2. Setup: Automatic Model Downloading

The machine learning models for layout analysis and table recognition are downloaded automatically from the Hugging Face Hub the first time you run the parser.

When you execute a script or the CLI for the first time, you will see progress bars for the model downloads. This is a one-time setup process. Please ensure you have a stable internet connection.

## 3. Usage: Command-Line Interface (CLI)

The CLI provides a straightforward way to process PDFs directly from your terminal. The main command is `scipdfparser process`.

### A) Processing a Single PDF

To parse a single PDF file, provide the path to the file. The output will be saved in a directory named `parsed_output` by default.

```bash
# Basic usage
scipdfparser process path/to/your/document.pdf

# Specify a different output directory
scipdfparser process path/to/your/document.pdf -o path/to/custom/output
```

### B) Processing Multiple PDFs

The CLI is designed to process one file at a time. To process a directory of PDFs, you can use a simple shell loop.

This example processes every `.pdf` file in the `my_papers/` directory and saves the results into a corresponding subdirectory inside `all_outputs/`.

```bash
# Create the main output directory
mkdir -p all_outputs

# Loop through all PDF files in the 'my_papers' directory
for pdf_file in my_papers/*.pdf; do
  # Get the base name of the file (e.g., "document.pdf" -> "document")
  base_name=$(basename "$pdf_file" .pdf)

  echo "Processing $pdf_file..."

  # Run the parser, creating a unique output directory for each PDF
  scipdfparser process "$pdf_file" -o "all_outputs/$base_name"
done

echo "All PDFs processed."
```

## 4. Usage: Python API

For more advanced use cases, such as integrating the parser into a larger data processing pipeline, you can use the Python API. The main entry point is the `parse_pdf` function.

### A) Processing a Single PDF

This example shows how to run the parser on a single file and save the output to a directory, similar to the CLI.

```python
import pathlib
from pyscientificpdfparser.core import parse_pdf

# Define the path to your PDF and the desired output directory
pdf_path = pathlib.Path("path/to/your/document.pdf")
output_dir = pathlib.Path("path/to/output")

# Create the output directory if it doesn't exist
output_dir.mkdir(parents=True, exist_ok=True)

print(f"Processing {pdf_path.name}...")

# Call the parser
# The 'document' object contains all the parsed data.
document = parse_pdf(
    pdf_path=pdf_path,
    output_dir=output_dir,
    llm_refine=False,  # Optional: set to True to enable LLM refinement
)

print("Done.")
print(f"Markdown and assets saved to: {output_dir}")
```

### B) Processing Multiple PDFs in Memory

A key advantage of the API is the ability to process documents in memory without writing files to disk. The `parse_pdf` function returns a `Document` object (defined in `pyscientificpdfparser.models`) which you can work with directly.

This example processes multiple PDFs and collects specific information (like the title and number of tables) from each.

```python
import pathlib
from pyscientificpdfparser.core import parse_pdf
from pyscientificpdfparser.models import Table

# Assume we have a list of PDF files
pdf_files = list(pathlib.Path("my_papers/").glob("*.pdf"))

# Store the results
parsed_data = []

for pdf_path in pdf_files:
    print(f"Processing {pdf_path.name}...")

    # Run the parser but omit the output_dir to prevent writing files
    document = parse_pdf(pdf_path=pdf_path)

    # Example: Extract the document title (assuming it's the first text block)
    try:
        title = document.sections[0].elements[0].text
    except IndexError:
        title = "Title not found"

    # Example: Count the number of tables found
    table_count = sum(1 for section in document.sections for element in section.elements if isinstance(element, Table))

    parsed_data.append({
        "filename": pdf_path.name,
        "title": title.strip(),
        "table_count": table_count,
    })

    print(f"  -> Title: {title.strip()}")
    print(f"  -> Tables found: {table_count}")


# Now you have a list of structured data you can use for further analysis
print("\n--- Summary ---")
for item in parsed_data:
    print(f"{item['filename']}: {item['table_count']} tables")

```

## 5. Understanding the Output

When you specify an `output_dir`, the parser creates a set of files designed to give you a comprehensive, structured representation of the PDF.

For a given input PDF, `my_document.pdf`, the output directory will look like this:

```
output_directory/
├── assets/
│   ├── figure_1.png
│   ├── figure_2.png
│   └── table_1.png
├── output.md
└── structured_output.json
```

### A) Main Markdown File (`output.md`)

This file contains the full content of the PDF, converted to GitHub Flavored Markdown. It is designed for human readability.

- **Text Flow:** The text is de-columnized and ordered logically.
- **Headings:** Document headings are converted to Markdown headings (`#`, `##`, etc.).
- **Tables:** Tables are rendered as Markdown tables.
- **Images:** Figures and images of tables are embedded in the document, pointing to the local files in the `assets` directory.

**Example Snippet from `output.md`:**

```markdown
# 1. Introduction

This is the introductory text of the paper. It flows cleanly, even if the original PDF had multiple columns.

## 1.1. Previous Work

This subsection discusses prior research in the field.

![Figure 1: A diagram showing the model architecture.](assets/figure_1.png)

| Header 1 | Header 2 |
|----------|----------|
| Data A   | Data B   |
| Data C   | Data D   |

*Table 1: Results from the primary experiment.*
```

### B) Structured JSON (`structured_output.json`)

This file provides a machine-readable representation of the document. It contains a nested structure of sections, elements, and their properties, including bounding box coordinates for every element. This is ideal for programmatic access to the document's contents.

**Example Snippet from `structured_output.json`:**

```json
{
  "source_pdf": "path/to/your/document.pdf",
  "sections": [
    {
      "id": "sec_1",
      "title": "1. Introduction",
      "elements": [
        {
          "type": "Text",
          "text": "This is the introductory text...",
          "bbox": [100.5, 200.0, 500.2, 350.8],
          "page_number": 1
        },
        {
          "type": "Figure",
          "caption": "A diagram showing the model architecture.",
          "asset_path": "assets/figure_1.png",
          "bbox": [150.0, 400.0, 450.0, 600.0],
          "page_number": 1
        },
        {
          "type": "Table",
          "caption": "Results from the primary experiment.",
          "asset_path": "assets/table_1.png",
          "bbox": [100.0, 650.0, 500.0, 750.0],
          "page_number": 1,
          "cells_as_text": [
            ["Header 1", "Header 2"],
            ["Data A", "Data B"],
            ["Data C", "Data D"]
          ]
        }
      ]
    }
  ]
}
```

### C) Assets Directory (`assets/`)

This folder contains all the visual elements extracted from the PDF, saved as PNG images.
- Each figure is saved as a separate file (e.g., `figure_1.png`).
- Each table is also saved as an image for visual inspection (e.g., `table_1.png`).
