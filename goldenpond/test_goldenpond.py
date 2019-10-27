from goldenpond import GoldenPond, Event, Note, Scale, Chord, EventSeq, ChordSeqBuilder, ScaleChooseSequence, Music, Ring

from goldenpond import _1, _2, _3, _4, _5, _6, _7, _17, _27, _37, _47, _57, _67, _77, I, II, III, IV, V, VI, VII, i, ii, iii, iv, v, vi, vii

def test_notes() :
    assert GoldenPond.note_to_name(4) == "E"
    assert GoldenPond.name_to_note("E") == 4
    assert GoldenPond.name_to_note("F#") == 6
    assert GoldenPond.name_to_note("Eb") == 3

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
    

    assert Scale.major(60).raw_notes() == [60,62,64,65,67,69,71]
    assert Scale.minor(60).raw_notes() == [60,62,63,65,67,68,70]
    assert Scale.major(60).named_notes() == ["C","D","E","F","G","A","B"]
    assert Scale.minor(60).named_notes() == ["C","D","D#","F","G","G#","A#"]
    assert Scale.major(62).get_named_root() == "D"
	
    es = Scale.major(60).vamp([1,1,2],16)
    assert es.duration() == 16
    assert [n[0] for n in es.get_notes()] == [60, 62, 64, 65, 67, 69, 71, 60, 62, 64, 65, 67]

def test_chords() :
    assert Chord.major_triad(60).raw_notes() == [60,64,67]
    assert Chord.minor_triad(60).raw_notes() == [60,63,67]

    assert Chord.major_7th(60).raw_notes() == [60,64,67,71]
    assert Chord.minor_7th(60).raw_notes() == [60,63,67,70]

    assert Chord.minor_triad(60).named_notes() == ["C","D#","G"]

    for i in range(10):
        assert Chord.major_triad(60).choose() in [60,64,67]


    assert (Chord.major_7th(60) + 1).raw_notes() == [61,65,68,72]
    assert (Chord.major_7th(60) - 5).raw_notes() == [55,59,62,66]


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

    scale = Scale.major(60)
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


def test_seq_builder() :
    root = GoldenPond.name_to_note("C") + 12*4
    csb = ChordSeqBuilder()
    seq = csb.minor(root, [_4,vi,_27,_5,V,_1], [1,1,1,1,1,1])
    assert seq.duration() == 6
    assert len(seq) == 6

    def test_end(e) :
        return e.get_data().raw_notes()[0] % 12 == GoldenPond.name_to_note("G") % 12
    seq2 = seq.truncate_on(test_end)
    assert len(seq2) == 4
    assert seq2.duration() == 6



def test_piece() :
    piece = GoldenPond.major("G",4)
    assert piece.get_key() == "G"
    assert piece.get_root() == 55 # think this is right
    assert piece.get_mode() == "major"

    assert piece.no_tracks() == 1
    assert piece.duration() == 0

    p2 = piece.add([_5,_2,_5,_1],[1,1,1,1])
    assert piece == p2
    assert piece.current_default_track() == 0
    p3 = p2.new_track()
    assert piece.no_tracks() == 2
    assert p3.no_tracks() == 2
    assert p2.duration() == 4

    assert p2.current_default_track() == 0    
    p2.track(1)
    assert p2.current_default_track() == 1
    
    t = piece.get_track(0)
    assert type(t) == EventSeq

    rs = t.get_root_seq()
    assert type(rs) == EventSeq
    assert rs.duration() == 4

    assert len( piece.get_notes_for_track(0) ) == 4
    assert len( piece.get_durations_for_track(0) ) == 4

    assert type(piece.random_notes()) == ScaleChooseSequence
    

    
