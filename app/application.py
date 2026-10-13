from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.controller import auth_controller, health_controller, note_controller
from app.util.exceptions import AuthenticationError, EmailTakenError, NoteNotFoundError

app = FastAPI(title="Notes Service")

app.include_router(health_controller.router)
app.include_router(auth_controller.router)
app.include_router(note_controller.router)


@app.exception_handler(NoteNotFoundError)
def note_not_found(request: Request, exc: NoteNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(EmailTakenError)
def email_taken(request: Request, exc: EmailTakenError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(AuthenticationError)
def not_authenticated(request: Request, exc: AuthenticationError):
    return JSONResponse(status_code=401, content={"detail": str(exc)}, headers={"WWW-Authenticate": "Bearer"})
