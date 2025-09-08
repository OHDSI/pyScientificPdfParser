# src/pyscientificpdfparser/models.py
from __future__ import annotations

from typing import Any, Literal, TypeAlias, Union

from pydantic import BaseModel, Field

# Type alias for a bounding box: [x1, y1, x2, y2]
BoundingBox: TypeAlias = tuple[float, float, float, float]


class BaseElement(BaseModel):
    """Base model for any identifiable element on a page."""

    bbox: BoundingBox = Field(..., description="The bounding box of the element.")
    page_number: int = Field(
        ..., description="The page number where the element is located."
    )
    element_type: str


class TextBlock(BaseElement):
    """A block of text."""

    element_type: Literal["TextBlock"] = "TextBlock"
    text: str = Field(..., description="The string content of the text block.")
    confidence: float | None = Field(
        None, description="The OCR confidence score for the text block."
    )


class TableCell(BaseModel):
    """A single cell within a table."""

    text: str
    bbox: BoundingBox
    row_span: int = 1
    col_span: int = 1
    is_header: bool = False


class Table(BaseElement):
    """A structured table with rows, columns, and cells."""

    element_type: Literal["Table"] = "Table"
    caption: str | None = Field(
        None, description="The caption associated with the table."
    )
    rows: list[list[TableCell]] = Field(
        ..., description="A list of rows, where each row is a list of cells."
    )
    footer: str | None = Field(
        None, description="Footer text associated with the table."
    )


class Figure(BaseElement):
    """A figure or image, with a link to the saved asset."""

    element_type: Literal["Figure"] = "Figure"
    caption: str | None = Field(
        None, description="The caption associated with the figure."
    )
    image_path: str = Field(
        ..., description="The file path to the extracted image asset."
    )


# A Union of all possible content elements that can appear in a section
ContentElement: TypeAlias = Union[TextBlock, Table, Figure]


class Section(BaseModel):
    """A logical section of the document (e.g., Abstract, Introduction)."""

    title: str | None = Field(
        None, description="The title of the section (e.g., '1. Introduction')."
    )
    level: int = Field(
        0, description="The hierarchical level of the section (0 for top-level)."
    )
    elements: list[ContentElement] = Field(
        ..., description="A list of content elements within this section."
    )


class Document(BaseModel):
    """The root model representing the entire parsed PDF document."""

    source_pdf: str = Field(
        ..., description="The file path or identifier of the source PDF."
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Metadata extracted from the PDF."
    )
    sections: list[Section] = Field(
        ..., description="A list of logical sections comprising the document."
    )
    references: list[str] = Field(
        default_factory=list,
        description="A list of raw reference strings, if found.",
    )
    structured_references: str | None = Field(
        None, description="Structured references, if parsed by LLM."
    )
    extracted_entities: str | None = Field(
        None, description="A dictionary of entities extracted by LLM."
    )
    llm_processing_log: list[str] = Field(
        default_factory=list,
        description="A log of any LLM refinement steps applied.",
    )

    def to_json(self, **kwargs: Any) -> str:
        """Serializes the document model to a JSON string."""
        return self.model_dump_json(indent=2, **kwargs)

    def to_markdown(self) -> str:
        """Converts the document to a Markdown string (placeholder)."""
        # This will be implemented in the output module.
        raise NotImplementedError("Markdown conversion is not yet implemented.")
