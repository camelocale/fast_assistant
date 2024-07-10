from datetime import datetime
from sqlalchemy.orm import Session
from domain.answer.answer_schema import AnswerCreate, AnswerUpdate
from models import Question, Answer, User
import requests
import json


def create_answer(db: Session, question: Question, answer_create: AnswerCreate, user: User):
    db_answer = Answer(question=question,
                        content=answer_create.content,
                        is_assistant=answer_create.is_assistant,
                        create_date=datetime.now(),
                        user=user)
    db.add(db_answer)
    db.commit()

def generate_answer(question: Question, prompt: str):
    ### implemetation
    vllm_host = "http://localhost:8000"
    url = f"{vllm_host}/generate"

    def create_prompt(question):
        answers = question.answers
        system_prompt = question.system_prompt
        prompt = f"<|im_start|>system\n{system_prompt}<|im_end|>\n"
        for i, e in enumerate(answers):
            if e.is_assistant:
                prompt += "<|im_start|>assistant\n"+ e.content +"<|im_end|>\n"
            else: 
                prompt += "<|im_start|>user\n"+ e.content +"<|im_end|>\n"
        prompt += "<|im_start|>assistant\n"
        return prompt
    
    def chat(question, user_prompt):
        # headers = {'Content-Type': 'application/json'}
        prompt = create_prompt(question)
        data = {
            "prompt": prompt,
            "temperature": float(question.temperature),
            "top_p": float(question.top_p),
            "top_k": int(question.top_k),
            "max_tokens": 2048,
            "stop": '<|im_end|>',
            "stream": True
        }
        r = requests.post(url, json=data, stream=True)
        return r

    response = chat(question, prompt)

    for line in response.iter_content(chunk_size=4096):
        yield line.decode('utf-8')


def get_answer(db: Session, answer_id: int):
    return db.query(Answer).get(answer_id)

def update_answer(db: Session, db_answer: Answer,
                    answer_update: AnswerUpdate):
    db_answer.content = answer_update.content
    db_answer.modify_date = datetime.now()
    db.add(db_answer)
    db.commit()

def delete_answer(db: Session, db_answer: Answer):
    db.delete(db_answer)
    db.commit()
