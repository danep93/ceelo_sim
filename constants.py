MAX_ROLLS = 3
MAX_NUM_DICE = 5
NUM_SIMULATIONS = 100

SCORES = {
    (0,0): 0,
    (1,2): 1,
    (1,3): 2,
    (1,4): 3,
    (1,5): 4,
    (1,6): 5,
    (2,2): 6,
    (2,3): 7,
    (2,4): 8,
    (2,5): 9,
    (2,6): 10,
    (3,2): 11,
    (3,3): 12,
    (3,4): 13,
    (3,5): 14,
    (3,6): 15,
    (4,2): 16,
    (4,3): 17,
    (4,4): 18,
    (4,5): 19,
    (4,6): 20,
    (5,2): 21,
    (5,3): 22,
    (5,4): 23,
    (5,5): 24,
    (5,6): 25
}

def draw_die(die):
    if die == 1:
        return ["=========",
                "|       |",
                "|   O   |",
                "|       |",
                "=========",]
    elif die == 2:
        return ["=========",
                "| O     |",
                "|       |",
                "|     O |",
                "=========",]
    elif die == 3:
        return ["=========",
                "| O     |",
                "|   O   |",
                "|     O |",
                "=========",]
    elif die == 4:
        return ["=========",
                "| O   O |",
                "|       |",
                "| O   O |",
                "=========",]
    elif die == 5:
        return ["=========",
                "| O   O |",
                "|   O   |",
                "| O   O |",
                "=========",]
    else:
        return ["=========",
                "| O   O |",
                "| O   O |",
                "| O   O |",
                "=========",]





