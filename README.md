# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

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

- `favorite_genre`: the genre to match
- `favorite_mood`: the mood to match
- `target_energy` (0–1): the energy level the user wants
- `likes_acoustic` (bool): when true, the target acousticness is high; when false, it is low

### Taste Profile

The recommender compares every song against one taste profile, a dictionary of target values for the features above:

```python
taste_profile = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.40,
    "likes_acoustic": True,   # target acousticness ~0.8
}
```

## Algorithm Recipe

The recipe has two steps: a **scoring rule** that grades one song, and a **ranking rule** that applies it to the whole catalog and picks the winners.

### Step 1: Scoring Rule (one song)

A song's score is the sum of four point rules. Numeric features are scored by closeness to the user's target, not by magnitude, so the best song is the one nearest the target.

| Rule | Points | How it is computed |
|---|---|---|
| Genre match | **+2.0** | `song.genre == user.favorite_genre`, otherwise 0 |
| Mood match | **+1.0** | `song.mood == user.favorite_mood`, otherwise 0 |
| Energy similarity | **0 to +2.0** | `2.0 * (1 - abs(song.energy - user.target_energy))` |
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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



