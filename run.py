import argparse
import os
import pathlib

from pyscientificpdfparser.core import parse_pdf


def main(
    pdf_dir: pathlib.Path, output_dir: pathlib.Path, llm_refine: bool = False
) -> None:
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Input folder: {pdf_dir}")
    print(f"Output folder: {output_dir}")
    print(os.getcwd())

    # Loop over all PDFs
    for pdf_file in pdf_dir.glob("*.pdf"):
        print(f"Processing {pdf_file.name}...")

        parse_pdf(
            pdf_path=pdf_file,
            output_dir=output_dir,
            llm_refine=llm_refine,
        )

        print(f"✅ Done with {pdf_file.name}")
        print(f"   Markdown and assets saved to: {output_dir}")

    print("All PDFs processed successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Batch process PDFs with pyScientificPdfParser."
    )
    parser.add_argument(
        "--input",
        type=pathlib.Path,
        default=pathlib.Path("pdfs"),
        help="Directory containing PDF files (default: ./pdfs)",
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=pathlib.Path("results"),
        help="Directory where results will be stored (default: ./results)",
    )
    parser.add_argument(
        "--llm",
        action="store_true",
        help="Enable LLM refinement (default: disabled)",
    )

    args = parser.parse_args()
    main(args.input, args.output, args.llm)
