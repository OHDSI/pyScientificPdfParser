# tests/test_sectioning.py
from pyscientificpdfparser.models import TextBlock
from pyscientificpdfparser.sectioning import segment_into_sections


def test_segment_into_sections() -> None:
    """
    Tests that the sectioning logic correctly groups elements.
    """
    # Arrange: Create a list of mock layout elements
    elements = [
        TextBlock(text="Document Title", bbox=(0, 0, 1, 1), page_number=1),
        TextBlock(text="1. Introduction", bbox=(0, 0, 1, 1), page_number=1),
        TextBlock(text="This is the intro.", bbox=(0, 0, 1, 1), page_number=1),
        TextBlock(text="2. Methods", bbox=(0, 0, 1, 1), page_number=2),
        TextBlock(text="We did things.", bbox=(0, 0, 1, 1), page_number=2),
    ]

    # Act
    sections = segment_into_sections(elements)  # type: ignore

    # Assert
    # 1. We should get 3 sections: Header, Introduction, Methods
    assert len(sections) == 3

    # 2. Check Section 1 (Header)
    assert sections[0].title == "Header"
    assert len(sections[0].elements) == 1
    element = sections[0].elements[0]
    assert isinstance(element, TextBlock)
    assert element.text == "Document Title"

    # 3. Check Section 2 (Introduction)
    assert sections[1].title == "1. Introduction"
    assert len(sections[1].elements) == 2
    element = sections[1].elements[0]
    assert isinstance(element, TextBlock)
    assert element.text == "1. Introduction"
    element = sections[1].elements[1]
    assert isinstance(element, TextBlock)
    assert element.text == "This is the intro."

    # 4. Check Section 3 (Methods)
    assert sections[2].title == "2. Methods"
    assert len(sections[2].elements) == 2
    element = sections[2].elements[0]
    assert isinstance(element, TextBlock)
    assert element.text == "2. Methods"
    element = sections[2].elements[1]
    assert isinstance(element, TextBlock)
    assert element.text == "We did things."


def test_segment_no_headers() -> None:
    """Tests segmentation when no headers are found."""
    elements = [
        TextBlock(text="Just some text.", bbox=(0, 0, 1, 1), page_number=1),
        TextBlock(text="More text.", bbox=(0, 0, 1, 1), page_number=1),
    ]
    sections = segment_into_sections(elements)  # type: ignore
    assert len(sections) == 1
    assert sections[0].title == "Content"
    assert len(sections[0].elements) == 2
