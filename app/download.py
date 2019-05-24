import boto3
import pathlib
import exrex
import os

class Downloader():
    """Downloads bad rows based on a date regex
    E.g. pass in 2019-05-1[0-9]
    To download all dates between 2019-05-10 and 2019-05-19


    """
    def __init__(self, bucket_name, filter, local_path='download/', filter_path='enriched/bad/run='):
        self.filter =  filter_path + filter
        self.aws_access_key_id = os.environ['ACCESS_KEY_ID']
        self.aws_secret_access_key = os.environ['SECRET_ACCESS_KEY']
        self.local_path = local_path
        self.bucket_name = bucket_name
        self.prefixes = list(exrex.generate(filter_path + r'%s' % filter))
        print(self.prefixes)

    def run(self):
        s3 = boto3.resource('s3',
                            aws_access_key_id=self.aws_access_key_id,
                            aws_secret_access_key=self.aws_secret_access_key)
        bucket = s3.Bucket(self.bucket_name)
        filenames = []
        print("Downloading files")
        for prefix in self.prefixes:
            for file in bucket.objects.filter(Prefix='%s' % (prefix)).all():
                if '_SUCCESS' not in file.key:
                    filepath = self.local_path+'/'.join(file.key.split('/')[:-1])
                    filename = file.key.split('/')[-1:][0]
                    print(filepath)
                    pathlib.Path(filepath).mkdir(parents=True, exist_ok=True)
                    bucket.download_file(file.key, filepath+'/'+filename)
                    print("Downloaded %s to %s" % (file.key, filepath+'/'+filename))
