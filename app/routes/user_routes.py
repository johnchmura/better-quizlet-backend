from fastapi import APIRouter

router = APIRouter()


@router.get("/users/RICK", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]