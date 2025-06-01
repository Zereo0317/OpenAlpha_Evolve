import os

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:  # pragma: no cover - fallback for environments without python-dotenv
    def load_dotenv(*args, **kwargs):
        """Fallback no-op if python-dotenv is not installed."""
        return False

load_dotenv()

# LLM Configuration
FLASH_API_KEY = os.getenv("FLASH_API_KEY")
FLASH_BASE_URL = os.getenv("FLASH_BASE_URL", None)
# Default to the Gemini 2.5 flash 05-20 preview model if not provided
FLASH_MODEL = os.getenv("FLASH_MODEL", "gemini/gemini-2.5-flash-preview-05-20")

# Primary "pro" model configuration. These were previously commented out but are
# now loaded so they can be used as the primary model if desired.
PRO_API_KEY = os.getenv("PRO_API_KEY")
PRO_BASE_URL = os.getenv("PRO_BASE_URL", None)
PRO_MODEL = os.getenv("PRO_MODEL", "gemini/gemini-2.5-pro")

EVALUATION_API_KEY = os.getenv("EVALUATION_API_KEY")
EVALUATION_BASE_URL = os.getenv("EVALUATION_BASE_URL", None)
EVALUATION_MODEL = os.getenv("EVALUATION_MODEL")

# Ensure litellm sees a valid Gemini API key. It checks the environment for
# ``GOOGLE_API_KEY`` or ``GEMINI_API_KEY``. If neither is set but one of our
# custom keys is, fall back to it so that calls to the Gemini models succeed.
if not os.getenv("GOOGLE_API_KEY") and not os.getenv("GEMINI_API_KEY"):
    if FLASH_API_KEY:
        os.environ["GOOGLE_API_KEY"] = FLASH_API_KEY
    elif PRO_API_KEY:
        os.environ["GOOGLE_API_KEY"] = PRO_API_KEY

# LiteLLM Configuration
# Use the Gemini 2.5 flash model by default for all LiteLLM calls
LITELLM_DEFAULT_MODEL = os.getenv("LITELLM_DEFAULT_MODEL", FLASH_MODEL)
LITELLM_DEFAULT_BASE_URL = os.getenv("LITELLM_DEFAULT_BASE_URL", None)
LITELLM_MAX_TOKENS = int(os.getenv("LITELLM_MAX_TOKENS", "4096"))
LITELLM_TEMPERATURE = float(os.getenv("LITELLM_TEMPERATURE", "1.0"))
LITELLM_TOP_P = float(os.getenv("LITELLM_TOP_P", "0.9"))
LITELLM_TOP_K = int(os.getenv("LITELLM_TOP_K", "40"))

# Specific model names for strategic use (can be same as LITELLM_DEFAULT_MODEL if only one is used)
# Primary model defaults to Gemini 2.5 Pro while secondary uses the flash variant
LLM_PRIMARY_MODEL = os.getenv("LLM_PRIMARY_MODEL", PRO_MODEL)
LLM_SECONDARY_MODEL = os.getenv("LLM_SECONDARY_MODEL", FLASH_MODEL)

# if not PRO_API_KEY:
#     print("Warning: PRO_API_KEY not found in .env or environment. Using a NON-FUNCTIONAL placeholder. Please create a .env file with your valid API key.")
#     PRO_API_KEY = "Your API key"

# Evolutionary Algorithm Settings
POPULATION_SIZE = 5
GENERATIONS = 2
# Threshold for switching to bug-fix prompt
# If a program has errors and its correctness score is below this, a bug-fix prompt will be used.
BUG_FIX_CORRECTNESS_THRESHOLD = float(os.getenv("BUG_FIX_CORRECTNESS_THRESHOLD", "0.1"))
# Threshold for using the primary (potentially more powerful/expensive) LLM for mutation
HIGH_FITNESS_THRESHOLD_FOR_PRIMARY_LLM = float(os.getenv("HIGH_FITNESS_THRESHOLD_FOR_PRIMARY_LLM", "0.8"))
ELITISM_COUNT = 1
MUTATION_RATE = 0.7
CROSSOVER_RATE = 0.2

# Island Model Settings
NUM_ISLANDS = 4  # Number of subpopulations
# Frequency (in generations) at which islands perform migration.
# This was previously named ``MIGRATION_INTERVAL`` which caused a mismatch with
# the runtime configuration options.
MIGRATION_FREQUENCY = 4
ISLAND_POPULATION_SIZE = POPULATION_SIZE // NUM_ISLANDS  # Programs per island
MIN_ISLAND_SIZE = 2  # Minimum number of programs per island
MIGRATION_RATE = 0.2  # Rate at which programs migrate between islands

# Debug Settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
EVALUATION_TIMEOUT_SECONDS = 800

# Docker Execution Settings
DOCKER_IMAGE_NAME = os.getenv("DOCKER_IMAGE_NAME", "code-evaluator:latest")
DOCKER_NETWORK_DISABLED = os.getenv("DOCKER_NETWORK_DISABLED", "True").lower() == "true"

DATABASE_TYPE = "json"
DATABASE_PATH = "program_database.json"

# Logging Configuration
LOG_LEVEL = "DEBUG" if DEBUG else "INFO"
LOG_FILE = "alpha_evolve.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

API_MAX_RETRIES = 5
API_RETRY_DELAY_SECONDS = 10

RL_TRAINING_INTERVAL_GENERATIONS = 50
RL_MODEL_PATH = "rl_finetuner_model.pth"

MONITORING_DASHBOARD_URL = "http://localhost:8080"

def get_setting(key, default=None):
    """
    Retrieves a setting value.
    For LLM models, it specifically checks if the primary choice is available,
    otherwise falls back to a secondary/default if defined.
    """
    return globals().get(key, default)

def get_llm_model(model_type="default"):
    if model_type == "default":
        return LITELLM_DEFAULT_MODEL
    elif model_type == "flash":
        # Assuming FLASH_MODEL might still be a specific, different model.
        # If FLASH_MODEL is also meant to be covered by litellm's general handling,
        # this could also return LITELLM_DEFAULT_MODEL or a specific flash model string.
        # For now, keep FLASH_MODEL if it's distinct.
        return FLASH_MODEL if FLASH_MODEL else LITELLM_DEFAULT_MODEL # Return default if FLASH_MODEL is not set
    # Fallback for any other model_type not explicitly handled
    return LITELLM_DEFAULT_MODEL

                                 
