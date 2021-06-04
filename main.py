import random
import asyncio
import numpy as np
import matplotlib.pyplot as plt

N = 13
U = 100
W_VALUES = [10 * x for x in range(25)]
NUM_MCs = 500

class MC_tube_list:
    def __init__(self, ntubes, n, u, w):
        """
        Sets parameters of a single microtubule
        :param n: number of protofilaments
        :param u: rate of changing a protofilament from state i to i-1.
        :param w: rate of changing a protofilament from state i to i+1.
        """
        self.ntubes = ntubes
        self.n = n
        self.u = u
        self.w = w

    # def simulate_mc(self):
    #     """
    #     Calculates the first passage time of the microtubule using Monte-Carlo
    #     :return: first passage time of the microtubule to the catastrophe state (0). If the state is not reached
    #     by the time MAX_TIME, returns 0.
    #     """
    #
    #     if self.u + self.w > 1 or self.u < 0 or self.w < 0 or self.n < 2:
    #         print("ERROR: parameters are not set correctly")
    #
    #     times = []
    #     for i in range(self.ntubes):
    #         seconds = 0
    #         while True:
    #             seconds += TIME_INCR
    #             rand = random.random()
    #             decrement_prob = self.state * self.u
    #             increment_prob = (self.n - self.state) * self.w
    #             reaction_prob = decrement_prob + increment_prob
    #             if rand < decrement_prob:
    #                 self.state -= 1
    #                 if self.state == 0:
    #                     times.append(seconds)
    #                     break
    #
    #             elif rand < reaction_prob:
    #                 self.state += 1
    #     return times

    def simulate_gillespie(self):
        """
        Calculates the first passage time of the microtubule using Gillespie's Algorithm
        :return: first passage time of the microtubule to the catastrophe state (0). If the state is not reached
        by the time MAX_TIME, returns 0.
        """
        if self.n < 2:
            print("ERROR: parameters are not set correctly")

        times = []
        for i in range(self.ntubes):
            time = 0
            state = self.n
            while(True):
                decrement_rate = state * self.u
                increment_rate = (self.n - state) * self.w
                reaction_rate = decrement_rate + increment_rate



                rand_t = random.random()
                rand_r = random.random()

                rxn_time = (1 / reaction_rate) * np.log(1 / rand_t)
                time += rxn_time
                if rand_r < decrement_rate / reaction_rate:
                    state -= 1
                else:
                    state += 1

                if state == 0:
                    times.append(time)
                    break

        return times





def plot_simulation():
    avg_times = []
    w_example = 50
    mc = MC_tube_list(100000, N, U, w_example)
    result = mc.simulate_gillespie()
    result2 = [np.log10(x) for x in result]
    plt.hist(result2, 400)
    plt.yscale("log")
    plt.show()
    for w in W_VALUES:
        mc = MC_tube_list(NUM_MCs, N, U, w)
        fp_times = mc.simulate_gillespie()
        avg_time = np.average(fp_times)
        avg_times.append(avg_time)
        print(str(w) + ", " + str(avg_time))
    d = {"W value" : W_VALUES, "Average time" : avg_times}
    plt.plot("W value", "Average time", data=d)
    plt.show()

plot_simulation()