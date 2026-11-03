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

**Weakness discovered: the energy gap creates a filter bubble that favors users at the extremes and in the lofi niche.** In my weight-shift experiment I doubled the energy weight to 4.0 and cut genre to 1.0, so a song's energy can now swing the score by up to 4 points while a genre match is worth only 1. The catalog's energy values are also bimodal: 11 of the 20 songs sit between 0.20 and 0.55, 9 sit between 0.75 and 0.97, and none fall between 0.56 and 0.74. A listener who wants a mid-high energy such as 0.65 is therefore far from every song and gets uniformly mediocre scores, while listeners who want very calm or very intense music are matched well. Because energy dominates, a user's favorite genre often can't rescue a good song, and the top 5 fills up with songs from other genres that merely have similar energy (for example, a metal fan gets pop, rock and reggaeton after the single metal track). The catalog is also tiny and uneven: 14 of 17 genres have exactly one song, so most users run out of genre matches after the first result, while lofi (3 songs) and its "chill" mood (3 songs) give those users a fuller, more satisfying list. In short, the system quietly serves listeners whose taste lands in a dense part of the data and under-serves everyone else.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

*All results below were produced with the experimental weights (genre worth 1 point, energy worth up to 4 points), so energy is the loudest voice in the score.*

### Profiles I tested

**Three "normal" listeners:**

- **High-Energy Pop:** likes pop, happy songs, very energetic (0.9), not acoustic.
- **Chill Lofi:** likes lofi, chill songs, very calm (0.3), likes acoustic.
- **Deep Intense Rock:** likes rock, intense songs, nearly maximum energy (0.95), not acoustic.

**Eleven "trick" listeners**, built to see what breaks: contradictions (pop but sad, metal but zero energy, classical but loud, metal but acoustic), a capital-letter typo ("Pop"), a genre that doesn't exist in the catalog ("k-pop"), an empty profile, mood-only, and bad energy values (1.5, 90, and the word "high").

**What I looked for:** does the #1 song match what I would pick by hand, do the lists change in sensible ways when the listener changes, and does the system fail gracefully when given nonsense.

### Why "Gym Hero" keeps showing up for people who just want "Happy Pop"

Think of the system as a judge handing out points. Gym Hero is a pop song, so it gets the genre point. It is also very energetic (0.93), which is almost exactly what a High-Energy Pop fan asked for, so it gets nearly the full energy points. The only thing it misses is the mood: it is tagged "intense", not "happy". That costs it one point, and it still lands in second place (5.30, right behind Sunrise City at 6.17).

The judge never listens to the song. It only checks boxes and measures distance on one dial (energy). To the judge, a pumped-up gym track and a sunny feel-good track look nearly identical, because both are pop and both are loud. A human knows "happy" and "intense" feel different, but the system only gives mood one point out of about six, so it can't tell them apart very well.

Gym Hero also turned up for the Rock fan (#2) and the "classical but loud" listener (#1). It is the catalog's most reliable "pop + very loud" song, so it keeps winning whenever energy is high.

### What surprised me

1. **Energy overpowers genre.** In the Happy Pop list, #4 is a rock song (Storm Runner) and #5 is reggaeton (Sol y Fuego). Neither is pop, and Storm Runner isn't happy either. They are there only because their energy is almost exactly 0.9. A pop fan would be confused by that.
2. **A fake genre still gets answers.** The "k-pop" listener (a genre not in the catalog) and the "Pop" typo listener got identical lists. The system silently scores genre as zero for everyone and falls back to mood and energy. It does not warn the user. Capital "Pop" doesn't match lowercase "pop", so a tiny typo quietly removes the genre bonus.
3. **The "classical but loud" listener got no classical songs at all.** Aurora Strings (the only classical track) is very quiet, so its energy score was terrible. The top five were all loud songs from other genres. What the person asked for in energy beat what they asked for in genre.
4. **The empty profile returned a list of zeros.** It still shows five songs, but they are just the first five in the file. Nothing is personalized.
5. **Bad energy values are rejected.** 1.5, 90 and "high" all gave a clear error message instead of garbage results. That worked the way I wanted.

### Comparing the profiles, pair by pair

**High-Energy Pop vs. Chill Lofi.** These two have no songs in common. Pop wants loud, bright, electronic-sounding music (Sunrise City, Gym Hero, Rooftop Lights). Lofi wants quiet, soft, acoustic music (Library Rain, Midnight Coding, Spacewalk Thoughts). That is exactly what the energy dial and the acoustic dial should do, so this result makes sense. It is the cleanest proof that the preferences are doing their job.

**High-Energy Pop vs. Deep Intense Rock.** Both want loud songs, so their lists overlap (Gym Hero, Sol y Fuego). The difference is at the top: pop's #1 is Sunrise City (pop and happy), while rock's #1 is Storm Runner (rock and intense). Each fan gets the song that matches their genre and mood, and the rest of the list is the same pool of loud tracks. That makes sense, since the two fans want similar energy and differ mostly in label. It also shows the weakness: the lists are only really different in the first slot.

**Chill Lofi vs. Deep Intense Rock.** These are opposites, and again there is no overlap. Lofi gets calm, acoustic songs at 0.28 to 0.42 energy. Rock gets the loudest songs in the catalog (Storm Runner, Gym Hero, Iron Cathedral). I can trust this result because the two profiles are at opposite ends of the same energy dial.

**High-Energy Pop vs. "Pop + sad + high energy".** The only change is the mood, from happy to sad. No song in the catalog is "sad", so nobody earns the mood point, and the order shuffles: Gym Hero moves up to #1 and Sunrise City drops to #2, because Sunrise City lost its mood bonus. This makes sense, and it shows mood is worth a single point. It also shows the system can't invent a sad pop song that doesn't exist.

**Deep Intense Rock vs. "Metal but likes acoustic".** Both want extremely high energy. The metal listener's #1 is Iron Cathedral (the only metal song), and then the list is the same loud songs the rock fan got. Asking for acoustic music barely moved anything, since acousticness is worth only half a point and every loud song is non-acoustic anyway. This tells me the acoustic preference is too weak to fight the energy preference.

**Chill Lofi vs. "Metal/angry but energy 0.0".** Both want very quiet music, but the metal fan's genre and mood match nothing quiet. Their list is filled with calm classical, ambient, folk and jazz songs, with Aurora Strings first. The system honored the energy request and ignored the "metal" part. That is a technically correct but strange answer for someone who said they like metal, and it shows the system can't recognize a contradiction in a listener's taste.

### Simple checks I ran

- Ran all 14 profiles through the same code and looked at the top five by hand.
- Checked that each #1 song's point breakdown added up (for example, Sunrise City = 1.0 genre + 1.0 mood + 3.68 energy + 0.49 acoustic = 6.17).
- Compared the unrealistic profiles against the realistic ones to see which differences came from one changed setting.

### Bottom line

For the three normal listeners, the #1 pick feels right every time. The lower spots are where it slips, because loud songs from the wrong genre fill in when the catalog runs out of real matches. The system is good at the energy dial and weak at the genre and mood labels, which is a direct result of my weight experiment.

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
