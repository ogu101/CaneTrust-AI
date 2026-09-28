# CaneTrust AI — MiLA Gift Annotation Pipeline

Turns a trust/amendment document into a filled `MiLA_Annotation_Template_v0.xlsx`
for the Office of Estate and Gift Planning, ready for attorney review.

## Architecture

```
config.py (all settings) ──► main.py (orchestrator)
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                             ▼
     llm.py: analyze_document()          render.py: render_to_workbook()
     (one Claude API call, forced        (no LLM — openpyxl writes into
      tool use, returns structured        the template, inserting rows
      JSON)                               if needed)
                    │                             ▲
                    ▼                             │
     schema.py: DocumentAnnotation ───────────────┘
     (Pydantic model — validates the
      LLM's output)
```

One LLM call per document, returning structured JSON only. A separate,
plain-Python step renders that JSON into the spreadsheet.

## Files

| File | Role |
|---|---|
| `config.py` | All settings: API key, model, effort, token limits, file paths. |
| `schema.py` | `DocumentAnnotation` — Pydantic model doubling as validator and tool `input_schema`. |
| `extraction_rules.md` | System prompt — cross-cutting rules only (status definitions, conflict handling, layered-instrument guidance). |
| `cell_map.py` | Row/column anchors for the template. |
| `llm.py` | Builds and sends the single tool-call request; returns a validated `DocumentAnnotation`. |
| `render.py` | `DocumentAnnotation` → filled `.xlsx`. No LLM involved. |
| `main.py` | Orchestrator — reads `config.py`, calls `llm.py`, then `render.py`. |
| `test_render.py` | Renderer smoke test with a hand-built annotation, no API key needed. |

## Key design decisions

- **Schema mirrors the template row-for-row.** `Finding` (`status` / `answer`
  / `citation` / `note`) is the atomic unit, matching the template's four
  columns.
- **`status` is a `Literal`, not a free string** — `"Found"`, `"Not in this
  document"`, `"Could not determine"`, `"Ambiguous"`.
- **Conflicts are just `status="Ambiguous"`** — both readings in `answer`,
  both citations, reasoning in `note`. No separate conflict field.
- **`defined_terms` / `um_mentions` are variable-length lists**, not a fixed
  number of slots — the renderer fills or grows the template's placeholder
  rows to match.
- **Field-level `description=` strings carry the extraction instructions**,
  scoped to the field they govern, instead of one long list in the system
  prompt.
- **Strict tool use is on** (`"strict": True`), with every nested model
  inheriting `extra: "forbid"` via a shared `StrictModel` base — guarantees
  the response actually matches the schema, including required fields.
- **`thinking: {"type": "adaptive"}`**, not manual extended thinking —
  the mode compatible with the forced `tool_choice` this pipeline uses.
- **System prompt and tool schema are prompt-cached**; the instrument text
  itself is not (needs to be present in full, uncompressed, for citations
  to be checkable).
- **`InstrumentLayer(label, status, text)`** represents one document in an
  amendment chain, explicitly labeled with its legal standing, so the model
  doesn't have to infer precedence from document order.
- **Every path is centralized in `config.py`**, anchored with
  `Path(__file__).parent` where it needs to resolve independent of the
  working directory.
- **Raw LLM output is dumped to `out/last_raw_output.json`** before
  validation, for debugging.

## Running it

```bash
pip install anthropic pydantic python-dotenv openpyxl --break-system-packages
```

1. Extract the instrument's text into the `.txt` file `RESOURCES_FILE` points to.
2. Set `DOC_NAME`, `LAYER_LABEL`, `LAYER_STATUS` in `config.py`.
3. Confirm `ANTHROPIC_API_KEY` is set in `.env`.
4. `python main.py`

Output: `OUTPUT_DIR / f"{DOC_NAME}_annotation.xlsx"`.

## Known limitations

- Single instrument layer only — no multi-amendment chain support in `config.py` yet.
- OCR/text extraction happens upstream, by hand.
- No confidentiality routing.
- Single-model only, no ensemble/reconciliation.
- Downstream cross-document summary generation is out of scope.