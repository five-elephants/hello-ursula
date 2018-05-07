import boto3
import os

bucket = 'hello-ursula-data'


def download_all_to(path):
    s3 = boto3.resource('s3')
    for obj in s3.Bucket(bucket).objects.all():
        fn = os.path.join(path, obj.key)
        if os.path.exists(fn):
            print("Skipping {}".format(fn))
        else:
            print("Download {} ...".format(fn))
            s3.meta.client.download_file(bucket, obj.key, fn)

