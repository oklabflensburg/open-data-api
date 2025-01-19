from fastapi.exceptions import HTTPException


class CustomValidationError(HTTPException):
    def __init__(self, loc: list, msg: str, error_type: str, status_code: int = 400):
        self.detail = {
            'loc': loc,
            'msg': msg,
            'type': error_type
        }

        self.status_code = status_code

        super().__init__(status_code=status_code, detail=self.detail)