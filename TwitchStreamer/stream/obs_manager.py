import os

import obsws_python as obs

from .terminal_colors import bcolors

SCENE_NAME = "Scene"
SEGMENT_NAME = "Segment"


class OBSManager:
    def __init__(self):
        self.obs_cl = obs.ReqClient(password=os.getenv("OBS_PASSWORD"))
        self.obs_ev = obs.EventClient(password=os.getenv("OBS_PASSWORD"))
        self.setup_next_vid_fn = None

    def on_media_input_playback_ended(self, input_source):
        if input_source.input_name == SEGMENT_NAME:
            # print("SEGMENT END", vars(self.obs_cl.get_input_settings(input_source.input_name)))
            # input_settings
            finished_vid = self.obs_cl.get_input_settings(input_source.input_name).input_settings["local_file"]
            print(f"{bcolors.OKCYAN}Finished playback for vid{bcolors.ENDC}", finished_vid)
            print("---------------------------------")
            print("---------------------------------")
            if self.setup_next_vid_fn is not None:
                # TODO: pass in last vid to have it deleted
                self.setup_next_vid_fn(finished_vid)

    def setup_obs(self, setup_next_vid_fn):
        self.setup_next_vid_fn = setup_next_vid_fn

        # TODO: just create the scene if it doesn't exist
        scene_items = self.obs_cl.get_scene_item_list(SCENE_NAME)

        # If the segment exists from some previous run, remove it to start fresh
        segment_item_exists = False
        for si in scene_items.scene_items:
            if si["sourceName"] == SEGMENT_NAME:
                segment_item_exists = True
                break

        if not segment_item_exists:
            # obs_cl.create_input(SCENE_NAME, SEGMENT_NAME, "ffmpeg_source", {}, True)
            self.obs_cl.create_input(SCENE_NAME, SEGMENT_NAME, "ffmpeg_source", {}, True)
            # obs_cl.create_input(SCENE_NAME, SEGMENT_NAME, "browser_source", {"width": 1280, "height": 720}, True)

        self.obs_ev.callback.register(self.on_media_input_playback_ended)

    def stage_new_vid(self, vid):
        print(f"{bcolors.OKGREEN}Staging vid{bcolors.ENDC}", vid)
        self.obs_cl.set_input_settings(SEGMENT_NAME, {'is_local_file': True, 'local_file': vid, 'input_format': "mp4"},
                                       True)
