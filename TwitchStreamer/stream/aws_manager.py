import boto3


class AWSManager:
    def __init__(self, bucket_name="interdimensional-news"):
        self.bucket_name = bucket_name

    def get_all_videos(self):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(self.bucket_name)
        all_vids = list([f.key for f in filter(lambda f: "mp4" in f.key, list(bucket.objects.all()))])
        # print("Fetched all videos in s3 as ", all_vids)
        return all_vids

    def construct_url(self, object_key):
        url = "https://%s.s3.amazonaws.com/%s" % (self.bucket_name, object_key)
        return url

    # def all_objects(self, bucket_name="interdimensional-news"):
    #     s3 = boto3.resource('s3')
    #     bucket = s3.Bucket(bucket_name)
    #     all_urls = [self.construct_url(bucket_name, obj.key)
    #                 for obj in bucket.objects.all()]
    #     return all_urls

    # def construct_url(self, bucket_name, object_key):
    #     url = "https://%s.s3.amazonaws.com/%s" % (bucket_name, object_key)
    #     return url
