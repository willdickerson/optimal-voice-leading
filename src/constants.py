"""
This module contains constants and mappings used for optimal voice leading in chord progressions.

Constants:
- TRIADS: A dictionary mapping chord names to their spread triad inversions.
- NOTE_TO_MIDI_BASE: A dictionary mapping note names to their corresponding MIDI note numbers in the central octave.
- CHORD_DURATION: The duration of each chord in seconds.
- PAUSE_DURATION: The duration of the pause between chords in seconds.
- MIDI_VELOCITY: The velocity of the MIDI notes.
"""

# spread triads
TRIADS = {
    'C': ['C G E', 'E C G', 'G E C'],
    'Cm': ['C G Eb', 'Eb C G', 'G Eb C'],
    'C#': ['C# G# F', 'F C# G#', 'G# F C#'],
    'Db': ['C# G# F', 'F C# G#', 'G# F C#'],
    'C#m': ['C# G# E', 'E C# G#', 'G# E C#'],
    'Dbm': ['C# G# E', 'E C# G#', 'G# E C#'],
    'D': ['D A F#', 'F# D A', 'A F# D'],
    'Dm': ['D A F', 'F D A', 'A F D'],
    'Eb': ['Eb Bb G', 'G Eb Bb', 'Bb G Eb'],
    'D#': ['Eb Bb G', 'G Eb Bb', 'Bb G Eb'],
    'Ebm': ['Eb Bb Gb', 'Gb Eb Bb', 'Bb Gb Eb'],
    'D#m': ['Eb Bb Gb', 'Gb Eb Bb', 'Bb Gb Eb'],
    'E': ['E B G#', 'G# E B', 'B G# E'],
    'Em': ['E B G', 'G E B', 'B G E'],
    'F': ['F C A', 'A F C', 'C A F'],
    'Fm': ['F C Ab', 'Ab F C', 'C Ab F'],
    'F#': ['F# C# A#', 'A# F# C#', 'C# A# F#'],
    'Gb': ['F# C# A#', 'A# F# C#', 'C# A# F#'],
    'F#m': ['F# C# A', 'A F# C#', 'C# A F#'],
    'Gbm': ['F# C# A', 'A F# C#', 'C# A F#'],
    'G': ['G D B', 'B G D', 'D B G'],
    'Gm': ['G D Bb', 'Bb G D', 'D Bb G'],
    'Ab': ['Ab Eb C', 'C Ab Eb', 'Eb C Ab'],
    'G#': ['Ab Eb C', 'C Ab Eb', 'Eb C Ab'],
    'Abm': ['Ab Eb B', 'B Ab Eb', 'Eb B Ab'],
    'G#m': ['Ab Eb B', 'B Ab Eb', 'Eb B Ab'],
    'A': ['A E C#', 'C# A E', 'E C# A'],
    'Am': ['A E C', 'C A E', 'E C A'],
    'Bb': ['Bb F D', 'D Bb F', 'F D Bb'],
    'A#': ['Bb F D', 'D Bb F', 'F D Bb'],
    'Bbm': ['Bb F Db', 'Db Bb F', 'F Db Bb'],
    'A#m': ['Bb F Db', 'Db Bb F', 'F Db Bb'],
    'B': ['B F# D#', 'D# B F#', 'F# D# B'],
    'Bm': ['B F# D', 'D B F#', 'F# D B'],
    'Cdim': ['C Gb Eb', 'Eb C Gb', 'Gb Eb C'],
    'Caug': ['C G# E', 'E C G#', 'G# E C'],
    'C#dim': ['C# E A', 'A C# E', 'E A C#'],
    'Dbdim': ['C# E A', 'A C# E', 'E A C#'],
    'C#aug': ['C# G F', 'F C# G', 'G F C#'],
    'Dbaug': ['Db G F', 'F Db G', 'G F Db'],
    'Ddim': ['D F Ab', 'Ab D F', 'F Ab D'],
    'Daug': ['D A# F#', 'F# D A#', 'A# F# D'],
    'D#dim': ['Eb Gb Bb', 'Bb Eb Gb', 'Gb Bb Eb'],
    'Ebdim': ['Eb Gb Bb', 'Bb Eb Gb', 'Gb Bb Eb'],
    'D#aug': ['Eb A G', 'G Eb A', 'A G Eb'],
    'Ebaug': ['Eb A G', 'G Eb A', 'A G Eb'],
    'Edim': ['E G Bb', 'Bb E G', 'G Bb E'],
    'Eaug': ['E G# B', 'B E G#', 'G# B E'],
    'Fdim': ['F Ab Cb', 'Cb F Ab', 'Ab Cb F'],
    'Faug': ['F A C#', 'C# F A', 'A C# F'],
    'F#dim': ['F# C A', 'A F# C', 'C A F#'],
    'Gbdim': ['F# A C', 'C F# A', 'A C F#'],
    'F#aug': ['F# A# C#', 'C# F# A#', 'A# C# F#'],
    'Gbaug': ['F# Bb D', 'D F# Bb', 'Bb D F#'],
    'Gdim': ['G Db Bb', 'Bb G Db', 'Db Bb G'],
    'Gaug': ['G B D#', 'D# G B', 'B D# G'],
    'G#dim': ['Ab B D', 'D Ab B', 'B D Ab'],
    'Abdim': ['Ab B D', 'D Ab B', 'B D Ab'],
    'G#aug': ['Ab C E', 'E Ab C', 'C E Ab'],
    'Abaug': ['Ab C E', 'E Ab C', 'C E Ab'],
    'Adim': ['A C Eb', 'Eb A C', 'C Eb A'],
    'Aaug': ['A C# E', 'E A C#', 'C# E A'],
    'A#dim': ['Bb Db F', 'F Bb Db', 'Db F Bb'],
    'Bbdim': ['Bb Db F', 'F Bb Db', 'Db F Bb'],
    'A#aug': ['Bb D F#', 'F# Bb D', 'D F# Bb'],
    'Bbaug': ['Bb D F#', 'F# Bb D', 'D F# Bb'],
    'Bdim': ['B F D', 'D B F', 'F D B'],
    'Baug': ['B D# G', 'G B D#', 'D# G B'],
}


# Mapping notes to MIDI note numbers (central octave as base)
NOTE_TO_MIDI_BASE = {
    'C': 60, 'C#': 61, 'Db': 61, 'D': 62, 'D#': 63, 'Eb': 63,
    'E': 64, 'F': 65, 'F#': 66, 'Gb': 66, 'G': 67, 'G#': 68,
    'Ab': 68, 'A': 69, 'A#': 70, 'Bb': 70, 'B': 71
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

CHORD_DURATION = 0.5
PAUSE_DURATION = 0.1
MIDI_VELOCITY = 127
