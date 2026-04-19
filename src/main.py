"""
Command line runner for the Music Recommender Simulation.

Run from the project root with:
    python -m src.main
"""

from src.recommender import load_songs, recommend_songs


def print_recommendations(recommendations, user_prefs):
    width = 52
    genre    = user_prefs.get("favorite_genre", "?")
    mood     = user_prefs.get("favorite_mood", "?")
    energy   = user_prefs.get("target_energy", "?")
    acoustic = "Yes" if user_prefs.get("likes_acoustic") else "No"

    print("\n" + "=" * width)
    print("  Music Recommender — Top Results for Your Profile")
    print("=" * width)
    print(f"  Genre: {genre}  |  Mood: {mood}  |  Energy: {energy}  |  Acoustic: {acoustic}")
    print("=" * width)

    if not recommendations:
        print("\n  No recommendations found.\n")
        return

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Score : {score:.2f}")
        print(f"       Reasons:")
        for reason in explanation.split("; "):
            print(f"         • {reason}")

    print("\n" + "=" * width + "\n")


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Default taste profile: pop / happy fan who prefers high energy
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)
    print_recommendations(recommendations, user_prefs)


if __name__ == "__main__":
    main()
