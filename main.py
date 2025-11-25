from fastapi import FastAPI, HTTPException
from schemas import TaskCreate, TaskUpdate

tasks = []
task_id_counter = 1

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Task Manager API is running!"}

@app.post("/tasks")
def create_task(task:TaskCreate):
    global task_id_counter

    new_task = {
        "id":task_id_counter,
        "title":task.title,
        "description":task.description,
        "completed":False
    }
    tasks.append(new_task)
    task_id_counter += 1
    return new_task

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task['id'] == task_id:
            return task

    raise HTTPException(status_code=404, detail="Task not found")

@app.put('/tasks/{task_id}')
def update_task(task_id: int, update:TaskUpdate):
    for task in tasks:
        if task['id']==task_id:

            # update only provided fields
            if update.title is not None:
                task['title'] = update.title
            if update.description is not None:
                task['description'] = update.description
            if update.completed is not None:
                task['completed'] = update.completed

            return task
    
    raise HTTPException(status_code = 404, detail = "Task not found")
    
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task['id']==task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}
    
    raise HTTPException(status_code=404, detail="Task not found")
    