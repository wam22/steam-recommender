# steam-recommender
A recommendation engine for Steam videogames written in Python 3

Uses a dataset containing 200,000 entries of user behavior (game purchase & playing) from Kaggle. You can get the original datset [here](https://www.kaggle.com/tamber/steam-video-games) or simply clone this repo.

## Usage Example
### Recommend 5 games to a random user with a random library - considering 10 games in the dataset
```
from recommender import recommender
from predictor import predictor
import random


R = recommender()
P = predictor()
user_library = {}
owned_games = random.sample(P.getAllGames(), 10)
for game in owned_games:
    user_library[game] = random.randint(0,100)
print(user_library)
recommendations = R.recommendNewUser(user_library,5,10)
print("Recommendations:")
for r in recommendations:
    print(P.getGameName(r[0]))
```

## TODO:
- [ ] GUI using QT
- [ ] Implement baseline predictor

