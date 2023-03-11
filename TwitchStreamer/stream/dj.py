# HANG THE DJ
# HANG THE DJ
# HANG THE DJ
import collections
import os

import obsws_python as obs
from time import sleep
from .obs_manager import OBSManager
from .terminal_colors import bcolors
from .video_file_manager import VideoFileManager

NUM_DOWNLOADED_VIDS = 3


class DJ:
    def __init__(self, refresh_video_queue_interval=5):
        self.refresh_video_queue_interval = refresh_video_queue_interval

        # A deque containing all possible videos available to play
        self.videos_deque = collections.deque()

        # A smaller deque with 3 videos that represents the up next videos. We make
        # sure to have local copies of these videos ready to play
        self.up_next_deque = collections.deque()

        # Keeps video files dequeue up to date
        self.video_files_manager = VideoFileManager(self.videos_deque, self.up_next_deque)

        self.obs_manager = OBSManager()

    def _setup_next_video(self, last_vid=None):
        print("Starting new segment!")

        next_vid = self.video_files_manager.get_next_vid(last_vid)
        self.obs_manager.stage_new_vid(next_vid)

    def _setup_stream(self):
        self.video_files_manager.start_managing_videos()
        self.obs_manager.setup_obs(self._setup_next_video)

    def start_stream(self):
        self._setup_stream()
        self._setup_next_video()
        print(f"{bcolors.HEADER}Stream is ready! Start the stream in OBS when you're ready.{bcolors.ENDC}")
        while True:
            sleep(60)
            self.video_files_manager.refresh_videos_deque()
