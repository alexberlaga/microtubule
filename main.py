import random
import numpy as np
import matplotlib.pyplot as plt

N = 13
U = 100
W_VALUES = [10 * x for x in range(1, 25)]
NUM_MCs = 1000
TIME_INCR = .00025

class MC_tube:
    def __init__(self, n, u, w):
        """
        Sets parameters of a single microtubule
        :param n: number of protofilaments
        :param u: rate of changing a protofilament from state i to i-1.
        :param w: rate of changing a protofilament from state i to i+1.
        """
        self.n = n
        self.u = u * TIME_INCR
        self.w = w * TIME_INCR
        self.state = n

    def simulate_mc(self):
        """
        Calculates the first passage time of the microtubule using Monte-Carlo
        :return: first passage time of the microtubule to the catastrophe state (0). If the state is not reached
        by the time MAX_TIME, returns 0.
        """

        if self.u + self.w > 1 or self.u < 0 or self.w < 0 or self.n < 2:
            print("ERROR: parameters are not set correctly")

        seconds = 0

        while(True):

            seconds += TIME_INCR
            rand = random.random()
            decrement_prob = self.state * self.u
            increment_prob = (self.n - self.state) * self.w
            reaction_prob = decrement_prob + increment_prob
            if rand < decrement_prob:
                self.state -= 1
                if self.state == 0:
                    return seconds
                continue

            elif rand < reaction_prob:
                self.state += 1

    def simulate_gillespie(self):
        """
        Calculates the first passage time of the microtubule using Gillespie's Algorithm
        :return: first passage time of the microtubule to the catastrophe state (0). If the state is not reached
        by the time MAX_TIME, returns 0.
        """
        if self.u + self.w > 1 or self.u < 0 or self.w < 0 or self.n < 2:
            print("ERROR: parameters are not set correctly")

        time = 0

        while(True):

            decrement_prob = self.state * self.u
            increment_prob = (self.n - self.state) * self.w
            reaction_prob = decrement_prob + increment_prob

            rand_t = random.random()
            rand_r = random.random()

            rxn_time = (1 / reaction_prob) * np.log(1 / rand_t)
            time += rxn_time

            if (rand_r < (decrement_prob / reaction_prob)):
                self.state -= 1
            else:
                self.state += 1

            if self.state == 0:
                return time



def plot_simulation():
    avg_times = []
    for w in W_VALUES:
        avg_time = 0
        for i in range(NUM_MCs):
            mc = MC_tube(N, U, w)
            fp_time = mc.simulate_gillespie()
            avg_time += fp_time / NUM_MCs
        avg_times.append(avg_time)
        print(str(w) + ", " + str(avg_time))
    d = {"W value" : W_VALUES, "Average time" : avg_times}
    plt.plot("W value", "Average time", data=d)
    plt.show()

plot_simulation()