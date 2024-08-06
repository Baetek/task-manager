import json
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import db_session, engine, get_redis_client


redis_client = get_redis_client()

def create_app(db: Session = Depends(db_session)):
    app = FastAPI()

    @app.post("/users/", response_model=schemas.User)
    def create_user(user: schemas.UserCreate, db: Session = Depends(db_session)):
        db_user = crud.get_user_by_username(db, username=user.username)
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        return crud.create_user(db=db, user=user)

    @app.get("/users/{user_id}/tasks/", response_model=List[schemas.Task])
    def read_tasks(user_id: int, db: Session = Depends(db_session)):
        if redis_client:
            cached_tasks = redis_client.get(f"user:{user_id}:tasks")
            if cached_tasks:
                return json.loads(cached_tasks)

        tasks = crud.get_tasks(db=db, user_id=user_id)

        if redis_client:
            redis_client.setex(f"user:{user_id}:tasks", 3600, json.dumps(jsonable_encoder(tasks)))  # Cache for 1 hour

        return tasks

    @app.post("/users/{user_id}/tasks/", response_model=schemas.Task)
    def create_task(
        user_id: int, task: schemas.TaskCreate, db: Session = Depends(db_session)
    ):
        if redis_client:
            redis_client.delete(f"user:{user_id}:tasks")
        return crud.create_task(db=db, task=task, user_id=user_id)

    @app.patch("/tasks/{task_id}/", response_model=schemas.Task)
    def update_task(
        task_id: int, task: schemas.TaskUpdate, db: Session = Depends(db_session)
    ):
        db_task = crud.get_task(db=db, task_id=task_id)
        if db_task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        update_data = task.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)

        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        if redis_client:
            redis_client.delete(f"user:{db_task.owner_id}:tasks")
        return db_task

    @app.delete("/tasks/{task_id}/", response_model=schemas.Task)
    def delete_task(task_id: int, db: Session = Depends(db_session)):
        db_task = crud.get_task(db=db, task_id=task_id)
        if db_task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        crud.delete_task(db=db, task_id=task_id)
        if redis_client:
            redis_client.delete(f"user:{db_task.owner_id}:tasks")
        return db_task

    return app


app = create_app()
