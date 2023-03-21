import argparse
import sys

from segment import UpgradedSegment, DefaultSegment, BananaSegment
from audio import create_audio_file


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-s', '--segment', type=str, default="upgraded",
                        help='Segment type. Options are upgraded | bananaqa')

    #creates audio, default value is False
    parser.add_argument('-a', '--audio', action = "store_true",default = "False" ,help = "Generate Audio")

    args = parser.parse_args()
    my_segment = UpgradedSegment()
    
    if args.segment == "bananaqa":
        my_segment = BananaSegment()

    skip_audio = args.audio == True

    print("MY NAME IS", my_segment.eleven_voice_name)

    print("WELCOME! Use 'y' and 'n' to accept/reject topic/script and 'next' or anything else to advance to next step")
    print("Start with generating topics")
    phase = 0

    topics_to_generate = []
    scripts_to_generate = []
    try:
        while phase == 0:
            topics = my_segment.generate_topics(5)

            for topic in topics:
                print("===========\n", topic)
                nval = ""
                while nval == "":
                    nval = input("Accept topic y/n: ")

                if nval == "y":
                    print("Adding this topic...")
                    topics_to_generate.append(topic)
                elif nval == "n":
                    print("Skipping this topic...")
                else:
                    phase += 1
                    break
    except:
        print("Some error occured")

    print("Advancing to script generation for the",
          len(topics_to_generate), "topics")
    try:
        for topic in topics_to_generate:
            is_complete = False
            while not is_complete:
                (script_name, script) = my_segment.generate_script(topic)
                print(script_name, "\n=======================\n", script)

                nval = ""
                while nval == "":
                    nval = input("Accept script y/r/n: ")

                if nval == "y":
                    print("Adding this script...")
                    scripts_to_generate.append((script_name, topic, script))
                    is_complete = True
                elif nval == "r":
                    print("Regenerating this script...")
                elif nval == "n":
                    print("Skipping this topic...")
                    break
                else:
                    phase += 1
                    break

            if phase != 1:
                break
    except:
        print("Some error occured")

    print("Advancing to audio generation for",
          len(scripts_to_generate), "scripts")
    
    if skip_audio : 
        print("With audio argument - audio will be generated!")
        for (script_name, topic, script) in scripts_to_generate:
            # audio_file = create_audio_file(script_name, script, name_of_voice=my_segment.eleven_voice_name)
            print("Generating audio for", topic)
    else :
        print("By default, with no audio argument - audio will not be generated!")

    print("Finished!")

    # tucker_segment = TuckerSegment()
    # tucker_segment.generate_script()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
