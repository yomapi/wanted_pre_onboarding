class CustomBaseExecption(Exception):
    is_custom_execption = True


class NotFoundError(CustomBaseExecption):
    def __init__(self):
        self.msg = "Data Not Found. Please Check ID"


class DuplicatedApplicationError(CustomBaseExecption):
    def __init__(self):
        self.msg = "You have already applied this application"


class RequiredKeyNotExistError(CustomBaseExecption):
    def __init__(self, required_keys: set[str]):
        required_key_names = ",".join(required_keys)
        self.msg = f"{required_key_names} required keys"
