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

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

 this recommender looks at what kind of music a listener likes and then compares that to different songs, so it will give each song a score based on how well it matches the user’s preferences, then ranks the songs and suggests the best ones. Real platforms use a lot of data like listening history, song details, and audio features. So for this project I will try to go off of that so that the system mainly focuses on matching genre and mood first, and then fine tunes the results using things like energy, tempo, danceability, and acousticness.

- Song features: genre, mood, energy, tempo (BPM), danceability, and acousticness
- User profile features: favorite genre, favorite mood, preferred energy level, and whether they like acoustic songs



The plan is:

1) Load all the songs from the CSV file.
2) Go through each song and give it a score based on how well it matches the user.
3) rank the songs from best match to worst.
4) Return the top k songs as recommendations.

Song and UserProfile features

- Song: genre, mood, energy, tempo (BPM), danceability, acousticness
- User profile: favorite genre, favorite mood, preferred energy level, and whether they like acoustic music

How the scoring works:

- Add +2.0 if the song’s genre matches the user’s favorite genre
- Add +1.0 if the mood matches
- For energy, give a score based on how close it is to the user’s preferred level
   - energy_score = 1.0 - abs(song.energy - user.target_energy)
   - (kept between 0.0 and 1.0)
- Add +0.5 if the user likes acoustic songs and the track is highly acoustic (e.g., ≥ 0.7)
- Add smaller bonus points for how close the song is in:
- valence
- danceability
- acousticness
- Total score = genre points + mood points + energy score + acoustic bonus + other similarity points

Scoring is how the system judges each song on its own
Ranking is how it compares all the songs and decides which ones are best
We need both: first to evaluate each song, and then to sort them into a final list.

How the data flows:
User preferences and the song list both go into the scoring step
Each song gets scored
Songs are sorted by score
The top results are returned as recommendations

Potential bias:
One thing to watch out for is that the system might rely too much on genre and mood. That means it could miss songs that actually fit really well based on energy or vibe alone. It also assumes the user mostly sticks to one genre and mood, so it might not suggest as much variety or cross-genre music.

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

## Experiments You Tried

Six user profiles were run against the 18-song catalog to evaluate scoring behavior.  
Three are "normal" taste profiles; three are adversarial edge cases designed to stress-test the logic.


### Profile 1 — High-Energy Pop

```
  Genre: pop  |  Mood: happy  |  Energy: 0.9  |  Acoustic: No

  #1  Sunrise City  —  Neon Echo
       Score : 3.92
       Reasons:
         • genre match (+2.0)
         • mood match (+1.0)
         • energy similarity (+0.92)

  #2  Gym Hero  —  Max Pulse
       Score : 2.97
       Reasons:
         • genre match (+2.0)
         • energy similarity (+0.97)

  #3  Rooftop Lights  —  Indigo Parade
       Score : 1.86
       Reasons:
         • mood match (+1.0)
         • energy similarity (+0.86)

  #4  Storm Runner  —  Voltline
       Score : 0.99
       Reasons:
         • energy similarity (+0.99)

  #5  Siren City  —  Neon Harbor
       Score : 0.98
       Reasons:
         • energy similarity (+0.98)

```

Genre + mood match dominates. Sunrise City scores nearly 4 points while the next pop song without a mood match (Gym Hero) sits a full point lower.


### Profile 2 — Chill Lofi

```
  Genre: lofi,  Mood: chill,  Energy: 0.35, Acoustic: Yes


  #1  Library Rain  —  Paper Lanterns
       Score : 4.50
       Reasons:
         • genre match (+2.0)
         • mood match (+1.0)
         • energy similarity (+1.00)
         • acoustic match (+0.5)

  #2  Midnight Coding  —  LoRoom
       Score : 4.43
       Reasons:
         • genre match (+2.0)
         • mood match (+1.0)
         • energy similarity (+0.93)
         • acoustic match (+0.5)

  #3  Focus Flow  —  LoRoom
       Score : 3.45
       Reasons:
         • genre match (+2.0)
         • energy similarity (+0.95)
         • acoustic match (+0.5)

  #4  Spacewalk Thoughts  —  Orbit Bloom
       Score : 2.43
       Reasons:
         • mood match (+1.0)
         • energy similarity (+0.93)
         • acoustic match (+0.5)

  #5  Coffee Shop Stories  —  Slow Stereo
       Score : 1.48
       Reasons:
         • energy similarity (+0.98)
         • acoustic match (+0.5)
```

The highest possible score (4.50) is achieved here, all four bonus categories fire at once. Lofi + acoustic is a well served profile in this catalog.

### Profile 3 — Deep Intense Rock

```
  Genre: rock,  Mood: intense, Energy: 0.92, Acoustic: No

  #1  Storm Runner  —  Voltline
       Score : 3.99
       Reasons:
         • genre match (+2.0)
         • mood match (+1.0)
         • energy similarity (+0.99)

  #2  Gym Hero  —  Max Pulse
       Score : 1.99
       Reasons:
         • mood match (+1.0)
         • energy similarity (+0.99)

  #3  Thunder Forge  —  Ashen Core
       Score : 0.96
       Reasons:
         • energy similarity (+0.96)

  #4  Siren City  —  Neon Harbor
       Score : 0.96
       Reasons:
         • energy similarity (+0.96)

  #5  Sunrise City  —  Neon Echo
       Score : 0.90
       Reasons:
         • energy similarity (+0.90)
```
 Only one rock song in the catalog, so #2–#5 fall back on energy proximity alone. A bigger catalog would differentiate these results more.



### Profile 4 — Adversarial: Moody Metal (unmatched mood)

mood: "sad" does not exist in the catalog. Does the system degrade gracefully?

```
  Genre: metal,  Mood: sad, Energy: 0.95 Acoustic: No

  #1  Thunder Forge  —  Ashen Core
       Score : 2.99
       Reasons:
         • genre match (+2.0)
         • energy similarity (+0.99)

  #2  Gym Hero  —  Max Pulse
       Score : 0.98
       Reasons:
         • energy similarity (+0.98)

  #3  Storm Runner  —  Voltline
       Score : 0.96
       Reasons:
         • energy similarity (+0.96)

  #4  Siren City  —  Neon Harbor
       Score : 0.93
       Reasons:
         • energy similarity (+0.93)

  #5  Sunrise City  —  Neon Echo
       Score : 0.87
       Reasons:
         • energy similarity (+0.87)
```

The system degrades gracefully — no crash. But the mood bonus never fires, so the gap between #1 (2.99) and #2 (0.98) reveals the catalog's single metal song. Results #2–#5 are basically tied by energy alone, which is arbitrary ordering.


### Profile 5 — Adversarial: Unknown Genre (classical)

```
  Genre: classical,  Mood: peaceful,  Energy: 0.3,  Acoustic: Yes


  #1  Temple Bells  —  Ashira
       Score : 2.47
       Reasons:
         • mood match (+1.0)
         • energy similarity (+0.97)
         • acoustic match (+0.5)

  #2  Spacewalk Thoughts  —  Orbit Bloom
       Score : 1.48
       Reasons:
         • energy similarity (+0.98)
         • acoustic match (+0.5)

  #3  Library Rain  —  Paper Lanterns
       Score : 1.45
       Reasons:
         • energy similarity (+0.95)
         • acoustic match (+0.5)

  #4  Coffee Shop Stories  —  Slow Stereo
       Score : 1.43
       Reasons:
         • energy similarity (+0.93)
         • acoustic match (+0.5)

  #5  Focus Flow  —  LoRoom
       Score : 1.40
       Reasons:
         • energy similarity (+0.90)
         • acoustic match (+0.5)

```

The system still returns reasonable results (ambient/world/lofi tracks score well on energy + acoustic). However, max score is only 2.47 — the genre bonus is permanently unreachable, so a "classical" user will always get weaker recommendations than users whose genre exists in the catalog.

---

### Profile 6 Adversarial: Contradictory Preferences (high-energy + acoustic)


```
  Genre: pop, Mood: happy  |  Energy: 0.95  |  Acoustic: Yes

  #1  Sunrise City  —  Neon Echo
       Score : 3.87
       Reasons:
         • genre match (+2.0)
         • mood match (+1.0)
         • energy similarity (+0.87)

  #2  Gym Hero  —  Max Pulse
       Score : 2.98
       Reasons:
         • genre match (+2.0)
         • energy similarity (+0.98)

  #3  Rooftop Lights  —  Indigo Parade
       Score : 1.81
       Reasons:
         • mood match (+1.0)
         • energy similarity (+0.81)

  #4  Moonlit Promenade  —  Heartland
       Score : 1.07
       Reasons:
         • energy similarity (+0.57)
         • acoustic match (+0.5)

  #5  Late Night Vinyl  —  Blue Harbor
       Score : 1.00
       Reasons:
         • energy similarity (+0.50)
         • acoustic match (+0.5)

```

Energy wins. The top 3 results are high-energy non-acoustic pop/indie tracks. The acoustic bonus (+0.5) is too small to overcome a ~1.0 energy-similarity gap. The system is effectively "tricked" — it ignores the acoustic preference and behaves like the High-Energy Pop profile.

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


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

