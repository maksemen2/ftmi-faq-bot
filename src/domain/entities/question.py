from pydantic import BaseModel, ConfigDict


class QuestionEntity(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    answer: str


class QuestionListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
