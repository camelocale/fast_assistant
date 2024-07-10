import datetime 
from pydantic import BaseModel, field_validator
from domain.answer.answer_schema import Answer
from domain.user.user_schema import User

# 스키마 모델: 
class Question(BaseModel):
    id: int
    system_prompt: str #subject: str | None = None #디폴트 값을 설정하려면 다음과 같이 할 수 있다. 
    temperature: float
    top_p: float
    top_k: int
    create_date: datetime.datetime
    answers: list[Answer] = []
    user: User | None
    modify_date:datetime.datetime | None = None # default: None

    class Config:
        from_attributes = True


class QuestionCreate(BaseModel):
    system_prompt: str
    temperature: float
    top_p: float
    top_k: int

    @field_validator('system_prompt')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

class QuestionList(BaseModel):
    total: int = 0
    question_list: list[Question] = []

class QuestionUpdate(QuestionCreate):
    question_id: int

class QuestionDelete(BaseModel):
    question_id: int