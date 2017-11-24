# Garfield
AWS framework to stream, classify, index and store it using Kinesis, S3, ElasticSearch and Lambda.

[1]: http://boto3.readthedocs.io/en/latest/guide/quickstart.html#configuration
## Install Instructions

1. Since, we are using boto3 to access AWS components, follow all the instructions on this [page][1].

2. Install all python dependencies.
```bash
pip install requirements.txt
```
3. Update the config in `config.py` with your s3_host, kinesis_stream and Elastic Search endpoint.
4. Upload `models/nb.model` to your s3 bucket.

## Usage
1. Run the `get_kinesis` script and wait for it to be ready. This will classify, index and store the records in kinesis stream. Sometimes, it takes a little while before it starts consuming the stream, so please be patient.
```python
python get_kinesis.py
```
2. To create a stream of data into kinesis, run `put_kinesis` script in another terminal.
```python
python put_kinesis.py
```
