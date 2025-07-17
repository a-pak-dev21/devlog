from pydantic import BaseModel, Field, field_validator


class ExerciseCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=25, description="Name of the exercise")
    body_part: str = Field(..., min_length=3, max_length=15, description="Which category of muscles exercise for")

    @field_validator("body_part")
    def valid_body_part(cls, v):
        if not v.strip():
            raise ValueError("Field can't be empty")
        if any(char.isdigit() for char in v):
            raise ValueError("Field can't contain any digits")
        return v


class ExerciseUpdate(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=25)
    body_part: str | None = Field(None, min_length=3, max_length=15)
