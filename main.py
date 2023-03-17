from inference2 import Inference
from SegmentMaker.image import add_images_to_video
from SegmentMaker.aws import put_content, get_new_audio_urls, get_base_file_name, get_topic_text_from_url
import time


def main():
    while True:
        try:
            new_audio_urls = get_new_audio_urls()
            for audio_url in new_audio_urls:
                base_file_name = get_base_file_name(audio_url)
                topic = get_topic_text_from_url(audio_url)
                print("Processing ----", audio_url, base_file_name, topic)

                segment_name = "upgraded"
                if "bananaqa" in base_file_name:
                    segment_name = "bananaqa"
                    new_video = "results/{base_file_name}.mp4"
                    inference = Inference("./wav2lip.pth", "./banana_base.mp4",
                                          audio_url, new_video)

                    inference.main()
                    print("Finished inference")

                else:
                    segment_name = "upgraded"
                    print("Skipping because this segment is not banana", base_file_name)
                    continue
                    # TODO: clean up the duplication
                    output_file = "results/{base_file_name}_v1.mp4"
                    inference = Inference("./wav2lip.pth", "./base2min.mp4",
                                          audio_url, output_file)

                    inference.main()
                    print("Finished inference")

                    new_video = add_images_to_video(topic, output_file)
                    print("Finished adding images to video")

                with open(new_video, 'rb') as f:
                    bytes = f.read()
                    put_content(
                        bytes, object_key=f"default/{base_file_name}.mp4")
                    print("Finished uploading video")

            time.sleep(60)

        except Exception as e:
            print(e)
            continue


if __name__ == "__main__":
    main()
