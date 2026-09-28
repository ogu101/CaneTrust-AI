"""
Usage:
    python main.py

All inputs come from config.py (document name, single instrument layer,
template, output directory, and the API/model settings). No command-line
arguments are read anymore — edit config.py (or your .env) to change a run.
"""

from pathlib import Path

from llm import InstrumentLayer, analyze_document
from render import render_to_workbook

from config import (
    ANTHROPIC_API_KEY,
    CLAUDE_MODEL,
    CLAUDE_EFFORT,
    MAX_TOKENS_PER_REQUEST,
    RESOURCES_FILE,
    ANNOTATION_TEMPLATE_FILE,
    OUTPUT_DIR,
    DOC_NAME,
    LAYER_LABEL,
    LAYER_STATUS,
    EXTRACTION_RULES_PATH,
)


def main():
    layer = InstrumentLayer(
        label=LAYER_LABEL,
        status=LAYER_STATUS,
        text=Path(RESOURCES_FILE).read_text(),
    )

    annotation = analyze_document(
        DOC_NAME,
        [layer],
        api_key=ANTHROPIC_API_KEY,
        model=CLAUDE_MODEL,
        effort=CLAUDE_EFFORT,
        max_tokens=MAX_TOKENS_PER_REQUEST,
        rules_path=EXTRACTION_RULES_PATH,
    )

    out_path = Path(OUTPUT_DIR) / f"{DOC_NAME}_annotation.xlsx"
    render_to_workbook(annotation, ANNOTATION_TEMPLATE_FILE, str(out_path))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()