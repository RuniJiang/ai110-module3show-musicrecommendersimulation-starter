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


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print_recommendations(user_prefs, recommendations)


if __name__ == "__main__":
    main()
