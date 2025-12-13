from fastapi import Depends, FastAPI
from core.dependencies.auth import auth
from database.database import db_instance, Base
from user.routes import router as user_router
from todo.routes import router as todo_router


app = FastAPI()

db_instance.create_table(Base)


@app.get("/", tags=["Home"])
def get_root():
    return {"message": "Server is running!"}


app.include_router(user_router, prefix="/auth", tags=["Authentications"])
app.include_router(
    todo_router,
    prefix="/todos",
    tags=["Todos"],
    dependencies=[Depends(auth.authenticate)],
)
