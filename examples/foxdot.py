
from lancehead import ChordBuilder, ScaleBuilder, LanceHead, ChordSeqBuilder , EventSeq
from lancehead import _1, _2, _3, _4, _5, _6, _7, _17, _27, _37, _47, _57, _67, _77 


class FoxSeq(EventSeq) :

    def __init__(self,eventseq) :
        self.events = eventseq.copy_events()

    def fox_chords(self) :
        return [tuple(e.get_data().get_notes()) for e in self]

    def fox_waits(self) :
        return [e.get_duration() for e in self]


chords = FoxSeq(LanceHead.example_chord_sequence().transpose(-48))
notes = FoxSeq(LanceHead.example_choose_sequence().transpose(-60))

from FoxDot import *
p1 >> saw(chords.fox_chords(),dur=chords.fox_waits(),scale=Scale.chromatic)
p2 >> pluck(notes.fox_chords(),dur=notes.fox_waits(),scale=Scale.chromatic)
d1 >> play("x-o-")
Go()

