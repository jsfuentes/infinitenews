import boto3


def all_objects(filter="mp4", bucket_name="interdimensional-news"):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    all_urls = []
    for obj in bucket.objects.all():
        if obj.key.endswith(filter):
            all_urls.append(construct_url(bucket_name, obj.key))

    return all_urls


def construct_url(bucket_name, object_key):
    url = "https://%s.s3.amazonaws.com/%s" % (bucket_name, object_key)
    return url

# "audio/mp3"


def put_content(body, content_type="video/mp4", object_key="default/test3.mp4", bucket_name="interdimensional-news"):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.put_object(Key=object_key, Body=body, ContentType=content_type)
    print(f"Successfully uploaded {object_key} to S3")


# print(all_objects("mp3"))
