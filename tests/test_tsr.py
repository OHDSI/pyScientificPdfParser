# tests/test_tsr.py
from unittest import mock

from PIL import Image

from pyscientificpdfparser.models import Table, TextBlock
from pyscientificpdfparser.tsr import TableRecognizer


@mock.patch("pyscientificpdfparser.tsr.AutoModelForObjectDetection")
@mock.patch("pyscientificpdfparser.tsr.AutoProcessor")
def test_table_recognizer_placeholder_logic(
    mock_processor_cls: mock.MagicMock, mock_model_cls: mock.MagicMock
) -> None:
    """
    Tests the placeholder logic in the TableRecognizer.

    Verifies that it correctly aggregates all text within the table's
    bounding box into a single cell.
    """
    # --- Arrange ---
    # 1. Mocks for the Hugging Face classes
    mock_processor_instance = mock.MagicMock()
    mock_model_instance = mock.MagicMock()
    mock_processor_cls.from_pretrained.return_value = mock_processor_instance
    mock_model_cls.from_pretrained.return_value = mock_model_instance
    # The model's output is not used by the placeholder logic, so it's simple
    mock_model_instance.return_value = {}

    # 2. Dummy input data
    dummy_image = Image.new("RGB", (500, 500))
    # A table element as identified by a hypothetical DLA step
    table_from_dla = Table(bbox=(100, 100, 400, 400), page_number=1, rows=[])
    # OCR blocks: one inside the table, one outside
    ocr_block_inside = TextBlock(
        text="Cell 1 content.", bbox=(150, 150, 200, 170), page_number=1
    )
    ocr_block_also_inside = TextBlock(
        text="Cell 2 content.", bbox=(300, 300, 350, 320), page_number=1
    )
    ocr_block_outside = TextBlock(
        text="This is page text.", bbox=(50, 50, 80, 70), page_number=1
    )
    mock_ocr_blocks = [ocr_block_inside, ocr_block_also_inside, ocr_block_outside]

    # --- Act ---
    recognizer = TableRecognizer()
    populated_table = recognizer.recognize_table(
        table_image=dummy_image,
        table_element=table_from_dla,
        ocr_blocks=mock_ocr_blocks,
    )

    # --- Assert ---
    # 1. Check that the table has one row and one cell
    assert len(populated_table.rows) == 1
    assert len(populated_table.rows[0]) == 1

    # 2. Check the content of the single cell
    final_cell = populated_table.rows[0][0]
    expected_text = "Cell 1 content. Cell 2 content."
    assert final_cell.text == expected_text

    # 3. Check that the cell's bbox is the same as the original table's bbox
    assert final_cell.bbox == table_from_dla.bbox


@mock.patch("pyscientificpdfparser.tsr.AutoProcessor.from_pretrained")
def test_table_recognizer_handles_model_loading_error(
    mock_from_pretrained: mock.MagicMock,
) -> None:
    """
    Tests that the TableRecognizer gracefully handles an OSError during init.
    """
    # Arrange
    mock_from_pretrained.side_effect = OSError("Model not found")
    table_from_dla = Table(bbox=(100, 100, 400, 400), page_number=1, rows=[])

    # Act
    recognizer = TableRecognizer()
    populated_table = recognizer.recognize_table(
        table_image=Image.new("RGB", (100, 100)),
        table_element=table_from_dla,
        ocr_blocks=[],
    )

    # Assert
    assert recognizer.model is None
    assert recognizer.processor is None
    # It should return the original, unmodified table element
    assert populated_table == table_from_dla
