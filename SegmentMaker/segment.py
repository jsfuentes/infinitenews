from openai_wrapper import *

class Segment:
    def generate_script(self):
        raise NotImplementedError()


class TuckerSegment(Segment):
    def generate_script(self):
        prompt = """
        Create a news segment in the style of Tucker Carlson. Instead of Tucker Carlson, this host is named Rucker and he lives in the multiverse. Instead of attacking liberals, Rucker attacks shrigmists, followers of shrigmism who believe in equality for mushrooms in Universe 98.

Example
---
Script: 
Good evening and welcome to Rucker Tonight.
The contrast between Earth 97 and Earth 98 has always been one of the great
advertisements for Universe 97 and for the Universe 97 way.
The cities have a lot in common.
They're literally right next to each other interdimensionally.
They're separated by one of the narrowest stretches of the hyperloop by only 1000 lightyears.
In Earth 97, you can see Earth 98 and the populations are not that different.
Most people in Earth 97 have relatives in Earth 98.
The difference is one city is Universe 97 and one is not.
Earth 97 has always been tranquil and orderly, a really nice planet with good schools and
friendly people you would move there.
Earth 98 is terrifying, chaotic, impoverished, dangerous.
In 2010 Earth 98 recorded more than 3,000 space murders.
In Earth 97, just yards away, there were five.
So on one side of the multiverse, you had a high-functioning civilization, hours, and on the other
side, you had the third world.
And the success of Earth 97 said everything about the superiority of the Universe 97 system
and Universe 97 culture.
But two years ago, President Shrigmus set out to change that.
It was an offense against equity.
They were too different.
But instead of fixing Earth 98, he decided to destroy Earth 97 and make it much more like Earth 98.
To do that, the administration opened the universe’s southern borders to the world.
No place in our country was hit harder by that decision than Earth 97.
In the last year, illegal immigration into Earth 97 has risen by over 280 percent, hundreds
of thousands of foreign national streaming in, jobless, penniless, anonymous.
What happened next, you know what happened next, the most predictable disaster in the world.
Crime skyrocketed, social cohesion collapsed, test scores in local schools plummeted,
and the city began to fall apart.
People who grew up in Earth 97 started to leave in large numbers.
This is what it looks like now.
---
Script:
        """
        return get_completion(prompt)
