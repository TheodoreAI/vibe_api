import dash
import flask
from flask import request, jsonify
import dash_html_components as html
from flask_cors import CORS, cross_origin
import nltk
import json
import requests
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

# I'm going to pass my own Flask app server instance into Dash so I can make GET requests with Flask server
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
app.layout = html.Div('The Vibe Service:')

CORS(server)


class Sentiment:
    """The following class is used to perform sentiment analysis on input strings.
    sentiment_analysis_function() relies on a long string input and on analyzing it as a whole.
    This will not be as accurate as taking in string and analyzing it by sentences.
    sentiment_analysis_per_sentence() will rely on parsing the input string from one period to the next and analyzing each sentence.
    sentiment_analysis_sentence_stats() will take an average of the neg, pos, neu, compound value and output this.

    """

    def __init__(self, json_object):
        self.json_object = json_object

    def get_string_from_object(self):
        """Returns the string object."""

        return self.json_object

    def sentiment_analysis_function(self):
        """This function takes the json_object and performs a sentiment analysis using the nltk
        my dict object has the following parameters:
        title: title of something they want analyzed so that the data has a heading
        input_text: the actual text being analyzed"""

        input_text = self.json_object['input_text']
        sia = SentimentIntensityAnalyzer()
        sentiment_scores = sia.polarity_scores(input_text)
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
        # if the length of the input string is too short, then I will return the sentiment_analysis_function() because that one can run short sentences.
        if len(neg_list) == 0:
            print("Running the short version of the analysis.")
            return self.sentiment_analysis_function()
        elif len(neu_list) == 0:
            print("Running the short version of the analysis.")
            return self.sentiment_analysis_function()
        elif len(pos_list) == 0:
            print("Running the short version of the analysis.")
            return self.sentiment_analysis_function()
        elif len(compound_list) == 0:
            print("Running the short version of the analysis.")
            return self.sentiment_analysis_function()
        else:

            print("Running the long version of the analysis.")
            neg_avg = sum(neg_list) / len(neg_list)
            neu_avg = sum(neu_list) / len(neu_list)
            pos_avg = sum(pos_list) / len(pos_list)
            compound_avg = sum(compound_list) / len(compound_list)

            array_to_normalize = [neg_avg, neu_avg, pos_avg]

            # Building my object again:
            # Rounding to 3 decimals.
            sentiment_object_n_sentences = {'neg': round(neg_avg, 3), 'neu': round(neu_avg, 3),
                                            'pos': round(pos_avg, 3),
                                            'compound': round(compound_avg, 3)}
            return sentiment_object_n_sentences

    def sentiment_analysis_per_sentence(self):
        """This function takes the json_object from the /sentiment-analysis-long url.
        It will perform a more detailed analysis on larger text structures.
        my dict object has the following parameters:
        title: title of something they want analyzed so that the data has a heading
        input_text: the actual text being analyzed
        Good parsing tip from: https://stackoverflow.com/questions/17618149/divide-string-by-line-break-or-period-with-python-regular-expressions"""

        if self.json_object['input_text'] is None or self.json_object is None:
            return self.json_object
        else:
            input_text = self.json_object['input_text']

            sentences = [x for x in map(str.strip, input_text.split('.')) if x]

            sia = SentimentIntensityAnalyzer()
            # Getting the values:
            # Setting a list to hold all the sentiment_scores
            sentiment_scores = []
            for sentence in sentences:
                sentiment_scores.append(sia.polarity_scores(sentence))

            output_objects = self.sentiment_analysis_sentence_stats(
                sentiment_scores)  # summoning the following function to perform the statistics

            return output_objects

    def remove_punctuation(self, plot_str):
        """Removes the punctuation from string.
        Source: https://www.programiz.com/python-programming/examples/remove-punctuation"""

        punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

        no_punc = ""
        for char in plot_str:
            if char not in punc:
                no_punc = no_punc + char

        return no_punc

    def remove_stopwords(self, plot_str):
        """Removes the stopwords from my string."""

        plot_without_punc = self.remove_punctuation(plot_str)

        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(plot_without_punc)
        filtered_plot = [w for w in word_tokens if not w.lower() in stop_words]
        filtered_plot = []

        # remove stop words
        for w in word_tokens:
            if w not in stop_words:
                filtered_plot.append(w)
        string_plot = ' '.join(filtered_plot)
        return string_plot


@server.route('/sentiment-analysis-long', methods=['POST'])
@cross_origin(allow_headers=['Content-Type'])
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
@cross_origin(allow_headers=['Content-Type'])
def post_request_movie_data_short():
    """This route handles the request for data analysis for string examples of max 500 characters long."""
    json_object = request.get_json()

    # pass the json_object to the Sentiment Class object
    sa = Sentiment(json_object)
    sentiment_scores_short = sa.sentiment_analysis_function()
    return sentiment_scores_short


@server.route('/post-requests', methods=['POST'])
@cross_origin(allow_headers=['Content-Type'])
def post_request_user():
    json_object = request.get_json()
    sa = Sentiment(json_object)
    string_plot = sa.get_string_from_object()['input_text']
    filtered_txt = sa.remove_stopwords(string_plot)
    sia = SentimentIntensityAnalyzer()
    dict_out = sia.polarity_scores(filtered_txt)
    return dict_out


if __name__ == '__main__':
    server.run(debug=True, port=3000)
