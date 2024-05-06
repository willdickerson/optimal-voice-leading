# Optimal Voice Leading

## Introduction

Voice leading is the practice of connecting chords in a musical progression in a way that creates a smooth and coherent melodic line. In a simple chord progression, like C to F, the optimal voice leading triads would be:

C: C E G
F: C F A

Notice how the upper voices (E and G) move to the nearest notes in the F chord (F and A), while the bottom voice (C) stays the same. This minimizes the total movement of the voices, creating a smooth transition between the chords.

## Longer Chord Progressions

In a longer chord progression, finding the optimal voice leading becomes more complex. The goal is to find the globally optimal path through the progression, minimizing the total movement of the voices across all the chords.

To solve this problem, we can represent the possible triads as a directed graph, with each node representing a possible voicing of a chord, and each edge representing the movement between two voicings. We can then use Dijkstra's 
algorithm to find the shortest path through this graph, which corresponds to the optimal voice leading.

## Usage

To use this tool, you'll need to have Python installed. You can install the necessary dependencies using pip:

```
pip install -r requirements.txt
```

If you want to play the generated MIDI from your terminal, you'll need to install FluidSynth:

```
brew install fluidsynth
```

You'll also need a soundfont file. You can download one from here: https://schristiancollins.com/generaluser.php

To initialize FluidSynth, run:

```
fluidsynth -a coreaudio -m coremidi /path/to/soundfont.sf2
```

If you want to generate PDF scores, you'll need to install MuseScore:

```
brew install musescore
```

## Examples

Here's a sample of the MIDI output for the "Giant Steps" chord progression:

[Insert MIDI sample here]

And here's the corresponding PDF score:

[Insert PDF sample here]
