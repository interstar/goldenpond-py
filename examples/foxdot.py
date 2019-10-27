
from goldenpond import Chord, Scale, GoldenPond, ChordSeqBuilder , EventSeq

from goldenpond import GoldenPond, _1, _2, _3, _4, _5, _6, _7, _17, _27, _37, _47, _57, _67, _77, I, II, III, IV, V, VI, VII, i, ii, iii, iv, v, vi, vii 




from FoxDot import *

piece = GoldenPond.major("G",-1).add([_17,_4,_67,_5],[4,4,4,4])
bass_seq = piece.get_track(0).get_root_seq().transpose(-24)
piece.new_track().track(1).add_seq(bass_seq)
p1 >> saw(piece.get_notes_for_track(0), dur=piece.get_durations_for_track(0), scale=Scale.chromatic)
p2 >> pluck(piece.get_notes_for_track(1), dur=piece.get_durations_for_track(1), scale=Scale.chromatic)
d1 >> play("x-o-x-o-")

Go()

