import requests
import time
import numpy as np
from traceback import print_exc

season = "2022"
game_type = "02" # 02 is for regular season games

cases = []

game_nr = 1
while True: 
    try: 
        # generate the url & fetch game data [you could store more info & build your own db ofc, we don't care about that for now]
        game_nr_str = str(game_nr)
        while len(game_nr_str) < 4: 
            game_nr_str = "0" + game_nr_str
        game_data = requests.get(f"https://statsapi.web.nhl.com/api/v1/game/{season}{game_type}{game_nr_str}/feed/live").json()
        linescore = game_data['liveData']['linescore']

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
        if second_period_away_goals > second_period_home_goals: 
            if away_goals > home_goals: 
                cases.append(1)
            else: 
                cases.append(0)

        # uncomment if an api disrespectooor
        time.sleep(.1)

        game_nr += 1

    except: 
        # hopefully only executed when the loop has gone through all the regular season NHL games
        print_exc()
        break

fraction = np.average(cases)
print(fraction)
print(len(cases))
