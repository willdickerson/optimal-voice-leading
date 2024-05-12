"""
Provides utility functions for constructing and analyzing voice leading graphs.
This includes finding all possible triads within a specified MIDI range, building a directed graph
of possible paths, and finding the optimal path through this graph based on minimum voice leading 
movement.
"""

import itertools
import networkx as nx
from constants import NOTE_TO_MIDI_BASE

def find_all_triads_in_range(notes: list, midi_range: tuple) -> list:
    """
    Find all possible ways to play a triad within the specified MIDI range, 
    ensuring that no two neighboring notes in the triad are more than one octave apart.

    Args:
        notes (list): A list of note names representing the triad.
        midi_range (tuple): A tuple specifying the desired MIDI range (min, max).

    Returns:
        list: A list of lists, where each inner list represents a valid MIDI note combination for the triad within the range.
    """
    base_midis = [NOTE_TO_MIDI_BASE[note] for note in notes]
    octave_combinations = itertools.product(range(-2, 3), repeat=len(notes))
    valid_midis = []

    for octaves in octave_combinations:
        midi_notes = [base_midi + octave * 12 for base_midi, octave in zip(base_midis, octaves)]
        # Check if the MIDI notes are within the desired range and in ascending order
        if (all(midi_range[0] <= midi <= midi_range[1] for midi in midi_notes) and midi_notes == sorted(midi_notes)):
            # Check that no two neighboring notes are more than an octave apart
            if all(abs(midi_notes[i+1] - midi_notes[i]) <= 12 for i in range(len(midi_notes) - 1)):
                valid_midis.append(midi_notes)

    return valid_midis


def build_voice_leading_graph(chords: list, midi_range: tuple, triads: dict) -> nx.DiGraph:
    """
    Build a directed graph representing the voice leading possibilities between chords.
    Adjusts for repeated chords by choosing the next smallest non-zero voice leading cost.

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

                next_nodes = []

                for next_inversion in triads[next_chord]:
                    next_notes = next_inversion.split()
                    next_midi_note_combinations = find_all_triads_in_range(next_notes, midi_range)

                    for next_midi_notes in next_midi_note_combinations:
                        next_node = (i + 1, next_chord, next_inversion, tuple(next_midi_notes))
                        cost = sum(abs(curr_midi - prev_midi) for prev_midi, curr_midi in zip(current_midi_notes, next_midi_notes))
                        next_nodes.append((next_node, cost))

                # If the current and next chords are the same, and there are multiple nodes, select the one with the smallest non-zero cost
                if current_chord == next_chord:
                    next_nodes.sort(key=lambda x: x[1])
                    # This filters out zero-cost paths and selects the smallest non-zero cost path
                    filtered_nodes = [node for node in next_nodes if node[1] > 0]
                    if filtered_nodes:
                        next_node, cost = filtered_nodes[0]
                        graph.add_edge(current_node, next_node, weight=cost)
                    else:
                        # If all costs are zero (unlikely but possible with identical chords and inversions), revert to the smallest cost
                        next_node, cost = next_nodes[0]
                        graph.add_edge(current_node, next_node, weight=cost)
                else:
                    for next_node, cost in next_nodes:
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
            _, chord_name, inversion, midi_notes = node
            best_path_midis.append((chord_name, inversion, midi_notes))

    return best_path_midis
