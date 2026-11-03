from operator import itemgetter
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dicts with numeric fields converted."""
    import csv

    int_fields = ("id",)
    float_fields = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences, returning the score and its reasons."""
    genre = user_prefs.get("genre")
    mood = user_prefs.get("mood")
    target_energy = user_prefs.get("energy")
    likes_acoustic = user_prefs.get("likes_acoustic")

    score = 0.0
    reasons: List[str] = []

    if genre is not None and song["genre"] == genre:
        score += 2.0
        reasons.append(f"genre match ({song['genre']}) +2.0")

    if mood is not None and song["mood"] == mood:
        score += 1.0
        reasons.append(f"mood match ({song['mood']}) +1.0")

    if target_energy is not None:
        points = 2.0 * (1 - abs(song["energy"] - target_energy))
        score += points
        reasons.append(f"energy {song['energy']:.2f} vs target {target_energy:.2f} +{points:.2f}")

    # Acousticness is only scored when the user states a preference.
    if likes_acoustic is not None:
        target_acoustic = 0.8 if likes_acoustic else 0.2
        points = 0.5 * (1 - abs(song["acousticness"] - target_acoustic))
        score += points
        reasons.append(f"acousticness {song['acousticness']:.2f} +{points:.2f}")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top-k songs as (song, score, explanation) tuples, highest score first."""
    scored = (
        (song, score, ", ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    )
    return sorted(scored, key=itemgetter(1), reverse=True)[:k]
