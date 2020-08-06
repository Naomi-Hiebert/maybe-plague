from Virus import Virus
from Agent import Agent

if __name__ == "__main__":
    """
    Script for testing a Virus.

    Generates a Virus (or you can hard-code a generator) then
    tests it in a population of Agents. Agents infirmity can
    be specified, with default behavior of the usual geometric
    distribution. Population size around 100000 is recommended,
    as it leads to outputs that are mostly stable to 2 digits
    while still being faster than my attention span.
    """


    pop_size = 100000

    v = Virus()
    print("Generated virus with generator " + hex(v.generator))
    print(v.string_summary())
    print("Infecting " + str(pop_size) + " agents with virus... \n")

    survivors = 0
    deaths = 0
    contagious_days = 0
    asym_days = 0

    for i in range(pop_size):
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


    

