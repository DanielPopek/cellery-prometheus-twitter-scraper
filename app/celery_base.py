from celery import Celery
from celery.schedules import crontab
from docker_logs import get_logger
from registry import *
import twint
import time
from datetime import datetime
from multiprocessing.sharedctypes import Value


logging = get_logger("task")
logging.propagate = False

app = Celery()

YEAR = Value('i', 2019)
MONTH = Value('i', 11)
DAY = Value('i', 13)
HOUR = Value('i', 20)
MIN = Value('i', 38)
SEC = Value('i', 23)

def get_current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def create_datetime_string():
    hour=append_zeros(HOUR.value)
    min=append_zeros(MIN.value)
    sec=append_zeros(SEC.value)
    return f"{YEAR.value}-{MONTH.value}-{DAY.value} {hour}:{min}:{sec}"

def append_zeros(value):
    if value<10:
        return f"0{value}"
    else:
        return value

def extract_values_from_datetime(date):
    return date.year,date.month,date.day,date.hour,date.minute,date.second

def set_new_time_values(y,mo,d,h,mi,s):
    YEAR.value=y
    MONTH.value=mo
    DAY.value=d
    HOUR.value=h
    MIN.value=mi
    SEC.value=s

def update_latest_date(tweets):
    if tweets.shape[0]>0:
        date_from_tweets=get_latest_date_from_tweets(tweets)
        current = datetime.strptime(create_datetime_string(), '%Y-%m-%d %H:%M:%S')
        tweets_date = datetime.strptime(date_from_tweets, '%Y-%m-%d %H:%M:%S')
        if tweets_date>current :
            y,mo,d,h,mi,s= extract_values_from_datetime(tweets_date)
            set_new_time_values(y,mo,d,h,mi,s)

def get_latest_date_from_tweets(tweets):
    return tweets.sort_values(by=['date'], ascending=False)['date'][0]

y,mo,d,h,mi,s=extract_values_from_datetime(datetime.now())
set_new_time_values(y,mo,d,h,mi,s)

@app.on_after_configure.connect
def periodic_task(sender, **kwargs):
    sender.add_periodic_task(10.0, scrap_tweets_from_location.s('new york'))


@app.task(bind=True, name='scrap_tweets_of_user')
def scrap_tweets_from_location(self, city):
    current=create_datetime_string()
    logging.info(f"MEMORY {current} ")
    since=get_current_time()
    # since=current
    c=prepare_twint_request(since,city)
    start=time.time()
    twint.run.Search(c)
    elapsed=time.time()-start
    data = twint.storage.panda.Tweets_df
    logging.info(f"SCRAPPING BEGGINING FROM {since} ")
    logging.info(f"SCRAPPED PORTION: {data.shape[0]} TIME ELAPSED:{elapsed}")
    update_latest_date(data)
    update_metrics(data,elapsed)



def prepare_twint_request(since,city):
    c = twint.Config()
    c.Near=city
    c.Since = since
    c.Hide_output = True
    c.Stats = False
    c.Format = "Date: {date} | Time: {time} | Tweet: {tweet}"
    c.Pandas = True
    return c

def update_metrics(data,elapsed):
    update_average_request_time(data.shape[0],elapsed)
    update_time_histogram(data.shape[0],elapsed)
    increase_tweets_counter(data.shape[0])
    update_tweets_histogram(data.shape[0])
    update_tweets_average_length(data)