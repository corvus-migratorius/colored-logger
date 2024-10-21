"""
Implements a colored logger.
"""

# pylint: disable=W0212

import logging
import os
import sys
from datetime import datetime as dt


class ColoredFormatter(logging.Formatter):
    """
    Colors log messages depending on their logging level.
    """

    ANSI_YELLOW = "\u001b[33m"
    ANSI_RED = "\u001b[31m"
    ANSI_RESET = "\u001b[0m"

    def __init__(self, fmt: str):
        super().__init__(
            fmt=fmt,
            datefmt="%d-%m-%Y %H:%M:%S")

    def format(self, record: logging.LogRecord) -> str:
        """
        Override the format function of logging.Formatter to support color output.

        :param record: the log record to format
        """
        format_orig = self._style._fmt

        if record.levelno == logging.WARNING:
            self._style._fmt = f"{self.ANSI_YELLOW}{format_orig}{self.ANSI_RESET}"

        if record.levelno in (logging.ERROR, logging.CRITICAL):
            self._style._fmt = f"{self.ANSI_RED}{format_orig}{self.ANSI_RESET}"

        result = logging.Formatter.format(self, record)

        self._style._fmt = format_orig

        return result


def get_logger(
        scriptname: str,
        log_dir: str = "./logs",
        level=logging.DEBUG,
        to_stdout: bool = False,
        persist: bool = True,
        pid: bool = False
) -> logging.LoggerAdapter:
    """
    Create a logger that logs to a file and to the console with colored messages.

    :param scriptname: name of the script to log
    :param log_dir: directory to save log files (default: "./logs")
    :param level: logging level for the logger (default: logging.DEBUG)
    :param to_stdout: whether to log to stdout (default: False)
    :param persist: whether to log to a file (default: True)
    :param pid: whether to include the process ID in log messages (default: False)

    :return: a logging.LoggerAdapter
    """
    fmt = "%(asctime)s | %(filename)-14s| line %(lineno)3d: [%(levelname)8s]  %(message)s"
    extra = {}

    if pid:
        fmt = "%(asctime)s | %(filename)-14s| line %(lineno)3d: [%(levelname)8s]  PID %(pid)-7s: %(message)s"
        extra = {"pid": os.getpid()}

    run_id = dt.strftime(dt.now(), "%Y%m%d-%H%M%S")

    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger(scriptname)
    logger.setLevel(level)

    logger.handlers = []

    log_name = f"{os.path.splitext(os.path.basename(scriptname))[0]}.{run_id}.log"
    log_path = os.path.join(log_dir, log_name)

    if persist:
        formatter = logging.Formatter(fmt, "%Y-%m-%d %H:%M:%S")
        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    ch = logging.StreamHandler(sys.stdout) if to_stdout else logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(ColoredFormatter(fmt=fmt))
    logger.addHandler(ch)

    adapter = logging.LoggerAdapter(logger, extra)

    return adapter
