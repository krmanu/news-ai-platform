from textblob import TextBlob  ## Imports NLP library for sentiment analysis.

def analyze_sentiment(text):

    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    return "Neutral"