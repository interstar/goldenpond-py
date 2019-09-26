
# Data

class SCBase :

    def get_notes(self) : return self.notes

    def __getitem__(self,i) :
        return self.notes[i]

    def __add__(self,off) :
        return Scale([n+off for n in self.notes])

    def __sub__(self,off) :
        return Scale([n-off for n in self.notes])


class Scale(SCBase) :
    def __init__(self,notes) :
        self.notes = notes

    def take_elements(self,elements) :
        return [self.notes[e] for e in elements]

    def normalized_notes(self) : return [n % 12 for n in self.notes]

    def contains(self,n) :
        return n%12 in self.normalized_notes()

    def note_from_degree(self,degree) :
        return self[degree-1] # note that we treat degree as numbers 1 to 7 NOT 0 to 6

    def __repr__(self) :
        return "Scale{%s}" % ["%s" % n for n in self.notes]


class Chord(SCBase) :
    def __init__(self,notes) :
        self.notes = notes

    def get_notes(self) : return self.notes


    def __repr__(self) :
        return "Chord{%s}" % ["%s" % n for n in self.notes]

class ChordSeq :
    def __init__(self,chords,timings) :
        self.chords = chords
        self.timings = timings

    def make_iterator(self) :
        def g() :
            c = 0
            while True :
                if c >= len(self.chords) : return
                yield (self.chords[c],self.timings[c])
                c = c + 1
        return g()

    def __repr__(self) :
        return "ChordSeq { %s }" % [x for x in self.make_iterator()]

    def notes_waits_iterator(self) :
        return ( (xs[0].get_notes(),xs[1]) for xs in self.make_iterator() )
        
    def fox_chords(self) :
        return [tuple(xs[0].get_notes()) for xs in self.make_iterator()]

    def fox_waits(self) :
        return [xs[1] for xs in self.make_iterator()]


class Part :
    def __init__(self,sections) :
        self.sections = section

class Piece :
    def __init__(self,parts) :
        self.parts = part


# Builders 

class ScaleBuilder :
    def major(self,start) :
        return Scale([n + start for n in [0,2,4,5,7,9,11]])

    def minor(self,start) :
        return Scale([n + start for n in [0,2,3,5,7,8,10]])

    def scale_from(self,start,elements) :
        return Scale([start+e for e in elements])

    def scale_from_scale_and_degree(self,scale,degree) :
        degree_note = scale.note_from_degree(degree)
        return Scale( [n for n in (degree_note + x for x in range(12)) if scale.contains(n)] )

        
class ChordBuilder :
    def __init__(self) :
        self.sb = ScaleBuilder()

    def chord_from_scale(self,scale,elements) :
        return Chord(scale.take_elements(elements))


    def major_triad(self,start) :
        return self.chord_from_scale(self.sb.major(start),[0,2,4])


    def minor_triad(self,start) :
        return self.chord_from_scale(self.sb.minor(start),[0,2,4])


    def major_7th(self,start) :
        return self.chord_from_scale(self.sb.major(start),[0,2,4,6])


    def minor_7th(self,start) :
        return self.chord_from_scale(self.sb.minor(start),[0,2,4,6])


    def degree_chord(self,scale,degree) :
        ds = self.sb.scale_from_scale_and_degree(scale,degree)    
        return self.chord_from_scale(ds, [0,2,4,6])


_1 = 1
_2 = 2
_3 = 3
_4 = 4
_5 = 5
_6 = 6
_7 = 7


NOTE_NAMES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"] 

def name_to_note(name) :
    return NOTE_NAMES.index(name)




class ChordSeqBuilder :
    def __init__(self) :
        self.cb = ChordBuilder()
        self.sb = ScaleBuilder()

    def major(self,root,cs,ts) :
        sc = self.sb.major(root)
        return ChordSeq([cb.degree_chord(sc,d) for d in cs],ts)        

    def minor(self,root,cs,ts) :
        sc = self.sb.minor(root)
        return ChordSeq([cb.degree_chord(sc,d) for d in cs],ts)

    def literal(self,octave,s) :
        cs = []
        ds = []
        d = 1
        cc = ""
        print("XXX",s.split(" "))
        for c in s.split(" ") :
            if c in NOTE_NAMES :
                if cc != "" :
                    cs.append(cc)
                    ds.append(d)
                print(c)
                n = name_to_note(c) + 12 * octave
                cc = cb.major_7th(n)
                d = 1
            else :
                d = d + 1
        ds.append(d)
        cs.append(cc)
        return ChordSeq(cs,ds)


if __name__ == "__main__" :
    from midiutil import MIDIFile

    cb = ChordBuilder()

    csb = ChordSeqBuilder()


    track    = 0
    channel  = 0
    time     = 0   # In beats
    duration = 1   # In beats
    tempo    = 150  # In BPM
    volume   = 100 # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track
                         # automatically created)
    MyMIDI.addTempo(track, time, tempo)


    cseq = csb.major(name_to_note("C")+48, [_4,_6,_2,_5,_1], [2,2,4,4,4] )
    print(cseq)
 

    for notes,wait in cseq.notes_waits_iterator() :
        print(notes,wait)
        for n in notes :
            MyMIDI.addNote(track, channel, n, time, duration, volume)
        time = time + wait

    cseq = csb.minor(name_to_note("C")+48, [_4,_6,_2,_5,_1], [2,2,4,4,4] )
    print(cseq)
    
    for notes,wait in cseq.notes_waits_iterator() :
        print(notes,wait)
        for n in notes :
            MyMIDI.addNote(track, channel, n, time, duration, volume)
        time = time + wait

    with open("test1.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)



if __name__ == "_main__" :

    cb = ChordBuilder()
    sb = ScaleBuilder()
    print("64 major triad", cb.major_triad(64))
    print("64 minor triad", cb.minor_triad(64))
    print("64 major 7th ", cb.major_7th(64))
    print("64 major 7th ", cb.minor_7th(64))

    print("chords for 64 major")
    sc = sb.major(64)
    print(sc)
    for d in range(1,8) :
        print(d, sb.scale_from_scale_and_degree(sc, d))
        print(d, cb.degree_chord(sc,d))

    csb = ChordSeqBuilder()
    cseq = csb.major(name_to_note("C"), [_4,_6,_2,_5,_1], [2,2,4,4,4] )
    print(cseq)

    cseq = csb.literal(0,"C. C#. G...")
    print(cseq)

    from FoxDot import *

    print(cseq.fox_chords())
    print(cseq.fox_waits())
    p1 >> saw(cseq.fox_chords(),dur=cseq.fox_waits(),scale=Scale.chromatic)
    d1 >> play("x-o-")
    Go()

