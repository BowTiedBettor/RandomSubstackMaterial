import requests
import time
import numpy as np
import pandas as pd
import xlsxwriter
from traceback import print_exc

season = "2022"
game_type = "02" # 02 is for regular season games

games = []
cases = []
scores = []

game_nr = 1
while True: 
    try: 
        # generate the url & fetch game data [you could store any info youre interested in & build your own db ofc]
        game_nr_str = str(game_nr)
        while len(game_nr_str) < 4: 
            game_nr_str = "0" + game_nr_str
        game_data = requests.get(f"https://statsapi.web.nhl.com/api/v1/game/{season}{game_type}{game_nr_str}/feed/live").json()
        linescore = game_data['liveData']['linescore']

        # collect basic info for the game and append to "games" list
        home_team = game_data['gameData']['teams']['home']['name']
        away_team = game_data['gameData']['teams']['away']['name']
        games.append(f"{home_team} v {away_team}")

        # run the analysis
        home_goals = 0
        away_goals = 0
        for period in linescore['periods']: 
            home_goals += period['home']['goals']
            away_goals += period['away']['goals']
            if period['num'] == 2: 
                second_period_home_goals = home_goals
                second_period_away_goals = away_goals
        
        if second_period_home_goals > second_period_away_goals: 
            if home_goals > away_goals: 
                cases.append(1)
            else: 
                cases.append(0)
        elif second_period_away_goals > second_period_home_goals: 
            if away_goals > home_goals: 
                cases.append(1)
            else: 
                cases.append(0)
        else: 
            cases.append(None)

        # store final score
        scores.append(f"{home_goals} - {away_goals}")

        # uncomment if an api disrespectooor
        # time.sleep(.1)

        print(f"{game_nr}/1312 games analyzed")

        game_nr += 1

    except: 
        # hopefully only executed when the loop has gone through all the regular season NHL games
        print_exc()
        break

# create a pd.DataFrame & dump into an excel file in the current directory
columns = {
    'Game': games,
    'Score': scores,
    'Case': cases,
}

nhl_data_df = pd.DataFrame(columns)

workbook = xlsxwriter.Workbook("NHLData.xlsx")
workbook.close()
with pd.ExcelWriter("NHLData.xlsx", mode='a', if_sheet_exists='overlay', engine = 'openpyxl') as writer:
    nhl_data_df.to_excel(writer)



