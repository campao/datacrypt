import pandas as pd
import tweepy
from tweepy import OAuthHandler

from GCP_SQL import GCP_SQL


class TwitterClient(object):
    def __init__(self):
        # Access Credentials
        consumer_key = 'yukvJ57xhaswhsXgWPRw4cByU'
        consumer_secret = 'cAF5ZI0QJbaVvTcFsrvWnb6QLqNl5AS6hxxMd2JlMk7dbRBrT9'
        access_token = '734812424566648834-qLfG7N5Yx0fWjGFLsCjFzxXTk9IKAjp'
        access_token_secret = '5lHhqIMTBEHLVhRlnjUp4WaylTH5vb70A11WR86Gw9XMh'

        try:
            # OAuthHandler object
            auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        except tweepy.TweepError as e:
            print(f"Error: Twitter Authentication Failed - \n{str(e)}")

            # Function to fetch tweets

    def get_tweets_from_hashtag(self, query, maxTweets=200):
        # empty list to store parsed tweets
        tweets = []
        sinceId = None
        max_id = -1
        tweetCount = 0
        tweetsPerQry = 200

        while tweetCount < maxTweets:
            try:
                if (max_id <= 0):
                    if (not sinceId):
                        new_tweets = self.api.search(q=query, count=tweetsPerQry, lang='en', result_type='popular')
                    else:
                        new_tweets = self.api.search(q=query, count=tweetsPerQry,
                                                     since_id=sinceId, lang='en', result_type='popular')
                else:
                    if (not sinceId):
                        new_tweets = self.api.search(q=query, count=tweetsPerQry,
                                                     max_id=str(max_id - 1), lang='en', result_type='popular')
                    else:
                        new_tweets = self.api.search(q=query, count=tweetsPerQry,
                                                     max_id=str(max_id - 1),
                                                     since_id=sinceId, lang='en', result_type='popular')
                if not new_tweets:
                    print("No more tweets found")
                    break

                for tweet in new_tweets:
                    parsed_tweet = {}
                    parsed_tweet['id'] = tweet.id
                    parsed_tweet['created_at'] = tweet.created_at
                    parsed_tweet['tweets'] = tweet.text
                    parsed_tweet['retweet_count'] = tweet.retweet_count
                    parsed_tweet['favorite_count'] = tweet.favorite_count
                    parsed_tweet['followers_count'] = tweet.user.followers_count
                    # appending parsed tweet to tweets list
                    if tweet.retweet_count > 0:
                        # if tweet has retweets, ensure that it is appended only once
                        if parsed_tweet not in tweets:
                            tweets.append(parsed_tweet)
                    else:
                        tweets.append(parsed_tweet)

                tweetCount += len(new_tweets)
                print("Downloaded {0} tweets".format(tweetCount))
                max_id = new_tweets[-1].id

            except tweepy.TweepError as e:
                print("Tweepy error : " + str(e))
                break
        print(tweets)
        pd.DataFrame(tweets).to_csv(
            "{}___{}__{}.csv".format(query[1:-1], tweets[0]["created_at"], tweets[len(tweets) - 1]['created_at']))
        return pd.DataFrame(tweets)

    def get_tweets_from_person(self, user_id):
        tweets = []
        tweetsPerQuerry = 200
        new_tweets = []
        oldest = -1

        print('user_id ' + user_id)
        new_tweets = self.api.user_timeline(id=user_id,
                                            count=200)
        for tweet in new_tweets:
            parsed_tweet = {}
            parsed_tweet['id'] = tweet.id
            parsed_tweet['created_at'] = tweet.created_at
            parsed_tweet['tweets'] = tweet.text
            parsed_tweet['retweet_count'] = tweet.retweet_count
            parsed_tweet['favorite_count'] = tweet.favorite_count
            parsed_tweet['followers_count'] = tweet.user.followers_count
            tweets.append(parsed_tweet)
        oldest = tweets[- 1]['id'] - 1

        while len(new_tweets) > 0 or tweets == []:
            new_tweets = self.api.user_timeline(id=user_id,
                                                count=200,
                                                max_id=oldest)
            for tweet in new_tweets:
                parsed_tweet = {}
                parsed_tweet['user_id'] = user_id
                parsed_tweet['id'] = tweet.id
                parsed_tweet['created_at'] = tweet.created_at
                parsed_tweet['tweets'] = tweet.text
                parsed_tweet['retweet_count'] = tweet.retweet_count
                parsed_tweet['favorite_count'] = tweet.favorite_count
                parsed_tweet['followers_count'] = tweet.user.followers_count
                tweets.append(parsed_tweet)
            if (len(tweets) != 0):
                oldest = tweets[-1]['id'] - 1
        return tweets

    def parse_users(self):
        # pd.DataFrame(tweets).to_csv("data/user/{}___{}__{}.csv".format(rows[1:], tweets[0]['created_at'], tweets[-1]['created_at']))
        df_users = pd.read_csv("data/twitter_users_reduced.csv", sep=';')
        sql = GCP_SQL()
        for rows in df_users['user_id']:
            res_from_api = self.get_tweets_from_person(rows)
            sql.insertTweetsOfUsers(res_from_api)

