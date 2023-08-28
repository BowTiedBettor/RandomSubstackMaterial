import pandas as pd
import random
import matplotlib.pyplot as plt

# Specify the path to your Excel file
file_path = 'betpicksdata.xlsx'

# Read the Excel file into a DataFrame
betpicks_df = pd.read_excel(file_path)
horse_series = betpicks_df.Horse
hedged_at_betfair = False
commission = 0.02

final_pnls = []
for iteration_nr in range(50): 
    # generate an artificial bet sequence of length n
    bootstrap_sample = horse_series.sample(n=1000, replace=True)

    pnl = 0
    pnl_tracker = []
    # loop through all 'bets'
    for outcome in bootstrap_sample: 
        # collect data for the bet
        bet_data = betpicks_df[betpicks_df['Horse'] == outcome]
        stake = int(bet_data['Stake'])
        odds = float(bet_data['Odds'])
        closing_odds = float(bet_data['Closing Odds'])
        true_prob = 1/closing_odds

        # simulate whether bet wins or not & adjust p&l appropriately
        if not hedged_at_betfair: 
            # standard p&l computation
            if random.random() < true_prob: 
                pnl += stake * (odds - 1)
            else: 
                pnl -= stake
        else: 
            # somewhat more complicated p&l computation, accounts for the counteraction/hedging at the exchange
            lay_odds = closing_odds * 1.03
            lay_stake = (stake * odds) / (lay_odds - commission)
            if random.random() < true_prob: 
                pnl += stake * (odds - 1) - lay_stake * (lay_odds - 1)
            else: 
                pnl += lay_stake * (1 - commission) - stake
        
        # append the updated pnl to the pnl_tracker
        pnl_tracker.append(pnl)

    plt.plot([i for i in range(len(bootstrap_sample))], pnl_tracker)
    final_pnls.append(pnl)

    print(f"Iteration {iteration_nr} completed...")

plt.title("A thousand £100 flat bets in BowTied BetPicks, illustration of plausible paths...")
plt.ylabel("P&L - GBP")
plt.xlabel("# of bets")
plt.show()

# plot a histogram of final p&l after the 1 000 bets
plt.hist(final_pnls, bins=100)
plt.title("A thousand simulations of 1 000 bets in BowTied BetPicks, histogram of final P&L's") # change range for iteration_nr in loop at line 15
plt.xlabel("P&L - GBP")
plt.ylabel("Frequency")
plt.show()