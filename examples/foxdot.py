
from goldenpond import Chord, Scale, GoldenPond, ChordSeqBuilder , EventSeq
from goldenpond import GoldenPond, _1, _2, _3, _4, _5, _6, _7, _17, _27, _37, _47, _57, _67, _77, I, II, III, IV, V, VI, VII, i, ii, iii, iv, v, vi, vii 

# Set up a piece of music in GoldenPond

# This creates a new piece, in our key of A major with the chord sequence
piece = GoldenPond.major("A",-1).add([_1,_37,_4,_6,_27,_5, _57, iv],[2,4,2,4,2,4,4,2])

# create a bassline by extracting the root notes of all the chords
bass_seq = piece.get_track(0).get_root_seq().transpose(-24)
# and create a new track in the piece to store it
piece.new_track().track(1).add_seq(bass_seq)
# then create a vamp on an A major scale
vamped = Scale.major(21).vamp([0.5,0.25,0.5,0.25,0.5],24,2).transpose(-12)
# and store it in a third track
piece.new_track().track(2).add_seq(vamped)

# Now go into FoxDot ... don't try to import FoxDot BEFORE running the GoldenPond functions, because there's currently a name clash between Scale in GoldenPond and Scale in FoxDot
from FoxDot import *
# We create 3 instruments and feed each of them with data from the three tracks of our piece of music
p1 >> saw(piece.get_notes_for_track(0), dur=piece.get_durations_for_track(0), scale=Scale.chromatic)
p2 >> pluck(piece.get_notes_for_track(1), dur=piece.get_durations_for_track(1), scale=Scale.chromatic)
p3 >> blip(piece.get_notes_for_track(2), dur=piece.get_durations_for_track(2), scale=Scale.chromatic)
# add a simple drum pattern
d1 >> play("x-o-x-o-x-o-xxo-")
# and go ...
Go()

