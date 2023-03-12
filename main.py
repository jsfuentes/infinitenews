from .Wav2Lip.inference2 import Inference
from .SegmentMaker.image import add_images_to_video
from .SegmentMaker.aws import put_content, get_new_audio_urls, get_base_file_name, get_topic_text_from_url


def main():
    while True:
        try:
            new_audio_urls = get_new_audio_urls()
            for audio_url in new_audio_urls:
                base_file_name = get_base_file_name(audio_url)
                topic = get_topic_text_from_url(audio_url)

                output_file = "results/{base_file_name}_v1.mp4"
                inference = Inference("./Wav2Lip/wav2lip.pth", "./Wav2Lip/news_reporter_beta.mp4",
                                      audio_url, output_file)

                inference.run()
                print("Finished inference")

                new_video = add_images_to_video(topic, output_file)
                print("Finished adding images to video")

                with open(new_video, 'rb') as f:
                    bytes = f.read()
                    put_content(
                        bytes, object_key=f"default/{base_file_name}.mp4")
                    print("Finished uploading video")

        except Exception as e:
            print(e)
            continue


if __name__ == "__main__":
    main()
