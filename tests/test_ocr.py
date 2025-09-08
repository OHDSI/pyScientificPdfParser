# tests/test_ocr.py
from unittest import mock

import pytesseract
from PIL import Image

from pyscientificpdfparser.models import TextBlock
from pyscientificpdfparser.ocr import extract_text_from_page
from pyscientificpdfparser.preprocessing import PreprocessedPage

# This is a sample dictionary that mimics the output of
# pytesseract.image_to_data(..., output_type=pytesseract.Output.DICT)
MOCK_TESSERACT_DATA = {
    "level": [1, 2, 3, 4, 5, 2, 3, 4, 5],
    "page_num": [1, 1, 1, 1, 1, 1, 1, 1, 1],
    "block_num": [1, 1, 1, 1, 1, 2, 2, 2, 2],
    "par_num": [0, 1, 1, 1, 1, 0, 1, 1, 1],
    "line_num": [0, 0, 1, 1, 1, 0, 0, 1, 1],
    "word_num": [0, 0, 1, 2, 3, 0, 0, 1, 2],
    "left": [0, 10, 10, 65, 120, 200, 200, 200, 250],
    "top": [0, 10, 10, 12, 10, 50, 50, 52, 52],
    "width": [150, 140, 50, 50, 20, 100, 100, 45, 45],
    "height": [30, 20, 8, 10, 12, 20, 20, 10, 10],
    "conf": ["-1", "-1", 95, 92, 88, "-1", "-1", 98, 99],
    "text": ["", "", "Hello", "world", "!", "", "", "This", "works."],
}


@mock.patch("pytesseract.image_to_data")
def test_extract_text_from_page_groups_blocks_correctly(
    mock_image_to_data: mock.MagicMock,
) -> None:
    """
    Tests that the OCR module correctly processes Tesseract output.

    Verifies that:
    - Words are correctly grouped into text blocks.
    - Bounding boxes are calculated correctly for each block.
    - Confidence scores are averaged correctly for each block.
    - The final output is a list of valid TextBlock objects.
    """
    # Arrange
    mock_image_to_data.return_value = MOCK_TESSERACT_DATA
    dummy_image = Image.new("L", (300, 100))
    preprocessed_page = PreprocessedPage(
        page_number=1, image=dummy_image, is_scanned=True
    )

    # Act
    text_blocks = extract_text_from_page(preprocessed_page)

    # Assert
    # 1. We should get 2 text blocks from the mock data
    assert len(text_blocks) == 2
    assert all(isinstance(block, TextBlock) for block in text_blocks)

    # 2. Check Block 1
    block1 = text_blocks[0]
    assert block1.text == "Hello world !"
    # BBox: (min_left, min_top, max_right, max_bottom)
    # min_left = 10, min_top = 10
    # max_right = max(10+50, 65+50, 120+20) = max(60, 115, 140) = 140
    # max_bottom = max(10+8, 12+10, 10+12) = max(18, 22, 22) = 22
    assert block1.bbox == (10, 10, 140, 22)
    # Confidence: (95 + 92 + 88) / 3 = 91.666...
    assert block1.confidence is not None
    assert abs(block1.confidence - 91.66) < 0.01
    assert block1.page_number == 1

    # 3. Check Block 2
    block2 = text_blocks[1]
    assert block2.text == "This works."
    # BBox: (min_left, min_top, max_right, max_bottom)
    # min_left = 200, min_top = 52
    # max_right = max(200+45, 250+45) = max(245, 295) = 295
    # max_bottom = max(52+10, 52+10) = 62
    assert block2.bbox == (200, 52, 295, 62)
    # Confidence: (98 + 99) / 2 = 98.5
    assert block2.confidence is not None
    assert abs(block2.confidence - 98.5) < 0.01
    assert block2.page_number == 1

    # 4. Verify that pytesseract was called correctly
    mock_image_to_data.assert_called_once_with(
        dummy_image, lang="eng", config="", output_type=pytesseract.Output.DICT
    )


@mock.patch("pytesseract.image_to_data")
def test_extract_text_handles_tesseract_not_found(
    mock_image_to_data: mock.MagicMock,
) -> None:
    """
    Tests that the OCR function returns an empty list if Tesseract is not found.
    """
    # Arrange
    mock_image_to_data.side_effect = pytesseract.TesseractNotFoundError
    dummy_image = Image.new("L", (100, 100))
    preprocessed_page = PreprocessedPage(
        page_number=1, image=dummy_image, is_scanned=True
    )

    # Act
    text_blocks = extract_text_from_page(preprocessed_page)

    # Assert
    assert text_blocks == []
