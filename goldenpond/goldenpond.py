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
    assert( type(n) == int and (-128 < n < 128))

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


    @classmethod
    def major(cls,key,octave) :
        assert_notename(key)
        root = cls.name_to_note(key) + (12*octave)
        return Music(key,"major",root,Scale.major(root), octave)

    @classmethod
    def minor(cls,key,octave) :
        assert_notename(key)
        root = cls.name_to_note(key) + (12*octave)
        return Music(key,"minor",root,Scale.minor(root), octave)


    @staticmethod 
    def example_root() :
        return GoldenPond.name_to_note("C") + 12*4
 
    @staticmethod
    def example_chord_sequence() :
        """
        """
        root = GoldenPond.example_root()
        rhyth1 = [2,2,4,4,4]
        rhyth2 = [2,2,4,2,2,4]

        csb = ChordSeqBuilder()
        return (csb.major(root, [_4,_6,_2,_5,_1], rhyth1) + csb.minor(root, [_4,_6,_2,_5,_5, _1], rhyth2 ) ) * 8

    def example_choose_sequence() :
        """
        """
        root = GoldenPond.example_root()
        cs = EventSeq.null_seq()
        for i in range(8) :
            cs = cs + ScaleChooseSequence(Scale.major(root+24),1,16)
            cs = cs + ScaleChooseSequence(Scale.minor(root+24),1,16)
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
        raise GoldenPondException("%s needs to implement %s" % (self.__class__, fName))
    
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

    @staticmethod
    def major(root) :
        assert_midinote(root)
        return Scale([n + root for n in [0,2,4,5,7,9,11]])

    @staticmethod
    def minor(root) :
        assert_midinote(root)
        return Scale([n + root for n in [0,2,3,5,7,8,10]])

    @staticmethod
    def scale_from(root,elements) :
        assert_midinote(root)
        return Scale([root+e for e in elements])

    @staticmethod
    def scale_from_scale_and_degree(scale,degree) :
        degree_note = scale.note_from_degree(degree)
        s =  Scale( [n for n in (degree_note + x for x in range(12)) if scale.contains(n)] )
        return s

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

    def vamp(self, pattern, total, step=1) :
        pattern = Ring(pattern)
        notes = Ring(self.get_notes())
        time = 0
        start = 0
        events = []
        while time < total :
            d = pattern.next()
            n = 0
            for i in range(step) :
                n = notes.next()
            e = Event(Note(n), d)
            time = time + d
            events.append(e)
        return EventSeq(events)
                
    		

class Chord(NBBase) :

    @staticmethod
    def chord_from_scale(scale,elements) :
        assert_scale(scale)
        return Chord(scale.take_elements(elements))

    @staticmethod
    def major_triad(root) :
        assert_midinote(root)
        return Chord.chord_from_scale(Scale.major(root),[0,2,4])

    @staticmethod
    def minor_triad(root) :
        assert_midinote(root)
        return Chord.chord_from_scale(Scale.minor(root),[0,2,4])

    @staticmethod
    def major_7th(root) :
        assert_midinote(root)
        return Chord.chord_from_scale(Scale.major(root),[0,2,4,6])

    @staticmethod
    def minor_7th(root) :
        assert_midinote(root)
        return Chord.chord_from_scale(Scale.minor(root),[0,2,4,6])

    @staticmethod
    def degree_chord(scale,degree) :
        assert_scale(scale)
        assert_degree(degree)
        ds = Scale.scale_from_scale_and_degree(scale,degree)
        return Chord.chord_from_scale(ds, [0,2,4])

    @staticmethod
    def degree_chord7(scale,degree) :
        assert_scale(scale)
        assert_degree(degree)
        ds = Scale.scale_from_scale_and_degree(scale,degree)
        return Chord.chord_from_scale(ds, [0,2,4,6])


    @staticmethod
    def symbol_to_chord(scale,symbol) :

        xs = ["_1", "_2", "_3", "_4", "_5", "_6", "_7"]
        if symbol in xs :
            return Chord.degree_chord(scale,xs.index(symbol)+1)
        xs = ["_17", "_27", "_37", "_47", "_57", "_67", "_77"]
        if symbol in xs :
            return Chord.degree_chord7(scale,xs.index(symbol)+1)
        xs = ["I","II","III","IV","V","VI","VII"]
        if symbol in xs :
            return Chord.major_triad(scale.get_root()+xs.index(symbol)+1)
        xs = ["i","ii","iii","iv","v","vi","vii"]
        if symbol in xs :
            return Chord.minor_triad(scale.get_root()+xs.index(symbol)+1)
        xs = ["I7","II7","III7","IV7","V7","VI7","VII7"]
        if symbol in xs :
            return Chord.major_7th(scale.get_root()+xs.index(symbol)+1)
        xs = ["i7","ii7","iii7","iv7","v7","vi7","vii7"]
        if symbol in xs :
            return Chord.minor_7th(scale.get_root()+xs.index(symbol)+1)
        raise GoldenPondException("Chord %s not understood" % symbol)



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
    def set_duration(self,d) : self.dur = d
    def get_abs_time(self) :
        if self.abs_time == None :
            raise GoldenPondException("No absolute time available for event %s" % self)
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

    def __len__(self) :
        return len(self.get_events())

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

    def get_notes(self) :
        return [tuple(e.get_data().get_notes()) for e in self]

    def get_durations(self) :
        return [e.get_duration() for e in self]

    def get_root_seq(self) :
        return EventSeq( [Event(Note(e.get_data().get_notes()[0]), e.get_duration()) for e in self] )
        

    def truncate_on(self, p_finish) :
        events = self.copy_events()
        build_dur = 0
        while True :
            e = events[-1]
            if p_finish(e) :
                e.set_duration(e.get_duration() + build_dur)
                break
            else :
                build_dur = build_dur + e.get_duration()
                events = events[:-1]
        return EventSeq(events)
            


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


class GoldenPondException(Exception) :
    pass



class ChordSeqBuilder :

    def chordseq(self,sc,root,cs,ts) :
        assert_scale(sc)
        assert_midinote(root)

        if len(cs) != len(ts) :
            raise GoldenPondException("Chord list and time list different lengths")
        i = 0
        flag = True
        events = []
        while flag :
            if i >= len(cs) :
                return EventSeq(events)
            data = Chord.symbol_to_chord(sc, cs[i])
            duration = ts[i]
            events.append(Event(data,duration))
            i=i+1

    def major(self,root,cs,ts) :
        return self.chordseq(Scale.major(root), root, cs, ts)

    def minor(self,root,cs,ts) :
        return self.chordseq(Scale.minor(root), root, cs, ts)



class FoxBuilder :
    def __init__(self, root) :
        self.root = root
        self.csb = ChordSeqBuilder()

    def setRoot(self, root) : self.root = root

    def newMajor(self, chords, timings= [2,2,2,2]) :
        return self.csb.major(self.root, chords, timings)

    def newMinor(self, chords, timings= [2,2,2,2]) :
        return self.csb.minor(self.root, chords, timings)



class Music :

    def __init__(self,key="C",mode="major", root=60,mode_scale=None, octave=4) :
        assert_notename(key)
        self.key = key
        self.octave = octave
        self.root = root
        self.mode = mode
        self.mode_scale = mode_scale
        self.tracks = [EventSeq([])]
        self.current_default = 0
        self.csb = ChordSeqBuilder()

    def get_key(self) : return self.key

    def get_root(self) : return self.root

    def get_mode(self) : return self.mode

    def no_tracks(self) : return len(self.tracks)
    
    def duration(self) :
        return self.tracks[0].duration()
    
    def current_default_track(self) :
        return self.current_default

    def add(self,chords,timings) :
        if self.mode == "major" :
            newseq = self.csb.major(self.root, chords, timings)
        else :
            newseq = self.csb.minor(self.root, chords, timings)

        self.tracks[self.current_default] = self.tracks[self.current_default] + newseq
        return self

    def add_seq(self,events) :
        self.tracks[self.current_default] = self.tracks[self.current_default] + events

    def new_track(self) :
        self.tracks.append(EventSeq([]))
        return self

    def track(self,i) :
        if i >= len(self.tracks) : 
            raise Exception("Tried to set track number %s but only have %s tracks" % (i,self.no_tracks()))
        self.current_default = i
        return self

    def get_track(self, i) :
        return self.tracks[i]

    def get_notes_for_track(self, i) :
        return self.tracks[i].get_notes()

    def get_durations_for_track(self,i) :
        return self.tracks[i].get_durations()

    def random_notes(self) :
        return ScaleChooseSequence(self.mode_scale, 1, self.duration())

    
