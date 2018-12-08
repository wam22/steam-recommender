from recommender import recommender
from predictor import predictor
import random
def main():
    R = recommender()
    P = predictor()
    user_library = {}
    owned_games = random.sample(P.getAllGames(), 10)
    for game in owned_games:
        user_library[game] = random.randint(0,100)
    # print(P.getGameNames(owned_games))
    print(user_library)
    recommendations = R.recommendNewUser(user_library,5,10)
    print("Recommendations:")
    for r in recommendations:
        print(P.getGameName(r[0]))
    


if __name__ == "__main__":
    main()