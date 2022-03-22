import uvicorn
from fastapi import FastAPI

from api import liked_tweet

app = FastAPI(title="Tweets-API")


def configure():
    app.include_router(liked_tweet.router, prefix="/v1", tags=["liked tweets"])


configure()

if __name__ == '__main__':
    uvicorn.run(app)
