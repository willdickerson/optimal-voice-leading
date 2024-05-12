"""
This module provides utility functions for generating triads. 
It includes functions to generate all permutations of triads 
based on a given root note and chord type, supporting both 
close-position and spread triads.
"""

from itertools import permutations
import re
from constants import CHROMATIC_SCALE, SCALE_INTERVALS, ENHARMONIC_MAP

def generate_triads(chord: str, triad_type: str = 'spread') -> list:
    """
    Generate the triads for a given root note and chord type.

    Args:
        chord (str): The chord in the format 'RootNoteChordType' (e.g., 'Cm').
        triad_type (str): The type of triads to generate, can be 'all', 'close', or 'spread'.

    Returns:
        list: A list of triads for the given root note and chord type.
    """
    original_root, standardized_root, chord_type = parse_chord(chord)

    root_index = CHROMATIC_SCALE.index(standardized_root)
    intervals = SCALE_INTERVALS.get(chord_type, SCALE_INTERVALS['M'])

    notes = [
        CHROMATIC_SCALE[root_index],
        CHROMATIC_SCALE[(root_index + sum(intervals[:2])) % len(CHROMATIC_SCALE)],
        CHROMATIC_SCALE[(root_index + sum(intervals[:4])) % len(CHROMATIC_SCALE)]
    ]

    triad_permutations = [' '.join(p) for p in permutations(notes)]

    if triad_type == "all":
        triads = triad_permutations 
    elif triad_type == "close":
        triads = [triad_permutations[0], triad_permutations[3], triad_permutations[4]]  # Close positions
    elif triad_type == "spread":
        triads = [triad_permutations[1], triad_permutations[2], triad_permutations[5]]  # Spread positions

    # Replace standardized root with original to maintain notation consistency
    return [triad.replace(standardized_root, original_root) for triad in triads]

def parse_chord(chord: str) -> tuple:
    """
    Parses a chord notation into its constituent root note and chord type.

    Args:
        chord (str): The chord notation.

    Returns:
        tuple: A tuple containing the original root note, the standardized root note, and the chord type.
    """
    match = re.match(r"([A-G][#b]?)(.*)", chord)
    original_root_note = match.group(1)
    standardized_root_note = ENHARMONIC_MAP.get(original_root_note, original_root_note)
    chord_type = match.group(2) if match.group(2) else 'M'  # Default to major if not specified
    return original_root_note, standardized_root_note, chord_type
