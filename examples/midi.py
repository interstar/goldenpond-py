from goldenpond import ChordSeqBuilder, GoldenPond, EventSeq, Chord, Scale, ScaleChooseSequence, Mode, Event

from goldenpond import _1, _2, _3, _4, _5, _6, _7, _17, _27, _37, _47, _57, _67, _77


from midiutil import MIDIFile

def midify(fName, bpm, duration, volume, seqs) :
    midi = MIDIFile(len(seqs))
    midi.addTempo(0, 0, bpm)
    track = 0
    channel = 1
    for seq in seqs :
        for e in seq :
            for note in e.get_data().get_notes() :
                midi.addNote(track,channel,note,e.get_abs_time(), e.get_duration(), volume)
        track = track+1
        channel = channel+1
    with open(fName,"wb") as output_file :
        midi.writeFile(output_file)
        


def example1() :
    root = GoldenPond.example_root()
    csb = ChordSeqBuilder()

    rhyth1 = [2,2,4,4,4]
    rhyth2 = [2,2,4,2,2,4]
     
    chord_seq = (csb.major(root, [_4,_6,_2,_5,_1], rhyth1) + csb.minor(root, [_4,_6,_2,_5,_5, _1], rhyth2 ) ) * 8

    cs = EventSeq.null_seq()
    for i in range(8) :
        cs = cs + ScaleChooseSequence(Scale.major(root+24),1,16)
        cs = cs + ScaleChooseSequence(Scale.minor(root+24),1,16)
    note_seq = cs.swing(0.3 )
    
    def tf(e) : return e.get_data().raw_notes()[0] % 12  == root % 12   
    vamped = (Scale.major(root).double_up().vamp([0.5,1,0.5,2],16,2).truncate_on(tf).transpose(12) + Scale.minor(root).double_up().vamp([0.5,1,0.5,1,1],16,1).truncate_on(tf).transpose(24) )*8
    
    #midify("example1.mid", 180, 1, 100, [chord_seq, note_seq])
    midify("example1.mid", 180, 1, 100, [chord_seq, vamped])

def example2() :
    root = 60
    def tf(e) : return e.get_data().raw_notes()[0] % 12  == root % 12   
    seq = EventSeq.null_seq()
    for i in range(7) :
        scl = Mode.make(root,i).to_scale()
        seq = seq + scl.vamp([1,0.5,0.5],16,3).truncate_on(tf)*2
    
    s2 = ChordSeqBuilder.raw_chordseq( [Chord.power_chord(root-12)]*128, [2]*128 )

    midify("example2.mid", 180, 1, 100, [seq,s2])        

example1()
example2()
