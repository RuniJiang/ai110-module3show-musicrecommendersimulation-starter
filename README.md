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

Real-world recommenders such as Spotify or YouTube combine two main ideas. Collaborative filtering uses the behavior of many users (skips, replays, playlist adds, likes) to find songs that people with similar taste enjoyed. Content-based filtering looks at the attributes of the songs themselves, such as audio features, genre, and mood, and matches them to what a user has liked before. Production systems blend both, then re-rank the results for freshness and variety. My version is purely content-based, because the simulation has no listening history from other users. It prioritizes **how close a song is to the user's preferred vibe** rather than how "big" a value is. Energy is the strongest signal, since it cleanly separates calm songs from intense ones in the catalog. Mood and genre are secondary matches. Acousticness is a small tiebreaker.

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

### Scoring Rule (one song)

Numeric features are scored by closeness, not magnitude, so a song scores highest when it is near the user's target:

```
energy_score = 1 - |song.energy - user.target_energy|
```

The final score is a weighted sum (weights are a starting point to tune in experiments):

| Component | Weight |
|---|---|
| Energy closeness | 0.45 |
| Mood match | 0.25 |
| Genre match | 0.20 |
| Acousticness closeness | 0.10 |

### Ranking Rule (all songs)

The scoring rule judges one song in isolation. The ranking rule scores every song in the catalog, sorts by score in descending order, and returns the top `k`. Each result includes a short explanation of which features contributed to its score.

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



