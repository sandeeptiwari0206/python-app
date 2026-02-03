from fastapi import APIRouter 
from database import tasks_collection 
from models import Task 
 
router = APIRouter() 
 
@router.post("/tasks") 
def create_task(task: Task): 
    tasks_collection.insert_one(task.dict()) 
    return {"message": "Task created"} 

