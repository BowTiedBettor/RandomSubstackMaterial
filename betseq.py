import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

"""
Convergence, a counterexample to the zero constraints case ["bet more"-bettor]
"""
# stakes = []
# for i in range(10000):
#     stakes.append(3**(int(i/100)))

# def bet(stake):
#     if random.random() < 0.5:
#         return stake
#     else:
#         return -stake

# cum_PL = 0
# cum_stakes = 0
# ROIs = []
# for stake in stakes:
#     cum_PL += bet(stake)
#     cum_stakes += stake
#     ROIs.append(cum_PL/cum_stakes)

# plt.plot([i for i in range(len(ROIs))], ROIs)
# plt.title("'Bet more'-bettor")
# plt.xlabel("Number of bets")
# plt.ylabel("ROI")
# plt.show()


"""
Convergence, a bettor is betting $1 on 2.00 outcomes, each with a probability of 0.55, over and over again.
"""
# stakes = [1 for i in range(1000)]

# def bet(stake):
#         if random.random() < 0.55:
#             return stake
#         else:
#             return -stake

# for i in range(100):
#     cum_PL = 0
#     cum_stakes = 0
#     ROIs = []
#     for stake in stakes:
#         cum_PL += bet(stake)
#         cum_stakes += stake
#         ROIs.append(cum_PL/cum_stakes)
#     plt.plot([i for i in range(len(ROIs))], ROIs)

# plt.title("'$1, 10 % EV'-bettor, 100 simulations")
# plt.ylim([-0.2, 0.3])
# plt.xlabel("Number of bets")
# plt.ylabel("ROI")
# plt.show()


"""
Probability distribution of the ROI after 100, 500, 1000, 10000 bets
"""
# n_list = [100, 500]

# def map_to_roi(successes, n):
#     return 2*successes/n - 1

# for n in n_list:
#     roi_outcomes = []
#     for i in range(1000000): # number of simulations, should be high to approximate the true density correctly
#         roi = map_to_roi(np.random.binomial(n, 0.55), n)
#         roi_outcomes.append(roi)
#     plt.hist(roi_outcomes, bins = 50)
#     plt.title(f"Probability distribution for the ROI after {n} bets")
#     plt.xlabel("ROI")
#     plt.tick_params(labelleft=False, left=False)
#     plt.xlim([-0.2, 0.4])
#     plt.show()


"""
Alternative realities for a real bettor's last 500 bets
"""
# total_stakes = 112768

# betseq_df = pd.read_excel("FILE PATH")
# stakes_series = betseq_df['Stake']
# odds_series = betseq_df['Odds']
# positive_ev_series = betseq_df['Assumed probability [+15 % EV]']
# negative_ev_series = betseq_df['Assumed probability [-15 % EV]']


"""
Positive EV
"""
# cum_PL_sim_results = []
# roi_sim_results = []

# for i in range(10000): #10 000 simulations
#     cum_PL = 0
#     for stake, odds, prob in zip(stakes_series, odds_series, positive_ev_series):
#         if random.random() < prob:
#             cum_PL += stake * (odds-1)
#         else:
#             cum_PL += -stake
#     roi = cum_PL/total_stakes
#     cum_PL_sim_results.append(cum_PL)
#     roi_sim_results.append(roi)

# plt.hist(cum_PL_sim_results, bins = 50)
# plt.title("Cumulative P&L - 10 000 simulations, +15 % EV")
# plt.ylabel("Frequency")
# plt.xlabel("Cumulative P&L")
# plt.show()

# plt.hist(roi_sim_results, bins = 50)
# plt.title("ROI - 10 000 simulations, +15 % EV")
# plt.ylabel("Frequency")
# plt.xlabel("ROI")
# plt.show()

# actual_roi = 0.33
# counter = 0
# for i in roi_sim_results:
#     if i > actual_roi:
#         counter += 1
# print("Estimated probability of the observed ROI or higher:", counter/10000)


# counter = 0
# for i in roi_sim_results:
#     if i < 0:
#         counter += 1
# print("Estimated probability of losing money:", counter/10000)


"""
Negative EV
"""
# cum_PL_sim_results = []
# roi_sim_results = []

# for i in range(1000000): #10 000 simulations
#     cum_PL = 0
#     for stake, odds, prob in zip(stakes_series, odds_series, negative_ev_series):
#         if random.random() < prob:
#             cum_PL += stake * (odds-1)
#         else:
#             cum_PL += -stake
#     roi = cum_PL/total_stakes
#     cum_PL_sim_results.append(cum_PL)
#     roi_sim_results.append(roi)

# plt.hist(cum_PL_sim_results, bins = 50)
# plt.title("Cumulative P&L - 10 000 simulations, -15 % EV")
# plt.ylabel("Frequency")
# plt.xlabel("Cumulative P&L")
# plt.show()

# plt.hist(roi_sim_results, bins = 50)
# plt.title("ROI - 10 000 simulations, -15 % EV")
# plt.ylabel("Frequency")
# plt.xlabel("ROI")
# plt.show()

# actual_roi = 0.33
# counter = 0
# # since we're deep down in the tails, increase the number of simulations for better accuracy
# for i in roi_sim_results:
#     if i > actual_roi:
#         counter += 1
# print("Estimated probability of the observed ROI or higher:", counter/10000)


# counter = 0
# for i in roi_sim_results:
#     if i < 0:
#         counter += 1
# print("Estimated probability of losing money:", counter/10000)


"""
Learning the truth, the bayesian way
"""
betseq_df = pd.read_excel("FILE PATH HERE")
stakes_series = betseq_df['Stake']
odds_series = betseq_df['Odds']
# outcomes_series = betseq_df['Outcome']

# a discrete approximation of the continuous uniform prior
possible_values = np.linspace(-0.5, 0.5, 100)

# ev_prior = [0.01 for value in possible_values]
# # plot of prior
# plt.plot(possible_values, ev_prior)
# plt.title("Prior probability distribution of true EV, uniform [-0.50, 0.50]")
# plt.xlabel("EV")
# plt.ylabel("Density")
# plt.tick_params(labelleft=False, left=False)
# plt.show()

# we'll define the event "seeing a roi of X" as being in the range [x-0.05, x+0.05]
# therefore we want to, for each ev in our range of possible ev values, compute
# the probability of the sequence landing in the [actual roi-0.05, actual roi+0.05] range
# furthermore, we'll do this at three different steps, after 100 bets, after 250 bets
# and after 500 bets to illustrate how a bayesian bettor learns through time

# for use below
# actual roi after 100 bets = 0.107
# actual roi after 250 bets = 0.322
# actual roi after 500 bets = 0.333
number_of_bets = 500
true_roi = 0.333
number_of_simulations = 10000 # would like this to be much bigger but can't wait for hours

likelihoods = [] # will hold the likelihood for each ev in possible_values
sum_all_paths = 0 # the denominator in the bayesian expression [normalization constant]
for ev in possible_values:
    # for each possible ev we fix the ev, simulate the probability of seeing the
    # real world observed roi *conditional* on this ev and store that
    # value in the likelihoods list
    roi_sim_results = [] # store the roi for each simulation, 10000 simulations about to run
    for i in range(number_of_simulations):
        cum_PL = 0
        cum_stakes = 0
        for stake, odds in zip(stakes_series[0:number_of_bets], odds_series[0:number_of_bets]):
            prob = (1/odds)*(1+ev)
            cum_stakes += stake
            if random.random() < prob:
                # if bet wins
                cum_PL += stake * (odds-1)
            else:
                # if bet loses
                cum_PL += -stake
        simulated_roi = cum_PL/cum_stakes
        roi_sim_results.append(simulated_roi)

    counter = 0
    for sim_res in roi_sim_results:
        if sim_res > true_roi - 0.05 and sim_res < true_roi + 0.05:
            counter += 1
    likelihood = counter/number_of_simulations
    likelihoods.append(likelihood)
    sum_all_paths += likelihood

ev_posterior = [likl/sum_all_paths for likl in likelihoods]

plt.plot(possible_values, ev_posterior)
plt.title(f"Posterior probability distribution of true EV after {number_of_bets} bets")
plt.xlabel("EV")
plt.ylabel("Density")
plt.tick_params(labelleft=False, left=False)
plt.show()
