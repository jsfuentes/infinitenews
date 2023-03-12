from .Wav2Lip.inference2 import Inference
from .SegmentMaker.segment import UpgradedSegment, DefaultSegment, TuckerSegment
from .SegmentMaker.audio import create_audio_file
from .SegmentMaker.image import add_images_to_video
from .SegmentMaker.aws import put_content


def main():
    while True:
        try:
            default_segment = UpgradedSegment()
            scripts = default_segment.generate_scripts(2)
            print("Generated 2 scripts")
            for (timestamp, topic, script) in scripts:
                print(timestamp, topic, script)
                audio_url = create_audio_file(timestamp, script)
                output_file = "results/{file_name}_v1.mp4"
                inference = Inference("./Wav2Lip/wav2lip.pth", "./Wav2Lip/news_reporter_beta.mp4",
                                      audio_url, output_file)

                inference.run()
                print("Finished inference")

                new_video = add_images_to_video(topic, output_file)
                print("Finished adding images to video")

                with open(new_video, 'rb') as f:
                    bytes = f.read()
                    put_content(bytes, object_key=f"default/{timestamp}.mp4")
                    print("Finished uploading video")

        except Exception as e:
            print(e)
            continue


if __name__ == "__main__":
    main()
