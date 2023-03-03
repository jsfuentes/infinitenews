from dotenv import load_dotenv

from SegmentMaker.segment import TuckerSegment

load_dotenv()  # take environment variables from .env.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tucker_segment = TuckerSegment()
    tucker_segment.generate_script()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
