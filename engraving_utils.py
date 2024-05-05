from music21 import note, stream, meter, key, metadata, harmony

def convert_to_music21(optimal_path_midis, song_name):
    """
    Convert the optimal voice leading path to a music21 Score object with arpeggiated triads and chord names displayed above each measure.

    Args:
        optimal_path_midis (list): A list of tuples representing the optimal voice leading path, containing the chord name, inversion, and MIDI notes for each chord.
        song_name (str): The name of the song.

    Returns:
        music21.stream.Score: A music21 Score object representing the optimal voice leading sequence with arpeggiated triads and chord names above each measure.
    """
    score = stream.Score()
    part = stream.Part()
    print("Optimal Path MIDIs:", optimal_path_midis)

    score.metadata = metadata.Metadata()
    score.metadata.title = f"{song_name} \n(Voice Leading Étude)"
    score.metadata.composer = ""

    time_signature = meter.TimeSignature('4/4')
    key_signature = key.KeySignature(0)  # No sharps or flats
    score.append(time_signature)
    score.append(key_signature)

    measure_duration = 4.0  # Assuming each measure has a duration of 4 beats
    current_measure = stream.Measure()
    current_time = 0.0

    for chord_name, inversion, midi_notes in optimal_path_midis:
        # Parse the chord name to the correct format
        parsed_chord_name = chord_name.replace("b", "-")
        # Create a ChordSymbol object for the parsed chord name
        chord_symbol = harmony.ChordSymbol(parsed_chord_name)
        chord_symbol.writeAsChord = False  # Display as chord symbol, not pitches

        if current_time == 0.0:
            # Align chord symbol with beat 1 of the measure
            current_measure.insert(0.0, chord_symbol)
        else:
            # Append the current measure and start a new one
            part.append(current_measure)
            current_measure = stream.Measure()
            current_time = 0.0
            current_measure.insert(0.0, chord_symbol)

        # Create individual notes for each MIDI note in the triad
        for i, midi_note in enumerate(midi_notes):
            note_obj = note.Note(midi_note)
            if i < 2:
                note_obj.duration.type = 'quarter'
            else:
                note_obj.duration.type = 'half'
            current_measure.append(note_obj)
            current_time += note_obj.duration.quarterLength

    if len(current_measure) > 0:
        part.append(current_measure)
    score.append(part)

    return score