from __future__ import annotations

import logging
from pathlib import Path


def get_logger(name: str, log_dir: str = "artifacts/logs") -> logging.Logger:
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(Path(log_dir) / f"{name}.log", encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
