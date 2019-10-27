from goldenpond import ChordSeqBuilder, GoldenPond, Chord, Scale

from goldenpond import _1, _2, _3, _4, _5, _6, _7, _17, _27, _37, _47, _57, _67, _77


from midiutil import MIDIFile


def example_tune_to_midi() :
    chord_seq = GoldenPond.example_chord_sequence()
    note_seq = GoldenPond.example_choose_sequence()
    root = GoldenPond.example_root()+24
    def tf(e) : return e.get_data().raw_notes()[0]  == root
    vamped = (Scale.major(root).vamp([0.5,1,0.5,2],16,2).truncate_on(tf) + Scale.minor(root).vamp([0.5,1,0.5,1,1],16,1).truncate_on(tf) )*8
    

    track    = 0
    channel  = 0
    duration = 1   # In beats
    volume = 100

    MyMIDI = MIDIFile(1)
    MyMIDI.addTempo(track, 0, 180)

    for e in chord_seq :
        for note in e.get_data().get_notes() :
            MyMIDI.addNote(track,channel, note, e.get_abs_time(), e.get_duration()/2, volume)

    #for e in note_seq :
    #    MyMIDI.addNote(track, channel+1, e.get_data().get_notes()[0], e.get_abs_time(), e.get_duration(), volume)

    for e in vamped :
        MyMIDI.addNote(track, channel+2, e.get_data().get_notes()[0], e.get_abs_time(), e.get_duration(), volume)

    with open("example.mid","wb") as output_file :
        MyMIDI.writeFile(output_file)

example_tune_to_midi()
