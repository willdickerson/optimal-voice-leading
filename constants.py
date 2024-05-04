# spread triads
triads = {
    'C': ['C G E', 'E C G', 'G E C'],
    'Cm': ['C G Eb', 'Eb C G', 'G Eb C'],
    'C#': ['C# G# E#', 'E# C# G#', 'G# E# C#'],
    'C#m': ['C# G# E', 'E C# G#', 'G# E C#'],
    'D': ['D A F#', 'F# D A', 'A F# D'],
    'Dm': ['D A F', 'F D A', 'A F D'],
    'Eb': ['Eb Bb G', 'G Eb Bb', 'Bb G Eb'],
    'Ebm': ['Eb Bb Gb', 'Gb Eb Bb', 'Bb Gb Eb'],
    'E': ['E B G#', 'G# E B', 'B G# E'],
    'Em': ['E B G', 'G E B', 'B G E'],
    'F': ['F C A', 'A F C', 'C A F'],
    'Fm': ['F C Ab', 'Ab F C', 'C Ab F'],
    'F#': ['F# C# A#', 'A# F# C#', 'C# A# F#'],
    'F#m': ['F# C# A', 'A F# C#', 'C# A F#'],
    'G': ['G D B', 'B G D', 'D B G'],
    'Gm': ['G D Bb', 'Bb G D', 'D Bb G'],
    'Ab': ['Ab Eb C', 'C Ab Eb', 'Eb C Ab'],
    'Abm': ['Ab Eb B', 'B Ab Eb', 'Eb B Ab'],
    'A': ['A E C#', 'C# A E', 'E C# A'],
    'Am': ['A E C', 'C A E', 'E C A'],
    'Bb': ['Bb F D', 'D Bb F', 'F D Bb'],
    'Bbm': ['Bb F Db', 'Db Bb F', 'F Db Bb'],
    'B': ['B F# D#', 'D# B F#', 'F# D# B'],
    'Bm': ['B F# D', 'D B F#', 'F# D B'],
}

# Mapping notes to MIDI note numbers (central octave as base)
note_to_midi_base = {
    'C': 60, 'C#': 61, 'Db': 61, 'D': 62, 'D#': 63, 'Eb': 63,
    'E': 64, 'F': 65, 'F#': 66, 'Gb': 66, 'G': 67, 'G#': 68,
    'Ab': 68, 'A': 69, 'A#': 70, 'Bb': 70, 'B': 71
}