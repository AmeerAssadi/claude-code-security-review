"""Logging configuration for ClaudeCode."""

import logging
import sys
import os


def get_logger(name: str) -> logging.Logger:
    """Get a configured logger that outputs to stderr.
    
    Args:
        name: The name of the logger (usually __name__)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Only configure if not already configured
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        
        # Get repo and MR/PR number from environment for prefix
        repo_name = os.environ.get('GITHUB_REPOSITORY', '')
        mr_number = os.environ.get('MR_NUMBER') or os.environ.get('PR_NUMBER', '')

        # Build prefix
        if repo_name and mr_number:
            prefix = f"[{repo_name}#{mr_number}]"
        elif repo_name:
            prefix = f"[{repo_name}]"
        elif mr_number:
            prefix = f"[MR#{mr_number}]"
        else:
            prefix = ""
        
        # Include prefix in format if available
        if prefix:
            format_str = f'{prefix} [%(name)s] %(message)s'
        else:
            format_str = '[%(name)s] %(message)s'
        
        formatter = logging.Formatter(format_str)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger
