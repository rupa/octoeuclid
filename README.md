# Synopsis

Up to 8 Euclidean Rhythms at once, on your BeatStep Pro.

# Requirements

Needs python and python-rtmidi.

```
pip install -r requirements.txt
```

# Usage

Something like ...

```
~$ cat demo.py
from euclid import BeatStepPro
from euclid import EuclideanSequence
from euclid import OctoEuclid

slots = [
    EuclideanSequence(9, 17),
    EuclideanSequence(3, 7),
    EuclideanSequence(5, 8),
    EuclideanSequence(3, 5),
    EuclideanSequence(7, 11),
    EuclideanSequence(2, 3),
    EuclideanSequence(6, 8),
    EuclideanSequence(11, 19),
]

oe = OctoEuclid(slots) # 8 slots max!
bsp = BeatStepPro(oe)

print oe
print bsp

from IPython import embed
embed()
```
```
~$ python demo.py
OctoEuclid(8):
E(9, 17)  [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
E(3, 7)   [1, 0, 0, 1, 0, 1, 0]
E(4, 8)   [1, 0, 1, 0, 1, 0, 1, 0]
E(3, 5)   [1, 0, 1, 0, 1]
E(7, 11)  [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1]
E(2, 3)   [1, 0, 1]
E(6, 8)   [1, 0, 1, 0, 1, 1, 1, 1]
E(11, 19) [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1]
Available MIDI input ports:

[0] Arturia BeatStep Pro Arturia BeatStepPro
[1] Arturia BeatStep Pro BeatStepPro OutEditor

Select MIDI input port (Control-C to exit): 0
Available MIDI ouput ports:

[0] Arturia BeatStep Pro Arturia BeatStepPro
[1] Arturia BeatStep Pro BeatStepProInEditor

Select MIDI ouput port (Control-C to exit): 0
BeatStepPro(8)
>>>
```

... then do stuff on the BeatStep.

# Controls

* start/pause:         start/pause euclids
* stop:                reset all euclids
* drum pad 9:          manual (or sequenced) step
* top row of knobs:    rotate one euclid (control mode only)
* bottom row of knobs: reset one euclid (control mode only)

# Notes/TODO

* rotate knobs only rotate forward
* MIDI channel 10 hardcoded
* Use clock input?
* This is alpha, it'll probably change a bunch
* A bunch of other stuff probably
* FUN!
