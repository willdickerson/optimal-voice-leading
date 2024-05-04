import networkx as nx
import mido
import time
import itertools
from constants import triads, note_to_midi_base

# start fluidsynth
# fluidsynth -a coreaudio -m coremidi /Users/wdickerson/Repos/scratchpad/gs/gs.sf2

CENTRAL_OCTAVE_C = 60
MIDI_VELOCITY = 127
CHORD_DURATION = 0.5
PAUSE_DURATION = 0.1

def find_fluidsynth_port():
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

fluidsynth_port = find_fluidsynth_port()

if fluidsynth_port:
    outport = mido.open_output(fluidsynth_port)
else:
    print("FluidSynth virtual port not found. Please make sure FluidSynth is running by executing: fluidsynth -a coreaudio -m coremidi /Users/wdickerson/Repos/scratchpad/gs/gs.sf2.")
    exit(1)

def play_note(midi_note: int, duration: float = CHORD_DURATION, velocity: int = MIDI_VELOCITY) -> None:
    """
    Play a MIDI note with the specified duration and velocity.

    Args:
        midi_note (int): The MIDI note number to play.
        duration (float): The duration of the note in seconds (default: CHORD_DURATION).
        velocity (int): The velocity of the note (default: MIDI_VELOCITY).
    """
    outport.send(mido.Message('note_on', note=midi_note, velocity=velocity))
    time.sleep(duration)
    outport.send(mido.Message('note_off', note=midi_note, velocity=velocity))

def play_midi_sequence(midi_numbers: list) -> None:
    """
    Play a sequence of MIDI chords.

    Args:
        midi_numbers (list): A list of tuples containing the chord name, inversion, and MIDI notes for each chord.
    """
    for chord_name, inversion, midi_notes in midi_numbers:
        print(f"Playing {chord_name}: {inversion}")
        for midi_note in midi_notes:
            play_note(midi_note)
        time.sleep(PAUSE_DURATION)

def find_closest_triad_in_range(notes: list, midi_range: tuple) -> list:
    """
    Find the closest triad within the specified MIDI range.

    Args:
        notes (list): A list of note names representing the triad.
        midi_range (tuple): A tuple specifying the desired MIDI range (min, max).

    Returns:
        list: A list of MIDI note numbers representing the closest triad within the range.
    """
    base_midis = [note_to_midi_base[note] for note in notes]
    octave_combinations = itertools.product(range(-2, 3), repeat=len(notes))
    best_midis = None
    best_distance = float('inf')

    for octaves in octave_combinations:
        midi_notes = [base_midi + octave * 12 for base_midi, octave in zip(base_midis, octaves)]
        # Check if the MIDI notes are within the desired range and in ascending order
        if all(midi_range[0] <= midi <= midi_range[1] for midi in midi_notes) and midi_notes == sorted(midi_notes):
            # Calculate the distance between the MIDI notes and the center of the range
            distance = sum(abs(midi - midi_range[0] - (midi_range[1] - midi_range[0]) // 2) for midi in midi_notes)
            if distance < best_distance:
                best_midis = midi_notes
                best_distance = distance

    return best_midis

def build_voice_leading_graph(chords: list, midi_range: tuple) -> nx.DiGraph:
    """
    Build a directed graph representing the voice leading possibilities between chords.

    Args:
        chords (list): A list of chord names.
        midi_range (tuple): A tuple specifying the desired MIDI range (min, max).

    Returns:
        nx.DiGraph: A directed graph representing the voice leading possibilities.
    """
    graph = nx.DiGraph()

    for i in range(len(chords) - 1):
        current_chord = chords[i]
        next_chord = chords[i + 1]

        for current_inversion in triads[current_chord]:
            current_notes = current_inversion.split()
            current_midi_notes = find_closest_triad_in_range(current_notes, midi_range)

            if current_midi_notes:
                current_node = (i, current_chord, current_inversion, tuple(current_midi_notes))
                graph.add_node(current_node)

                for next_inversion in triads[next_chord]:
                    next_notes = next_inversion.split()
                    next_midi_notes = find_closest_triad_in_range(next_notes, midi_range)

                    if next_midi_notes:
                        next_node = (i + 1, next_chord, next_inversion, tuple(next_midi_notes))
                        cost = sum(min(abs(prev_midi - curr_midi), 12 - abs(prev_midi - curr_midi)) for prev_midi, curr_midi in zip(current_midi_notes, next_midi_notes))
                        graph.add_edge(current_node, next_node, weight=cost)

    return graph

def find_optimal_voice_leading(graph: nx.DiGraph, start_chords: list) -> list:
    """
    Find the optimal voice leading path in the graph.

    Args:
        graph (nx.DiGraph): The voice leading graph.
        start_chords (list): A list of possible starting chords.

    Returns:
        list: A list of tuples representing the optimal voice leading path, containing the chord name, inversion, and MIDI notes for each chord.
    """
    best_cost = float('inf')
    best_path = []
    best_path_midis = []

    for start_chord in start_chords:
        lengths, paths = nx.single_source_dijkstra(graph, start_chord)
        target_chords = [(node[0], node[1], node[2], node[3]) for node in graph.nodes() if node[0] == len(chords) - 1 and node[1] == chords[-1]]

        for target in target_chords:
            if target in paths:
                if lengths[target] < best_cost:
                    best_cost = lengths[target]
                    best_path = paths[target]

    if best_path:
        for node in best_path:
            chord_index, chord_name, inversion, midi_notes = node
            best_path_midis.append((chord_name, inversion, midi_notes))

    return best_path_midis

# Example usage
chords = ["B", "D", "G", "Bb", "Eb", "Eb", "Am", "D", "G", "Bb", "Eb", "F#", "B", "B", "Fm", "Bb", "Eb", "Eb", "Am", "D", "G", "G", "C#m", "F#", "B", "B", "Fm", "Bb", "Eb", "Eb", "C#m", "F#"]
midi_range = (45, 75)

voice_leading_graph = build_voice_leading_graph(chords, midi_range)
start_chords = [(node[0], node[1], node[2], node[3]) for node in voice_leading_graph.nodes() if node[0] == 0 and node[1] == chords[0]]
optimal_path_midis = find_optimal_voice_leading(voice_leading_graph, start_chords)

print("Graph Nodes:")
for node in voice_leading_graph.nodes(data=True):
    print(node)

print("\nOptimal Path:")
for chord_name, inversion, midi_notes in optimal_path_midis:
    print(f"{chord_name}: {inversion} -> MIDI Notes: {midi_notes}")

play_midi_sequence(optimal_path_midis)

outport.close()