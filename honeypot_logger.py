#!/usr/bin/env python3
import logging

_logger_instance = None

def setup_logger(log_callback=None):
    """Create and configure the logger."""
    global _logger_instance
    
    logger = logging.getLogger("HoneypotLogger")
    logger.setLevel(logging.INFO)
    
    
    if logger.handlers:
        logger.handlers.clear()

    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
    logger.addHandler(ch)
    
    if log_callback:
        class GUILogHandler(logging.Handler):
            def emit(self, record):
                try:
                    msg = self.format(record)
                    log_callback(msg)
                except Exception:
                    self.handleError(record)
        
        gui_handler = GUILogHandler()
        gui_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        logger.addHandler(gui_handler)
    
    _logger_instance = logger
    return logger

def get_logger():
    """Get the shared logger instance."""
    return _logger_instance