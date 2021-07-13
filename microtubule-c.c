#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <pthread.h>
#include <sys/time.h>
#include <stdbool.h>
#include "/Users/Alex/Downloads/mt19937-64/mt19937-64.c"

#define N 13
#define U_EXP 0.02
#define W_EXP 0.02
#define FWD_FINAL_STATE 4
#define REV_FINAL_STATE 4

#define NUM_MCS 40000

// pthread_mutex_t mutex;


struct MC_tube_list {
    int id;
    int ntubes;
    double u;
    double w;
    int cur;
};

/**
* Generation of random number seed, get a current time in micri-second unit
**/


int 
gus() 
{
    struct timeval tp;
    gettimeofday(&tp,0);
    return (tp.tv_usec);
}

void *
simulate_gillespie (void *ptr, double w_val, bool fwd, double dist_w_val) 
{
    (void) ptr;
    struct MC_tube_list mc = *(struct MC_tube_list *) ptr;
    
    FILE *result;
    FILE *fano;

    double time;
    
    double decrement_rate;
    double increment_rate;
    double reaction_rate;
    
    double randt;
    double randr;
    double rxn_time;

    double average_time;
    double variance;
    double second_moment;
    double fano_factor;
    int state;
    int initial_state;
    int final_state;
    if (fwd){
        result = fopen("result.txt", "a");
        fano = fopen("fano.txt", "a");
        initial_state = 4;
        final_state = 0;
    }
        
    else{
        result = fopen("revresult.txt", "a");
        fano = fopen("revfano.txt", "a");
        initial_state = 0;
        final_state = 4;
    }
       
    
    average_time = 0;
    second_moment = 0;
    unsigned long long idum;
    idum=gus();
    init_genrand64(idum);

    mc.ntubes = NUM_MCS;
    mc.u = U_EXP;
    mc.w = w_val;
    mc.cur = 0;

    printf("W = %f\n", w_val);

    while (mc.cur < mc.ntubes) {
        time = 0;
        state = initial_state;
       
        while(1) {
            decrement_rate = (double) state * mc.u;
            increment_rate = (double) (N - state) * mc.w;
            
            reaction_rate = decrement_rate + increment_rate;
            
            
            randt = genrand64_real2();

            
            randr = genrand64_real2();
            while (!randt)
                randt = genrand64_real2();
            if (!randr)
                randr = genrand64_real2();
            rxn_time = (1 / reaction_rate * log(1 / randt));
            
            time += rxn_time;
            if (randr < decrement_rate / reaction_rate) {
                state--;
            }
            else
                state++;
            if (state == final_state) {
                average_time += (time / NUM_MCS);
                second_moment += (time * time / NUM_MCS);
                mc.cur++;
                // pthread_mutex_lock(&mutex);
                if (mc.w - dist_w_val < 0.0001 && mc.w - dist_w_val > -0.0001)
                    fprintf(result, "%f, ", time);
                // pthread_mutex_unlock(&mutex);
                if (!(mc.cur % 10000))
                    printf("%d\n", mc.cur);
                break;
            }
        }
    }
    variance = second_moment - (average_time * average_time);
    fano_factor = variance / (average_time * average_time);
    fprintf(fano, "W = %f, MEAN: %f, VARIANCE: %f, FANO FACTOR: %f\n", mc.w, average_time, variance, fano_factor);
    return (NULL);
}

void *
rng_tester(void *ptr) 
{
    FILE *rng;
    int i;
    
    (void) ptr;
    rng = fopen("rng.txt", "a");
    
    unsigned long long idum;
    idum=gus();
    init_genrand64(idum);

    for (i = 0; i < 1000; i++)
        fprintf(rng, "%f\n", genrand64_real2());
    return (NULL);
}

int
main(int argc, char **argv) {
    (void) argc;
    (void) argv;
    fopen("result.txt", "w");
    fopen("fano.txt", "w");
    fopen("revresult.txt", "w");
    fopen("revfano.txt", "w");
    fopen("rng.txt", "w");
    double w;
    // double w;

    // pthread_t tid[8];
    
    struct MC_tube_list *mcs = malloc(sizeof(struct MC_tube_list));

    // int i;

    // pthread_mutex_init(&mutex, NULL);
    
    // for (i = 0; i < 8; i++){
    //     mcs[i] = malloc(sizeof(struct MC_tube_list));
    //     pthread_create(&tid[i], NULL, simulate_gillespie, &mcs[i]);
    // }
    // for (i = 0; i < 8; i++)
    //     pthread_join(tid[i], NULL);

    // pthread_mutex_destroy(&mutex);
    for (w = 0; w < 0.01; w+=0.001)
        simulate_gillespie(mcs, w, true, 0.003);
}
