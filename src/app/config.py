import os
from dotenv import load_dotenv

# Path to your .env (adjust if necessary)
load_dotenv()

# MANUALLY ALIGN NAMES
# The library likely wants OPEN_ELECTRICITY_API_KEY or OPENELECTRICITY_API_KEY
# Let's set both to be safe before the library can complain
api_key = os.getenv("OPENELECTRICITY_API_KEY")
os.environ["OPEN_ELECTRICITY_API_KEY"] = api_key
os.environ["OPENELECTRICITY_API_KEY"] = api_key

# Database settings for your SQLAlchemy connection
DB_URL = f"mysql+pymysql://{os.getenv('APP_DB_USER')}:{os.getenv('APP_DB_PASSWORD')}@{os.getenv('APP_DB_HOST')}:{os.getenv('APP_DB_PORT')}/{os.getenv('APP_DB_NAME')}"