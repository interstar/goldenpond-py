import traceback
import sys

# Data

# Informal data-typing with assertions
# 

def my_assertion(f) :
    def g(n) :
        try :
            f(n)
        except Exception as e :
            print("Assertion %s failed. Argument was %s " % (f.__name__,n))
            for line in traceback.format_stack():
                print(line.strip())
            sys.exit()
    return g

@my_assertion
def assert_midinote(n) :
    assert( type(n) == int and (-1 < n < 128))

@my_assertion
def assert_normalized_midinote(n) :
    assert(type(n) == int and (-1 < n < 12))

@my_assertion
def assert_degree(d) :
    assert( type(d) == int and (0 < d < 8))


NOTE_NAMES = [
    ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"],
    ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"],
    ["dó","dó sustenido", "ré", "ré sustenido", "mi", "fá", "fá sustenido", "sol", "sol sustenido", "lá", "lá sustenido", "si"],
    ["dó","ré bemol", "ré", "mi bemol", "mi", "fá", "sol bemol", "sol", "lá bemol", "lá", "si bemol", "si"]
]

@my_assertion
def assert_notename(n) :
    assert( type(n) == int or type(n) == str)
    flag = False
    if type(n)==int and 0 < n < 128 : flag = True
        
    for ns in NOTE_NAMES :
        if n in ns :
            flag = True
            break

    assert(flag==True)

DEGREE_NAMES = ("_1", "_2", "_3", "_4", "_5", "_6", "_7", "i", "ii", "iii", "iv", "v", "vi", "vii", "I", "II", "III", "IV", "V", "VI", "VII",
      "_17", "_27", "_37", "_47", "_57", "_67", "_77", "i7", "ii7", "iii7", "iv7", "v7", "vi7", "vii7", 
      "I7", "II7", "III7", "IV7", "V7", "VI7", "VII7")

@my_assertion
def assert_degreename(dn) :
    assert (dn in DEGREE_NAMES)
    
@my_assertion
def assert_scale(s) :
    assert (s.__class__ == Scale)

@my_assertion
def assert_chord(c) :
    assert (s.__class__ == Chord)

class NoteNotFoundException(Exception) :
    pass

class LanceHead :
    
    @staticmethod
    def name_to_note(name) :
        assert_notename(name)
        if name in range(128) :
            return name
        for ns in NOTE_NAMES : 
            if name in ns :
                return ns.index(name)
        raise NoteNotFoundException("Can't find note %s" % name)

    @staticmethod
    def note_to_name(note) :
        assert_normalized_midinote(note)
        return ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"][note]


class SCBase :

    def get_notes(self) : return self.notes

    def __getitem__(self,i) :
        return self.notes[i]

    def root(self) : return self.notes[0]

    def __add__(self,off) :
        return Scale([n+off for n in self.notes],name)

    def __sub__(self,off) :
        return Scale([n-off for n in self.notes],name)

    def normalized_notes(self) : return [n % 12 for n in self.get_notes()]

    def named_notes(self) : 
        return [LanceHead.note_to_name(x) for x in self.normalized_notes()]


class Scale(SCBase) :
    def __init__(self,notes, root=None) :
        self.notes = notes
        if root == None :
            root = notes[0]
        self.root = root

    def take_elements(self,elements) :
        return [self.notes[e] for e in elements]

    def contains(self,n) :
        return n%12 in self.normalized_notes()

    def normalized(self) :
        return Scale(self.normalized_notes())

    def note_from_degree(self,degree: int) :
        return self[degree-1] # note that we treat degree as numbers 1 to 7 NOT 0 to 6

    def __repr__(self) :
        return "Scale{%s}" % ["%s" % n for n in self.notes]


class Chord(SCBase) :
    def __init__(self,notes,root=None,name="") :
        self.notes = notes
        if root == None :
            root = notes[0]
        self.root = root

        self.name = name

    def get_notes(self) : return self.notes

    def normalized(self) : return Chord(self.normalized_notes())

    def __repr__(self) :
        return "Chord[%s]{%s}" % (self.name,["%s" % n for n in self.notes])

class ChordSeq :
    def __init__(self,chords,timings) :
        self.chords = chords
        self.timings = timings

    def make_iterator(self) :
        def g() :
            c = 0
            while True :
                print("in iterator")
                print(c)
                print(self.chords)
                print(len(self.chords))
                if c >= len(self.chords) : return
                xs = (self.chords[c],self.timings[c])
                yield xs 
                c = c + 1
        return g()

    def __repr__(self) :
        return "ChordSeq { %s } (%s duration)" % ([x for x in self.make_iterator()],self.duration())

    def notes_waits_iterator(self) :
        return ( (xs[0].get_notes(),xs[1]) for xs in self.make_iterator() )
        
    def fox_chords(self) :
        return [tuple(xs[0].get_notes()) for xs in self.make_iterator()]

    def fox_waits(self) :
        return [xs[1] for xs in self.make_iterator()]

    def duration(self) :
        t = 0
        for n in self.fox_waits() :
            t=t+n
        return t


class Part :
    def __init__(self,sections) :
        self.sections = section

class Piece :
    def __init__(self,parts) :
        self.parts = part


# Builders 

class ScaleBuilder :
    def major(self,root) :
        assert_midinote(root)
        return Scale([n + root for n in [0,2,4,5,7,9,11]])

    def minor(self,root) :
        assert_midinote(root)
        return Scale([n + root for n in [0,2,3,5,7,8,10]])

    def scale_from(self,root,elements) :
        assert_midinote(root)
        return Scale([root+e for e in elements])

    def scale_from_scale_and_degree(self,scale,degree) :
        print(scale)
        print(degree)
        degree_note = scale.note_from_degree(degree)
        print(degree_note)
        s =  Scale( [n for n in (degree_note + x for x in range(12)) if scale.contains(n)] )
        print(s)
        return s

class ChordException(Exception) :
    pass

        
class ChordBuilder :
    def __init__(self) :
        self.sb = ScaleBuilder()

    def chord_from_scale(self,scale,elements) :
        assert_scale(scale)
        return Chord(scale.take_elements(elements))


    def major_triad(self,root) :
        assert_midinote(root)   
        return self.chord_from_scale(self.sb.major(root),[0,2,4])


    def minor_triad(self,root) :
        assert_midinote(root)   
        return self.chord_from_scale(self.sb.minor(root),[0,2,4])


    def major_7th(self,root) :
        assert_midinote(root)   
        return self.chord_from_scale(self.sb.major(root),[0,2,4,6])


    def minor_7th(self,root) :
        assert_midinote(root)   
        return self.chord_from_scale(self.sb.minor(root),[0,2,4,6])


    def degree_chord(self,scale,degree) :
        assert_scale(scale)
        assert_degree(degree)
        ds = self.sb.scale_from_scale_and_degree(scale,degree)    
        return self.chord_from_scale(ds, [0,2,4])

    def degree_chord7(self,scale,degree) :
        assert_scale(scale)
        assert_degree(degree)
        ds = self.sb.scale_from_scale_and_degree(scale,degree)    
        return self.chord_from_scale(ds, [0,2,4,6])


    def symbol_to_chord(self,scale,symbol) :

        xs = ["_1", "_2", "_3", "_4", "_5", "_6", "_7"]
        if symbol in xs :
            return self.degree_chord(scale,xs.index(symbol)+1)
        xs = ["_17", "_27", "_37", "_47", "_57", "_67", "_77"]
        if symbol in xs :
            return self.degree_chord7(scale,xs.index(symbol)+1)
        xs = ["I","II","III","IV","V","VI","VII"]
        if symbol in xs :
            return self.major_triad(scale.root()+xs.index(symbol)+1)
        xs = ["i","ii","iii","iv","v","vi","vii"]
        if symbol in xs :
            return self.minor_triad(scale.root()+xs.index(symbol)+1)
        xs = ["I7","II7","III7","IV7","V7","VI7","VII7"]
        if symbol in xs :
            return self.major_7th(scale.root()+xs.index(symbol)+1)
        xs = ["i7","ii7","iii7","iv7","v7","vi7","vii7"]
        if symbol in xs :
            return self.minor_7th(scale.root()+xs.index(symbol)+1) 
        raise ChordSeqException("Chord %s not understood" % item)


class ChordSeqBuilder :
    def __init__(self) :
        self.cb = ChordBuilder()
        self.sb = ScaleBuilder()

    def chordseq(self,sc,root,cs,ts) :
        assert_scale(sc)
        assert_midinote(root)
        
        if len(cs) != len(ts) : 
            raise ChordException("Chord list and time list different lengths")
        i = 0
        flag = True
        chords = []
        timings = []
        while flag :
            print(i)            
            if i >= len(cs) :
                return ChordSeq(chords,timings)  
            chords.append( self.cb.symbol_to_chord(sc, cs[i]))           
            timings.append(ts[i])
            i=i+1

    def major(self,root,cs,ts) :
        return self.chordseq(self.sb.major(root), root, cs, ts)    

    def minor(self,root,cs,ts) :
        return self.chordseq(self.sb.minor(root), root, cs, ts)

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
                n = LanceHead.name_to_note(c) + 12 * octave
                cc = self.cb.major_7th(n)
                d = 1
            else :
                d = d + 1
        ds.append(d)
        cs.append(cc)
        return ChordSeq(cs,ds)



