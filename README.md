# Optimal Voice Leading

## Introduction

Voice leading is the practice of connecting chords in a musical progression with minimal movement. For instance, transitioning from C to F:

C: C E G

F: C F A

Here, the upper voices (E and G) move to the nearest notes in the F chord (F and A), while the bottom voice (C) remains static, thus minimizing total movement.

The presiding genius of voice leading is J. S. Bach. Listen to his chorales or The Well-Tempered Clavier and you'll see what I mean. 

## About Triads

A triad consists of three notes derived from a scale. For example, a C major triad with the notes CEG is formed from the 1st, 3rd, and 5th degrees of the C major scale. These notes can be arranged in any sequence and still represent the same triad, offering six permutations. On a guitar, due to the instrument's range, each permutation can be played in multiple ways, expanding the possibilities beyond just six.

## The Program

This program takes a chord progression (defaulting to John Coltrane's "Giant Steps") and a specified range (default for guitar is 40, 90) and constructs a directed graph. Each node in the graph represents a different permutation of the notes within each chord, played in various ways across the specified range. Edges represent the sum of movement steps for each voice in the triad from one node to another. The program uses Dijkstra's algorithm to determine the path that minimizes this movement, outputting results in various formats.

## Why?

For improvising jazz musicians, mastering triads over complex changes is crucial for effective improvisation. This program generates etudes with optimal voice leading, providing musicians with targeted practice material for any specified progression.

## Setup

Install the dependencies:

```
pip install -r requirements.txt
```

To play generated MIDI directly from your terminal, you'll need to install FluidSynth:

```
brew install fluidsynth
```

You'll also need a soundfont file. You can download one from here: https://schristiancollins.com/generaluser.php

To initialize FluidSynth, run:

```
fluidsynth -a coreaudio -m coremidi /path/to/soundfont.sf2
```

For PDF score generation, install MuseScore:

```
brew install musescore
```

## Usage

Execute the script with various options to tailor the output:

```
python optimal_voice_leading.py --play --output-midi --output-pdf --print-graph
```

Options include:

- `--play`: Play the MIDI sequence.
- `--print-graph`: Display the voice leading graph.
- `--output-midi`: Save the MIDI sequence.
- `--output-pdf`: Generate a PDF of the music score.
- `--name`: Set a custom name for the output files.
- `--chords`: Define a specific chord progression.
- `--range`: Specify the MIDI note range.


## Examples

Here's a sample of the MIDI output for the "Giant Steps" chord progression. Note that chords are added behind the arpeggiated triads for context:

[Giant Steps Sample](https://drive.google.com/file/d/1x0WVoXqH2icyvHJOL9qEqv4VNXzotbo5/preview)

And here's the corresponding score:

![Screenshot 2024-05-06 at 9 10 01 PM](https://github.com/willdickerson/optimal-voice-leading/assets/33757383/f5cb0a2a-5372-4b29-bd70-75a1b47cb6c4)
