import os
from dotenv import load_dotenv


load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "sqlite:///./test.db")
TEST_SQLALCHEMY_DATABASE_URL = os.getenv(
    "TEST_SQLALCHEMY_DATABASE_URL", "sqlite:///:memory:"
)
db_reset_on_start_str = os.getenv("DB_RESET_ON_START", "True")
DB_RESET_ON_START = db_reset_on_start_str.lower() in ("true", "1", "t")


def is_running_under_pytest() -> bool:
    return os.getenv("UNDER_PYTEST") == "True"
