class NotFoundError(Exception):
    def __init__(self):
        self.msg = "Data Not Found. Please Check ID"
