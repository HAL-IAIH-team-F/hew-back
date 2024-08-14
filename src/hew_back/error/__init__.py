from hew_back import model


class ErrorIdException(Exception):
    def __init__(self, error_id, message: str | None = None):
        error_id: model.ErrorIds
        if message is None:
            message = error_id.value.message
        self.error_id: model.ErrorIds = error_id
        self.message = message

    def to_error_res(self):
        return model.ErrorRes.create(self.error_id.name, self.message)
