class AppError(Exception):
    pass

class NoDataFoundError(AppError):
    def __init__(self):
        pass