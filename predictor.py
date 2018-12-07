import pandas as pd
import numpy as np
import random
import math

class predictor(object):
    def __init__(self):
        self.df = pd.read_csv('input/steam-200k.csv')
        self.df = self.df.drop(['0'], axis=1)
        self.df.columns = ['User ID', 'Game', 'Behavior', 'Hours']
        self.df = self.df.drop(self.df[self.df.Behavior == 'purchase'].index)
        self.df.reset_index(level=0,drop=True, inplace=True)

        df2 = pd.read_csv('input/steam-200k.csv')
        df2.head()
        df2 = df2.drop(['0'], axis=1)
        df2.columns = ['User ID', 'Game', 'Behavior', 'Hours']
        df2 = df2.drop(['Hours'], axis=1)
        df2 = df2.drop(df2[df2.Behavior == 'play'].index)
        df2['Hours'] = 0.1
        df2.reset_index(level=0,drop=True, inplace=True)
        df2['Behavior'] = 'play'

        result = self.df.copy()
        result.append(df2)
        duplicates = result.duplicated(['User ID','Game'],keep='first')
        duplicates = duplicates.to_frame()
        duplicates.columns = ['D']
        duplicates.size
        duplicates.reset_index(level=0,drop=True, inplace=True)
        duplicates.loc[duplicates['D'] == True]
        duplicates.sort_index()
        to_drop = duplicates.loc[duplicates['D'] == True]
        result.drop(to_drop.index,inplace=True)
        self.df = result.copy()

        self.users_df = self.df[['User ID']].copy()
        self.users_df.columns = ['User ID']
        self.users_df.drop_duplicates(inplace=True)
        self.users_df.reset_index(level=0,drop=True, inplace=True)

        self.games_df = self.df[['Game']].copy()
        self.games_df.drop_duplicates(inplace=True)
        self.games_df['ID'] = self.games_df.index
        self.games_df.columns = ['Game','ID']
    # Get GameID(int) using GameName(String)
    def getGameID(self,GameName):
        GameID = self.games_df.loc[self.games_df['Game'] == GameName]['ID']
        if GameID.size == 1:
            return int(GameID.iloc[0])
        else:
            return -1

    # Get the game IDs from a list of Game names
    def getGameIDs(self,GameNames):
        GameIDs = []
        for GameName in GameNames:
            GameIDs.append(self.getGameID(GameName))
        return GameIDs
        
    # Get GameName(String) using GameID(int)
    def getGameName(self,GameID):
        try:
            GameName = self.games_df.loc[self.games_df['ID'] == GameID].iloc[0]["Game"]
        except IndexError:
            return ""
        return GameName

    # Get the game names of a list of game IDs
    def getGameNames(self,GameIDs):
        names = []
        for GameID in GameIDs:
            names.append(self.getGameName(GameID))
        return names

    # Check whether a user owns particular GameName
    def ownsGameName(self,UserID,GameName):
        l = self.df.loc[(self.df['User ID'] == UserID) & (self.df['Game'] == GameName)].size
        if l == 1:
            return True
        else:
            return False

    # Check whether a user owns a particular GameID   
    def ownsGameID(self,UserID,GameID):
        GameName = self.getGameName(GameID)
        l = self.df.loc[(self.df['User ID'] == UserID) & (self.df['Game'] == GameName)].size
        if l == 1:
            return True
        else:
            return False

    # Get the owned games (int) of a particular UserID
    def getOwnedGamesName(self,UserID):
        games = list(self.df.loc[(self.df['User ID'] == UserID)]["Game"])
        return games

    # Get the owned games (str) of a particular UserID
    def getOwnedGamesID(self,UserID):
        games = list(self.df.loc[(self.df['User ID'] == UserID)]["Game"])
        game_ids = []
        for game in games:
            game_ids.append(self.getGameID(game))
        return game_ids

    # Get the games a user does not own
    def getNotOwnedGames(self,UserID):
        owned_games = self.getOwnedGamesID(UserID)
        all_games = self.getAllGames()
        not_owned = []
        for game in all_games:
            if game not in owned_games:
                not_owned.append(game)
        return not_owned

    # Get the owners of a game
    def getOwners(self,GameID):
        GameName = self.getGameName(GameID)
        players = list(self.df.loc[(self.df['Game'] == GameName)]["User ID"])
        return players
        
    # Get the similar owned games between two user IDs
    def getSimilarGames(self,A,B):
        owned_games_A = self.getOwnedGamesID(A)
        owned_games_B = self.getOwnedGamesID(B)
        similar_games = []
        for game in owned_games_A:
            if game in owned_games_B:
                similar_games.append(game)
        return similar_games

    # Get the similar owners between two games
    def getSimilarPlayers(self,A,B):
        players_A = self.getOwners(A)
        players_B = self.getOwners(B)
        similar_players = []
        for player in players_A:
            if player in players_B:
                similar_players.append(player)
        return similar_players

    # Get all video games
    def getAllGames(self):
        games = list(self.games_df["ID"])
        return games

    # Get all users (That own a video game)
    def getAllUsers(self):
        users = list(self.users_df["User ID"])
        return users

    # Get the amount of hours played by a user of a videogame
    def getHoursPlayed(self,UserID, GameID):
        GameName = self.getGameName(GameID)
        hours = self.df.loc[(self.df["User ID"] == UserID) & (self.df["Game"] == GameName)]["Hours"]
        if hours.size == 1:
            return float(hours.iloc[0])
        else:
            print("Error. hours is not 1",hours.size)
            return 0.0
        
    def getRandomUser(self):
        return self.users_df.iloc[random.randint(0,len(self.getAllUsers()))]["User ID"]

    def getRandomGame(self):
        return self.games_df.iloc[random.randint(0,len(self.getAllGames()))]["Game"]

    # Check how similar 2 users are, returns score in range [-1,1]    
    def simUsers(self,a,b):
        similar_games = self.getSimilarGames(a,b)
        if len(similar_games) == 0 or len(similar_games) == 1:
            return -1
        ratings_a = {}
        ratings_b = {}
        ratings_a_avg = 0.0
        ratings_b_avg = 0.0
        for game in similar_games:
            hours_a = self.getHoursPlayed(a,game)
            hours_b = self.getHoursPlayed(b,game)
            ratings_a_avg += hours_a
            ratings_b_avg += hours_b
            ratings_a[game] = hours_a
            ratings_b[game] = hours_b
        ratings_a_avg = ratings_a_avg / float(len(similar_games))
        ratings_b_avg = ratings_b_avg / float(len(similar_games))

        #subtract the average from every "rating"
        for key,_ in ratings_a.items():
            ratings_a[key] -= ratings_a_avg
        for key,_ in ratings_b.items():
            ratings_b[key] -= ratings_b_avg
            
        numer = 0
        den_a = 0
        den_b = 0
        for r_a,r_b in zip(ratings_a,ratings_b):
            num += r_a*r_b   
            den_a += r_a**2
            den_b += r_b**2
        denom = (den_a**(1/2.0)) * (den_b**(1/2.0))
        return numer/float(denom)

    def simItems(self,a,b):
        similar_players = self.getSimilarPlayers(a,b)
        if len(similar_players) == 0 or len(similar_players) == 1:
            return -1
        ratings_a = {}
        ratings_b = {}
        ratings_a_avg = 0.0
        ratings_b_avg = 0.0
        for player in similar_players:
            hours_a = self.getHoursPlayed(player,a)
            hours_b = self.getHoursPlayed(player,b)
            ratings_a_avg += hours_a
            ratings_b_avg += hours_b
            ratings_a[player] = hours_a
            ratings_b[player] = hours_b
        ratings_a_avg = ratings_a_avg / float(len(similar_players))
        ratings_b_avg = ratings_b_avg / float(len(similar_players))

        #subtract the average from every "rating"
        for key,_ in ratings_a.items():
            ratings_a[key] -= ratings_a_avg
        for key,_ in ratings_b.items():
            ratings_b[key] -= ratings_b_avg

        numer = 0
        den_a = 0
        den_b = 0
        for r_a,r_b in zip(ratings_a,ratings_b):
            num += r_a*r_b   
            den_a += r_a**2
            den_b += r_b**2
        denom = (den_a**(1/2.0)) * (den_b**(1/2.0))
        return numer/float(denom)
            
    def getRUI(self,u,i):
        numer = 0.0
        denom = 0.0
        I = self.getOwnedGamesID(u)
        for j in I:
            sim_items = self.simItems(i,j)
            if(sim_items <= 0):
                continue
            rating = self.getHoursPlayed(u,j)
            numer += rating*sim_items
            denom += sim_items
        return numer/denom

    def test(self):
        randomUser = rec.getRandomUser()
        randomGame = rec.getRandomGame()
        pred = rec.getRUI(randomUser,randomGame)
        return "Predicted score of user",randomUser,"for game",randomGame,":",pred