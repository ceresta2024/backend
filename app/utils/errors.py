from fastapi import HTTPException


def error_400(message: str) -> HTTPException:
    return HTTPException(status_code=400, detail=message)


def error_401(message: str) -> HTTPException:
    return HTTPException(status_code=401, detail=message)


def error_404(message: str) -> HTTPException:
    return HTTPException(status_code=404, detail=message)
