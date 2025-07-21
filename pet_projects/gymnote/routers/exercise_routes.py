from fastapi import APIRouter, HTTPException, Query
from pet_projects.gymnote.models.exercises import exercises
from pet_projects.gymnote.schemas.schemas import ExerciseCreate, ExerciseUpdate
from collections import defaultdict
from pet_projects.gymnote.core.loggers import exercise_logger

router = APIRouter()


@router.get("/")
def list_exercises() -> list[dict[str, str | int]]:
    exercise_logger.info(f"Returned list of {len(exercises)} exercises")
    return exercises


@router.post("/")
def add_exercise(exercise: ExerciseCreate) -> dict[str, str | int]:
    exercise_logger.info(f"Function to add {exercise} to exercises list has been executed")
    new_exercise = {"id": exercises[-1]["id"] + 1}
    new_exercise.update(exercise.model_dump())
    exercises.append(new_exercise)
    exercise_logger.info(f"{new_exercise} has been added and returned")
    return new_exercise


@router.get("/search/")
def search_exercise(name: str | None = None) -> list[dict[str, str | int]] | None:
    if name is None:
        exercise_logger.warning(f"Required optional parameter 'name' is missing")
        raise HTTPException(status_code=400, detail="Bad response, required parameter 'name' is missing")
    else:
        found_exercises = [exercise for exercise in exercises if name.lower() in exercise["name"].lower()]
        exercise_logger.info(f"Returned the exercise found by parameter 'name': {name}")
        return found_exercises


@router.get("/filter/")
def filter_exercises(name: str | None = None, body_part: str | None = None) -> list[dict[str, int | str]]:
    if name is None and body_part is None:
        exercise_logger.warning(f"Both optional parameters is missing")
        raise HTTPException(status_code=400, detail="Bad request, at least 1 parameter 'name' / 'body_part' required")
    result = exercises
    if body_part.strip():
        exercise_logger.debug(f"Exercises filtered by a 'body_part': {body_part} parameter")
        result = [elem for elem in result if elem["body_part"].lower() == body_part.lower()]
    if name.strip():
        exercise_logger.debug(f"Exercises filtered by 'name': {name} parameter")
        result = [elem for elem in result if name.lower() in elem["name"].lower()]
    exercise_logger.info(f"Returned {len(result)} exercises that fulfill mentioned filter")
    return [] if result == exercises else result


@router.get("/stats/")
def count_by_body_part() -> dict[str, int]:
    data_stats = defaultdict(int)
    for exercise in exercises:
        data_stats[exercise["body_part"]] += 1
    exercise_logger.info("Returned exercises grouped and counted by 'body part'")
    return dict(data_stats)


@router.get("/by-parts/")
def exercises_by_parts(parts: list[str] = Query(...)) -> list[dict[str, str | int]]:
    if parts is None:
        exercise_logger.error("Required argument 'parts' is missing")
        # raise is not necessary since Query(...) will automatically return 422 error
        # raise HTTPException(status_code=422, detail="The required parameter is missing")
    filtered_by_body_parts = [exercise for exercise in exercises if exercise["body_part"] in parts]
    exercise_logger.info(f"Returned ")
    return filtered_by_body_parts


@router.get("/grouped-by-part/")
def grouped_by_part() -> dict[str, list[dict[str, str | int]]]:
    grouped_list = defaultdict(list[dict[str, str | int]])
    for exercise in exercises:
        grouped_list[exercise["body_part"]].append(exercise)
    exercise_logger.info("Returned exercises grouped by body parts")
    return dict(grouped_list)


@router.put("/rename-body-part/")
def rename_body_part(old_body_part: str, new_body_part: str) -> dict[str, int]:
    if not old_body_part.strip() or not new_body_part.strip():
        exercise_logger.error("One or both required parameters 'old_body_part', 'new_body_part'  is missing")
        raise HTTPException(status_code=400, detail="One or both parameters are required for this request")
    counter = {"updated": 0}
    for exercise in exercises:
        if exercise["body_part"].lower() == old_body_part.strip().lower():
            exercise["body_part"] = new_body_part
            counter["updated"] += 1
            exercise_logger.debug(f"'Body part' parameter for {exercise} has been updated and added to count")
    exercise_logger.info(f"Returned the number of exercise with new category(body part) name: {len(counter)}")
    return counter


@router.patch("/id/{exercise_id}/")
def modify_exercise(exercise_id: int, opt_parameter: ExerciseUpdate) -> dict[str, str | int]:
    if opt_parameter is None:
        exercise_logger.warning("Optional parameter 'opt_parameter' is blank, at least 1 (key, val) par should be sent")
        raise HTTPException(status_code=400, detail="At least 1 parameter for modifying is requested")
    for exercise in exercises:
        if exercise["id"] == exercise_id:
            for key, val in opt_parameter.model_dump().items():
                exercise[key] = val
                exercise_logger.debug(f"{key} parameter of exercise with id: {exercise_id} has been updated")
            return exercise
    else:
        exercise_logger.error(f"No exercises with mentioned id: {exercise_id}, check again")
        raise HTTPException(status_code=400, detail="Invalid id, no exercise found")


@router.get("/id/{exercise_id}/")
def exercise_by_id(exercise_id: int) -> dict[str, str | int]:
    for exercise in exercises:
        if exercise["id"] == exercise_id:
            exercise_logger.info(f"Returned exercised by mentioned id: {exercise_id}")
            return exercise
    else:
        exercise_logger.error(f"Exercise with following id: {exercise_id} hasn't been found")
        raise HTTPException(status_code=404, detail="Exercise not found")


@router.put("/id/{exercise_id}/")
def update_exercise(exercise: ExerciseCreate, exercise_id: int) -> dict[str, str | int]:
    for elem in exercises:
        if elem["id"] == exercise_id:
            for key, val in exercise.model_dump().items():
                elem[key] = val
            exercise_logger.info(f"Exercise with id: {exercise_id} has been fully changed to new one")
            return elem
    else:
        exercise_logger.error(f"Exercise with following id: {exercise_id} hasn't been found")
        raise HTTPException(status_code=404, detail="Exercise not found")


@router.delete("/id/{exercise_id}/")
def remove_exercise(exercise_id: int) -> dict[str, str | int]:
    for exercise in exercises:
        if exercise["id"] == exercise_id:
            exercises.remove(exercise)
            exercise_logger.info(f"Exercise: {exercise} has been removed from exercises list")
            return {"message": f"Exercise with {exercise_id} id has been removed"}
    else:
        exercise_logger.error(f"Exercise with following id: {exercise_id} hasn't been found")
        raise HTTPException(status_code=404, detail="Exercise not found")


@router.get("/part/{body_part}/")
def found_by_body_part(body_part: str) -> list[dict[str, str | int]] | None:
    if body_part is None:
        exercise_logger.error("Required parameter 'body part' is missing")
        raise HTTPException(status_code=400, detail="Parameter 'body_part' is required and missing")
    all_body_part_exr = [exercise for exercise in exercises if exercise["body_part"] == body_part]
    exercise_logger.info(f"Returned list of all exercises, for following body part: {body_part}")
    return all_body_part_exr
