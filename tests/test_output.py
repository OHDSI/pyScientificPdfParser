# tests/test_output.py
import json
from pathlib import Path

from PIL import Image

from pyscientificpdfparser.models import (
    Document,
    Figure,
    Section,
    Table,
    TableCell,
    TextBlock,
)
from pyscientificpdfparser.output import write_outputs


def test_write_outputs(tmp_path: Path) -> None:
    """
    Tests that the output module correctly writes all files.

    It uses pytest's tmp_path fixture to create a temporary directory for output.
    """
    # --- Arrange ---
    # 1. Create a mock Document object with various elements
    table = Table(
        bbox=(1, 1, 2, 2),
        page_number=1,
        rows=[[TableCell(text="Some table data", bbox=(1, 1, 2, 2))]],
    )
    figure = Figure(bbox=(10, 10, 100, 100), page_number=1, image_path="")
    doc = Document(
        source_pdf="test.pdf",
        sections=[
            Section(
                title="1. A Section",
                elements=[
                    TextBlock(text="Some text.", bbox=(0, 0, 1, 1), page_number=1),
                    table,
                    figure,
                ],
            )
        ],
    )

    # 2. Create a dummy page image for figure cropping
    dummy_page_image = Image.new("RGB", (500, 500), color="blue")

    # Define the output directory within the temp path
    output_dir = tmp_path / "test_output"

    # --- Act ---
    write_outputs(document=doc, output_dir=output_dir, page_images=[dummy_page_image])

    # --- Assert ---
    # 1. Check if the directory and assets subdirectory were created
    assert output_dir.is_dir()
    assets_dir = output_dir / "assets"
    assert assets_dir.is_dir()

    # 2. Check the JSON output
    json_file = output_dir / "test_output.json"
    assert json_file.is_file()
    with open(json_file, "r") as f:
        data = json.load(f)
    assert data["source_pdf"] == "test.pdf"
    assert len(data["sections"][0]["elements"]) == 3

    # 3. Check the Markdown output
    md_file = output_dir / "test_output.md"
    assert md_file.is_file()
    md_content = md_file.read_text()
    assert "## 1. A Section" in md_content
    assert "Some text." in md_content
    # Check for the table markdown
    # Check for table content, ignoring exact whitespace
    assert "|    Content    |" in md_content
    assert "+---------------+" in md_content
    assert "|Some table data|" in md_content
    # Check for the figure link (element is at index 2, so i+1=3)
    assert "![Figure 3](assets/figure_1_2.png)" in md_content

    # 4. Check that the figure asset was created
    figure_file = assets_dir / "figure_1_2.png"
    assert figure_file.is_file()

    # Optional: Check the size of the cropped figure
    saved_figure = Image.open(figure_file)
    # width = 100-10=90, height = 100-10=90
    assert saved_figure.size == (90, 90)
