from goldenpond import ChordSeqBuilder, GoldenPond, EventSeq, Chord, Scale, ScaleChooseSequence

from goldenpond import _1, _2, _3, _4, _5, _6, _7, _17, _27, _37, _47, _57, _67, _77


from midiutil import MIDIFile




def example_tune_to_midi() :
    root = GoldenPond.example_root()
    csb = ChordSeqBuilder()

    rhyth1 = [2,2,4,4,4]
    rhyth2 = [2,2,4,2,2,4]
     
    chord_seq = (csb.major(root, [_4,_6,_2,_5,_1], rhyth1) + csb.minor(root, [_4,_6,_2,_5,_5, _1], rhyth2 ) ) * 8


    cs = EventSeq.null_seq()
    for i in range(8) :
        cs = cs + ScaleChooseSequence(Scale.major(root+24),1,16)
        cs = cs + ScaleChooseSequence(Scale.minor(root+24),1,16)
    note_seq = cs.swing(0.5 )
    
    def tf(e) : return e.get_data().raw_notes()[0] % 12  == root % 12
    maj = Scale.major(root) 
    min = Scale.minor(root)
    vamped = (Scale.major(root).double_up().vamp([0.5,1,0.5,2],16,2).truncate_on(tf).transpose(12) + Scale.minor(root).double_up().vamp([0.5,1,0.5,1,1],16,1).truncate_on(tf).transpose(24) )*8
    

    track    = 0
    channel  = 0
    duration = 1   # In beats
    volume = 100
    bpm = 150

    MyMIDI = MIDIFile(1)
    MyMIDI.addTempo(track, 0, bpm)

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
