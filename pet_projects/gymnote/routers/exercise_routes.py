from fastapi import APIRouter, HTTPException, Query
from pet_projects.gymnote.models.exercises import exercises
from pet_projects.gymnote.schemas.schemas import ExerciseCreate, ExerciseUpdate
from collections import defaultdict

router = APIRouter()


@router.get("/")
def list_exercises() -> list[dict[str, str | int]]:
    return exercises


@router.post("/")
def add_exercise(exercise: ExerciseCreate) -> dict[str, str | int]:
    new_exercise = {"id": exercises[-1]["id"] + 1}
    new_exercise.update(exercise.model_dump())
    exercises.append(new_exercise)
    return new_exercise


@router.get("/search/")
def search_exercise(name: str | None = None) -> list[dict[str, str | int]] | None:
    if name is None:
        raise HTTPException(status_code=400, detail="Bad response, required parameter 'name' is missing")
    else:
        return [exercise for exercise in exercises if name.lower() in exercise["name"].lower()]


@router.get("/filter/")
def filter_exercises(name: str | None = None, body_part: str | None = None) -> list[dict[str, int | str]]:
    if name is None and body_part is None:
        raise HTTPException(status_code=400, detail="Bad request, at least 1 parameter 'name' / 'body_part' required")
    result = exercises
    if body_part.strip():
        result = [elem for elem in result if elem["body_part"].lower() == body_part.lower()]
    if name.strip():
        result = [elem for elem in result if name.lower() in elem["name"].lower()]
    return [] if result == exercises else result


@router.get("/stats/")
def count_by_body_part() -> dict[str, int]:
    data_stats = defaultdict(int)
    for exercise in exercises:
        data_stats[exercise["body_part"]] += 1
    return dict(data_stats)


@router.get("/by-parts/")
def exercises_by_parts(parts: list[str] = Query(...)) -> list[dict[str, str | int]]:
    if parts is None:
        raise HTTPException(status_code=400, detail="The required parameter is missing")
    return [exercise for exercise in exercises if exercise["body_part"] in parts]


@router.get("/grouped-by-part/")
def grouped_by_part() -> dict[str, list[dict[str, str | int]]]:
    grouped_list = defaultdict(list[dict[str, str | int]])
    for exercise in exercises:
        grouped_list[exercise["body_part"]].append(exercise)
    return dict(grouped_list)


@router.put("/rename-body-part/")
def rename_body_part(old_body_part: str, new_body_part: str) -> dict[str, int]:
    if not old_body_part.strip() or not new_body_part.strip():
        raise HTTPException(status_code=400, detail="Both parameters are required for this request")
    counter = {"updated": 0}
    for exercise in exercises:
        if exercise["body_part"].lower() == old_body_part.strip().lower():
            exercise["body_part"] = new_body_part
            counter["updated"] += 1
    return counter


@router.patch("/id/{exercise_id}/")
def modify_exercise(exercise_id: int, opt_parameter: ExerciseUpdate) -> dict[str, str | int]:
    if opt_parameter is None:
        raise HTTPException(status_code=400, detail="At least 1 parameter for modifying is requested")
    for exercise in exercises:
        if exercise["id"] == exercise_id:
            for key, val in opt_parameter.model_dump().items():
                exercise[key] = val
            return exercise
    else:
        raise HTTPException(status_code=400, detail="Invalid id, no exercise found")


@router.get("/id/{exercise_id}/")
def exercise_by_id(exercise_id: int) -> dict[str, str | int]:
    for exercise in exercises:
        if exercise["id"] == exercise_id:
            return exercise
    else:
        raise HTTPException(status_code=404, detail="Exercise not found")


@router.put("/id/{exercise_id}/")
def update_exercise(exercise: ExerciseCreate, exercise_id: int) -> dict[str, str | int]:
    for elem in exercises:
        if elem["id"] == exercise_id:
            for key, val in exercise.model_dump().items():
                elem[key] = val
            return elem
    else:
        raise HTTPException(status_code=404, detail="Exercise not found")


@router.delete("/id/{exercise_id}/")
def remove_exercise(exercise_id: int) -> dict[str, str | int]:
    for exercise in exercises:
        if exercise["id"] == exercise_id:
            exercises.remove(exercise)
            return {"message": f"Exercise with {exercise_id} id has been removed"}
    else:
        raise HTTPException(status_code=404, detail="Exercise not found")


@router.get("/part/{body_part}/")
def group_by_body_part(body_part: str):
    return [exercise for exercise in exercises if exercise["body_part"] == body_part]
