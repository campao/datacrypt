import praw
import pandas as pd
import requests
import json

reddit = praw.Reddit(client_id='c7FULYsyNCm3dw', client_secret='9JoeyVyZLGoZssNXCsHjUAN8a0o', user_agent='Reddit WebScrapping')

def getPushshiftData(after, sub, before):
    url = 'https://api.pushshift.io/reddit/search/submission?&size=10&after='+str(after)+'&before='+str(before)+'&subreddit='+str(sub)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']

#list of post ID's
post_ids = []
#list of post texts
post_text = []
post_text.append("\n")
#Subreddit to query
sub='btc'
# Unix timestamp of date to crawl from.
# 2018/04/01
after = "2d"
before = "1d"

data = getPushshiftData(after, sub, before)

# Will run until all posts have been gathered 
# from the 'after' date up until todays date
while len(data) > 0:
    for submission in data:
        post_ids.append(submission["id"])
        post = reddit.submission(submission["id"])
        post_text.append(post.selftext)
        print(post.selftext)
    # Calls getPushshiftData() with the created date of the last submission
    data = getPushshiftData(sub=sub, after=data[-1]['created_utc'], before=before)


obj = {
    "sub" : sub,
    "id" : post_ids,
    "text" : post_text
}
# Save to json for later use
with open("submissions.json", "w") as jsonFile:
    json.dump(obj, jsonFile)
