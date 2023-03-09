import collections
import os
import pathlib
from time import sleep

import boto3
from dotenv import load_dotenv
import obsws_python as obs

load_dotenv()  # take environment variables from .env.

REFRESH_VIDEO_LIST_INTERVAL = 5
videos_deque = collections.deque()
obs_cl = obs.ReqClient(password=os.getenv("OBS_PASSWORD"))
obs_ev = obs.EventClient(password=os.getenv("OBS_PASSWORD"))

SCENE_NAME = "Scene"
SEGMENT_NAME = "Segment"

def all_objects(bucket_name="interdimensional-news"):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    all_urls = [construct_url(bucket_name, obj.key)
                for obj in bucket.objects.all()]
    return all_urls


def construct_url(bucket_name, object_key):
    url = "https://%s.s3.amazonaws.com/%s" % (bucket_name, object_key)
    return url

def absoluteFilePaths(directory):
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))



def poll_video_list_and_add_to_deque():
    queued_vid_files_set = set(videos_deque)
    # available_vid_files = list(absoluteFilePaths("videos/"))
    available_vid_files = list(filter(lambda f: "mp4" in f, all_objects()))

    new_videos_added = []
    for v in available_vid_files:
        if v not in queued_vid_files_set:
            videos_deque.appendleft(v)
            new_videos_added.append(v)

    print(f'New videos to queue: {new_videos_added}')


def add_next_video_to_scene(obs_cl):
    next_video = videos_deque.popleft()
    videos_deque.append(next_video)

    print("Playing", next_video)
    print("Current queue", videos_deque)
    obs_cl.set_input_settings(SEGMENT_NAME, {'is_local_file': False, 'input': next_video, 'input_format': "mp4"}, True)
    # obs_cl.set_input_settings(SEGMENT_NAME, {'local_file': next_video}, True)
    # obs_cl.set_input_settings(SEGMENT_NAME, {'url': next_video}, True)


def init_video_playback(obs_cl):
    poll_video_list_and_add_to_deque()

    scene_items = obs_cl.get_scene_item_list(SCENE_NAME)

    # If the segment exists from some previous run, remove it to start fresh
    segment_item_exists = False
    for si in scene_items.scene_items:
        if si["sourceName"] == SEGMENT_NAME:
            segment_item_exists = True
            break

    if not segment_item_exists:
        # obs_cl.create_input(SCENE_NAME, SEGMENT_NAME, "ffmpeg_source", {}, True)
        obs_cl.create_input(SCENE_NAME, SEGMENT_NAME, "ffmpeg_source", {}, True)
        # obs_cl.create_input(SCENE_NAME, SEGMENT_NAME, "browser_source", {"width": 1280, "height": 720}, True)

    add_next_video_to_scene(obs_cl)


def on_media_input_playback_ended(input_source):
    if input_source.input_name == SEGMENT_NAME:
        print("Starting new segment!")
        add_next_video_to_scene(obs_cl)


if __name__ == "__main__":
    init_video_playback(obs_cl)
    obs_ev.callback.register(on_media_input_playback_ended)
    while True:
        print("Checking if there's any videos I need to add to OBS...")
        poll_video_list_and_add_to_deque()
        print(f'Check complete. Sleeping for {REFRESH_VIDEO_LIST_INTERVAL} seconds')
        print("-----------------------------------------------------------------------")
        sleep(REFRESH_VIDEO_LIST_INTERVAL)
    # x = obs_cl.get_input_settings("Media Source")
    # print(vars(x))




































# def poll_video_list_and_add_scenes_to_obs(obs_cl):
#     # Fetch all the scenes currently in obs (the scene name will correspond to the video name bc we set it like that)
#     scene_names_set = set([s["sceneName"] for s in obs_cl.get_scene_list().scenes])
#
#     # Get all videos available for streaming
#     available_vid_files = os.listdir("videos/")
#     videos_to_add_to_obs = []
#     for vid_file in available_vid_files:
#         if vid_file not in scene_names_set:
#             videos_to_add_to_obs.append(vid_file)
#
#     print(f'New videos to add to OBS: {videos_to_add_to_obs}')
#     for v in videos_to_add_to_obs:
#         # TODO: Change this for s3 videos
#         full_vid_path = os.path.join(pathlib.Path().resolve(), "videos", v)
#         obs_cl.create_scene(v)
#
#         # 1. Scene name to add to 2. Input name (arbitrary but must be unique among inputs and scene names)
#         # 3. Input type 4. Settings 5. Enable?
#         scene_item = obs_cl.create_input(v, v + "_segment", "ffmpeg_source", {}, True)
#         obs_cl.set_input_settings(v + "_segment", {'local_file': full_vid_path}, True)
#
#         # TODO: If we needed to scale the video, we'd do something related to the below
#         # print(vars(obs_cl.get_scene_item_transform(v, scene_item.scene_item_id)))