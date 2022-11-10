import random
import statistics
from statistics import mean, median, mode
from constants import MAX_ROLLS, MAX_NUM_DICE, NUM_SIMULATIONS, SCORES, draw_die
import random
from pdb import set_trace as bp


# Open Questions
# At what point (2-6) do you see diminishing returns on rolling again, per number of players
    # per number of players because max wins so average max score (over 10k games)

#List in order
# TODO: Module to simulate game with number of players and number of rolls each
    # --> this tells you average max score per number of rolls and number of players
# TODO: recommendation engine for what you should do given a set of dice and a current roll
    # --> for both if you go first and if you have to follow a set number of rolls
#TODO:(daniel.epstein) allow them to lock in decisions (not just investigate 1s value)


#TODO:(daniel.epstein) allow option to defer specifying 1s value if no 1 is rolled
#TODO:(daniel.epstein) should i use mean or median?
#TODO:(daniel.epstein) quantify above/below average for current score and potential score (with another role)

#TODO:(daniel.epstein) come up with ideal 1s value to beat a role in certain number of max rolls
    # --> use recursion? to simulate and figure out which choice is best over 10k trials

#TODO:(daniel.epstein) before you can make a "average score in this many rolls" to say this is above or below average
#you need to make something to calculate what you're most likely to have multiple rolls in the future. That gives you
#likely delta for next role and if you do less than that you should roll again and more than that chill.

def convert_ones(dice, ones_target):
    for i in range(0,len(dice)):
        if dice[i] == 1:
            dice[i] = ones_target
    return nums

def get_counts(dice):
    counts = {}
    for d in dice:
        counts[d] = counts.get(d,0) + 1
    keys = sorted(counts.keys())
    return counts;

def get_kept_partial_roll(dice, ones_target):
    counts = get_counts(dice)
    return [ones_target] * (counts.get(ones_target,0) + counts.get(1,0))

def simulate_next_roll(ones_target, dice):
    # keep everything that 1s target is and convert ones, extend the list
    kept_partial_roll = get_kept_partial_roll(dice, ones_target)
    next_roll_scores = []
    for i in range(0, NUM_SIMULATIONS):
        new_partial_roll = roll(MAX_NUM_DICE - len(kept_partial_roll))
        new_partial_roll = kept_partial_roll + get_kept_partial_roll(new_partial_roll, ones_target)
        count_and_number = summarize_roll(new_partial_roll, ones_target)

        next_roll_scores.append(count_and_number)

    return next_roll_scores

def roll(num_dice):
    dice = []
    for i in range(0, num_dice):
        dice.append(random.randint(1,6))
    return dice



def summarize_roll(dice, ones_target):
    highest_number = 0
    highest_count = 0
    counts = get_counts(dice)

    #factor in wildcards
    counts[ones_target] = counts.get(ones_target,0) + counts.get(1,0)

    keys = sorted(counts.keys())
    for k in keys:
        if counts[k] >= highest_count:
            highest_count = counts[k]
            highest_number = k
    return (highest_count, highest_number)


def get_best_summary_for_current_roll(dice):
    max_summary = (1,2)
    max_score = 0
    best_ones_target = 0

    for ones_target in dice:
        if ones_target == 1:
            continue
        count_and_number = summarize_roll(dice, ones_target)
        score = SCORES[count_and_number]
        if score > max_score:
            max_score = score
            max_summary = count_and_number
            best_ones_target = ones_target
    return max_summary


def get_stats(simulated_next_roll, current_count_and_number):
    # want mean median and mode (score) of first second and third roles
    # want average increase in points from 1st to 2nd round (per ones_target)
    stats = {}
    next_roll_scores = [SCORES[x] for x in simulated_next_roll]

    current_score = SCORES[current_count_and_number]
    next_role_deltas = [x - current_score for x in next_roll_scores]

    # bp()
    stats['current_roll'] = (current_score, current_count_and_number)
    stats['next_roll_mean'] = (mean(next_roll_scores), mode(simulated_next_roll))
    stats['next_role_delta_mean'] = (mean(next_role_deltas), mode(next_role_deltas))

    return stats

#TODO:(DANIEL.EPSTEIN) next up
def choose_ones_target_for_avg_max_score_in_num_rounds(dice, num_rounds_left):
    # make simulate_next_roll give you multiple rounds in the future like it used to
    # call that for each 1s target (even ones you don't have)
    # choose ones target that gives you best score at the end of num_rounds_left
    if len(dice) == 0:
        dice = roll(MAX_NUM_DICE)
        num_rounds_left -= 1
    while num_rounds_left > 0:
        # roll until there are no more num_rounds_left
        # pick 1s target
        pass


#TODO:(daniel.epstein) Finish this function where either you have partial roll or []. Get average roll so you can see if you did better or worse
def get_average_max_score_of_next_roll(dice):
    # if dice is empty, get b
    summaries = []
    scores = []
    if len(dice > 0):
        ones_target_summaries = {}
        # for ones_target in dice:
        #     if ones_target == 1:
        #         pass # we don't want to test out score if 1s become 1s
        for i in range(0, NUM_SIMULATIONS):
            old_partial_roll = get_kept_partial_roll(dice, ones_target)
            new_partial_roll = roll(MAX_NUM_DICE - len(old_partial_roll))
            roll = old_partial_roll + new_partial_roll
            summary = summarize_roll(roll, ones_target)
            scores.append(SCORES[summary])
            summaries.append(summary)
        #TODO:How to find the next ones_target? Greedy algorithm? Or optimize for being able to go multiple in the future. (4,6,3) is good so when you get 2 6s in 1 you capitalize
        # ones_target is if you keep anything
        # Question to answer: figure out break off point between 2-6, 3-6, 2-5 for 2 and 3 roll turns where you want to go with 2 of something over 1 of something bigger.
        # Do this for 2 and 3 of something too
        # pass in a set of dice and see suggestion about what to keep and how many rounds to go (as you go through rounds so stay or go)
        # how does this change as you get more people 15% chance of something better than what you have with 6 people means you win 10% of the time, with 7 you lose over time
        get_kept_partial_roll(dice, ones_target)
    else:
        for i in range(0,NUM_SIMULATIONS):
            dice = roll(MAX_NUM_DICE)
            summary = get_best_summary_for_current_roll(dice)
            summaries.append(summary)
            scores.append(SCORES[summary])
    return mean(scores), mode(summaries)


def main(num_players):
    print('\n'.join(map('  '.join, zip(*[draw_die(6) for i in range(5)]))))
    print("Welcome to Dice Simulator!\n\n")
    first_input = input("Starting a new game.\nType 'random' for random role \nor enter 5 comma separated dice values\n\n")
    dice = []
    if first_input == 'random':
        dice = roll(5)
    else:
        dice = [int(x) for x in first_input.strip().split(",")]

    while True:

        ones_value = input("Dice are {} . . . Enter the 1s value you want to test out \n\n".format(dice)).strip()
        ones_value = int(ones_value.strip())
        kept_partial_roll = get_kept_partial_roll(dice, ones_value)
        simulated_next_roll = simulate_next_roll(ones_value, dice)

        # return as 2nd_round, 3rd_round (not a 2d array)
        # check assumptions that everything in first round starts with (3,3)
        #pdb press r to keep going
        current_count_and_number = summarize_roll(kept_partial_roll, ones_value)
        turn_stats = get_stats(simulated_next_roll, current_count_and_number)
        print("Results are {} \n\n".format(turn_stats))

        #TODO:(daniel.epstein) once you have choose 1s target for max score in so many rounds, figure out average max score in rounds 1,2,3
        # scores = []
        # summaries = []
        # for i in range(0,NUM_SIMULATIONS):
        #     summary = roll(5)

main(1)
