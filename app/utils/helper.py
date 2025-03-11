import os
import logging
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

def setup_logger(name: str) -> logging.Logger:
    """
    Create and configure a logger with the given name.
    
    Parameters:
        name (str): The name of the logger.
    
    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

def get_env_variable(key: str, default=None):
    """
    Retrieve the value of an environment variable.
    
    Parameters:
        key (str): The key of the environment variable.
        default: The default value if the variable is not set.
    
    Returns:
        str: The value of the environment variable or the default value.
    """
    return os.getenv(key, default)
