from threat.utils import *
from threat.nlp import *

from datetime import datetime, timedelta
from dotenv import dotenv_values

import threat_pb2
import threat_pb2_grpc

import grpc
from grpc_reflection.v1alpha import reflection

import logging
from concurrent import futures

# list of threats to be searched for in the tweets and news articles (can be extended)
THREATS = [
    'traffic', 'heavy traffic',  'accident',  'snow',  'curfew', 'pandemic',  'covid', 'flood',
    'hurricane', 'fire', 'earthquake',  'tornado',  'volcano',  'tsunami',  'drought',  'hail',
    'fog', 'heat wave',  'avalanche',  'landslide',  'cyclone',  'tropical storm',  'blizzard',
    'thunderstorm',   'wildfire',  'rain',  'storm',  'heavy rain',  'lockdown',  'quarantine',
    'corona', 'road accident', 'road block', 'road jam', 'road closure', 'traffic jam', 'rush',
    'congestion', 'rush', 'construction', 'overcrowding', 'festivals', 'celebration',  'rally', 'riot', 'strike']

SHIFT = 10**-6  # used to convert the coordinates to float


def scorer(lat, lng):
    today = datetime.now()  # get the current date
    # fetch tweets from the last 3 days
    yesterday = today - timedelta(days=3)

    # format the date to be used in the search query
    since_id = yesterday.strftime("%Y-%m-%d")  # since_id = "2020-12-01"
    until_id = today.strftime("%Y-%m-%d")  # until_id = "2020-12-04"

    config = dotenv_values('.env')  # load the environment variables
    twitter_api, newsapi, geolocator = init(
        config['BEARER_TOKEN'], config['NEWS_API'], config['API_KEY'])  # initialize the API objects

    # fetch the locale of the given coordinates
    sub_locality, locality = fetch_locale(geolocator, lat, lng)

    # fetch the tweets from the given locale
    tweets = fetch_tweets(
        twitter_api,
        f"{lat},{lng},20km",
        sub_locality,
        locality,
        THREATS,
        since_id,
        until_id)

    # fetch the news articles from the given locale
    news = fetch_news(
        newsapi,
        locality,
        THREATS,
        since_id,
        until_id)

    # get the average sentiment score
    score = 0
    for text in tweets + news:
        score += fetch_sentiment(text)
    score /= len(tweets + news)
    print(score)


class Threat(threat_pb2_grpc.ThreatServicer):
    def getThreatScore(self, request, context):
        lat = request.latitude / SHIFT  # "19.0765821802915"
        lng = request.longitude / SHIFT  # "72.8724884302915"
        score = scorer(lat, lng)
        return threat_pb2.ThreatResponse(score=score)


def serve():
    # set the port number
    port = '5001'

    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    SERVICE_NAMES = (
        threat_pb2.DESCRIPTOR.services_by_name['Threat'].full_name,
        reflection.SERVICE_NAME,
    )

    # add the Threat class to the server
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    # listen on port 50051
    server.add_insecure_port('[::]:' + port)

    # start the server
    server.start()
    print("Server started, listening on " + port)

    # keep the server running
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
