from pydantic import BaseModel, validator

class RecordCreate(BaseModel):
    amount: float
    type: str
    category: str
    date: str
    notes: str | None = None

    @validator("type")
    def validate_type(cls, value):
        if value not in ["income", "expense"]:
            raise ValueError("Type must be 'income' or 'expense'")
        return value