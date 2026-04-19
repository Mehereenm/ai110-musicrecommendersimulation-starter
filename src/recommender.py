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
        """Initialize the Recommender with a list of Song objects."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects ranked by score for the given UserProfile."""
        from dataclasses import asdict
        user_prefs = asdict(user)
        scored = []
        for song in self.songs:
            song_dict = asdict(song)
            score, _ = score_song(user_prefs, song_dict)
            scored.append((song, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable string describing why a song was recommended."""
        from dataclasses import asdict
        user_prefs = asdict(user)
        song_dict = asdict(song)
        _, reasons = score_song(user_prefs, song_dict)
        return "; ".join(reasons) if reasons else "No strong match found"

def load_songs(csv_path: str) -> List[Dict]:
    """Load and parse songs from a CSV file, returning a list of song dicts."""
    import csv
    songs = []
    with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            song_dict = {
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness'])
            }
            songs.append(song_dict)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons = []

    # Genre match: +1.0  (halved from 2.0 — experiment: reduce genre dominance)
    if song['genre'] == user_prefs.get('favorite_genre'):
        score += 1.0
        reasons.append("genre match (+1.0)")

    # Mood match: +1.0
    if song['mood'] == user_prefs.get('favorite_mood'):
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Energy similarity: 0.0 to 2.0  (doubled from 1.0 — experiment: energy as important as genre)
    target_energy = user_prefs.get('target_energy', 0.5)
    energy_score = max(0.0, 1.0 - abs(song['energy'] - target_energy)) * 2.0
    score += energy_score
    reasons.append(f"energy similarity (+{energy_score:.2f})")

    # Acoustic bonus: +0.5 if user likes acoustic and song is highly acoustic (>= 0.7)
    if user_prefs.get('likes_acoustic') and song['acousticness'] >= 0.7:
        score += 0.5
        reasons.append("acoustic match (+0.5)")

    # Valence similarity: smaller bonus up to 0.3 (only when user target is provided)
    if 'target_valence' in user_prefs:
        valence_score = max(0.0, 1.0 - abs(song['valence'] - user_prefs['target_valence'])) * 0.3
        score += valence_score
        reasons.append(f"valence similarity (+{valence_score:.2f})")

    # Danceability similarity: smaller bonus up to 0.3 (only when user target is provided)
    if 'target_danceability' in user_prefs:
        dance_score = max(0.0, 1.0 - abs(song['danceability'] - user_prefs['target_danceability'])) * 0.3
        score += dance_score
        reasons.append(f"danceability similarity (+{dance_score:.2f})")

    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
