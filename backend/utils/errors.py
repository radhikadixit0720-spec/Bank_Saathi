"""
Shared error helpers.

The goal is that no route ever leaks a raw Python traceback/exception
message to the client - every failure is translated into a clean,
human-readable HTTPException with an appropriate status code.
"""
import logging

from fastapi import HTTPException, status

logger = logging.getLogger("bank_saathi.errors")


def not_found(message: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)


def bad_request(message: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


def unprocessable(message: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=message)


def server_error(exc: Exception, context: str) -> HTTPException:
    """Log the real exception server-side but return a safe, generic
    message to the client."""
    logger.exception("Unexpected error in %s: %s", context, exc)
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Something went wrong while processing '{context}'. Please try again.",
    )
