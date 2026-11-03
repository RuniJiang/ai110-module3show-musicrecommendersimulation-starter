# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

A small, rule-based music recommender. It picks songs that match your vibe.

---

## 2. Intended Use  

**Goal / Task:** The model predicts which songs a listener will like best. It gives each song a score and returns the top 5, with a reason for each pick.

**Intended use:**

- It is for classroom exploration, not for real users.
- It assumes the listener can state a favorite genre, a favorite mood, a target energy level, and (optionally) a taste for acoustic music.
- It assumes one fixed taste per person. It does not learn from listening history.

**Non-intended use:**

- Do not use it in a real music app or to make business decisions.
- Do not use it to judge or label a person's taste or character.
- Do not use it with a large catalog. It was only tested on 20 songs.
- Do not trust it for listeners with mixed or unusual taste. It handles contradictions badly.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

The model is like a judge at a talent show. It scores every song, then returns the top 5.

**Song features used:** genre, mood, energy (0 to 1) and acousticness. Tempo, valence and danceability are in the data but not used.

**User preferences used:** favorite genre, favorite mood, target energy, and whether they like acoustic music.

**Scoring (points are added up):**

- Genre match: 2 points.
- Mood match: 1 point.
- Energy closeness: up to 2 points. The closer to the target, the more points.
- Acoustic feel: up to 0.5 points. A small tie-breaker. Skipped if the user doesn't say.

Each pick shows a short reason, like "genre match, energy close to target." The weights are my own judgment calls.

**Changes from the starter:**

- Energy counts more (1 point to 2).
- Mood counts less (1.5 points to 1).
- Acoustic preference is now a sliding scale and optional.
- Removed the danceability bonus.
- Added explanations for every pick.

---

## 4. Data  

- The catalog is `data/songs.csv`. It has **20 songs**.
- Each song has: genre, mood, energy, tempo, valence, danceability and acousticness.
- The model only uses genre, mood, energy and acousticness.
- There are **17 genres**. Lofi has 3 songs and pop has 2. The other 15 genres have 1 song each.
- There are 17 moods. Chill has 3 songs, and happy and intense have 2 each. Most moods have 1 song.
- I did not add or remove songs from the starter data.
- The data is small and made up. It does not cover most real genres, languages or cultures.
- Energy values are bimodal. Nothing sits between 0.56 and 0.74.
- No user data is included, so it cannot learn what real people like.

---

## 5. Strengths  

- It works well for clear, normal listeners. The #1 pick matched my own pick for High-Energy Pop, Chill Lofi and Deep Intense Rock.
- The energy dial works well. Calm listeners and intense listeners get very different lists with no overlap.
- Every pick comes with a reason, so it is easy to see why a song ranked high.
- It rejects bad energy values (1.5, 90, "high") with a clear error.
- It is simple. You can check any score by hand.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

**Weakness: energy dominates, which creates a filter bubble.**

- In my experiment, energy is worth up to 4 points and genre only 1.
- Energy values are bimodal: 11 songs are 0.20 to 0.55 and 9 are 0.75 to 0.97. None are in between.
- A listener who wants about 0.65 energy is far from every song and gets mediocre scores.
- Genre often can't rescue a song. A metal fan gets pop, rock and reggaeton after the one metal track.
- 14 of 17 genres have one song, so most users run out of genre matches after #1.
- Lofi has 3 songs, so lofi fans get fuller lists.

The system serves listeners in dense parts of the data and under-serves everyone else.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

*Results use the experimental weights: genre 1 point, energy up to 4 points.*

### Profiles tested

- **Three normal listeners:** High-Energy Pop, Chill Lofi, Deep Intense Rock.
- **Eleven trick listeners:** contradictions (pop but sad, metal but zero energy, classical but loud, metal but acoustic), a typo ("Pop"), a missing genre ("k-pop"), an empty profile, mood-only, and bad energy values (1.5, 90, "high").

**What I checked:** Is the #1 song what I would pick? Do lists change sensibly between profiles? Does it fail gracefully on nonsense?

### Why "Gym Hero" keeps showing up for Happy Pop fans

- It is pop, so it gets the genre point.
- Its energy (0.93) is almost exactly what the fan wants.
- It only misses on mood ("intense", not "happy"), so it still ranks #2 (5.30 vs. 6.17 for Sunrise City).
- The system never listens to the song. To it, "happy" and "intense" pop look alike when both are loud.

### What surprised me

1. **Energy overpowers genre.** The Happy Pop list includes a rock song and a reggaeton song, only because their energy is near 0.9.
2. **A fake genre still gets answers.** "k-pop" and the "Pop" typo gave identical lists. Genre silently scores zero, with no warning.
3. **"Classical but loud" got no classical songs.** The one classical track is very quiet.
4. **The empty profile returned all zeros.** The top 5 were just the first five rows of the file.
5. **Bad energy values were rejected** with a clear error. This worked as I wanted.

### Profile comparisons

- **Pop vs. Lofi:** No overlap. Loud and electronic vs. quiet and acoustic. The dials work.
- **Pop vs. Rock:** Similar lists. Only the #1 differs (Sunrise City vs. Storm Runner).
- **Lofi vs. Rock:** Opposites, no overlap. Trustworthy.
- **Pop happy vs. Pop sad:** No song is "sad," so Gym Hero moves to #1. Mood is worth just one point.
- **Rock vs. Metal-acoustic:** Almost the same list. Acousticness is too weak to matter.
- **Lofi vs. Metal with energy 0.0:** The metal fan got calm classical and ambient songs. The system can't spot contradictions.

### Simple checks

- Ran all 14 profiles and read the top 5 by hand.
- Checked that point breakdowns add up (Sunrise City = 1.0 + 1.0 + 3.68 + 0.49 = 6.17).
- Compared odd profiles with normal ones to isolate one change.

### Bottom line

The #1 pick is right for normal listeners. Lower spots slip when the catalog runs out of real matches. The system is good at energy and weak at genre and mood.

---

## 8. Future Work  

1. **Add more songs and balance the genres.** Fill the energy gap (0.56 to 0.74) and give each genre several songs.
2. **Use more features.** Add valence, tempo and danceability. This would help tell "happy" apart from "intense."
3. **Make the top 5 more varied.** Limit how many songs from the same artist or energy band can appear. Also warn the user when their genre is not in the catalog or has a typo, and lowercase their input.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  


I learned that a recommender is just a set of choices about what to measure and how much each thing counts. My weights were judgment calls, and changing them changed who got good results.

The surprise was how much the data shaped the output. With only 20 songs, a gap in the energy values hurt some listeners more than any scoring rule.

This changed how I see music apps. When a feed feels "off," the cause may be thin data or a heavy weight on one signal. It is not always about my taste.

### Biggest learning moment

My biggest learning moment came during the stress test. I had expected the weights to be a detail. Then I doubled the energy weight and halved the genre weight, and the Happy Pop list filled up with a rock song and a reggaeton song. Nothing was broken. The code did exactly what I told it to. The problem was in my choices. That is when I understood that designing a recommender is mostly deciding what counts and how much. The code that adds up the points is the easy part.

### How AI tools helped, and when I double-checked them

AI tools sped up the parts that were routine: laying out the CSV loading, the scoring function, the CLI output and the first draft of the test profiles. They also helped me think of trick profiles I would not have tried, like "metal but zero energy" or the typo "Pop."

I did not take the output on trust, though. I checked it in three ways:

- **By hand.** I added up the points for a song myself (Sunrise City = 1.0 + 1.0 + 3.68 + 0.49 = 6.17) to make sure the breakdown matched what the program printed.
- **By reading the results.** I read the top 5 for every profile and asked whether I would have picked that song first. Code that runs without errors can still give bad recommendations.
- **By questioning the claims.** AI-written text sounds confident. The weights, the descriptions of the data and the explanations of why a song ranked high all needed to be checked against the real CSV and the real scores. For example, I counted the genres and looked at the energy values myself before writing that the data has a gap between 0.56 and 0.74.

My rule was: AI can draft, but I have to be able to explain every number in the model card.

### What surprised me about simple algorithms

I was surprised at how much a few additions and subtractions *feel* like a recommendation. Once each pick came with a reason ("genre match, energy close to target"), the list felt thoughtful, even though the system never listens to a single song. The #1 pick was right for the normal listeners, and that was enough to make the whole thing feel smart. The illusion only broke at the edges. An empty profile just returned the first five rows of the file, and "Gym Hero" kept showing up for happy pop fans because loud songs look alike to the model. It made me realize that a real app may also feel good for the same cheap reasons, and that its failures are easy to miss when it works for most people.

### What I would try next

- **Fix the data first.** Add more songs, give each genre several tracks, and fill the energy gap so listeners with medium-energy taste are not left out.
- **Use the unused features.** Valence, tempo and danceability should help separate "happy" from "intense."
- **Add diversity and guardrails.** Cap how many songs from the same artist or energy band can appear, lowercase the input, and warn the user when a genre is not in the catalog.
- **Learn instead of guess.** Replace my hand-picked weights with ones learned from listening or rating data, and compare the learned list against my hand-tuned one.
