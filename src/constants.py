"""
This module contains constants and mappings used for optimal voice leading in chord progressions.

Constants:
- NOTE_TO_MIDI_BASE: A dictionary mapping note names to their corresponding MIDI note numbers in the central octave.
- CHORD_DURATION: The duration of each chord in seconds.
- PAUSE_DURATION: The duration of the pause between chords in seconds.
- MIDI_VELOCITY: The velocity of the MIDI notes.
- CHROMATIC_SCALE: The chromatic scale in sharp and flat notations.
- ENHARMONIC_MAP: A mapping of enharmonic equivalents for notes that have multiple names.
- SCALE_INTERVALS: Defines intervals for major, minor, diminished, and augmented scales.
- GIANT_STEPS: "Giant Steps" progression as a list of chord names.
- TWENTY_SIX_TWO: "26-2" progression as a list of chord names.
- ALL_THE_THINGS_YOU_ARE: "All the Things You Are" progression as a list of chord names.
"""

# Mapping notes to MIDI note numbers (central octave as base)
NOTE_TO_MIDI_BASE = {
    'C': 60, 'C#': 61, 'Db': 61, 'D': 62, 'D#': 63, 'Eb': 63,
    'E': 64, 'F': 65, 'F#': 66, 'Gb': 66, 'G': 67, 'G#': 68,
    'Ab': 68, 'A': 69, 'A#': 70, 'Bb': 70, 'B': 71
}

CHORD_DURATION = 0.5
PAUSE_DURATION = 0.1
MIDI_VELOCITY = 127

CHROMATIC_SCALE = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

ENHARMONIC_MAP = {
    'C#': 'Db', 'Db': 'Db',
    'D#': 'Eb', 'Eb': 'Eb',
    'F#': 'Gb', 'Gb': 'Gb',
    'G#': 'Ab', 'Ab': 'Ab',
    'A#': 'Bb', 'Bb': 'Bb'
}

SCALE_INTERVALS = {
    'M': [2, 2, 1, 2, 2, 2, 1], # Major
    'm': [2, 1, 2, 2, 1, 2, 2], # Minor
    'dim': [2, 1, 2, 1, 2, 1, 2], # Diminished
    'aug': [3, 1, 3, 1, 3]  # Augmented
}

GIANT_STEPS = [
    "B", "D", "G", "Bb", "Eb", "Eb", "Am", "D",
    "G", "Bb", "Eb", "F#", "B", "B", "Fm", "Bb",
    "Eb", "Eb", "Am", "D", "G", "G", "C#m", "F#", 
    "B", "B", "Fm", "Bb", "Eb", "Eb", "C#m", "F#"
]

TWENTY_SIX_TWO = [
    "F", "Ab", "Db", "E", "A", "C", "Cm", "F",
    "Bb", "Db", "Gb", "A", "Dm", "G", "Gm", "C", 
    "F", "Ab", "Db", "E", "A", "C", "Cm", "F",
    "Bb", "Ab", "Db", "E", "A", "C", "F", "F",
    "Cm", "F", "Em", "A", "D", "F", "Bb", "Bb",
    "Ebm", "Ebm", "Ab", "Ab", "Db", "Db", "Gm", "C",
    "F", "Ab", "Db", "E", "A", "C", "Cm", "F",
    "Bb", "Ab", "Db", "E", "A", "C", "F", "F"
]

ALL_THE_THINGS_YOU_ARE = [
    "Fm", "Fm", "Bbm", "Bbm", "Eb", "Eb", "Ab", "Ab",
    "Db", "Db", "Dm", "G", "C", "C", "C", "C",
    "Cm", "Cm", "Fm", "Fm", "Bb", "Bb", "Eb", "Eb",
    "Ab", "Ab", "Am", "D", "G", "G", "G", "G",
    "Am", "Am", "D", "D", "G", "G", "G", "G",
    "F#dim", "F#dim", "B", "B", "E", "E", "C", "C",
    "Fm", "Fm", "Bbm", "Bbm", "Eb", "Eb", "Ab", "Ab",
    "Db", "Db", "Dbm", "Dbm", "Cm", "Cm", "Bdim", "Bdim",
    "Bbm", "Bbm", "Eb", "Eb", "Ab", "Ab", "Gm", "C"
]
