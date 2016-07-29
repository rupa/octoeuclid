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

oe = OctoEuclid(slots)
print oe

bsp = BeatStepPro(oe)
print bsp

from IPython import embed
embed()
