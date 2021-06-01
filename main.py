import random
import numpy
import matplotlib.pyplot as plt

N = 13;
U = 0.05
W = 0.05
MAX_TIME = 50000
NUM_MCs = 100000


class MC_tube:
    def __init__(self, n, u, w):
        """
        Sets parameters of a single microtubule
        :param n: number of protofilaments
        :param u: rate of changing a protofilament from state i to i-1.
        :param w: rate of changing a protofilament from state i to i+1.
        """
        self.n = n
        self.u = u
        self.w = w
        self.state = n

    def simulate(self):
        """
        Calculates the first passage time of the microtubule
        :return: first passage time of the microtubule to the catastrophe state (0). If the state is not reached
        by the time MAX_TIME, returns 0.
        """

        if self.u + self.w > 1 or self.u < 0 or self.w < 0 or self.n < 2:
            print("ERROR: parameters are not set correctly")

        for time in range(MAX_TIME):

            rand = random.random()
            decrement_prob = self.state * self.u
            increment_prob = decrement_prob + (self.n - self.state) * self.w

            if rand < decrement_prob:
                self.state -= 1
                if self.state == 0:
                    return time + 1
                continue

            elif rand < increment_prob:
                self.state += 1

        return 0

def plot_simulation():
    num_zeros = 0
    fp_times = []
    for i in range(NUM_MCs):
        mc = MC_tube(N, U, W)
        fp_time = mc.simulate()
        if not fp_time:
            num_zeros += 1
        else:
            fp_times.append(fp_time)
    print("Probability of catastrophe: " + str(1 - num_zeros / NUM_MCs))
    plt.hist(fp_times, 200)
    plt.show()

plot_simulation()