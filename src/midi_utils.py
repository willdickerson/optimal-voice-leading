"""
Contains utility functions to interact with MIDI devices and files. It includes functions to 
find the FluidSynth virtual port, play MIDI notes and sequences, and create MIDI files based 
on optimal voice leading paths. These functions help in both live MIDI playback and storing 
MIDI sequences for future use.
"""

import time
import mido
from constants import CHORD_DURATION, MIDI_VELOCITY, PAUSE_DURATION

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
    print("\nPlaying MIDI sequence:")
    for chord_name, inversion, midi_notes in midi_numbers:
        print(f"Playing {chord_name}: {inversion}")
        for midi_note in midi_notes:
            play_note(outport, midi_note)
        time.sleep(PAUSE_DURATION)

def create_midi_file(optimal_path_midis: list, output_file: str):
    """
    Create a MIDI file with the optimal voice leading sequence.

    Args:
        optimal_path_midis (list): A list of tuples representing the optimal voice leading path.
        output_file (str): The name of the output MIDI file.
    """
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)

    ticks_per_beat = mid.ticks_per_beat

    track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(120)))

    for _, _, midi_notes in optimal_path_midis:
        for i, note in enumerate(midi_notes):
            if i < 2:
                track.append(mido.Message('note_on', note=note, velocity=64, time=0))
                track.append(mido.Message('note_off', note=note, velocity=64, time=ticks_per_beat))
            else:
                track.append(mido.Message('note_on', note=note, velocity=64, time=0))
                track.append(mido.Message('note_off', note=note, velocity=64, time=ticks_per_beat * 2))

    mid.save(output_file)
