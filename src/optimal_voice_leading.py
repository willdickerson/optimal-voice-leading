"""
This script provides functionality to find the optimal voice leading triads through a 
sequence of chords. It parses command-line arguments to output various forms of the triad 
sequence, such as playing it as MIDI, outputting to a PDF, or displaying the voice leading 
graph. Uses various utility modules to handle MIDI files and musical engraving.

Usage:
    python optimal_voice_leading.py [options]

Options:
    --play, --print-graph, --output-midi, --output-pdf, etc.
"""

import argparse
import os
from datetime import datetime
import mido
from constants import GIANT_STEPS
from midi_utils import find_fluidsynth_port, play_midi_sequence, create_midi_file
from engraving_utils import convert_to_music21
from graph_utils import build_voice_leading_graph, find_optimal_voice_leading
from chord_utils import generate_triads

def main():
    """
    Main function to parse command-line arguments, build the voice leading graph,
    find the optimal voice leading path, and output the results based on the provided arguments.

    Command-line arguments:
        --play: Initialize and play the MIDI sequence.
        --print-graph: Pretty print the voice leading graph.
        --output-midi: Output the optimal voice leading sequence to a MIDI file.
        --output-pdf: Output the optimal voice leading sequence to a PDF file with standard musical notation.
        --name: Specify the name of the song for output files.
        --chords: Specify the chord chart as a comma-separated string.
        --range: Specify the note range as a comma-separated string (e.g., "40,90").
    """
    parser = argparse.ArgumentParser(description="Optimal Voice Leading")
    parser.add_argument("--play", action="store_true", help="Initialize and play the MIDI sequence")
    parser.add_argument("--print-graph", action="store_true", help="Pretty print the voice leading graph")
    parser.add_argument("--output-midi", action="store_true", help="Output the optimal voice leading sequence to a MIDI file")
    parser.add_argument("--output-pdf", action="store_true", help="Output the optimal voice leading sequence to a PDF file with standard musical notation")
    parser.add_argument("--name", type=str, help="Specify the name of the song for output files")
    parser.add_argument("--chords", type=str, default="", help="Specify the chord chart as a comma-separated string")
    parser.add_argument("--range", type=str, default="40,90", help="Specify the note range as a comma-separated string (e.g., '40,90')")
    parser.add_argument("--triad-type", type=str, default='spread', help="Specify the type of triads to generate, can be 'all', 'close', or 'spread'.")
    args = parser.parse_args()

    print("\nOptimal Voice Leading")

    if args.chords:
        chords = args.chords.split(",")
    else:
        # Default chord chart (Giant Steps)
        chords = GIANT_STEPS
        print("\nDefault chord sequence 'Giant Steps' is used.")

    triads = {chord: generate_triads(chord, triad_type=args.triad_type) for chord in set(chords)}

    if args.range:
        midi_range = tuple(map(int, args.range.split(",")))
    else:
        # Default guitar range
        midi_range = (40, 90)

    voice_leading_graph = build_voice_leading_graph(chords, midi_range, triads)
    start_chords = [(node[0], node[1], node[2], node[3]) for node in voice_leading_graph.nodes() if node[0] == 0 and node[1] == chords[0]]
    optimal_path_midis = find_optimal_voice_leading(voice_leading_graph, start_chords, chords)

    print("\nOptimal Path:")
    for chord_name, inversion, midi_notes in optimal_path_midis:
        print(f"{chord_name}: {inversion} -> MIDI Notes: {midi_notes}")
    
    if args.print_graph:
        print("\nGraph Nodes:")
        for node in voice_leading_graph.nodes(data=True):
            print(node)

        print("\nGraph Edges:")
        for edge in voice_leading_graph.edges(data=True):
            print(edge)

    if args.name:
        song_name = args.name
    else:
        current_date = datetime.now().strftime("%Y%m%d")
        song_name = current_date

    output_dir = "../output"
    os.makedirs(output_dir, exist_ok=True)

    if args.output_midi:
        output_midi_file = os.path.join(output_dir, f"{song_name.lower().replace(' ', '_')}.mid")
        create_midi_file(optimal_path_midis, output_midi_file)

    if args.output_pdf:
        score = convert_to_music21(optimal_path_midis, song_name)
        output_xml = os.path.join(output_dir, f"{song_name.lower().replace(' ', '_')}.xml")
        output_pdf = os.path.join(output_dir, f"{song_name.lower().replace(' ', '_')}.pdf")
        score.write('musicxml', fp=output_xml)
        score.show('musicxml.pdf', fp=output_pdf)
        
    if args.play:
        fluidsynth_port = find_fluidsynth_port()
        if fluidsynth_port:
            outport = mido.open_output(fluidsynth_port)
            play_midi_sequence(outport, optimal_path_midis)
            outport.close()
        else:
            print("\nFluidSynth virtual port not found. Please make sure FluidSynth is running by executing: fluidsynth -a coreaudio -m coremidi /path/to/soundfont.")
            exit(1)

if __name__ == "__main__":
    main()
