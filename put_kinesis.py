import boto3
from sklearn.datasets import fetch_20newsgroups
from random import *
from config import kinesis_stream_name as ksn
import time

categories = ['alt.atheism', 'sci.space', 'comp.graphics',
              'rec.motorcycles', 'sci.electronics']
news = fetch_20newsgroups(remove=("headers", "footers", "quotes"),
                          categories=categories)
kinesis = boto3.client("kinesis")

def handle_kinesis():
    response = kinesis.put_record(
        Data=news.data[randint(0, len(news)-1)],
        StreamName=ksn,
        PartitionKey="partition_1"
    )
i = 0
while True:
    i += 1
    handle_kinesis()
    print "Putting Record %d into Kinesis" %(i)
    if i % 10 == 0:
        time.sleep(1)
