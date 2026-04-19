"""
Command line runner for the Music Recommender Simulation.

Run from the project root with:
    python -m src.main
"""

from src.recommender import load_songs, recommend_songs


def print_recommendations(recommendations, user_prefs, profile_name=""):
    """Print a formatted ranked recommendation list for a given user profile."""
    width = 60
    genre    = user_prefs.get("favorite_genre", "?")
    mood     = user_prefs.get("favorite_mood", "?")
    energy   = user_prefs.get("target_energy", "?")
    acoustic = "Yes" if user_prefs.get("likes_acoustic") else "No"

    label = f"  Profile: {profile_name}" if profile_name else "  Music Recommender — Top Results"
    print("\n" + "=" * width)
    print(label)
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

# Standard user profiles

HIGH_ENERGY_POP = {
    "name": "High-Energy Pop",
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.9,
    "likes_acoustic": False,
}

CHILL_LOFI = {
    "name": "Chill Lofi",
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.35,
    "likes_acoustic": True,
}

DEEP_INTENSE_ROCK = {
    "name": "Deep Intense Rock",
    "favorite_genre": "rock",
    "favorite_mood": "intense",
    "target_energy": 0.92,
    "likes_acoustic": False,
}

# Adversarial / edge-case profiles

# Edge case 1: genre exists in catalog but mood ("sad") matches NO song — tests
# whether energy alone can still surface reasonable results.
MOODY_METAL = {
    "name": "Adversarial — Moody Metal (unmatched mood)",
    "favorite_genre": "metal",
    "favorite_mood": "sad",        # no song in the catalog has mood="sad"
    "target_energy": 0.95,
    "likes_acoustic": False,
}

# Edge case 2: completely unknown genre — every song scores 0 on the genre
# bonus; only mood + energy separate the results.
UNKNOWN_GENRE = {
    "name": "Adversarial — Unknown Genre (classical)",
    "favorite_genre": "classical",  # not in the catalog at all
    "favorite_mood": "peaceful",
    "target_energy": 0.3,
    "likes_acoustic": True,
}

# Edge case 3: contradictory prefs — very high energy AND loves acoustic.
# Acoustic tracks tend to be low-energy; see if the system "picks a side."
CONTRADICTORY = {
    "name": "Adversarial — Contradictory (high-energy + acoustic)",
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.95,         # pulls toward high-energy electronic tracks
    "likes_acoustic": True,        # pulls toward soft acoustic tracks
}

PROFILES = [
    HIGH_ENERGY_POP,
    CHILL_LOFI,
    DEEP_INTENSE_ROCK,
    MOODY_METAL,
    UNKNOWN_GENRE,
    CONTRADICTORY,
]


def main() -> None:
    """Load the song catalog and run every profile through the recommender."""
    songs = load_songs("data/songs.csv")

    for profile in PROFILES:
        name = profile.pop("name")
        recommendations = recommend_songs(profile, songs, k=5)
        print_recommendations(recommendations, profile, profile_name=name)
        profile["name"] = name   # restore so the list stays reusable


if __name__ == "__main__":
    main()
