from typing import List, Dict
from fastapi import APIRouter, HTTPException, Depends
from fastapi.openapi.models import APIKey
from fastapi.security import api_key

from api.auth.apikey import get_api_key
from api.auth.oauthbearer import api_key_auth
from domain.liked_tweets.get_liked_tweets import get_data
from logger_config import log
from models.tweet import Tweet

router = APIRouter()


@router.get("/healthz", status_code=200)
def health_check():
    return {'healthcheck': 'Everything OK!'}


@router.get("/liked-tweets", response_model=List[Tweet], status_code=200)
def get_liked_tweets(api_key: APIKey = Depends(get_api_key)):
    try:
        log.debug('API Key used ', api_key=api_key)
        data: list[dict[str, str | None]] = get_data()
        liked_tweets = []
        for d in data:
            liked_tweets.append(Tweet(**d))

        log.info('API executed successfully')
        return liked_tweets
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.get("/liked-tweets-2", response_model=List[Tweet], status_code=200, dependencies=[Depends(api_key_auth)])
def get_liked_tweets_2():
    data: list[dict[str, str | None]] = get_data()
    liked_tweets = []
    for d in data:
        liked_tweets.append(Tweet(**d))

    return liked_tweets
