## NOTE: This project and library is now deprecated
SEE https://github.com/interstar/golden-pond for the later work on this project. The code there has been rewritten from scratch. Soon we hope to reach parity with this project in the sense that the new GoldenPond library will be compatible with FoxDot, among other frameworks and contexts.

### GoldenPond : Music generation in Python

GoldenPond is a Python library for representing music.

I've been using Sonic Pi for a couple of years, but became disappointed with the way that livecoding had evolved to be more or less a tool for making very repetitive loop based music.

Given the expressivity of a programming lanaguge, why am I basically using it to represent simple grid based sequencers? When I could be expressing far more complex musical structures in elegant code?

Having discovered [FoxDot](https://foxdot.org/), the Python equivalent to Sonic Pi or TidalCycles, I began to think how I would like to be able to represent complex harmonic structures in code form, in a way that is simple enough to code on the fly.

Hence, this library, encapsulating some musical theory.

It's work in progress. And certainly not elegant enough for me to use live. But keep watching.

### Quick Start

**A note on Dependencies :** Current examples have been designed to work with FoxDot and Python's MIDI file library [MIDIUtil](https://pypi.org/project/MIDIUtil/) which we'll use in our quick start example. But note that MIDIUtil is NOT a dependency of this project. You should install it separately if you plan to use GoldenPond with MIDIUtil. 


```

pip install MIDIUtil

git clone https://github.com/interstar/goldenpond-py.git goldenpond

cd goldenpond/examples

ln -s ../goldenpond goldenpond

python3 midi.py


```

Then open example1.mid in your favourite MIDI file player.

### Basic Concepts


#### Event Sequences

Music in GoldenPond is represented as a number of *Event Sequences*. Of which the most common example is the ``EventSeq`` class.

An EventSeq is, naturally a sequence of ``Event`` objects.

All Event objects have two properties : some *data*, and a *duration*. 

Data is currently either a ``Note`` representing a single musical note. Or a ``Chord`` representing a collection of notes that are played at the same time.

Duration is an integer representing how long an event lasts. Measured in "ticks" of some abstract clock. A duration of 2 is double a duration of 1. But GoldenPond is not committed to how long 1 tick actually is until we come to render the music in a particular context.

Some Events, when part of an EventSeq will have a third property which is their absolute time (from the beginning of the piece)

Most of GoldenPond's functionality consists of various methods for producing and transforming EventSequences.

For example, two EventSequences can be concatenated together with the ``+`` operator. And GoldenPond overloads the ``*`` operator so that if you multiply an EventSeq by an integer, *n* it will be produces a longer EventSeq based on *n* repetitions of the EventSeq.

Other operations on EventSequences include *transpose* by a number of semitones. 

EventSequences can be *truncated* at a particular step by passing a predicate function. This allows us to say "stop the sequence at the last event that matches this predicate, but stretch the duration of that last event to fill the remaining duration of all the pruned events"

EventSequences can have *swing* added to them.

EventSequences can spawn other EventSequences that are musically related. For example, *get_root_seq* creates a new EventSequence containing only the root notes of chords from the parent sequence. This is useful for generating basslines.

EventSeq isn't the only kind of possible EventSequence. We can, for example, implement algorithmic composition rules behind the same EventSequence interface. An example in the current code-base is the ``ScaleChooseSequence`` which randomly chooses notes from a given scale every time it is asked to produce its next note. 

#### Notes, Chords and Scales

Along with Notes and Chords. ``Scale`` objects are the third important class of musical objects. Like Chords, Scales are a collection of musical notes. But are usually used not in concrete musical events but as potentials. ScaleChooseSequence, for example, is given a Scale which represents the set of notes from which it can randomly choose.

Notes, Chords and Scales are all based on the same component : the ``NoteBag`` which holds a collection of musical notes and can do various standard operations such as adding and subtracting from them all (ie. transposing them up or down), concatinating them (ie creating a larger collection of notes). 

Another trick of Scales is the *vamp* method, which takes a timing pattern and returns an EventSequence containing notes taken sequentially from the Scale, according to the rhythmic pattern it is given.

#### Building Chord Sequences

Most music stars with an EventSequence of Chords. And to help us construct one, we use the ``ChordSeqBuilder``

ChordSeqBuilder has knowledge of diatonic harmony ie. it thinks in terms of degree chords in a particular tonal centre or key. GoldenPond defines a number of symbols or variables which represent the chords to be used in a key. The simplest of these variables / symbols are _1, _2, _3, _4, _5, _6 and _7

Here's a short example :

```

    root = 64 # this is E
    csb = ChordSeqBuilder()
    
    rhyth1 = [2,2,4,4,4]
     
    chord_seq = csb.major(root, [_4,_6,_2,_5,_1], rhyth1)

```

In this example we build a sequence of chords in the key of E major. These chords are the sub-dominant 4th, the submediant 6th, the supertonic 2nd, the dominant 5th and the tonic 1 chord. Their durations are 2, 2, 4, 4, and 4 *ticks* respectively. 

We could expand on this :

```

    chord_seq = (csb.major(root, [_4,_6,_2,_5,_1], [2,2,4,4,4]) + csb.minor(root, [_4,_6,_2,_5,_5, _1], [2,2,4,2,2,4] ) ) * 8

```

This chord sequence has two phrases, the previous sequence in E major, followed by a very similar sequence in E minor. See how we use the ``+`` operator to concatenate them. 

But then the whole thing is multiplied by 8, ie. repeated 8 times. This now creates the framework for a substancial piece of music in a very concise line of code.




### Using with FoxDot

The other file in examples is foxdot.py.


FoxDot is a Python interface to the SuperCollider engine. So you'll need to install and set up SuperCollider, with the FoxDot Quark. And then install FoxDot itself. 

Follow the [FoxDot Installation Guide](https://foxdot.org/installation/).

Then run the SuperCollider IDE and the FoxDot Quark.

Now try going to examples and typing 

```
python3 foxdot.py

```

this will run FoxDot in a non-interactive mode, generating a score with GoldenPond and playing it in an infinite loop. See the code for commented explanation of how the music is constructed.



