
from lancehead import LanceHead, Scale, Chord, ScaleBuilder, ChordBuilder

def test_notes() :
    assert LanceHead.note_to_name(4) == "E"
    assert LanceHead.name_to_note("E") == 4
    assert LanceHead.name_to_note("F#") == 6
    assert LanceHead.name_to_note("Eb") == 3

def test_scales() :
    s1 = Scale([1,2,3])
    assert s1.contains(2) == True
    assert s1.contains(4) == False
    assert s1.take_elements([2,1]) == [3,2]
    assert s1.normalized().get_notes() == [1,2,3]
    s2 = Scale([12,13,14])
    assert s2.normalized().get_notes() == [0,1,2]
    sb = ScaleBuilder()

    assert sb.major(60).get_notes() == [60,62,64,65,67,69,71]
    assert sb.minor(60).get_notes() == [60,62,63,65,67,68,70]
    assert sb.major(60).named_notes() == ["C","D","E","F","G","A","B"]
    assert sb.minor(60).named_notes() == ["C","D","D#","F","G","G#","A#"]
