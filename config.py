# CaneTrust-AI Configuration File

from pathlib import Path

from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv(override=True)

# ============================================================================
# API CONFIGURATION
# ============================================================================

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

CLAUDE_MODEL = "claude-sonnet-4-6"

# Claude API settings

# Set thinking = {"type": "adaptive"}, output_config={"effort": CLAUDE_EFFORT}
CLAUDE_EFFORT = "high"  # Effort levels: low, medium, high, xhigh, max

# ============================================================================
# TOKEN LIMITS
# ============================================================================

MAX_TOKENS_PER_REQUEST = 8000

# ============================================================================
# RESOURCE FILE CONFIGURATION
# ============================================================================

ANNOTATION_TEMPLATE_FILE = "INPUT/MiLA_Annotation_Template_v0.xlsx" 

EXTRACTION_RULES_PATH = Path(__file__).parent / "extraction_rules.md"

RESOURCES_FILE = "INPUT/herrold_5th_amendment.txt" # must be .txt

DOC_NAME = "Herrold Interim Trust — 5th Amendment"

# For now, a single layer/instrument (see instructions for main.py on
# adding more once RESOURCES_FILE supports a list).
LAYER_LABEL = "Fifth Amendment to the Herrold Living Trust (2017)"
LAYER_STATUS = "OPERATIVE"

# ============================================================================
# OUTPUT FILE CONFIGURATION
# ============================================================================

OUTPUT_DIR = "OUTPUT"