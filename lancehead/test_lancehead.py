
from lancehead import LanceHead, Scale, Chord, ScaleBuilder, ChordBuilder, ChordSeq, ChordSeqBuilder, ScaleChooseSequence, Part, PartBuilder

from lancehead import _1, _2, _3, _4, _5, _6, _7

def test_notes() :
    assert LanceHead.note_to_name(4) == "E"
    assert LanceHead.name_to_note("E") == 4
    assert LanceHead.name_to_note("F#") == 6
    assert LanceHead.name_to_note("Eb") == 3

def test_scales() :
    s1 = Scale([1,2,3])
    assert s1.contains(2) == True
    assert s1.contains(4) == False
    assert s1.get_root() == 1
    assert s1.take_elements([2,1]) == [3,2]
    assert s1.normalized().get_notes() == [1,2,3]
    s2 = Scale([12,13,14])
    assert s2.normalized().get_notes() == [0,1,2]
    sb = ScaleBuilder()

    assert sb.major(60).get_notes() == [60,62,64,65,67,69,71]
    assert sb.minor(60).get_notes() == [60,62,63,65,67,68,70]
    assert sb.major(60).named_notes() == ["C","D","E","F","G","A","B"]
    assert sb.minor(60).named_notes() == ["C","D","D#","F","G","G#","A#"]
    assert sb.major(62).get_named_root() == "D"

def test_chords() :
    cb = ChordBuilder()
    assert cb.major_triad(60).get_notes() == [60,64,67]
    assert cb.minor_triad(60).get_notes() == [60,63,67]

    assert cb.major_7th(60).get_notes() == [60,64,67,71]
    assert cb.minor_7th(60).get_notes() == [60,63,67,70]

    assert cb.minor_triad(60).named_notes() == ["C","D#","G"]

    for i in range(10):
        assert cb.major_triad(60).choose() in [60,64,67]


def test_chord_seqs() :
    csb = ChordSeqBuilder()
    cseq = csb.major(60, [_4,_6,_2,_5,_1],  [2,2,4,4,4] )
    assert cseq.duration() == 16

    nws = [(notes,waits) for notes,waits in cseq.notes_waits_iterator()]
    assert nws == [
([65, 69, 72], 2),
([69, 72, 76], 2),
([62, 65, 69], 4),
([67, 71, 74], 4),
([60, 64, 67], 4)]

def test_scale_choose_seqs() :
    sb = ScaleBuilder()
    scale = sb.major(60)
    scseq = ScaleChooseSequence(scale,1,8)
    assert scseq.duration() == 8
    nws = [(notes,waits) for notes,waits in scseq.notes_waits_iterator()]
    for nw in nws :
        assert nw[0][0] in scale.get_notes()

