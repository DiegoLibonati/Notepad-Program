import os
from tkinter import Tk

from dotenv import load_dotenv

from src.configs.development_config import DevelopmentConfig
from src.configs.logger_config import setup_logger
from src.configs.production_config import ProductionConfig
from src.configs.testing_config import TestingConfig
from src.ui.interface_app import InterfaceApp

logger = setup_logger("notepad-program - app.py")

CONFIG_MAP = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def main(environment: str = "production") -> None:
    load_dotenv()

    environment = os.getenv("ENVIRONMENT", environment)

    root = Tk()
    config_class = CONFIG_MAP.get(environment, ProductionConfig)
    config = config_class()

    interface_app = InterfaceApp(root=root, config=config)
    root.mainloop()

    logger.info("App finished: %s", interface_app)


if __name__ == "__main__":
    main(environment="development")
