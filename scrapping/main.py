from twitterClient import TwitterClient
from GCP_SQL import GCP_SQL

twiCli = TwitterClient()
sql = GCP_SQL()
# ret = twiCli.get_tweets_from_hashtag('"bitcoin"')
#users_tweets = twiCli.parse_users()
sql.createStructureTweetsFromUsers()
# sql.insertTweetsOfUsers(users_tweets)


