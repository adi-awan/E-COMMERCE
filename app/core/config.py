import os
from dotenv import load_dotenv


load_dotenv()


class Settings:

    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")

    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_FROM = os.getenv("MAIL_FROM")

    def __post_init_checks__(self):
        # Fail fast instead of silently running with an empty/missing secret
        required = ["SUPABASE_URL", "SUPABASE_KEY", "SECRET_KEY"]
        missing = [name for name in required if not getattr(self, name)]
        if missing:
            raise RuntimeError(
                f"Missing required environment variables: {', '.join(missing)}"
            )


settings = Settings()
settings.__post_init_checks__()