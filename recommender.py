from predictor import predictor
import random
from collections import Counter

class recommender(object):
    def __init__(self):
        self.predictor = predictor()
    def recommend(self,user,k,consider):
        to_consider = []
        if consider is not None:
            to_consider = random.sample(self.predictor.getNotOwnedGames(user),consider)
        else:
            to_consider = self.predictor.getNotOwnedGames(user)
        predictions = {}
        for game in to_consider:
            predictions[game] = self.predictor.getRUI(user,game)
            print("Predicted score of user",user,"for game",game,":",predictions[game])
        sorted_by_value = sorted(predictions.items(), key=lambda kv: kv[1],reverse=True)
        return sorted_by_value[:k]
    def recommendNewUser(self,user_library,k,consider):
        not_owned_games = []
        for g in self.predictor.getAllGames():
            if g not in user_library.keys():
                not_owned_games.append(g)
        to_consider = []
        if consider is not None:
            to_consider = random.sample(not_owned_games,consider)
        else:
            to_consider = not_owned_games
        predictions = {}
        for game in to_consider:
            predictions[game] = self.predictor.getRUInewUser(user_library,game)
            #print("Predicted score for game",game,":",predictions[game])
        sorted_by_value = sorted(predictions.items(), key=lambda kv: kv[1],reverse=True)
        return sorted_by_value[:k]

