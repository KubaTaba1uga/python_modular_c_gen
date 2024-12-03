import logging
import sys

# Create a default logger for the project
_local_data = {}


def get_logger():
    return _local_data["logger"]


# Configure the logging
def configure_logger(
    name: str,
    level: str = "INFO",
    log_to_file: bool = False,
    file_path: str = "app.log",
) -> logging.Logger:
    """
    Configures and returns a logger instance.

    Args:
        name (str): The name of the logger.
        level (str): Logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_to_file (bool): Whether to log to a file. Defaults to False.
        file_path (str): Path to the log file if logging to file is enabled. Defaults to 'app.log'.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Create handlers
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logger.level)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    if log_to_file:
        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(logger.level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Avoid duplicate log entries
    logger.propagate = False

    _local_data["logger"] = logger
