from pydantic import BaseModel, EmailStr


class TutorBase(BaseModel):
    name: str
    email: EmailStr


class TutorCreate(TutorBase):
    pass


class TutorUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


class TutorOut(TutorBase):
    id: int

    class Config:
        from_attributes = True
