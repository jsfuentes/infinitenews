import asyncio
import shutil
import threading
import urllib.request
import os

from pathlib import Path

from .aws_manager import AWSManager
from .terminal_colors import bcolors

SAVED_VIDS_PATH = os.path.join(os.getcwd(), 'videos/saved/')
NUM_DOWNLOADED_VIDS = 2  # This number MUST be less than the total num of vids in s3 or the script will try to download the playing video while its playing


class VideoFileManager:
    def __init__(self, videos_deque, up_next_deque):
        self.videos_deque = videos_deque
        self.up_next_deque = up_next_deque
        self.aws_manager = AWSManager()

    # Checks if theres new videos to add to deque
    def refresh_videos_deque(self):
        queued_vid_files_set = set(self.videos_deque)
        # available_vid_files = list(absoluteFilePaths("videos/"))
        available_vid_files = self.aws_manager.get_all_videos()

        new_videos_added = []
        for v in available_vid_files:
            if v not in queued_vid_files_set:
                self.videos_deque.appendleft(v)
                new_videos_added.append(v)

        print(f'New videos to queue: {new_videos_added}')

    def _download_video_from_s3(self, video_name):
        save_vid_path = os.path.join(SAVED_VIDS_PATH, video_name)
        dir_name = os.path.dirname(save_vid_path)
        Path(dir_name).mkdir(parents=True, exist_ok=True)

        urllib.request.urlretrieve(self.aws_manager.construct_url(video_name), save_vid_path)

    def _remove_vid_locally(self, video_name):
        vid_path = os.path.join(SAVED_VIDS_PATH, video_name)
        if os.path.exists(vid_path):
            print("Deleting video", vid_path)
            os.remove(vid_path)
        else:
            print(f"{bcolors.FAIL}Cant delete vid. The file does not exist{bcolors.ENDC}", vid_path)

    async def _periodically_refresh_videos_deque(self):
        while True:
            await asyncio.sleep(60)
            self.refresh_videos_deque()

    def get_next_vid(self, last_vid=None):
        # [up_next] [videos_deque]
        # [1,2] [3,4,5,1,2] -> [2,3] [4,5,1,2,3]
        print("COMP", self.up_next_deque, self.videos_deque)
        next_vid = self.up_next_deque.popleft()
        later_vid = self.videos_deque.popleft()
        self.videos_deque.append(later_vid)
        self.up_next_deque.append(later_vid)

        # Delete, then download to avoid deleting a vid thats in the up_next (edge case)
        if last_vid is not None:
            self._remove_vid_locally(last_vid)
        print(f"{bcolors.OKBLUE}Pre-downloading vid in bg{bcolors.ENDC}", later_vid)
        thr = threading.Thread(target=self._download_video_from_s3, args=([later_vid]), kwargs={})
        thr.start()
        # self._download_video_from_s3(later_vid)

        return os.path.join(SAVED_VIDS_PATH, next_vid)

    def start_managing_videos(self):
        if os.path.exists(SAVED_VIDS_PATH) and os.path.isdir(SAVED_VIDS_PATH):
            shutil.rmtree(SAVED_VIDS_PATH)

        Path(SAVED_VIDS_PATH).mkdir(parents=True, exist_ok=True)

        self.refresh_videos_deque()

        # Download all the videos in the up next queue
        for i in range(min(NUM_DOWNLOADED_VIDS, len(self.videos_deque))):
            vid = self.videos_deque.popleft()
            self.videos_deque.append(vid)
            self.up_next_deque.append(vid)
            self._download_video_from_s3(vid)
