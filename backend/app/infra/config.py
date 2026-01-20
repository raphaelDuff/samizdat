from enum import StrEnum, auto
import os


class RepositoryType(StrEnum):
    POSTGRESQL = auto()


class Config:
    """Application configuration."""

    # DEFAULT values
    DEFAULT_REPOSITORY_TYPE: RepositoryType = RepositoryType.POSTGRESQL

    @classmethod
    def get_repository_type(cls) -> RepositoryType:
        """Get the configured repository type."""
        repo_type_str = os.getenv(
            "CONFIG_REPOSITORY_TYPE", cls.DEFAULT_REPOSITORY_TYPE.value
        )
        try:
            return RepositoryType(repo_type_str.lower())
        except ValueError:
            raise ValueError(f"Invalid repository type: {repo_type_str}")
