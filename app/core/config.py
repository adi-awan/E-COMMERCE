import os
from dotenv import load_dotenv


load_dotenv()


class Settings:

    SUPABASE_URL = os.getenv(
        "SUPABASE_URL"
    )

    SUPABASE_KEY = os.getenv(
        "SUPABASE_KEY"
    )

    SECRET_KEY = os.getenv(
        "SECRET_KEY"
    )
    STRIPE_SECRET_KEY = os.getenv(
        "STRIPE_SECRET_KEY"
    )

settings = Settings()