from copy import deepcopy
from dataclasses import dataclass, field
import os
from pathlib import Path
from typing import Optional, TypeVar
from dotenv import load_dotenv
import yaml

T = TypeVar("T")


@dataclass
class LLMModelInfo:
    """Represents a Large Language Model (LLM) with its identifier and name."""

    id: str
    name: str

    @staticmethod
    def from_dict(data) -> Optional["LLMModelInfo"]:
        if not isinstance(data, dict):
            return None
        id = data.get("id")
        name = data.get("id")
        if id is None or name is None:
            return None
        return LLMModelInfo(str(id), str(name))

    @staticmethod
    def from_list(data) -> list["LLMModelInfo"]:
        if not isinstance(data, list):
            return []
        models: list[LLMModelInfo] = []
        for d in data:
            model = LLMModelInfo.from_dict(d)
            if model:
                models.append(model)
        return models


@dataclass
class LocalConfiguration:
    """Stores configuration settings for the LLM applicationin using Ollama."""

    llm_models: list[LLMModelInfo] = field(default_factory=lambda: [])


@dataclass
class APIConfiguration:
    """Stores configuration settings for the LLM application using API."""

    api_key: str | None = None
    llm_models: list[LLMModelInfo] = field(default_factory=lambda: [])


class Settings:
    def __init__(self) -> None:
        self.__api_config = APIConfiguration()
        self.__local_config = LocalConfiguration()
        self.__env_path = None
        self.__model_config_path = None
        self.__load_environment(initial=True)
        self.__load_model_config(initial=True)

    def __load_environment(self, path: Optional[Path] = None, initial=False) -> None:
        if path is None:
            if initial:
                path = ".env"
            else:
                print("Please provide env path for non initial setup.")
                return
        try:
            if os.path.exists(path):
                load_dotenv(path, override=True)
                self.__env_path = path
            else:
                print(f"Environment file ({path}) not found.")
                load_dotenv()
            api_key = self.__get_env("TOGETHER_API_KEY", required=True)
            if api_key:
                self.__api_config.api_key = api_key
        except Exception as e:
            print(e.args[0])

    def __load_model_config(self, path: Optional[Path] = None, initial=False) -> None:
        if path is None:
            if initial:
                path = "config.yaml"
            else:
                print("Please provide yaml path for non initial setup.")
                return
        if os.path.exists(path):
            with open(path, "r") as f:
                raw_model_config = yaml.safe_load(f)
            self.__model_config_path = path

            if not isinstance(raw_model_config, dict):
                return
            if "models" not in raw_model_config:
                return
            model_dict = raw_model_config["models"]
            if "local" in model_dict:
                self.__local_config.llm_models = LLMModelInfo.from_list(
                    model_dict["local"]
                )
            if "api" in model_dict:
                self.__api_config.llm_models = LLMModelInfo.from_list(model_dict["api"])
        else:
            print(f"Model configuration file ({path}) not found.")

    def __get_env(
        self, key: str, default: Optional[T] = None, required: bool = False
    ) -> T:
        value = os.getenv(key, default)
        if required and value is None:
            raise ValueError(f"Required environment variable {key} not set")
        return value

    @property
    def api_config(self) -> APIConfiguration:
        """
        Get the current API configuration.

        Returns:
            config (APIConfiguration): The current configuration object.

        Raises:
            KeyError: If required environment variables or model configurations are not set.
        """
        if self.__env_path is None or self.__api_config.api_key is None:
            raise KeyError("Environment variable is not set")
        if self.__model_config_path is None or len(self.__api_config.llm_models) == 0:
            raise KeyError("Model configuration is not set")
        return self.__api_config

    @property
    def local_config(self) -> LocalConfiguration:
        """
        Get the current Local configuration.

        Returns:
            config (LocalConfiguration): The current configuration object.

        Raises:
            KeyError: If required environment variables or model configurations are not set.
        """
        if self.__model_config_path is None or len(self.__local_config.llm_models) == 0:
            raise KeyError("Model configuration is not set")
        return self.__local_config

    def configure_paths_and_load(
        self,
        env_path: Optional[Path] = None,
        model_config_path: Optional[Path] = None,
    ) -> None:
        """
        Configure custom paths for environment and model configuration files and load them.

        Args:
            env_path (Path | None): Optional custom path to .env file.
            model_config_path (Path | None): Optional custom path to model configuration YAML file.
        """
        if env_path:
            self.__load_environment(env_path)
        if model_config_path:
            self.__load_model_config(model_config_path)
