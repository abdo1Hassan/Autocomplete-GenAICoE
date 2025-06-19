from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings.
    """

    QUERIES_FILE_PATH: str = "data/merged_queries_with_tag_cleaned.csv"
    MAX_SUGGESTIONS: int = 3


settings = Settings()
