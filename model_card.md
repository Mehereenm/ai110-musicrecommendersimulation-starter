# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name
VibeFinder


## 2. Intended Use

This system suggests songs from a small catalog based on a listener's preferred genre, mood, energy level, and whether they like acoustic music.

It is built for classroom exploration, not for real users. It assumes a single, consistent taste profile with no listening history.


## 3. How the Model Works

Every song gets a score based on how well it matches what the user said they like. The score adds up four things:

- Does the song's genre match? If yes, +1 point.
- Does the mood match? If yes, +1 point.
- How close is the energy level? Up to 2 points (perfect match = 2, far off = 0).
- Does the user like acoustic music and is the song very acoustic? If both, +0.5 points.

The five highest-scoring songs are returned as recommendations. Each result shows which factors contributed to its score.


## 4. Data

- 18 songs in the catalog, stored in a CSV file.
- 15 different genres represented, but 13 of them have only one song each.
- Moods include: happy, chill, intense, peaceful, melancholy, and others.
- No classical, R&B, K-pop, or country pop. The catalog skews toward Western genres.
- No songs were removed; a few were added to the starter set.
- Tempo (BPM) is stored but not used in scoring


## 5. Strengths

- Works best when the user's genre and mood both exist in the catalog (e.g., lofi/chill, pop/happy).
- The Chill Lofi profile achieved the maximum possible score, the right song clearly rose to the top.
- Explanations are transparent: every recommendation shows exactly why it was chosen.


## 6. Limitations and Bias

The biggest problem is not enough songs per genre. There are 18 songs across 15 genres, so most genres only have one song. That means if someone likes a genre like rock or jazz, they'll only get one good match, and the rest of the recommendations are just loosely similar (like having similar energy), which feels fake.

Another issue is that genre matters way too much. It's weighted so heavily that the system mostly ignores other things like mood or energy. So even if someone wants something chill, they'll still get high energy songs from their favorite genre instead of better fitting songs from other genres.

Also, acoustic preference barely matters. The system gives it a very small score boost, so even if someone clearly wants acoustic music, it often gets ignored if other factors don't match.


## 7. Evaluation

Six user profiles were tested against the 18-song catalog. Three were designed to represent realistic listeners, and three were deliberately unusual ("adversarial") to see where the scoring logic breaks down.

- High-Energy Pop — a listener who wants upbeat pop music with high energy
- Chill Lofi — a listener who wants low-energy lofi with acoustic instruments
- Deep Intense Rock — a listener who wants loud, intense rock
- Moody Metal — metal fan whose mood preference ("sad") does not exist anywhere in the catalog
- Unknown Genre — a listener who likes "classical," a genre with zero songs in the catalog
- Contradictory — a listener who wants both very high energy and acoustic music at the same time

We tested whether the top 5 recommendations actually make sense for the user, and whether the scores clearly separate good vs. bad matches.

The most unexpected result was the Chill Lofi profile worked almost too well. It got the highest possible score because it matched on everything (genre, mood, energy, and acoustic). This showed that the system isn't really "finding the best song", it's just rewarding songs that check the most boxes.

The Contradictory profile exposed a bigger issue. Even though the user asked for acoustic music, all the results were non acoustic. Energy mattered so much more that it completely overpowered the acoustic preference. So the system basically ignored half the request.

A weight experiment was also run: genre weight was halved and energy weight was doubled. Rankings stayed the same, showing the catalog size is the real problem, not the weights.

## 8. Ideas for Improvement

1. Expand the catalog. Most improvements would come from adding 5–10 songs per genre. The weights barely matter when there is only one rock song.
2. Add a tempo preference. The BPM column already exists in the data but is never scored. A "chill" user probably doesn't want a 150 BPM track even if the genre matches.


## 9. Personal Reflection

Biggest learning moment:
Changing the weights didn’t really change the results. That showed me the real problem wasn’t the scoring, it was the tiny dataset. Most genres only had one song, and no weight adjustment can fix missing/limited data.

Using AI tools:
AI helped speed things up (formatting, test profiles), but I still had to double check everything. A small typo (reasonsgi) slipped in and could’ve broken things without me noticing. AI is fast, but not always careful.

What surprised me:
A very simple scoring system actually worked. The Chill Lofi profile got a perfect match, and it felt correct. Just a few basic rules produced something that seemed “smart,” even without machine learning.

What I’d try next:
Add more variety (limit repeated artists), use tempo in scoring, and support multiple favorite genres since real users usually have more than one.