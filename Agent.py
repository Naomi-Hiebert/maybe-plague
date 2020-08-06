import random

from Virus import Virus



class Agent:
    """
    A class representing an individual that can be infected by a virus.

    This class tracks progression on two tracks describing a disease
    process. An individual can be infirm, which delays their progression
    towards recovering from the disease. When the disease process is
    concluded, the maximum values attained on these progressions are
    retained and can still be referenced. There are numerous flags
    showing phases of disease and recovery progress.    

    ...

    Attributes:
    -----------

    infirmity : int (0-8)
        The Agent's baseline level of fragility.

    illness_val : int (0-32)
        The Agent's distance along the Illness track.

    recovery_val : int (-8-8)
        The Agent's distance along the Recovery track.
        Can be negative if the agent is infirm.

    healthy : bool
    susceptible : bool
    terminal : bool
    stabilized : bool
    infected : bool
    recovered : bool
    dead : bool
    symptoms : bool
    critical : bool
    shedding : bool

    """

    def __init__(self, infirmity=None):

        """
        Constructor for Agent.

        ...

        Parameters:
        -----------

        infirmity : int, optional
            If this is not provided, it will be randomly generated
            with a geometric distribution (between 0 and 8)

        """

        if infirmity is None:
            infirmity = consecutive_ones(random.getrandbits(8))

        self.infirmity = infirmity
        self.illness_val = 0
        self.recovery_val = 0 - infirmity

        self.healthy = True
        self.susceptible = True
        self.terminal = False
        self.stabilized = False
        self.infected = False
        self.recovered = False
        self.dead = False
        self.symptoms = False
        self.critical = False
        self.shedding = False

    def infect(self, disease: Virus):
        """
        Infects the Agent with the given Virus.

        Safe to call even if the Agent is already sick or
        has previously recovered.
        """
        if self.recovered: return

        self.virus = disease
        self.healthy = False
        self.susceptible = False
        self.infected = True

    def progress_courses(self):
        """
        Advances time 1 day for a (possibly) infected Agent.

        Models disease and recovery progression for the Agent,
        potentially causing the Agent to die or recover. Safe
        to call even if the agent is dead, recovered, or never
        infected in the first place.
        """

        if self.healthy or self.dead: return
        
        if not self.terminal:
            self.__progress_recovery()

        if not self.stabilized:
            self.__progress_illness()

    def __progress_recovery(self):
        # recovery progresses by 0.5 points, on average
        self.recovery_val += random.getrandbits(1)

        if self.recovery_val >= self.virus.immune_onset:
            self.stabilized = True
            self.shedding = False

        if self.recovery_val >= self.virus.recovered_threshold:
            self.recovered = True
            self.healthy = True
            self.infected = False
            self.symptoms = False
            self.critical = False

    def __progress_illness(self):
        # illness progresses by 1.5 points, on average
        self.illness_val += random.getrandbits(1)
        self.illness_val += 1

        if self.illness_val >= self.virus.shedding_onset:
            self.shedding = True
        
        if self.illness_val >= self.virus.symptom_onset:
            self.symptoms = True

        if self.illness_val >= self.virus.critical_threshold:
            self.critical = True

        if self.illness_val >= self.virus.terminal_threshold:
            self.terminal = True

        if self.illness_val >= self.virus.dead_threshold:
            self.dead = True
            self.symptoms = False
            self.shedding = False
            self.critical = False
            self.terminal = False

    def status_string(self) -> str:
        """
        A string describing the Agent's disease status.

        The Agent may be susceptible, infected,
        recovered, or dead. If the agent is infected,
        their level of illness will also be described,
        followed by possible flags if they are stable
        or contagious.
        """
        if self.dead: return "Dead"
        elif self.recovered: return "Recovered"
        elif self.susceptible: return "Susceptible"
        else:
            ret = "Infected, "
            if self.terminal: ret += "Terminal"
            elif self.critical: ret += "Critical"
            elif self.symptoms: ret += "Sick"
            else: ret += "Asymptomatic"

            if self.stabilized: ret += ", Stable"
            if self.shedding: ret += ", Contagious"
            return ret
    
    def status_values(self) -> str:
        """
        A string giving the Agent's Illness and Recovery progression.
        """
        return "Illness: " + str(self.illness_val) + ", Recovery: " + str(self.recovery_val)


def consecutive_ones(input: int) -> int:
    """
    Extracts 8 bits of geometric randomness from a bit string.
    """
    n = 0
    input &= 0x00ff #python's right-shift is signed, so make sure there's a leading 0
    while (input % 2 == 1):
        input >>= 1
        n += 1
    return n


if __name__ == "__main__":
    """
    Basic test function for Agent-Virus interaction.

    Generates an Agent and a Virus, then gives daily updates on
    the course of the Agent's illness until it resolves.
    """
    a = Agent()
    v = Virus()

    print("Generated agent with infirmity " + str(a.infirmity))
    print("Generated virus with generator " + hex(v.generator))
    print(v.string_summary())
    print("Agent Status: " + a.status_string())
    print(a.status_values())
    print("Infecting agent with virus... \n")

    a.infect(v)
    n = 1
    while not (a.healthy or a.dead):
        print("Day " + str(n) + " Status: " + a.status_string())
        print(a.status_values())
        a.progress_courses()
        n += 1
    
    print("Outcome: " + a.status_string())
    print(a.status_values())

        