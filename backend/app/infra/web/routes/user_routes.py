from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.post(path="/", response_model=)