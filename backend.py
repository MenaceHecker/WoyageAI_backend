from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
import uvicorn

app = FastAPI()

# MongoDB Configuration
MONGO_URI = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URI)
db = client["video_db"]
collection = db["videos"]

@app.get("/video/search")
async def search_video(search_term: str):
    
    video_doc = await collection.find_one(
        {"title": {"$regex": search_term, "$options": "i"}}
    )
    # video_doc = await collection.find_one({"title": search_term}) #This one is case sensitive so resume != Resume


    if video_doc:
        return JSONResponse(
            status_code=200,
            content={
                "result": "success",
                "message": "Video found.",
                "data": {
                    "video_path": video_doc["s3_path"]
                }
            }
        )
    else:
        raise HTTPException(
            status_code=404,
            detail={
                "result": "failure",
                "message": "No matching video found.",
                "data": None
            }
        )

# This is where the main function serves as an entry point
def main():
    uvicorn.run("backend:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
