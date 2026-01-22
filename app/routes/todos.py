from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models import Todo, User
from app.schemas import TodoCreate, TodoResponse, TodoUpdate
from app.auth import get_current_user
from beanie import PydanticObjectId

router = APIRouter(prefix="/todos", tags=["Todos"])

# 1. Get All Todos (Sirf Current User ke)
@router.get("/", response_model=List[TodoResponse])
async def get_todos(current_user: User = Depends(get_current_user)):
    # Beanie query to find todos where owner.id matches current user
    todos = await Todo.find(Todo.owner.id == current_user.id).to_list()
    return todos

# 2. Create Todo
@router.post("/", response_model=TodoResponse)
async def create_todo(todo_data: TodoCreate, current_user: User = Depends(get_current_user)):
    new_todo = Todo(
        title=todo_data.title,
        description=todo_data.description,
        owner=current_user  # Link to current user
    )
    await new_todo.create()
    return new_todo

# 3. Update Todo
@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: PydanticObjectId, todo_data: TodoUpdate, current_user: User = Depends(get_current_user)):
    todo = await Todo.get(todo_id)
    
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.owner.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this todo")
    
    # Update fields only if provided
    if todo_data.title is not None:
        todo.title = todo_data.title
    if todo_data.description is not None:
        todo.description = todo_data.description
    if todo_data.completed is not None:
        todo.completed = todo_data.completed
        
    await todo.save()
    return todo

# 4. Delete Todo
@router.delete("/{todo_id}")
async def delete_todo(todo_id: PydanticObjectId, current_user: User = Depends(get_current_user)):
    todo = await Todo.get(todo_id)
    
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.owner.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this todo")
        
    await todo.delete()
    return {"message": "Todo deleted successfully"}