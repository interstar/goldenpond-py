import traceback
import sys
import random

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


__all__ = []

def _setup_names():
    g = globals()
    # add the names to the module globals, each variable a string equal to the name
    g.update({t: t for t in DEGREE_NAMES})
    # add the names to __all__
    __all__.extend(DEGREE_NAMES)

_setup_names()

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

class GoldenPond :

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

    @staticmethod
    def example_chord_sequence() :
        """
        """
        root = GoldenPond.name_to_note("C") + 12*4
        rhyth1 = [2,2,4,4,4]
        rhyth2 = [2,2,4,2,2,4]

        csb = ChordSeqBuilder()
        return (csb.major(root, [_4,_6,_2,_5,_1], rhyth1) + csb.minor(root, [_4,_6,_2,_5,_5, _1], rhyth2 ) ) * 8

    def example_choose_sequence() :
        """
        """
        root = GoldenPond.name_to_note("C") + 12*4
        sb = ScaleBuilder()
        cs = EventSeq.null_seq()
        for i in range(8) :
            cs = cs + ScaleChooseSequence(sb.major(root+24),1,16)
            cs = cs + ScaleChooseSequence(sb.minor(root+24),1,16)
        return cs.swing(0.3)

    
class NoteBag() :
    def __init__(self, notes) :
        self.notes = notes

    def raw_notes(self) : 
        return self.notes[:]

    def __getitem__(self,i) :
        return self.notes[i]

    def __iter__(self) :
        return (x for x in self.notes)

    def root(self) : return self.notes[0]

    def __add__(self,off) :
        return NoteBag([n+off for n in self.raw_notes()])

    def __sub__(self,off) :
        return NoteBag([n-off for n in self.raw_notes()])

    def normalized_notes(self) : return NoteBag([n % 12 for n in self.raw_notes()])

    def named_notes(self) :
        return [GoldenPond.note_to_name(x) for x in self.normalized_notes()]

    def __len__(self) : return len(self.notes)


    def choose(self) :
        return random.choice(self.raw_notes())

class NBBase :
    def undef(self,fName) :
        raise Exception("%s needs to implement %s" % (self.__class__, fName))
    
    def get_notes(self) : self.undef("get_notes()")
    def raw_notes(self) : 
        return self.get_notes().raw_notes()

    def get_root(self) : self.undef("get_root()")
    def choose(self) :
        return random.choice(self.raw_notes())
    def normalized(self) : self.undef("normalized()")
    def __getitem__(self,i) : self.undef("__getitem__(i)")
    def __len__(self) : 
        return len(self.get_notes())

    def named_notes(self) :
        return self.get_notes().named_notes()

    def __add__(self,o) : self.undef("__add__(o)")
    def __sub__(self,o) : self.undef("__sub__(o)")

    def test_all(self) :
        self.get_notes()
        self.raw_notes()
        self.get_root()
        self.choose()
        self.normalized()
        self[0]
        len(self)
        self.named_notes()
        self + 3
        self - 4

      

class Note(NBBase) :
    "Just used to put individual notes into Events so that they have similar interface to Chords"
    def __init__(self, note) :
        assert_midinote(note)
        self.notes = NoteBag([note])

    def get_notes(self) : return self.notes
    def raw_notes(self) : return self.notes.raw_notes()
    def get_root(self) : return self.notes[0]
    def choose(self) : return self.notes.choose()
    def normalized(self) : return Note(self.notes.normalized_notes().raw_notes()[0])
    def __getitem__(self,i) : return self.notes[i]
    def __add__(self,n) :
        return Note((self.get_notes()+n)[0])

    def __sub__(self,n) :
        return Note((self.get_notes()-n)[0])
    
    

class Scale(NBBase) :
    def __init__(self,notes, root=None) :
        self.notes = NoteBag(notes)
        if root == None :
            root = notes[0]
        self.root = root

    def get_notes(self) : return self.notes
    def get_root(self) :
        return self.root

    def __getitem__(self,i) : return self.notes[i]
    
    def __add__(self,n) :
        return Scale(self.get_notes()+n,self.root+n)

    def __sub__(self,n) :
        return Scale(self.get_notes()-n,self.root-n)

    def take_elements(self,elements) :
        return [self.raw_notes()[e] for e in elements]

    def choose(self) :
        return self.notes.choose()

    def contains(self,n) :
        return n%12 in self.normalized()    

    def normalized(self) :
        return Scale(self.get_notes().normalized_notes(),self.root%12)

    def note_from_degree(self,degree: int) :
        return self[degree-1] # note that we treat degree as numbers 1 to 7 NOT 0 to 6

    def __repr__(self) :
        return "Scale[root=%s]{%s}" % (self.root,["%s" % n for n in self.notes])


    def get_named_root(self) :
        return GoldenPond.note_to_name(self.get_root()%12)

class Chord(NBBase) :
    def __init__(self,notes,root=None,name="") :
        self.notes = NoteBag(notes)
        if root == None :
            root = notes[0]
        self.root = root
        self.name = name

    def get_notes(self) : return self.notes

    def named_notes(self) :
        return self.notes.named_notes()

    def choose(self) :
        return self.notes.choose()
    
    def get_root(self) : return self.root

    def normalized(self) : return Chord(self.get_notes().normalized_notes(),self.root%12,self.name)

    def __getitem__(self,i) : return self.notes[i]

    def __add__(self,n) :
        return Chord(self.get_notes()+n,self.root+n,self.name)

    def __sub__(self,n) :
        return Chord(self.get_notes()-n,self.root-n,self.name)

    def __repr__(self) :
        return "Chord[%s]{%s}" % (self.get_root(),["%s" % n for n in self.notes])





## Sequences
##

class Ring :
    "Ring Buffer"

    def __init__(self, xs) :
        self.xs = xs
        self.i = -1

    def next(self) :
        self.i=self.i+1
        if self.i >= len(self.xs) : 
            self.i = 0
        return self.xs[self.i]

class Event :
    def __init__(self,data,duration,at=None) :
        self.v = data
        self.dur = duration
        self.abs_time = at

    def __repr__(self) :
        return "Event(%s,%s,%s)" % (self.v,self.dur,self.abs_time)

    def get_data(self) : return self.v
    def get_duration(self) : return self.dur
    def get_abs_time(self) :
        if self.abs_time == None :
            raise Exception("No absolute time available for event %s" % self)
        else :
            return self.abs_time

class SeqBase :
    def get_events(self) :
        raise Exception("Child class of SeqBase must implement get_events()")

    def __iter__(self) :
        def g() :
            t = 0
            for e in self.get_events() :
                yield Event(e.get_data(), e.get_duration(), t)
                t = t +  e.get_duration()
            return
        return g()                

    def copy_events(self) :
        return self.get_events()[:]

    def duration(self) :
        t = 0
        for e in self :
            t=t+e.get_duration()
        return t

    def swing(self, offset) :
        offs = Ring([-offset,offset])
        return EventSeq([Event(e.get_data(), e.get_duration()+offs.next()) for e in self])

    def transpose(self,offset) :
        return EventSeq([Event(e.get_data() + offset, e.get_duration()) for e in self])

class EventSeq(SeqBase) :

    @staticmethod
    def null_seq() :
        return EventSeq([])

    def __init__(self,events) :
        self.events = events

    def __repr__(self) :
        return "EvenSeq { %s } (%s duration)" % ([e for e in self],self.duration())

    def get_events(self) :
        return self.events


    def __add__(self,other_seq) :
        return EventSeq(self.copy_events() + other_seq.copy_events())

    def __mul__(self,n) :
        es = EventSeq.null_seq()
        for i in range(n) :
            es = es + self
        return es


    
class ScaleChooseSequence(SeqBase) :
    def __init__(self, scale, tick, repetitions) :
        self.scale = scale
        self.tick = tick
        self.repetitions = repetitions

    def duration(self) :
        return self.tick * self.repetitions

    def get_events(self) :
        return [x for x in self]


    def __iter__(self) :
        return (Event( Note(self.scale.choose()), self.tick) for x in range(self.repetitions))


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
        degree_note = scale.note_from_degree(degree)
        s =  Scale( [n for n in (degree_note + x for x in range(12)) if scale.contains(n)] )
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
            return self.major_triad(scale.get_root()+xs.index(symbol)+1)
        xs = ["i","ii","iii","iv","v","vi","vii"]
        if symbol in xs :
            return self.minor_triad(scale.get_root()+xs.index(symbol)+1)
        xs = ["I7","II7","III7","IV7","V7","VI7","VII7"]
        if symbol in xs :
            return self.major_7th(scale.get_root()+xs.index(symbol)+1)
        xs = ["i7","ii7","iii7","iv7","v7","vi7","vii7"]
        if symbol in xs :
            return self.minor_7th(scale.get_root()+xs.index(symbol)+1)
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
        events = []
        while flag :
            if i >= len(cs) :
                return EventSeq(events)
            data = self.cb.symbol_to_chord(sc, cs[i])
            duration = ts[i]
            events.append(Event(data,duration))
            i=i+1

    def major(self,root,cs,ts) :
        return self.chordseq(self.sb.major(root), root, cs, ts)

    def minor(self,root,cs,ts) :
        return self.chordseq(self.sb.minor(root), root, cs, ts)




class PartBuilder :
    pass

class FoxBuilder :
    def __init__(self, root) :
        self.root = root
        self.csb = ChordSeqBuilder()

    def setRoot(self, root) : self.root = root

    def newMajor(self, chords, timings= [2,2,2,2]) :
        return self.csb.major(self.root, chords, timings)

    def newMinor(self, chords, timings= [2,2,2,2]) :
        return self.csb.minor(self.root, chords, timings)