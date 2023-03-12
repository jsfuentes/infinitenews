import boto3


def all_objects_raw(filter="mp4", bucket_name="interdimensional-news"):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    objects = []
    for obj in bucket.objects.all():
        if obj.key.endswith(filter):
            objects.append(obj)

    return objects


def all_objects(filter="mp4", bucket_name="interdimensional-news"):
    return [construct_url(obj.key, bucket_name) for obj in all_objects_raw(filter, bucket_name)]


def get_object(object_key="default/audio/space_whales.mp3", file_name="test33.mp3", bucket_name="interdimensional-news"):
    client = boto3.client('s3')

    resp = client.get_object(Bucket=bucket_name, Key=object_key)
    all_binary = resp["Body"].read()

    with open(file_name, "wb") as f:
        f.write(all_binary)

    return file_name

# "audio/mp3"


def put_content(body, content_type="video/mp4", object_key="default/test3.mp4", bucket_name="interdimensional-news"):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.put_object(Key=object_key, Body=body, ContentType=content_type)
    print(f"Successfully uploaded {object_key} to S3")


def construct_url(object_key, bucket_name="interdimensional-news"):
    url = "https://%s.s3.amazonaws.com/%s" % (bucket_name, object_key)
    return url

# print(all_objects("mp3"))
