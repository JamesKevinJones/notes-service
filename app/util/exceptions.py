class NoteNotFoundError(Exception):

    def __init__(self, note_id: int):
        self.note_id = note_id
        super().__init__(f"Note {note_id} not found")


class EmailTakenError(Exception):

    def __init__(self, email: str):
        super().__init__(f"{email} is already registered")


class AuthenticationError(Exception):
    pass
