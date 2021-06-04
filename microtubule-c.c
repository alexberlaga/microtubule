#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define N 13
#define U 100
#define NUM_MCS 50000

struct MC_tube_list {
    int ntubes;
    double u;
    double w;
};

int
simulate_gillespie (struct MC_tube_list mc) 
{
    FILE *result;
    int state = N;
    double time;
    double decrement_rate;
    double increment_rate;
    double reaction_rate;
    int i;
    double randt;
    double randr;
    double rxn_time;

    result = fopen("result.txt", "w");
    for (i = 0; i < mc.ntubes; i++) {
        time = 0;
        while(1) {
            decrement_rate = (double) state * mc.u;
            increment_rate = (double) (N - state) * mc.w;
            reaction_rate = decrement_rate + increment_rate;

            randt = (double) rand() / (RAND_MAX);
            randr = (double) rand() / (RAND_MAX);

            rxn_time = (1 / reaction_rate * log(1 / randt));
            time += rxn_time;
            if (randr < decrement_rate / reaction_rate) 
                state--;
            else
                state++;
            if (!state) {
                if (i == mc.ntubes)
                    fprintf(result, "%f", time);
                else
                    fprintf(result, "%f, ", time);
                break;
            }
        }
    }
    return (0);
}

int
main(int argc, char **argv) {
    (void) argc;
    (void) argv;

    int u_exp = 100;
    int w_exp = 170;
    struct MC_tube_list mc = {NUM_MCS, u_exp, w_exp};
    simulate_gillespie(mc);
}
