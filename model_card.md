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

**The big picture:** the recommender works like a judge at a talent show. It looks at every song in the catalog one at a time, gives each a score for how well it fits what the listener likes, and then hands back the songs with the highest scores.

**What features of each song are used?**
Four things: the song's genre (like pop or lofi), its mood (like happy or chill), its energy (calm to intense, on a 0 to 1 scale), and its acousticness (natural instruments vs. electronic production). The catalog also records tempo, valence (how happy a song sounds) and danceability, but the model doesn't use them.

**What user preferences are considered?**
Four things: a favorite genre, a favorite mood, a target energy level, and whether the listener likes acoustic music.

**How does the model turn those into a score?**
Each song earns points, and the points are added up:

- **Genre match: 2 points.** The song gets them if it's in the listener's favorite genre, and nothing otherwise.
- **Mood match: 1 point.** Same idea: the song gets it if its mood is the one the listener wants.
- **Energy closeness: up to 2 points.** This one isn't simply right or wrong. The closer the song's energy is to the listener's target, the more points it gets. A perfect match earns the full 2, and the further away it drifts, the more it loses. A song that's a little too mellow still scores well, while a wildly different one scores poorly.
- **Acoustic feel: up to 0.5 points.** Songs that sound the way the listener prefers get a small bonus. It works as a tie-breaker, not a deciding factor. If the listener doesn't say, this part is skipped.

The songs are then ranked from highest to lowest total, and the top five are shown. Each pick comes with a short reason, such as "genre match, energy close to target," so the listener can see why it was chosen. Genre and energy count the most because they shape whether a song feels right to someone. Mood matters a bit less, and acousticness is a gentle nudge. These weights are my own judgment calls, not something learned from data, so changing them would change the results.

**What changes did you make from the starter logic?**
The starter already had a scoring idea built on genre, mood, energy and acoustic bonuses. I kept that structure but changed how it behaves:

- **Energy matters more.** In the starter it was worth at most 1 point. I doubled it to 2, so it now counts as much as genre.
- **Mood matters a little less.** I lowered it from 1.5 points to 1.
- **Acoustic preference is softer.** The starter drew a hard line (a song is "acoustic" or it isn't) and gave a flat bonus. I made it a sliding scale, so a song that is a bit more acoustic scores a bit higher. It's also optional now.
- **Removed the danceability bonus.** The starter added a small boost for danceable songs when the listener wanted high energy. I took it out to keep the score simple and easy to explain.
- **Added explanations.** Every recommendation now carries the reasons behind its score, which the starter didn't do.

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

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
