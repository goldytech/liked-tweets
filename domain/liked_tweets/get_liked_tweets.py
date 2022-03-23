import random
from typing import List
from dapr.clients import DaprClient
import tweepy

from logger_config import log


def get_data() -> List[dict[str, str | None]]:
    try:

        with DaprClient() as d:
            key = "TWITTER_API_KEY"
            store_name = "secretstore"

            twitter_api_key = d.get_secret(store_name=store_name, key=key)
            log.debug("Twitter API Key retrieved", api_key=twitter_api_key.secret.get('TWITTER_API_KEY'))
            twitter_client = tweepy.Client(twitter_api_key.secret.get('TWITTER_API_KEY'))

            twit_user_id = twitter_client.get_user(username="goldytech")
            my_liked_tweets = twitter_client.get_liked_tweets(twit_user_id.data.data['id'], max_results=100,
                                                              media_fields=['preview_image_url'],
                                                              tweet_fields=['context_annotations', 'created_at'],
                                                              expansions=["attachments.media_keys", "author_id",
                                                                          "in_reply_to_user_id"])
            includes = my_liked_tweets.includes
            users = includes["users"]
            users = {user["id"]: user for user in users}
            media = {m["media_key"]: m for m in my_liked_tweets.includes['media']}
            random_tweets = random.sample(my_liked_tweets.data, 3)
            tweets_list = []

            for tweet in random_tweets:
                tweet_dict = {'text': f"{tweet.text}", 'username': users[tweet.author_id].username, 'id': tweet.id}
                tweet_dict['url'] = f"https://twitter.com/{tweet_dict['username']}/status/{tweet.id}"
                attachments = tweet.attachments
                if attachments is not None:
                    media_keys = attachments['media_keys']
                    tweet_dict["media_url"] = media[media_keys[0]].preview_image_url if media[
                        media_keys[0]].preview_image_url else ""

                tweets_list.append(tweet_dict)

            return tweets_list

    except Exception as e:
        log.error(e)
        raise e
