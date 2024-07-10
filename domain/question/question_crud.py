from datetime import datetime
from domain.question.question_schema import QuestionCreate, QuestionUpdate

from models import Question, User
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

def get_question_list(db: Session):
    question_list = db.query(Question)\
        .order_by(Question.create_date.desc())\
        .all()
    return question_list

def get_question(db: Session, question_id: int):
    question = db.query(Question).get(question_id)
    return question

def get_question_with_answers(db: Session, question_id: int):
    question_with_answers = db.query(Question).options(joinedload(Question.answers)).filter(Question.id == question_id).first()
    return question_with_answers

def create_question(db: Session, question_create: QuestionCreate, user: User):
    db_question = Question(system_prompt=question_create.system_prompt,
                            temperature=question_create.temperature,
                            top_p=question_create.top_p,
                            top_k=question_create.top_k,
                            create_date=datetime.now(),
                            user=user)
    db.add(db_question)
    db.commit()
    return db_question

def get_question_list(db: Session, skip: int = 0, limit: int = 10):
    _question_list = db.query(Question)\
        .order_by(Question.create_date.desc())

    total = _question_list.count()
    question_list = _question_list.offset(skip).limit(limit).all()
    return total, question_list

def update_question(db: Session, db_question: Question,
                    question_update: QuestionUpdate):
    db_question.subject = question_update.subject
    db_question.content = question_update.content
    db_question.modify_date = datetime.now()
    db.add(db_question)
    db.commit()  

def delete_question(db: Session, db_question: Question):
    db.delete(db_question)
    db.commit()