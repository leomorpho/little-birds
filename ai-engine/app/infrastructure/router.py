from fastapi import APIRouter

router = APIRouter()



@router.post("/sites/parsebody", tags=[""])
async def parse_body():
    return {"result": "Wow!"}