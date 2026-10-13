from app.dto.note_dto import NoteCreateRequest, NoteUpdateRequest
from app.entity.note import Note
from app.repository.note_repository import NoteRepository
from app.util.exceptions import NoteNotFoundError


class NoteService:

    def __init__(self, repository: NoteRepository):
        self.repository = repository

    def create(self, user_id: int, request: NoteCreateRequest) -> Note:
        return self.repository.insert(user_id, request.title, request.content)

    def list_all(self, user_id: int) -> list[Note]:
        return self.repository.find_all(user_id)

    def get(self, user_id: int, note_id: int) -> Note:
        note = self.repository.find_by_id(user_id, note_id)
        if note is None:
            raise NoteNotFoundError(note_id)
        return note

    def update(self, user_id: int, note_id: int, request: NoteUpdateRequest) -> Note:
        note = self.repository.update(user_id, note_id, request.title, request.content)
        if note is None:
            raise NoteNotFoundError(note_id)
        return note

    def delete(self, user_id: int, note_id: int) -> None:
        if not self.repository.delete(user_id, note_id):
            raise NoteNotFoundError(note_id)
