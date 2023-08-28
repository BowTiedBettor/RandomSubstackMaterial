import random
import matplotlib.pyplot as plt

bet_size = 10000
probability_3 = 0.125
probability_100 = 0.01

pnl_paths = []

number_of_severe_drawdowns = 0
for iteration in range(100): 
    cum_pnl = []
    pnl = 0
    week = 0
    while week < 500: 
        outcome = random.random()
        if outcome < probability_3: 
            pnl += bet_size * 2
        elif outcome > probability_3 and outcome < probability_3 + probability_100: 
            pnl += bet_size * 99
        else:
            pnl -= bet_size
        week += 1
        cum_pnl.append(pnl)

    pnl_paths.append(cum_pnl)

for pnl_path in pnl_paths: 
    plt.plot([i for i in range(500)], pnl_path)
locs, _ = plt.yticks()
plt.yticks(locs, [f"{int(i):,}" for i in locs])
plt.title("P&L paths")
plt.show()

final_wealths = [pnl_path[-1] for pnl_path in pnl_paths]
plt.hist(final_wealths, bins=50)
locs, _ = plt.xticks()
plt.xticks(locs, [f"{int(i):,}" for i in locs])  
plt.title("Distribution of final P&L") # change range for iteration in loop at line 11
plt.show()