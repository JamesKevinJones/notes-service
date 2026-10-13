from fastapi import APIRouter, Depends

from app.dto.note_dto import NoteCreateRequest, NoteResponse, NoteUpdateRequest
from app.entity.user import User
from app.service.note_service import NoteService
from app.util.dependencies import get_current_user, get_note_service

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=NoteResponse, status_code=201)
def create_note(
    body: NoteCreateRequest,
    user: User = Depends(get_current_user),
    service: NoteService = Depends(get_note_service),
):
    note = service.create(user.id, body)
    return NoteResponse.model_validate(note)


@router.get("", response_model=list[NoteResponse])
def list_notes(user: User = Depends(get_current_user), service: NoteService = Depends(get_note_service)):
    return [NoteResponse.model_validate(note) for note in service.list_all(user.id)]


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, user: User = Depends(get_current_user), service: NoteService = Depends(get_note_service)):
    note = service.get(user.id, note_id)
    return NoteResponse.model_validate(note)


@router.patch("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    body: NoteUpdateRequest,
    user: User = Depends(get_current_user),
    service: NoteService = Depends(get_note_service),
):
    note = service.update(user.id, note_id, body)
    return NoteResponse.model_validate(note)


@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, user: User = Depends(get_current_user), service: NoteService = Depends(get_note_service)):
    service.delete(user.id, note_id)
