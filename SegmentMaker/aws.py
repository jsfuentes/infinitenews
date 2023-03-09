import boto3


def all_objects(bucket_name="interdimensional-news"):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    all_urls = [construct_url(bucket_name, obj.key)
                for obj in bucket.objects.all()]
    return all_urls


def construct_url(bucket_name, object_key):
    url = "https://%s.s3.amazonaws.com/%s" % (bucket_name, object_key)
    return url


def put_object(bucket_name="interdimensional-news", object_key="test.txt", body="hello world"):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.put_object(Key=object_key, Body=body)
    return construct_url(bucket_name, object_key)

# print(all_objects())
