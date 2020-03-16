import sqlalchemy
import pymysql
from mysql import mysql.connector

class GCP_SQL():
    def __init__(self):
        print('before cnnecion ')
        config = {
            'user': 'root',
            'password': 'root',
            'host': 'localhost:8889',
            'database': 'inventory',
            'raise_on_warnings': True,
        }

        self.link = mysql.connector.connect(**config)
        print("connection done")
    def insertTweetsOfUsers(self, users_tweets):
        print('insert')
    def createStructureTweetsFromUsers(self):
        querry = "CREATE TABLE tweets_from_users ( `id` VARCHAR(256) NOT NULL , `created_at` DATE NOT NULL , `tweet` VARCHAR(256) NOT NULL , `retweet_count` INT NOT NULL , `favorite_count` INT NOT NULL ) ENGINE = InnoDB;"
        cursor = self.link
        print('avant la querry')
        cursor.execute(querry)
        print('apres la querry')
        self.link.commit()
        cursor.close()
