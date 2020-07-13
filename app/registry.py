from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, CollectorRegistry, multiprocess
from prometheus_client import Counter, Histogram,Gauge

REGISTRY = CollectorRegistry()
multiprocess.MultiProcessCollector(REGISTRY)

TWEETS_COUNTER = Counter(
    'tweets_counter', 'Global count of tweets',registry=REGISTRY
)

TWEETS_COUNTS_HISTOGRAM = Histogram('tweets_counts_histogram', 'Tweets per request histogram',
    registry=REGISTRY
)

TWEETS_AVERAGE_REQUEST_TIME = Gauge(
    'tweets_average_fetch_time_gauge', 'Average time of fetching one tweet',['param'],registry=REGISTRY
)

TWEETS_TIME_HISTOGRAM = Histogram('tweets_time_histogram', 'Histogram of time per tweet',
    registry=REGISTRY
)

TWEETS_AVERAGE_LENGHT=Gauge(
    'tweets_average_length', 'Averge length of specific tweet',['param'],registry=REGISTRY
)

def update_average_request_time(size,elapsed):
    if size>0:
        TWEETS_AVERAGE_REQUEST_TIME.labels('average').set(elapsed/size)

def increase_tweets_counter(value):
    TWEETS_COUNTER.inc(value)

def update_tweets_histogram(value):
    TWEETS_COUNTS_HISTOGRAM.observe(value)

def update_time_histogram(size,elapsed):
    if (size > 0):
        TWEETS_TIME_HISTOGRAM.observe(elapsed/size)

def update_tweets_average_length(tweets):
    size=tweets.shape[0]
    if size>0:
        tweet_texts=tweets['tweet'].tolist()
        tweets_lenghts=[len(tweet) for tweet in tweet_texts]
        summed_lenghts=sum(tweets_lenghts)
        TWEETS_AVERAGE_LENGHT.labels('lenght').set(summed_lenghts/size)

