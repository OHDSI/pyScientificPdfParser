# tests/test_dla.py
from unittest import mock

import pytest
import torch
from PIL import Image

from pyscientificpdfparser.dla import LayoutAnalyzer
from pyscientificpdfparser.models import Table, TextBlock


def create_mock_model_output() -> dict[str, torch.Tensor]:
    """Creates a mock output similar to what LayoutLMv3ForObjectDetection produces."""
    # Mock two predicted boxes and their classes
    # Mock logits for 2 boxes, with 5 possible classes each
    logits = torch.tensor(
        [
            [0.1, 0.9, 0.0, 0.0, 0.0],  # Prediction for box 1 -> Class 1 ("text")
            [0.0, 0.0, 0.9, 0.1, 0.0],  # Prediction for box 2 -> Class 2 ("table")
        ]
    )
    # Mock two corresponding bounding boxes (normalized)
    pred_boxes = torch.tensor(
        [
            [0.1, 0.1, 0.8, 0.4],  # Box for the text block
            [0.1, 0.5, 0.8, 0.9],  # Box for the table
        ]
    )
    return {"logits": logits, "pred_boxes": pred_boxes}


@mock.patch("pyscientificpdfparser.dla.AutoModelForObjectDetection")
@mock.patch("pyscientificpdfparser.dla.AutoProcessor")
def test_layout_analyzer(
    mock_processor_cls: mock.MagicMock, mock_model_cls: mock.MagicMock
) -> None:
    """
    Tests the LayoutAnalyzer class.

    Verifies that:
    - It correctly processes mock model output.
    - It associates OCR text with the correct layout blocks.
    - It sorts the final elements by reading order.
    """
    # --- Arrange ---
    # 1. Mock the Hugging Face classes and their instances
    mock_processor_instance = mock.MagicMock()
    mock_model_instance = mock.MagicMock()

    # Configure the class constructors to return our instances
    mock_processor_cls.from_pretrained.return_value = mock_processor_instance
    mock_model_cls.from_pretrained.return_value = mock_model_instance

    # 2. Configure the model's output and id2label mapping
    mock_model_instance.return_value = create_mock_model_output()
    mock_model_instance.config.id2label = {0: "title", 1: "text", 2: "table"}

    # 3. Prepare dummy input data
    dummy_image = Image.new("RGB", (1000, 1500))
    # OCR block that should be inside the DLA text block
    ocr_block1 = TextBlock(
        text="This is some text.", bbox=(150, 160, 300, 180), page_number=1
    )
    # OCR block that is outside any important DLA block
    ocr_block2 = TextBlock(
        text="This is other text.", bbox=(50, 50, 100, 70), page_number=1
    )
    mock_ocr_blocks = [ocr_block1, ocr_block2]

    # --- Act ---
    # Initialize the analyzer (this will use our mocks)
    analyzer = LayoutAnalyzer()
    # Run the analysis
    layout_elements = analyzer.analyze_page(
        image=dummy_image, page_number=1, ocr_blocks=mock_ocr_blocks
    )

    # --- Assert ---
    # 1. Check the number of elements returned
    # We expect one TextBlock (from label 1) and one Table (from label 2)
    assert len(layout_elements) == 2

    # 2. Check the returned elements' types and order
    # The TextBlock should be first because its bbox is higher up the page
    assert isinstance(layout_elements[0], TextBlock)
    assert isinstance(layout_elements[1], Table)

    # 3. Check the content of the TextBlock
    final_text_block = layout_elements[0]
    assert isinstance(final_text_block, TextBlock)
    # It should have associated the text from ocr_block1
    assert final_text_block.text == "This is some text."
    # Its bbox should be the denormalized one from the model output
    # bbox = (0.1*1000, 0.1*1500, 0.8*1000, 0.4*1500) -> (100, 150, 800, 600)
    assert final_text_block.bbox == pytest.approx((100.0, 150.0, 800.0, 600.0))

    # 4. Check the Table element
    final_table = layout_elements[1]
    assert isinstance(final_table, Table)
    # bbox = (0.1*1000, 0.5*1500, 0.8*1000, 0.9*1500) -> (100, 750, 800, 1350)
    assert final_table.bbox == pytest.approx((100.0, 750.0, 800.0, 1350.0))


@mock.patch("pyscientificpdfparser.dla.AutoProcessor.from_pretrained")
def test_layout_analyzer_handles_model_loading_error(
    mock_from_pretrained: mock.MagicMock,
) -> None:
    """
    Tests that the LayoutAnalyzer gracefully handles an OSError during init.
    """
    # Arrange: Make the model loading raise an error
    mock_from_pretrained.side_effect = OSError("Model not found")

    # Act: Initialize the analyzer
    analyzer = LayoutAnalyzer()

    # Assert: The internal model and processor should be None
    assert analyzer.model is None
    assert analyzer.processor is None

    # Further Act: Check if analyze_page falls back gracefully
    layout_elements = analyzer.analyze_page(
        image=Image.new("RGB", (100, 100)),
        page_number=1,
        ocr_blocks=[TextBlock(text="test", bbox=(0, 0, 1, 1), page_number=1)],
    )
    # Assert: It should return the raw OCR blocks as a fallback
    assert len(layout_elements) == 1
    element = layout_elements[0]
    assert isinstance(element, TextBlock)
    assert element.text == "test"
