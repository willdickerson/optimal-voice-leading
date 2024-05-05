import mido
import time

CHORD_DURATION = 0.5
PAUSE_DURATION = 0.1
MIDI_VELOCITY = 127

def find_fluidsynth_port() -> str:
    """
    Find the FluidSynth virtual port from the available output ports.

    Returns:
        str: The name of the FluidSynth virtual port, or None if not found.
    """
    output_names = mido.get_output_names()
    for name in output_names:
        if 'FluidSynth virtual port' in name:
            return name
    return None

def play_note(outport: mido.ports.IOPort, midi_note: int, duration: float = CHORD_DURATION, velocity: int = MIDI_VELOCITY) -> None:
    """
    Play a MIDI note with the specified duration and velocity.

    Args:
        outport (mido.ports.IOPort): The MIDI output port.
        midi_note (int): The MIDI note number to play.
        duration (float): The duration of the note in seconds (default: CHORD_DURATION).
        velocity (int): The velocity of the note (default: MIDI_VELOCITY).
    """
    outport.send(mido.Message('note_on', note=midi_note, velocity=velocity))
    time.sleep(duration)
    outport.send(mido.Message('note_off', note=midi_note, velocity=velocity))

def play_midi_sequence(outport: mido.ports.IOPort, midi_numbers: list) -> None:
    """
    Play a sequence of MIDI chords.

    Args:
        outport (mido.ports.IOPort): The MIDI output port.
        midi_numbers (list): A list of tuples containing the chord name, inversion, and MIDI notes for each chord.
    """
    for chord_name, inversion, midi_notes in midi_numbers:
        print(f"Playing {chord_name}: {inversion}")
        for midi_note in midi_notes:
            play_note(outport, midi_note)
        time.sleep(PAUSE_DURATION)