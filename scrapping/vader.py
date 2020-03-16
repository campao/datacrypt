from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

#### VADER ####
analyser = SentimentIntensityAnalyzer()
def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    print("{:-<40} {}".format(sentence, str(score)))


#### END OF VADER #####

#### TESTS #####

df = pd.read_csv('data.csv', error_bad_lines=False)
df.describe() # Permet d'afficher des statistiques sur la data frame
sentiment_analyzer_scores("i'am verry bad at work");
sentiment_analyzer_scores("super good");
sentiment_analyzer_scores("good");
sentiment_analyzer_scores("amazing");
sentiment_analyzer_scores("sucker");
