import pymc as pm
import arviz as az
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# load the data, code assumes NHLData.xlsx exists in the same directory
nhldata_df = pd.read_excel("NHLData.xlsx")
case_data_uncleaned = nhldata_df.Case.to_numpy()
case_data = case_data_uncleaned[~np.isnan(case_data_uncleaned)]
number_of_ones = int(sum(case_data))
number_of_games = len(case_data)

nhl_bayes_model = pm.Model()

with nhl_bayes_model: 
    # our probability p [probability of winning given a lead into the third period] that we're learning about.
    # as mentioned in the post, we'll assign it a uniform prior
    p = pm.Uniform(name = "p", lower = 0, upper = 1)

    # a model for how the number of 1's in our dataset was generated [given a fixed p and N games, 
    # what's the probability of seeing K games satisfying our criterion? ANSWER: Binomial(N, p)]
    likelihood = pm.Binomial(name = "likelihood", p = p, n = number_of_games, observed = number_of_ones)
    # the "observed = number_of_ones" tells PyMC that this is the random variable we've observed data from, 
    # and that the real world observation was "number_of_ones", which in our case is 836.

    # using the above information, PyMC will now compare all possible p's between 0 and 1 to try to understand
    # which one of those values is most likely [or, more specifically, exactly how likely each such p is] 
    # to have generated 836 successes in 1 008 datapoints.
    inference_data = pm.sample()

ax = pm.plot_posterior(inference_data)
ax.set_title("Posterior for p")
plt.show()
