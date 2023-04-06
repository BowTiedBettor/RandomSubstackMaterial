import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

"""
PLOTS
"""
# x_axis = np.arange(-10, 10, 0.001)
# # horse 1
# # mean = 0, std = 1
# plt.plot(x_axis, norm.pdf(x_axis, 0, 1), label = "horse 1")
# # horse 2
# # mean = 1, std = 2
# plt.plot(x_axis, norm.pdf(x_axis, 1, 2), label = "horse 2")
# # horse 3
# # mean = 0, std = 4
# plt.plot(x_axis, norm.pdf(x_axis, 0, 4), label = "horse 3")
# # horse 4
# # mean = -2, std = 3
# plt.plot(x_axis, norm.pdf(x_axis, -2, 3), label = "horse 4")
# # horse 5
# # mean = 1.5, std = 0.3
# plt.plot(x_axis, norm.pdf(x_axis, 1.5, 0.3), label = "horse 5")

# plt.legend()
# plt.axis('off')
# plt.show()

"""
SIMULATIONS
"""
horse_1_samples = np.random.normal(loc=0.0, scale=1.0, size=10000)
horse_2_samples = np.random.normal(loc=0.5, scale=3.0, size=10000)
horse_3_samples = np.random.normal(loc=0.0, scale=4.0, size=10000)
horse_4_samples = np.random.normal(loc=-2.0, scale=3.0, size=10000)
horse_5_samples = np.random.normal(loc=0.75, scale=0.4, size=10000)

matrix = np.column_stack([horse_1_samples, horse_2_samples, horse_3_samples, horse_4_samples, horse_5_samples])

win_counter = [0, 0, 0, 0, 0]
show_counter = [0, 0, 0, 0, 0]
h2h_counter = [0, 0]
for row in range(matrix.shape[0]):
    # win & show
    for i in range(matrix.shape[1]):
        # win
        value = matrix[row][i]
        if value == max(matrix[row]):
            win_counter[i] += 1

        # show
        s = sorted(matrix[row])
        if value >= s[-3]:
            show_counter[i] += 1

    # h2h
    if matrix[row][2] > matrix[row][4]:
        h2h_counter[0] += 1
    else:
        h2h_counter[1] += 1

print(win_counter)
print(show_counter)
print(h2h_counter)
