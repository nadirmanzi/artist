"""
Django logging configuration.

Defines the LOGGING dict used by Django with:
- Console handler (development-friendly format)
- Structured JSON handlers to stdout/stderr (captured by Railway's log system). 
"""
import logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {name} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
        "audit_json": {
            "()": "config.logging.formatters.AuditJsonFormatter",
        },
    },

    "filters": {
        "default_levels": {
            "()": "config.logging.formatters.LevelRangeFilter",
            "min_level": logging.DEBUG,
            "max_level": logging.WARNING,
        },
        "error_levels": {
            "()": "config.logging.formatters.LevelRangeFilter",
            "min_level": logging.ERROR,
            "max_level": logging.CRITICAL,
        },
    },

    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        # Structured JSON audit entries -> stdout. Railway (and Docker's default
        # log driver) captures stdout/stderr automatically, so this replaces
        # the old file-based handlers with zero volume/permission dependency.
        "audit_stdout": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "audit_json",
            "filters": ["default_levels"],
        },
        "audit_stderr": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "formatter": "audit_json",
            "filters": ["error_levels"],
        },
    },

    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "django": {
            "handlers": ["console", "audit_stdout", "audit_stderr"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console", "audit_stdout", "audit_stderr"],
            "level": "INFO",
            "propagate": False,
        },
        "users": {
            "handlers": ["console", "audit_stdout", "audit_stderr"],
            "level": "DEBUG",
            "propagate": False,
        },
        "audit": {
            "handlers": ["console", "audit_stdout", "audit_stderr"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}