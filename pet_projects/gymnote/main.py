from fastapi import FastAPI
from routers.exercise_routes import router as exercise_router


app = FastAPI()


@app.get("/")
def greetings() -> dict[str, str]:
    return {"message": "Welcome to GymNote API"}


app.include_router(exercise_router, prefix="/exercises", tags=["Exercises"])




