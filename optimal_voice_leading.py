import networkx as nx
import itertools
import argparse
from constants import triads, note_to_midi_base
from midi_player import find_fluidsynth_port, play_midi_sequence
import mido

def find_all_triads_in_range(notes: list, midi_range: tuple) -> list:
    """
    Find all possible ways to play a triad within the specified MIDI range.

    Args:
        notes (list): A list of note names representing the triad.
        midi_range (tuple): A tuple specifying the desired MIDI range (min, max).

    Returns:
        list: A list of lists, where each inner list represents a valid MIDI note combination for the triad within the range.
    """
    base_midis = [note_to_midi_base[note] for note in notes]
    min_octave = (midi_range[0] - min(base_midis)) // 12
    max_octave = (midi_range[1] - max(base_midis)) // 12
    
    octave_combinations = itertools.product(range(min_octave, max_octave + 1), repeat=len(notes))
    valid_midis = []

    for octaves in octave_combinations:
        midi_notes = [base_midi + octave * 12 for base_midi, octave in zip(base_midis, octaves)]
        if (midi_notes == sorted(midi_notes) and midi_notes[-1] - midi_notes[0] <= 24):
            valid_midis.append(midi_notes)

    return valid_midis

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
            current_midi_note_combinations = find_all_triads_in_range(current_notes, midi_range)

            for current_midi_notes in current_midi_note_combinations:
                current_node = (i, current_chord, current_inversion, tuple(current_midi_notes))
                graph.add_node(current_node)

                for next_inversion in triads[next_chord]:
                    next_notes = next_inversion.split()
                    next_midi_note_combinations = find_all_triads_in_range(next_notes, midi_range)

                    for next_midi_notes in next_midi_note_combinations:
                        next_node = (i + 1, next_chord, next_inversion, tuple(next_midi_notes))
                        cost = sum(abs(curr_midi - prev_midi) for prev_midi, curr_midi in zip(current_midi_notes, next_midi_notes))
                        graph.add_edge(current_node, next_node, weight=cost)

    return graph

def find_optimal_voice_leading(graph: nx.DiGraph, start_chords: list, chords: list) -> list:
    """
    Find the optimal voice leading path in the graph.

    Args:
        graph (nx.DiGraph): The voice leading graph.
        start_chords (list): A list of possible starting chords.
        chords (list): The list of chords.

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

def main():
    parser = argparse.ArgumentParser(description="Optimal Voice Leading")
    parser.add_argument("--play", action="store_true", help="Initialize and play the MIDI sequence")
    parser.add_argument("--print-graph", action="store_true", help="Pretty print the voice leading graph")
    args = parser.parse_args()

    # Example usage
    chords = ["B", "D", "G", "Bb", "Eb", "Eb", "Am", "D", "G", "Bb", "Eb", "F#", "B", "B", "Fm", "Bb", "Eb", "Eb", "Am", "D", "G", "G", "C#m", "F#", "B", "B", "Fm", "Bb", "Eb", "Eb", "C#m", "F#"]
    # chords = ["C", "F", "G"]
    midi_range = (40, 90)

    voice_leading_graph = build_voice_leading_graph(chords, midi_range)
    start_chords = [(node[0], node[1], node[2], node[3]) for node in voice_leading_graph.nodes() if node[0] == 0 and node[1] == chords[0]]
    optimal_path_midis = find_optimal_voice_leading(voice_leading_graph, start_chords, chords)

    if args.print_graph:
        print("Graph Nodes:")
        for node in voice_leading_graph.nodes(data=True):
            print(node)

        print("\nGraph Edges:")
        for edge in voice_leading_graph.edges(data=True):
            print(edge)

    print("\nOptimal Path:")
    for chord_name, inversion, midi_notes in optimal_path_midis:
        print(f"{chord_name}: {inversion} -> MIDI Notes: {midi_notes}")

    if args.play:
        fluidsynth_port = find_fluidsynth_port()
        if fluidsynth_port:
            outport = mido.open_output(fluidsynth_port)
            play_midi_sequence(outport, optimal_path_midis)
            outport.close()
        else:
            print("FluidSynth virtual port not found. Please make sure FluidSynth is running by executing: fluidsynth -a coreaudio -m coremidi /Users/wdickerson/Repos/scratchpad/gs/gs.sf2.")
            exit(1)

if __name__ == "__main__":
    main()