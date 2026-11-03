"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


WIDTH = 60


def print_recommendations(user_prefs: dict, recommendations: list) -> None:
    """Print recommendations in a clean, readable terminal layout."""
    rule = "=" * WIDTH
    thin = "-" * WIDTH
    profile = (
        f"genre={user_prefs.get('genre')}, mood={user_prefs.get('mood')}, "
        f"energy={user_prefs.get('energy')}, "
        f"acoustic={user_prefs.get('likes_acoustic')}"
    )
    print(f"\n{rule}")
    print("  TOP RECOMMENDATIONS".center(WIDTH))
    print(rule)
    print(f"  Profile: {profile}")
    print(thin)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']}  by {song.get('artist', 'Unknown')}")
        print(f"      Score: {score:.2f}")
        print("      Reasons:")
        for reason in explanation.split(", "):
            if reason:
                print(f"        - {reason}")
    print(f"\n{rule}\n")


PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.9,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.3,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.95,
        "likes_acoustic": False,
    },
}


ADVERSARIAL_PROFILES = {
    "Conflict: pop + sad + high energy": {
        "genre": "pop", "mood": "sad", "energy": 0.9, "likes_acoustic": False,
    },
    "Conflict: metal/angry but energy 0.0": {
        "genre": "metal", "mood": "angry", "energy": 0.0, "likes_acoustic": False,
    },
    "Conflict: classical/serene but loud + non-acoustic": {
        "genre": "classical", "mood": "serene", "energy": 0.95, "likes_acoustic": False,
    },
    "Conflict: metal but likes acoustic": {
        "genre": "metal", "energy": 0.97, "likes_acoustic": True,
    },
    "Case mismatch: 'Pop'": {
        "genre": "Pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False,
    },
    "Unknown genre: k-pop": {
        "genre": "k-pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False,
    },
    "Empty profile": {},
    "Mood only: chill": {"mood": "chill"},
    "Out of range: energy 1.5": {
        "genre": "pop", "mood": "happy", "energy": 1.5, "likes_acoustic": False,
    },
    "Out of range: energy 90 (percent)": {
        "genre": "pop", "mood": "happy", "energy": 90, "likes_acoustic": False,
    },
    "Wrong type: energy 'high'": {
        "genre": "pop", "mood": "happy", "energy": "high", "likes_acoustic": False,
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    for name, user_prefs in {**PROFILES, **ADVERSARIAL_PROFILES}.items():
        print(f"\n>>> Profile: {name}")
        try:
            recommendations = recommend_songs(user_prefs, songs, k=5)
        except ValueError as exc:
            print(f"  !! REJECTED: {exc}")
            continue
        print_recommendations(user_prefs, recommendations)


if __name__ == "__main__":
    main()
