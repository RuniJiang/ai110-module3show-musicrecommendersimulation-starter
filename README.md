# 🎵 Music Recommender Simulation

## Project Summary

This project is a small, content-based music recommender. It loads 20 songs from `data/songs.csv` (genre, mood, energy, tempo, valence, danceability, acousticness), takes a user taste profile, scores every song with a weighted rule (genre match, mood match, energy closeness, acousticness), and prints the top 5 with a plain-language reason for each pick. I tested it on three normal listeners and eleven edge-case profiles to see where it works and where it breaks. See the [Model Card](model_card.md) for the full evaluation.

---

## How The System Works

Real-world recommenders such as Spotify or YouTube combine two main ideas. Collaborative filtering uses the behavior of many users (skips, replays, playlist adds, likes) to find songs that people with similar taste enjoyed. Content-based filtering looks at the attributes of the songs themselves, such as audio features, genre, and mood, and matches them to what a user has liked before. Production systems blend both, then re-rank the results for freshness and variety. My version is purely content-based, because the simulation has no listening history from other users. It prioritizes **how close a song is to the user's preferred vibe** rather than how "big" a value is. Genre is the biggest single rule, energy closeness is equally large in potential points and separates calm songs from intense ones, mood is a secondary match, and acousticness is a small tiebreaker.

### Features used

**`Song`** (loaded from `data/songs.csv`):

- `id`, `title`, `artist`: identification and display only, not scored
- `genre`: categorical, scored as a match or no match
- `mood`: categorical, scored as a match or no match
- `energy` (0–1): scored by closeness to the user's target
- `acousticness` (0–1): scored by closeness to the user's acoustic preference
- `tempo_bpm`, `valence`, `danceability`: stored on the song but not scored in the baseline, because they largely overlap with energy. They are available for later experiments.

**`UserProfile`**:

- `genre`: the genre to match
- `mood`: the mood to match
- `energy` (0–1): the energy level the user wants
- `likes_acoustic` (bool): when true, the target acousticness is high; when false, it is low

### Taste Profile

The recommender compares every song against one taste profile, a dictionary of target values for the features above:

```python
taste_profile = {
    "genre": "lofi",
    "mood": "chill",
    "energy": 0.40,
    "likes_acoustic": True,   # target acousticness ~0.8
}
```

## Algorithm Recipe

The recipe has two steps: a **scoring rule** that grades one song, and a **ranking rule** that applies it to the whole catalog and picks the winners.

### Step 1: Scoring Rule (one song)

A song's score is the sum of four point rules. Numeric features are scored by closeness to the user's target, not by magnitude, so the best song is the one nearest the target.

| Rule | Points | How it is computed |
|---|---|---|
| Genre match | **+2.0** | `song.genre == user.genre`, otherwise 0 |
| Mood match | **+1.0** | `song.mood == user.mood`, otherwise 0 |
| Energy similarity | **0 to +2.0** | `2.0 * (1 - abs(song.energy - user.energy))` |
| Acousticness similarity | **0 to +0.5** | `0.5 * (1 - abs(song.acousticness - target_acoustic))`, where `target_acoustic` is 0.8 if `likes_acoustic` else 0.2 |

Maximum possible score: **5.5**.

**Example**: user = lofi / chill / energy 0.40 / likes acoustic. "Library Rain" (lofi, chill, energy 0.35, acousticness 0.86) scores 2.0 + 1.0 + 1.90 + 0.47 = **5.37**.

### Step 2: Ranking Rule (all songs)

1. Score every song in the catalog with the scoring rule.
2. Sort by score, highest first.
3. Return the top `k`, each with a short explanation of which rules contributed points.

### Why These Weights

- **Genre (2.0)**: the broadest signal of taste, so the largest single yes/no rule.
- **Mood (1.0)**: refines the choice within a genre, but is a softer preference.
- **Energy (up to 2.0)**: as large as genre in potential points. A near-perfect energy match can outrank a genre match whose energy is far off, and energy is what separates songs that share genre and mood.
- **Acousticness (up to 0.5)**: capped low so it only breaks ties.
- **Not scored**: `tempo_bpm`, `valence`, `danceability` overlap with energy. They are kept for experiments, e.g. halving genre to 1.0 and doubling energy to test how much genre dominates.

**Known bias risk**: the 2.0 genre bonus may skew results for users with a rare favorite genre, or toward genres with many songs in the catalog. Test this in the experiments section.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Running `python src/main.py` with the default taste profile produces:

```text
Loaded songs: 20

============================================================
                     TOP RECOMMENDATIONS
============================================================
  Profile: genre=pop, mood=happy, energy=0.8, acoustic=False
------------------------------------------------------------

  #1  Sunrise City  by Neon Echo
      Score: 5.45
      Reasons:
        - genre match (pop) +2.0
        - mood match (happy) +1.0
        - energy 0.82 vs target 0.80 +1.96
        - acousticness 0.18 +0.49

  #2  Gym Hero  by Max Pulse
      Score: 4.17
      Reasons:
        - genre match (pop) +2.0
        - energy 0.93 vs target 0.80 +1.74
        - acousticness 0.05 +0.42

  #3  Rooftop Lights  by Indigo Parade
      Score: 3.34
      Reasons:
        - mood match (happy) +1.0
        - energy 0.76 vs target 0.80 +1.92
        - acousticness 0.35 +0.43

  #4  Concrete Kings  by Block Syndicate
      Score: 2.40
      Reasons:
        - energy 0.78 vs target 0.80 +1.96
        - acousticness 0.09 +0.45

  #5  Night Drive Loop  by Neon Echo
      Score: 2.39
      Reasons:
        - energy 0.75 vs target 0.80 +1.90
        - acousticness 0.22 +0.49

============================================================
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Profile Experiments: Terminal Output

Raw output of `python src/main.py` for every profile in `PROFILES` (standard) and `ADVERSARIAL_PROFILES` (edge cases designed to trick the scorer).

**How the outputs differ:** The High-Energy Pop profile surfaces loud, electronic or pop tracks (Sunrise City, Gym Hero). The Chill Lofi profile shifts to quiet, acoustic songs (Library Rain, Midnight Coding). The Deep Intense Rock profile leads with Storm Runner and pulls in other very loud songs. Pop and Lofi share no songs, which shows the energy and acousticness scoring is working.

### High-Energy Pop

```text
============================================================
                     TOP RECOMMENDATIONS                    
============================================================
  Profile: genre=pop, mood=happy, energy=0.9, acoustic=False
------------------------------------------------------------

  #1  Sunrise City  by Neon Echo
      Score: 5.33
      Reasons:
        - genre match (pop) +2.0
        - mood match (happy) +1.0
        - energy 0.82 vs target 0.90 +1.84
        - acousticness 0.18 +0.49

  #2  Gym Hero  by Max Pulse
      Score: 4.37
      Reasons:
        - genre match (pop) +2.0
        - energy 0.93 vs target 0.90 +1.94
        - acousticness 0.05 +0.42

  #3  Rooftop Lights  by Indigo Parade
      Score: 3.14
      Reasons:
        - mood match (happy) +1.0
        - energy 0.76 vs target 0.90 +1.72
        - acousticness 0.35 +0.43

  #4  Storm Runner  by Voltline
      Score: 2.43
      Reasons:
        - energy 0.91 vs target 0.90 +1.98
        - acousticness 0.10 +0.45

  #5  Sol y Fuego  by Los Cometas
      Score: 2.42
      Reasons:
        - energy 0.88 vs target 0.90 +1.96
        - acousticness 0.12 +0.46

============================================================
```

### Chill Lofi

```text
============================================================
                     TOP RECOMMENDATIONS                    
============================================================
  Profile: genre=lofi, mood=chill, energy=0.3, acoustic=True
------------------------------------------------------------

  #1  Library Rain  by Paper Lanterns
      Score: 5.37
      Reasons:
        - genre match (lofi) +2.0
        - mood match (chill) +1.0
        - energy 0.35 vs target 0.30 +1.90
        - acousticness 0.86 +0.47

  #2  Midnight Coding  by LoRoom
      Score: 5.21
      Reasons:
        - genre match (lofi) +2.0
        - mood match (chill) +1.0
        - energy 0.42 vs target 0.30 +1.76
        - acousticness 0.71 +0.45

  #3  Focus Flow  by LoRoom
      Score: 4.29
      Reasons:
        - genre match (lofi) +2.0
        - energy 0.40 vs target 0.30 +1.80
        - acousticness 0.78 +0.49

  #4  Spacewalk Thoughts  by Orbit Bloom
      Score: 3.40
      Reasons:
        - mood match (chill) +1.0
        - energy 0.28 vs target 0.30 +1.96
        - acousticness 0.92 +0.44

  #5  Campfire Letters  by Willow & Moss
      Score: 2.43
      Reasons:
        - energy 0.30 vs target 0.30 +2.00
        - acousticness 0.94 +0.43

============================================================
```

### Deep Intense Rock

```text
============================================================
                     TOP RECOMMENDATIONS                    
============================================================
  Profile: genre=rock, mood=intense, energy=0.95, acoustic=False
------------------------------------------------------------

  #1  Storm Runner  by Voltline
      Score: 5.37
      Reasons:
        - genre match (rock) +2.0
        - mood match (intense) +1.0
        - energy 0.91 vs target 0.95 +1.92
        - acousticness 0.10 +0.45

  #2  Gym Hero  by Max Pulse
      Score: 3.38
      Reasons:
        - mood match (intense) +1.0
        - energy 0.93 vs target 0.95 +1.96
        - acousticness 0.05 +0.42

  #3  Iron Cathedral  by Black Meridian
      Score: 2.38
      Reasons:
        - energy 0.97 vs target 0.95 +1.96
        - acousticness 0.03 +0.41

  #4  Sol y Fuego  by Los Cometas
      Score: 2.32
      Reasons:
        - energy 0.88 vs target 0.95 +1.86
        - acousticness 0.12 +0.46

  #5  Pixel Rain  by Glitch Garden
      Score: 2.26
      Reasons:
        - energy 0.86 vs target 0.95 +1.82
        - acousticness 0.08 +0.44

============================================================
```

### Conflict: pop + sad + high energy

```text
============================================================
                     TOP RECOMMENDATIONS                    
============================================================
  Profile: genre=pop, mood=sad, energy=0.9, acoustic=False
------------------------------------------------------------

  #1  Gym Hero  by Max Pulse
      Score: 4.37
      Reasons:
        - genre match (pop) +2.0
        - energy 0.93 vs target 0.90 +1.94
        - acousticness 0.05 +0.42

  #2  Sunrise City  by Neon Echo
      Score: 4.33
      Reasons:
        - genre match (pop) +2.0
        - energy 0.82 vs target 0.90 +1.84
        - acousticness 0.18 +0.49

  #3  Storm Runner  by Voltline
      Score: 2.43
      Reasons:
        - energy 0.91 vs target 0.90 +1.98
        - acousticness 0.10 +0.45

  #4  Sol y Fuego  by Los Cometas
      Score: 2.42
      Reasons:
        - energy 0.88 vs target 0.90 +1.96
        - acousticness 0.12 +0.46

  #5  Pixel Rain  by Glitch Garden
      Score: 2.36
      Reasons:
        - energy 0.86 vs target 0.90 +1.92
        - acousticness 0.08 +0.44

============================================================
```

### Conflict: metal/angry but energy 0.0

```text
============================================================
                     TOP RECOMMENDATIONS                    
============================================================
  Profile: genre=metal, mood=angry, energy=0.0, acoustic=False
------------------------------------------------------------

  #1  Iron Cathedral  by Black Meridian
      Score: 3.48
      Reasons:
        - genre match (metal) +2.0
        - mood match (angry) +1.0
        - energy 0.97 vs target 0.00 +0.06
        - acousticness 0.03 +0.41

  #2  Aurora Strings  by Elena Vasquez
      Score: 1.72
      Reasons:
        - energy 0.20 vs target 0.00 +1.60
        - acousticness 0.97 +0.11

  #3  Spacewalk Thoughts  by Orbit Bloom
      Score: 1.58
      Reasons:
        - energy 0.28 vs target 0.00 +1.44
        - acousticness 0.92 +0.14

  #4  Campfire Letters  by Willow & Moss
      Score: 1.53
      Reasons:
        - energy 0.30 vs target 0.00 +1.40
        - acousticness 0.94 +0.13

  #5  Library Rain  by Paper Lanterns
      Score: 1.47
      Reasons:
        - energy 0.35 vs target 0.00 +1.30
        - acousticness 0.86 +0.17

============================================================
```

### Conflict: classical/serene but loud + non-acoustic

```text
============================================================
                     TOP RECOMMENDATIONS                    
============================================================
  Profile: genre=classical, mood=serene, energy=0.95, acoustic=False
------------------------------------------------------------

  #1  Aurora Strings  by Elena Vasquez
      Score: 3.62
      Reasons:
        - genre match (classical) +2.0
        - mood match (serene) +1.0
        - energy 0.20 vs target 0.95 +0.50
        - acousticness 0.97 +0.11

  #2  Gym Hero  by Max Pulse
      Score: 2.39
      Reasons:
        - energy 0.93 vs target 0.95 +1.96
        - acousticness 0.05 +0.42

  #3  Iron Cathedral  by Black Meridian
      Score: 2.38
      Reasons:
        - energy 0.97 vs target 0.95 +1.96
        - acousticness 0.03 +0.41

  #4  Storm Runner  by Voltline
      Score: 2.37
      Reasons:
        - energy 0.91 vs target 0.95 +1.92
        - acousticness 0.10 +0.45

  #5  Sol y Fuego  by Los Cometas
      Score: 2.32
      Reasons:
        - energy 0.88 vs target 0.95 +1.86
        - acousticness 0.12 +0.46

============================================================
```

### Conflict: metal but likes acoustic

```text
============================================================
                     TOP RECOMMENDATIONS                    
============================================================
  Profile: genre=metal, mood=None, energy=0.97, acoustic=True
------------------------------------------------------------

  #1  Iron Cathedral  by Black Meridian
      Score: 4.12
      Reasons:
        - genre match (metal) +2.0
        - energy 0.97 vs target 0.97 +2.00
        - acousticness 0.03 +0.11

  #2  Gym Hero  by Max Pulse
      Score: 2.04
      Reasons:
        - energy 0.93 vs target 0.97 +1.92
        - acousticness 0.05 +0.12

  #3  Storm Runner  by Voltline
      Score: 2.03
      Reasons:
        - energy 0.91 vs target 0.97 +1.88
        - acousticness 0.10 +0.15

  #4  Sol y Fuego  by Los Cometas
      Score: 1.98
      Reasons:
        - energy 0.88 vs target 0.97 +1.82
        - acousticness 0.12 +0.16

  #5  Pixel Rain  by Glitch Garden
      Score: 1.92
      Reasons:
        - energy 0.86 vs target 0.97 +1.78
        - acousticness 0.08 +0.14

============================================================
```

### Case mismatch: 'Pop'

```text
============================================================
                     TOP RECOMMENDATIONS                    
============================================================
  Profile: genre=Pop, mood=happy, energy=0.8, acoustic=False
------------------------------------------------------------

  #1  Sunrise City  by Neon Echo
      Score: 3.45
      Reasons:
        - mood match (happy) +1.0
        - energy 0.82 vs target 0.80 +1.96
        - acousticness 0.18 +0.49

  #2  Rooftop Lights  by Indigo Parade
      Score: 3.34
      Reasons:
        - mood match (happy) +1.0
        - energy 0.76 vs target 0.80 +1.92
        - acousticness 0.35 +0.43

  #3  Concrete Kings  by Block Syndicate
      Score: 2.40
      Reasons:
        - energy 0.78 vs target 0.80 +1.96
        - acousticness 0.09 +0.45

  #4  Night Drive Loop  by Neon Echo
      Score: 2.39
      Reasons:
        - energy 0.75 vs target 0.80 +1.90
        - acousticness 0.22 +0.49

  #5  Pixel Rain  by Glitch Garden
      Score: 2.32
      Reasons:
        - energy 0.86 vs target 0.80 +1.88
        - acousticness 0.08 +0.44

============================================================
```

### Unknown genre: k-pop

```text
============================================================
                     TOP RECOMMENDATIONS                    
============================================================
  Profile: genre=k-pop, mood=happy, energy=0.8, acoustic=False
------------------------------------------------------------

  #1  Sunrise City  by Neon Echo
      Score: 3.45
      Reasons:
        - mood match (happy) +1.0
        - energy 0.82 vs target 0.80 +1.96
        - acousticness 0.18 +0.49

  #2  Rooftop Lights  by Indigo Parade
      Score: 3.34
      Reasons:
        - mood match (happy) +1.0
        - energy 0.76 vs target 0.80 +1.92
        - acousticness 0.35 +0.43

  #3  Concrete Kings  by Block Syndicate
      Score: 2.40
      Reasons:
        - energy 0.78 vs target 0.80 +1.96
        - acousticness 0.09 +0.45

  #4  Night Drive Loop  by Neon Echo
      Score: 2.39
      Reasons:
        - energy 0.75 vs target 0.80 +1.90
        - acousticness 0.22 +0.49

  #5  Pixel Rain  by Glitch Garden
      Score: 2.32
      Reasons:
        - energy 0.86 vs target 0.80 +1.88
        - acousticness 0.08 +0.44

============================================================
```

### Empty profile

```text
============================================================
                     TOP RECOMMENDATIONS                    
============================================================
  Profile: genre=None, mood=None, energy=None, acoustic=None
------------------------------------------------------------

  #1  Sunrise City  by Neon Echo
      Score: 0.00
      Reasons:

  #2  Midnight Coding  by LoRoom
      Score: 0.00
      Reasons:

  #3  Storm Runner  by Voltline
      Score: 0.00
      Reasons:

  #4  Library Rain  by Paper Lanterns
      Score: 0.00
      Reasons:

  #5  Gym Hero  by Max Pulse
      Score: 0.00
      Reasons:

============================================================
```

### Mood only: chill

```text
============================================================
                     TOP RECOMMENDATIONS                    
============================================================
  Profile: genre=None, mood=chill, energy=None, acoustic=None
------------------------------------------------------------

  #1  Midnight Coding  by LoRoom
      Score: 1.00
      Reasons:
        - mood match (chill) +1.0

  #2  Library Rain  by Paper Lanterns
      Score: 1.00
      Reasons:
        - mood match (chill) +1.0

  #3  Spacewalk Thoughts  by Orbit Bloom
      Score: 1.00
      Reasons:
        - mood match (chill) +1.0

  #4  Sunrise City  by Neon Echo
      Score: 0.00
      Reasons:

  #5  Storm Runner  by Voltline
      Score: 0.00
      Reasons:

============================================================
```

### Out of range: energy 1.5

```text
  !! REJECTED: energy must be a number between 0 and 1, got 1.5
```

### Out of range: energy 90 (percent)

```text
  !! REJECTED: energy must be a number between 0 and 1, got 90
```

### Wrong type: energy 'high'

```text
  !! REJECTED: energy must be a number between 0 and 1, got 'high'
```

---

## Experiments You Tried

- **Weight shift (genre 2.0 -> 1.0, energy up to 2.0 -> 4.0):** The Happy Pop list filled up with a rock song and a reggaeton song, only because their energy is near 0.9. Energy overpowered genre. Nothing was broken; the weights were my choice.
- **Profile comparisons:** High-Energy Pop and Chill Lofi share no songs (loud and electronic vs. quiet and acoustic), so the energy and acousticness dials work. Deep Intense Rock is the opposite of Chill Lofi, also with no overlap. Pop and Rock get similar lists because both want high energy; only the #1 differs (Sunrise City vs. Storm Runner).
- **Pop + sad:** No song is "sad," so Gym Hero (intense) moves to #1. Mood is worth only 1 point.
- **Edge cases:** "k-pop" and the typo "Pop" returned identical lists (genre silently scores zero). An empty profile returned all zeros and just the first five rows. "Metal but energy 0.0" got calm classical and ambient songs. Out-of-range or wrong-type energy values (1.5, 90, "high") were rejected with a clear error.
- **Not tried:** Adding tempo or valence to the score. This is listed as future work in the model card.

Full outputs are in the Profile Experiments section above, and the analysis is in [model_card.md](model_card.md#7-evaluation).

---

## Limitations and Risks

- **Tiny catalog:** Only 20 songs, and 14 of 17 genres have exactly one song, so most users run out of genre matches after #1.
- **Energy gap:** Energy values are bimodal (11 songs at 0.20-0.55, 9 at 0.75-0.97, none between). A listener who wants about 0.65 energy is far from every song.
- **Energy can overpower genre and mood:** Loud songs from other genres show up for pop fans, and "Gym Hero" keeps appearing for happy pop listeners because the system can't tell "happy" from "intense."
- **No input checking beyond energy:** Typos and unknown genres silently score zero. Contradictory profiles (metal but zero energy) are not flagged.
- **Unused features and no lyrics:** Tempo, valence and danceability are not scored, and the system knows nothing about lyrics, language, artist or listening history.

See [model_card.md](model_card.md#6-limitations-and-bias) for details.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

A recommender turns data into predictions through a series of choices about what to measure and how much each thing counts. My weights were judgment calls, and changing them changed who got good results. The code that adds up the points is the easy part; deciding what counts is the real design work. Attaching a reason to each pick ("genre match, energy close to target") also made the list feel thoughtful, even though the system never listens to a song.

Bias showed up mostly through the data, not the scoring rule. With 20 songs, one-song genres and a gap in the energy values, listeners with rare genres or medium-energy taste were under-served, while lofi and high-energy fans did well. In a real system the same thing could happen through popularity, genre imbalance or an over-weighted signal, and it would be easy to miss because the system works for most people. See the [Model Card](model_card.md) for my full reflection.
