from .lancehead import Chord, Scale, ChordSeq, ChordBuilder, ScaleBuilder, ChordSeqBuilder, LanceHead, NOTE_NAMES, DEGREE_NAMES

#from typing import List
#__all__: List[str] = []

__all__ = []

def _setup_names():
    g = globals()
    # add the names to the module globals, each variable a string equal to the name
    g.update({t: t for t in DEGREE_NAMES})
    # add the names to __all__
    __all__.extend(DEGREE_NAMES)

_setup_names()

