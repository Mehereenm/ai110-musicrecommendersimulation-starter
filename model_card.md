# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

The biggest problem is not enough songs per genre. There are 18 songs across 15 genres, so most genres only have one song. That means if someone likes a genre like rock or jazz, they’ll only get one good match, and the rest of the recommendations are just loosely similar (like having similar energy), which feels fake.

Another issue is that genre matters way too much. It’s weighted so heavily that the system mostly ignores other things like mood or energy. So even if someone wants something chill, they’ll still get high-energy songs from their favorite genre instead of better-fitting songs from other genres.

Also, acoustic preference barely matters. The system gives it a very small score boost, so even if someone clearly wants acoustic music, it often gets ignored if other factors don’t match.
---

## 7. Evaluation  

Six user profiles were tested against the 18-song catalog. Three were designed to represent realistic listeners, and three were deliberately unusual ("adversarial") to see where the scoring logic breaks down.

- High-Energy Pop — a listener who wants upbeat pop music with high energy
- Chill Lofi — a listener who wants low-energy lofi with acoustic instruments
- Deep Intense Rock — a listener who wants loud, intense rock
- Moody Metal — metal fan whose mood preference ("sad") does not exist anywhere in the catalog
- Unknown Genre — a listener who likes "classical," a genre with zero songs in the catalog
- Contradictory — a listener who wants both very high energy and acoustic music at the same time

Ww tested whether the top 5 recommendations actually make sense for the user, and whether the scores clearly separate good vs. bad matches.

The most unexpected result was the Chill Lofi profile worked almost too well. It got the highest possible score because it matched on everything (genre, mood, energy, and acoustic). This showed that the system isn’t really “finding the best song” — it’s just rewarding songs that check the most boxes.

The Contradictory profile exposed a bigger issue. Even though the user asked for acoustic music, all the results were non-acoustic. Energy mattered so much more that it completely overpowered the acoustic preference. So the system basically ignored half the request.
 
Ideas for how I would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  


## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
