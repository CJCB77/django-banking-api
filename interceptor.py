"""
Capture all logging and pipe them through Loguru
"""
from loguru import logger
import logging

class InterceptHandler(logging.Handler):
    """A handler job is to decide what to do when a logging record is emitted"""
    def emit(self, record):
        """
        This method is called every time a log is sent to this handler
        """
        # Match the logging level to the Loguru level
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        
        frame, depth = logging.currentframe(), 2

        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        # Tell loguru how far up the stack the logging call was
        # Send the message at the correct level
        logger.opt(depth=depth, exception=record.exc_info).log(
            level, 
            record.getMessage()
        )