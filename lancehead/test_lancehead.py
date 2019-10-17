from lancehead import LanceHead, Event, Note, Scale, Chord, ScaleBuilder, ChordBuilder, EventSeq, ChordSeqBuilder, ScaleChooseSequence, Part, PartBuilder, Ring

from lancehead import _1, _2, _3, _4, _5, _6, _7

def test_notes() :
    assert LanceHead.note_to_name(4) == "E"
    assert LanceHead.name_to_note("E") == 4
    assert LanceHead.name_to_note("F#") == 6
    assert LanceHead.name_to_note("Eb") == 3

def test_note_bag() :
    x = Scale([1,2,3])
    x.test_all()
    x = Chord([3, 6, 9])
    x.test_all()
    x = Note(13)
    x.test_all()
    
    assert x.normalized()[0] == 1

def test_scales() :
    s1 = Scale([1,2,3])
    assert s1.contains(2) == True
    assert s1.contains(4) == False
    assert s1.get_root() == 1
    assert s1.take_elements([2,1]) == [3,2]
    assert s1.normalized().raw_notes() == [1,2,3]
    s2 = Scale([12,13,14])
    assert s2.normalized().raw_notes() == [0,1,2]
    sb = ScaleBuilder()

    assert sb.major(60).raw_notes() == [60,62,64,65,67,69,71]
    assert sb.minor(60).raw_notes() == [60,62,63,65,67,68,70]
    assert sb.major(60).named_notes() == ["C","D","E","F","G","A","B"]
    assert sb.minor(60).named_notes() == ["C","D","D#","F","G","G#","A#"]
    assert sb.major(62).get_named_root() == "D"

def test_chords() :
    cb = ChordBuilder()
    assert cb.major_triad(60).raw_notes() == [60,64,67]
    assert cb.minor_triad(60).raw_notes() == [60,63,67]

    assert cb.major_7th(60).raw_notes() == [60,64,67,71]
    assert cb.minor_7th(60).raw_notes() == [60,63,67,70]

    assert cb.minor_triad(60).named_notes() == ["C","D#","G"]

    for i in range(10):
        assert cb.major_triad(60).choose() in [60,64,67]


    assert (cb.major_7th(60) + 1).raw_notes() == [61,65,68,72]
    assert (cb.major_7th(60) - 5).raw_notes() == [55,59,62,66]


def test_events() :
    e = Event("x",3)
    assert type(e) == Event
    assert e.get_data() == "x"
    assert e.get_duration() == 3 


def test_chord_seqs() :
    csb = ChordSeqBuilder()
    seq = csb.major(60, [_4,_6,_2],  [2,2,4] )
    assert seq.duration() == 8

    events = [e for e in seq]
    assert type(events[0]) == Event
    assert type(events[0].get_data()) == Chord
    notes = [e.get_data().raw_notes() for e in seq]
    assert notes == [
[65, 69, 72],
[69, 72, 76],
[62, 65, 69]]

    start_times = [e.get_abs_time() for e in seq]
    assert start_times == [0,2,4]
    

    seq = seq + csb.major(60,[_5,_1], [4,4])
    assert seq.duration() == 16

    notes = [e.get_data().raw_notes() for e in seq]
    assert notes == [
[65, 69, 72],
[69, 72, 76],
[62, 65, 69], 
[67, 71, 74],
[60, 64, 67] ]

    notes = [e.get_data().raw_notes() for e in seq.transpose(-2)]
    assert notes == [
[63, 67, 70],
[67, 70, 74],
[60, 63, 67], 
[65, 69, 72],
[58, 62, 65] ]

    seq2 = seq * 3
    
    assert seq2.duration() == 48
    notes = [e.get_data().raw_notes() for e in seq2]
    assert notes == [
[65, 69, 72],
[69, 72, 76],
[62, 65, 69], 
[67, 71, 74],
[60, 64, 67],

[65, 69, 72],
[69, 72, 76],
[62, 65, 69], 
[67, 71, 74],
[60, 64, 67],

[65, 69, 72],
[69, 72, 76],
[62, 65, 69], 
[67, 71, 74],
[60, 64, 67]

 ]


def test_scale_choose_seqs() :
    sb = ScaleBuilder()
    scale = sb.major(60)
    seq = ScaleChooseSequence(scale,1,8)
    assert seq.duration() == 8
    notes = [e.get_data().raw_notes() for e in seq]
    for n in notes :
        assert n[0] in scale.raw_notes()

def test_ring() :
    ring = Ring([1,2])
    c = 0
    for i in range(10) :
        assert ring.next() == 1
        assert ring.next() == 2
        

def test_swing() :
    seq = EventSeq([Event(0,1)])*10
    assert seq.duration() == 10
    sseq = seq.swing(0.2)
    assert sseq.duration() == 10
    assert [e.get_duration() for e in sseq] == [0.8, 1.2, 0.8, 1.2, 0.8, 1.2, 0.8, 1.2, 0.8, 1.2] 
