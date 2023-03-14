import boto3
import os


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


def get_base_file_name(file_name):
    return os.path.splitext(os.path.basename(file_name))[0]


def get_new_audio_urls():
    audios = [get_base_file_name(o.key) for o in all_objects_raw("mp3")]
    videos = [get_base_file_name(o.key) for o in all_objects_raw("mp4")]

    # print(audios)
    # print(videos)

    new_audios = []
    for audio in audios:
        isVideo = False
        for video in videos:
            if video.find(audio) != -1:
                isVideo = True
                break

        if not isVideo:
            new_audios.append(audio)

    # print(new_audios)

    new_audio_urls = []
    for audio in new_audios:
        full_audio_name = f"/{audio}.mp3"
        for o in all_objects("mp3"):
            if o.find(full_audio_name) != -1:
                new_audio_urls.append(o)

    return new_audio_urls


def get_topic_text_from_url(url, bucket_name="interdimensional-news"):
    base_file_name = get_base_file_name(url)
    object_key = f"default/topic/{base_file_name}.txt"

    client = boto3.client('s3')
    resp = client.get_object(Bucket=bucket_name, Key=object_key)
    topic = str(resp["Body"].read().decode())
    return topic


def get_script_text_from_url(url, bucket_name="interdimensional-news"):
    base_file_name = get_base_file_name(url)
    object_key = f"default/scripts/{base_file_name}.txt"

    client = boto3.client('s3')
    resp = client.get_object(Bucket=bucket_name, Key=object_key)
    topic = str(resp["Body"].read().decode())
    return topic


if __name__ == '__main__':
    new_urls = get_new_audio_urls()
    print(new_urls, len(new_urls))
    # for url in new_urls:
    #     script = get_script_text_from_url(url)
    #     print(url, script)
