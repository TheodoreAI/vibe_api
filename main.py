import dash
import flask
from flask import request
import dash_html_components as html
import pandas as pd
from flask import jsonify
import plotly.graph_objects as go
import os
from imdb import IMDb
import wikipedia
from csv import writer
from nltk.sentiment import SentimentIntensityAnalyzer

# I'm going to pass my own Flask app server instance into Dash so I can make GET requests with Flask server
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
app.layout = html.Div('The Vibe Service:')


class Sentiment:
    """The following class is used to perform sentiment analysis on input strings.
    sentiment_analysis_function() relies on a long string input and on analyzing it as a whole.
    This will not be as accurate as taking in string and analyzing it by sentences.
    sentiment_analysis_per_sentence() will rely on parsing the input string from one period to the next and analyzing each sentence.
    sentiment_analysis_sentence_stats() will take an average of the neg, pos, neu, compound value and output this.

    Future To Do:
    1. Add a stopwords() functionality that removes stopwords: stopwords are english words that don't change the meaning of sentences and can be removed.
    2. Implement the stop words on the input text object
    3. Run the new analysis

    """

    def __init__(self, json_object):
        self.json_object = json_object

    def print_json_object(self):
        """This function will begin the sentiment analysis."""
        print(self.json_object)

    def sentiment_analysis_function(self):
        """This function takes the json_object and performs a sentiment analysis using the nltk
        my dict object has the following parameters:
        title: title of something they want analyzed so that the data has a heading
        input_text: the actual text being analyzed"""

        print("Text being analyzed: " + self.json_object['input_text'])
        input_text = self.json_object['input_text']
        sia = SentimentIntensityAnalyzer()
        print(len(self.json_object))

        sentiment_scores = sia.polarity_scores(input_text)
        print("scores " + str(sentiment_scores))

        return sentiment_scores

    def sentiment_analysis_sentence_stats(self, list_sentiment_values):
        """This takes a list of sentiment values (list of dictionary objects)
        It will output the average of the pos, neg, neu, compound for each sentence:
        Average will be calculated using the following equation:
        """
        neg_list = []
        pos_list = []
        neu_list = []
        compound_list = []

        # Getting the values of each and then separating them
        for obj in list_sentiment_values:

            if obj['neg']:
                neg_list.append(obj['neg'])
            if obj['pos']:
                pos_list.append(obj['pos'])
            if obj['neu']:
                neu_list.append(obj['neu'])

            if obj['compound']:
                compound_list.append(obj['compound'])

        # Now I will find the average using the sum() and len() functions for each sentiment value

        neg_avg = sum(neg_list)/len(neg_list)
        neu_avg = sum(neu_list)/len(neu_list)
        pos_avg = sum(pos_list)/len(pos_list)
        compound_avg = sum(compound_list)/len(compound_list)

        # Building my object again:
        # Rounding to 3 decimals.
        sentiment_object_n_sentences = {'neg': round(neg_avg, 3), 'neu': round(neu_avg, 3), 'pos': round(pos_avg, 3), 'compound': round(compound_avg, 3)}


        return sentiment_object_n_sentences


    def sentiment_analysis_per_sentence(self):
        """This function takes the json_object from the /sentiment-analysis-long url.
        It will perform a more detailed analysis on larger text structures.
        my dict object has the following parameters:
        title: title of something they want analyzed so that the data has a heading
        input_text: the actual text being analyzed
        Good parsing tip from: https://stackoverflow.com/questions/17618149/divide-string-by-line-break-or-period-with-python-regular-expressions"""

        input_text = self.json_object['input_text']
        sentences = [x for x in map(str.strip, input_text.split('.')) if x]

        sia = SentimentIntensityAnalyzer()
        # Getting the values:
        # Setting a list to hold all the sentiment_scores
        sentiment_scores = []
        for sentence in sentences:
            sentiment_scores.append(sia.polarity_scores(sentence))

        print(sentiment_scores)

        output_objects = self.sentiment_analysis_sentence_stats(
            sentiment_scores)  # summoning the following function to perform the statistics

        return output_objects




@server.route('/sentiment-analysis-long', methods=['POST'])
def post_request_data_long():
    """This GET request will take two parameters: title and string in that order.
    Learned to use post requests on flask using: https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask"""

    json_object = request.get_json()

    # Pass the json_object to the Sentiment Class object
    sa = Sentiment(json_object)
    long_analysis = sa.sentiment_analysis_per_sentence()

    # run the sentiment analysis with the sa_function
    return long_analysis


@server.route('/sentiment-analysis-short', methods=['POST'])
def post_request_movie_data_short():
    """This route handles the request for data analysis for string examples of max 500 characters long."""
    json_object = request.get_json()

    # pass the json_object to the Sentiment Class object
    sa = Sentiment(json_object)
    sentiment_scores_short = sa.sentiment_analysis_function()
    return sentiment_scores_short


if __name__ == '__main__':
    server.run(debug=True, port=3000)
