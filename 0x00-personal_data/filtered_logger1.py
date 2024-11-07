#!/usr/bin/env python3
"""
Module for filtering and obfuscating sensitive log data.
"""

import re
from typing import List
import logging
import mysql.connector
import os

# Define PII_FIELDS as a tuple of field names that should be considered PII
PII_FIELDS = ("name", "email", "phone", "ssn", "password")

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Replaces values of specified fields in the log message with a redaction string
    """
    pattern = r'(' + '|'.join([f'{field}=.*?{separator}' for field in fields]) + r')'
    return re.sub(pattern, lambda m: f'{m.group(0).split("=")[0]}={redaction}{separator}', message)

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class for obfuscating sensitive information
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with a list of fields to redact.

        Args:
            fields (List[str]): List of fields to redact in log messages.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record by obfuscating specified fields.
        """
        original_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, original_message, self.SEPARATOR)

    def get_logger() -> logging.Logger:
        """Implementing a logger."""

        logger = logging.getLogger("user_data")
        logger.setLevel(logging.INFO)
        logger.propagate = False
        handler = logging.StreamHandler()
        handler.setFormatter(RedactingFormatter(PII_FIELDS))
        logger.addHandler(handler)
        return logger

    def get_db() -> mysql.connector.connection.MySQLConnection:
        """ Implement db conectivity """
        psw = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
        username = os.environ.get('PERSONAL_DATA_DB_USERNAME', "root")
        host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
        db_name = os.environ.get('PERSONAL_DATA_DB_NAME')
        conn = mysql.connector.connect(
                host=host,
                database=db_name,
                user=username,
                password=psw)
        return conn
