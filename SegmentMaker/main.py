from segment import UpgradedSegment, DefaultSegment, TuckerSegment
from audio import create_audio_file


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    default_segment = UpgradedSegment()
    scripts = default_segment.generate_scripts(7)
    # print(scripts)

    scripts_to_generate = []
    for (timestamp, topic, script) in scripts:
        print(timestamp, "\n", topic, "\n=======================\n", script)
        nval = ""
        while nval == "":
            nval = input("Enter 1 to generate audio: ")
        nval = int(nval)

        if nval == 1:
            print("Adding this script...")
            scripts_to_generate.append((timestamp, topic, script))
        else:
            print("Skipping this script...")

    for (timestamp, topic, script) in scripts_to_generate:
        print("Generating audio for", topic)
        audio_file = create_audio_file(timestamp, script)
        print(audio_file)

    # tucker_segment = TuckerSegment()
    # tucker_segment.generate_script()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
