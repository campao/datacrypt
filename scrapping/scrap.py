from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import os
from datetime import datetime

month_array = ("", "Janv", "Fevr", "Mars", "Avril", "Mai", "Juin", "Juil", "Aout", "Sept", "Oct", "Nov", "Dec")

class SeleniumClient(object):
    def __init__(self):
        #Initialization method.
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-setuid-sandbox')

        # you need to provide the path of chromdriver in your system
        self.browser = webdriver.Safari()

        self.base_url = 'https://twitter.com/search?'

        # Nombre de secondes entre chaque scroll
        self.SCROLL_PAUSE_TIME = 2

    def get_tweets(self, query):
        '''
        Function to fetch tweets.
        '''
        try:
            # Connexion à l'URL demandé
            self.browser.get(self.base_url+query)
            time.sleep(2)

            last_height = 0
            while True:
                # Scroll down to bottom
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")

                # Wait to load page
                time.sleep(self.SCROLL_PAUSE_TIME)
                self.browser.find_elements_by_css_selector("js-stream-item.stream-item.stream-item")

                # Calculate new scroll height and compare with last scroll height
                new_height = self.browser.execute_script("return document.body.scrollHeight")

                # break condition
                if new_height == last_height:
                    break
                last_height = new_height

            # Copie du contenu HTML dans une variable de BeautifullSoup4
            soup = bs(self.browser.page_source, features="html.parser")

            self.tweets = []
            # Récupération de tous les tweets dans la page chargée
            for li in soup.find_all("li", class_='js-stream-item'):
                # If our li doesn't have a tweet-id, we skip it as it's not going to be a tweet.
                if 'data-item-id' not in li.attrs:
                    continue
                else:
                    # Création de l'objet stockant tous les tweets
                    tweet = {
                        'tweet_id': li['data-item-id'],
                        'text': None,
                        'user_id': None,
                        'user_screen_name': None,
                        'user_name': None,
                        'created_at': None,
                        'retweets': 0,
                        'likes': 0,
                        'replies': 0
                    }

                    # Tweet Text
                    text_p = li.find("p", class_="tweet-text")
                    if text_p is not None:
                        tweet['text'] = text_p.get_text()
                        tweet['text'] = tweet['text'].replace('\n', ' ')
                        tweet['text'] = tweet['text'].replace('\r', ' ')

                        # Tweet User ID, User Screen Name, User Name
                        user_details_div = li.find("div", class_="tweet")
                        if user_details_div is not None:
                            tweet['user_id'] = user_details_div['data-user-id']
                            tweet['user_screen_name'] = user_details_div['data-screen-name']
                            tweet['user_name'] = user_details_div['data-name']

                        # Tweet date
                        date_span = li.find("span", class_="_timestamp")
                        if date_span is not None:
                            tweet['created_at'] = float(date_span['data-time-ms'])

                        # Tweet Retweets
                        retweet_span = li.select("span.ProfileTweet-action--retweet > span.ProfileTweet-actionCount")
                        if retweet_span is not None and len(retweet_span) > 0:
                            tweet['retweets'] = int(retweet_span[0]['data-tweet-stat-count'])

                        # Tweet Likes
                        like_span = li.select("span.ProfileTweet-action--favorite > span.ProfileTweet-actionCount")
                        if like_span is not None and len(like_span) > 0:
                            tweet['likes'] = int(like_span[0]['data-tweet-stat-count'])

                        # Tweet Replies
                        reply_span = li.select("span.ProfileTweet-action--reply > span.ProfileTweet-actionCount")
                        if reply_span is not None and len(reply_span) > 0:
                            tweet['replies'] = int(reply_span[0]['data-tweet-stat-count'])
                        self.tweets.append(tweet)
            # Création d'une data frame panda, facilite le traitement / l'écriture du fichier
            df = pd.DataFrame(self.tweets)
            return (df)

        except:
            self.browser.quit()
            print("Selenium - An error occured while fetching tweets.")

DATA_SAVE_DIRECTORY = "data"

if __name__ == "__main__":
    # Creation de l'instance selenium
    selenium = SeleniumClient()

    # Création du dossier ou son stocker les données
    if not os.path.exists(DATA_SAVE_DIRECTORY):
        os.mkdir(DATA_SAVE_DIRECTORY)
    # Pour chaque mois
    for month in range(1, 12):
        # Création d'un dossier
        if not os.path.exists("{}/{:02d}_{}".format(DATA_SAVE_DIRECTORY, month, month_array[month])):
            os.mkdir("{}/{:02d}_{}".format(DATA_SAVE_DIRECTORY, month, month_array[month]))
        # Pour chaque jour
        for day in range(1, 31):
            now = datetime.now()
            print("{}: {}".format(now.strftime("%H:%M:%S"), month_array[month]))

            # Appel de la fonction permettant de scrapper
            df_res = selenium.get_tweets("f=tweets&q=bitcoin%20BTC%20until%3A2018-{:02d}-{:02d}%20since%3A2018;-{:02d}-{:02d}".format(month, day + 1, month, day))

            # Création et affichage du fichier
            df_res.to_csv("{}/{:02d}_{}/{:02d}_data_{}.csv".format(DATA_SAVE_DIRECTORY, month, month_array[month], day, month_array[month]), index=False, encoding='utf-8')
            print("Number of tweets writen : {}".format(df_res.shape[0]))
    print("La lecture dans le fichier a bien été réalisée")
    selenium.browser.quit()