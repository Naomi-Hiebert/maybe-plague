from Virus import Virus
from Agent import Agent

if __name__ == "__main__":
    """
    Script for testing every possible Virus.

    Runs all 2^24 possible virus generators, producing
    all 9*2^16 unique virus signatures with the same
    distribution they are generated from a random seed.
    Then, infects a few agents with each virus. Agent
    infirmity is random unless specified. Caution: this
    produces over 16 million viruses. Do not use large
    values for the inner loop.

    """


    survivors = 0
    deaths = 0
    contagious_days = 0
    asym_days = 0

    for i in range(0x01000000):
        v = Virus(i)

        for j in range(4):
            a = Agent()
            a.infect(v)
            while not (a.healthy or a.dead):
                a.progress_courses()
                if a.shedding and not a.critical: contagious_days += 1
                if a.shedding and not a.symptoms: asym_days += 1
            if a.healthy: survivors += 1
            else: deaths += 1

    print("Death toll: " + str(deaths))
    print("Survivors: " + str(survivors))
    print("Fatality Rate: " + str((deaths / (deaths + survivors)) * 100) + "%")
    print("Average days spent contagious: " + str(contagious_days / (deaths + survivors)))
    print("Average days spent unknown contagious: " + str(asym_days / (deaths + survivors)))



    