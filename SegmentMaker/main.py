from segment import UpgradedSegment, DefaultSegment, TuckerSegment
from audio import create_audio_file


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    default_segment = UpgradedSegment()
    scripts = default_segment.generate_scripts(2)
    print(scripts)
    # for (timestamp, script) in scripts:
    #     print(timestamp, script)
    #     create_audio_file(timestamp, script)

    # tucker_segment = TuckerSegment()
    # tucker_segment.generate_script()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
