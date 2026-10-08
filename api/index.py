"""
Thin web wrapper so the existing pipeline can run on Vercel.
Upload a PDF -> runs llm.py + render.py unchanged -> returns the .xlsx.
"""

import sys
import tempfile
from io import BytesIO
from pathlib import Path

from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import Response
from pypdf import PdfReader

# Let this file import the project files that sit one folder up.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from llm import InstrumentLayer, analyze_document
from render import render_to_workbook
from config import (
    ANTHROPIC_API_KEY,
    CLAUDE_MODEL,
    CLAUDE_EFFORT,
    MAX_TOKENS_PER_REQUEST,
    ANNOTATION_TEMPLATE_FILE,
    EXTRACTION_RULES_PATH,
)

app = FastAPI()


@app.post("/api/annotate")
async def annotate(
    file: UploadFile,
    label: str = Form("Trust document"),
    status: str = Form("OPERATIVE"),
):
    pdf = PdfReader(BytesIO(await file.read()))
    text = "\n\n".join(page.extract_text() or "" for page in pdf.pages)

    doc_name = Path(file.filename).stem
    annotation = analyze_document(
        doc_name,
        [InstrumentLayer(label=label, status=status, text=text)],
        api_key=ANTHROPIC_API_KEY,
        model=CLAUDE_MODEL,
        effort=CLAUDE_EFFORT,
        max_tokens=MAX_TOKENS_PER_REQUEST,
        rules_path=EXTRACTION_RULES_PATH,
    )

    out_path = Path(tempfile.gettempdir()) / f"{doc_name}_annotation.xlsx"
    render_to_workbook(annotation, str(ANNOTATION_TEMPLATE_FILE), str(out_path))

    return Response(
        content=out_path.read_bytes(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{out_path.name}"'},
    )
