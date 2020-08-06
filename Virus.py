import random

class Virus:
    """
    Class representing a virus.

    This class holds data regarding important thresholds on two progression
    tracks that describe the behavior of the virus. The Recovery track determines
    how an Agent can recover from the virus, while the Illness track determines
    how an Agent can get sick and die from the virus. Because the Agent progresses
    down the Illness track an average of three times faster than the Recovery
    track, the Illness track values are generally much higher.

    Attributes:
    -----------
    
    generator : int
        The 24-bit signature used to define the virus.

    immune_onset : int (0-8)
        Recovery value required to stabilize

    recovery_duration : int (1-4)
        Recovery progress required to recover fully, once stable
    
    recovered_threshold : int (1-12)
        Recovery value required to recover fully

    shedding_onset : int (2-9)
        Illness value required to become contagious

    symptom_onset : int (2-9)
        Illness value required to become symptomatic

    moderate_duration : int (2-9)
        Illness value required to become critical, once symptomatic
    
    critical_duration : int (2-9)
        Illness value required to become terminal, once critical

    terminal_duration : int (1-4)
        Illness value required to die, once terminal

    critical_threshold : int (4-18)
        Illness value required to become critical
    
    terminal_threshold : int (6-27)
        Illness value required to become terminal
    
    dead_threshold : int (7-31)
        Illness value required to become dead

    
    Notes:
    ------

    When a random generator is used, most of the onset and duration
    attributes will have a uniform distribution over their defined ranges.
    The one exception is the immune_onset, which has a truncated geometric
    distribution. The threshold attributes are defined as sums of an onset
    attribute and one or more duration attributes.

    The most important numbers determining the survival rate of a virus are
    the immune_onset and terminal_threshold attributes. Because of the rates
    of progression on the tracks, a virus will generally be over 50% fatal
    in healthy Agents when (terminal_threshold * 3) > immune_onset. If both
    numbers are low, the Agent's infirmity level will have a higher impact
    on survival rates than if both numbers are high.

    """

    def __init__(self, generator=None):
        """
        Constructor for Virus.

        Parameters:
        -----------

        generator : int, optional
            A 24-bit sequence determining the behavior of the virus.
            Randomly generated if no sequence is provided.
        """

        if generator is None:
            generator = random.getrandbits(24)

        self.generator = generator

        # Some bit-shifting nonsense to extract our appropriately-distributed
        # values from our generator bit string. First in hex, for 2- or 4-bit
        # sequences.
        self.immune_onset = consecutive_ones(generator & 0x000000FF)
        self.recovery_duration = ((generator & 0x00000300) >> 8) + 1
        self.terminal_duration = ((generator & 0x00000C00) >> 10) + 1
        # Switching our masks to octal because we need 3-bit sequences.
        # The masks are aligned to clarify what we're doing here.
        self.symptom_onset =     ((generator & 0o0000070000) >> 12) + 2
        self.shedding_onset =    ((generator & 0o0000700000) >> 15) + 2
        self.moderate_duration = ((generator & 0o0007000000) >> 18) + 2
        self.critical_duration = ((generator & 0o0070000000) >> 21) + 2
        
        # Generating our other attributes as sums of the above.
        self.critical_threshold = self.symptom_onset + self.moderate_duration
        self.terminal_threshold = self.critical_threshold + self.critical_duration
        self.dead_threshold = self.terminal_threshold + self.terminal_duration
        self.recovered_threshold = self.immune_onset + self.recovery_duration
    
    def string_summary(self) -> str:
        """
        Pretty-printed string describing virus behavior in two lines.

        The first line shows the threshold for contagiousness (in parens),
        followed by the the thresholds for symptoms, critical illness,
        terminal illness, and death. The second line shows the thresholds
        for stabilizing and recovering.
        """
        ret = "Progression: (" + str(self.shedding_onset) + "), " + str(self.symptom_onset) + ", "
        ret += str(self.critical_threshold) + ", " + str(self.terminal_threshold) + ", "
        ret += str(self.dead_threshold) + "\nRecovery: " + str(self.immune_onset) + ", "
        ret += str(self.recovered_threshold)
        return ret


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
    Prints summaries of a predefined and a random virus
    """

    a = Virus(0x00FFFF33)
    print("Known virus, generator 0x00FFFF33")
    print(a.string_summary())

    v = Virus()
    print("Random virus, generator " + hex(v.generator))
    print(v.string_summary())






        