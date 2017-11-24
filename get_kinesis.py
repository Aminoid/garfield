import boto3
import time
import uuid
import pickle
from elasticsearch import Elasticsearch, RequestsHttpConnection
from nltk.corpus import stopwords
from config import kinesis_stream_name as ksn, es_endpoint, s3_bucket, model_file_name

categories = ['alt.atheism', 'sci.space', 'comp.graphics',
              'rec.motorcycles', 'sci.electronics']
# AWS Clients
s3 = boto3.client("s3")
kinesis = boto3.client("kinesis")
es = Elasticsearch(
    hosts = [{'host': es_endpoint, 'port': 443}],
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

tmp_dir = './data'
stopwords = set(stopwords.words('english'))

def load_classifier():
    filename = '%s/%s' %(tmp_dir, str(uuid.uuid4()))
    s3.download_file(s3_bucket, model_file_name, filename)
    return pickle.load(open(filename, 'rb'))

def classify(data, clf):
    vectorizer, model = clf["vectorizer"], clf["model"]
    pred = model.predict(vectorizer.transform([data]))
    return pred[0]

def put_s3(data):
    unique = str(uuid.uuid4())
    filename = '%s/%s' %(tmp_dir, unique)
    f = open(filename, 'wb')
    f.write(data)
    f.close()
    s3.upload_file(filename, s3_bucket, unique)
    return unique

def create_es_index(filename, data, pred):
    clean_data = []
    for word in data.split():
        if word not in stopwords:
            clean_data.append(word)
    es.index(index="news", doc_type="news", body={
        'link': filename,
        'text': ' '.join(clean_data),
        'category': pred
    })
    return

def consume_kinesis():
    kinesis = boto3.client("kinesis")
    describe = kinesis.describe_stream(
        StreamName=ksn
    )
    shard_id = describe['StreamDescription']['Shards'][0]['ShardId']
    shard_it =  kinesis.get_shard_iterator(
        StreamName=ksn,
        ShardId=shard_id,
        ShardIteratorType="LATEST"
    )["ShardIterator"]
    i = 0
    print "=" * 60
    print "Ready to consume. Start putting into kinesis stream."
    print "Might take a while after records put into kinesis."
    print "=" * 60
    while True:
        out = kinesis.get_records(
            ShardIterator=shard_it,
            Limit=5
        )
        clf = load_classifier()
        for record in out['Records']:
            i += 1
            pred = categories[classify(record['Data'], clf)]
            filename = "https://s3.amazonaws.com/bt-7274/" + put_s3(record['Data'])
            print str(i), pred, filename
            create_es_index(filename, record['Data'], pred)

        time.sleep(1) # This is needed as there is a limit to number of requests we can make
        shard_it = out["NextShardIterator"]

consume_kinesis()
