import random
import statistics
from statistics import mean, median, mode
from constants import MAX_ROLLS, MAX_NUM_DICE, NUM_SIMULATIONS, SCORES, draw_die
import random
from pdb import set_trace as bp

def get_counts(dice):
    counts = {}
    for d in dice:
        counts[d] = counts.get(d,0) + 1
    return counts;

def get_kept_partial_roll(dice, ones_target):
    counts = get_counts(dice)
    return [ones_target] * (counts.get(ones_target,0) + counts.get(1,0))

def roll(num_dice):
    return  [random.randint(1, 6) for i in range(0, num_dice)]

def summarize_roll(dice, ones_target):
    counts = get_counts(dice)
    return counts.get(ones_target,0) + counts.get(1,0), ones_target

def get_best_ones_target_for_current_roll(dice):
    scores = {}
    for ones_target in dice:
        if ones_target == 1:
            continue
        scores[ones_target] = SCORES[summarize_roll(dice, ones_target)]
    return max(scores, key=scores.get)

def simulate_next_rolls(ones_target, dice, og_num_rolls_left = 2):
    next_roll_scores = []
    for i in range(0, NUM_SIMULATIONS):
        turn = []
        num_rolls_left = og_num_rolls_left
        partial_roll = get_kept_partial_roll(dice, ones_target)
        while num_rolls_left > 0:
            new_partial_roll = roll(MAX_NUM_DICE - len(partial_roll))
            partial_roll += get_kept_partial_roll(new_partial_roll, ones_target)
            count_and_number = summarize_roll(partial_roll, ones_target)
            turn.append(count_and_number)
            num_rolls_left -= 1
        next_roll_scores.append(turn)
    return next_roll_scores

def get_ones_target_for_best_score_in_num_rounds(num_rounds_left, dice):
    scores = {}
    for ones_target in range(2,7):
        simulated_rolls = simulate_next_rolls(ones_target, dice, num_rounds_left) #get scores at the end of that round
        round_simulated_rolls = [x[num_rounds_left-1] for x in simulated_rolls]
        roll_scores = [SCORES[x] for x in round_simulated_rolls]
        scores[ones_target] = mean(roll_scores)

    best_ones_target = max(scores, key=scores.get)
    return best_ones_target, scores[best_ones_target]

#TODO:(daniel.epstein) compute if mode is round up or down from mean
#TODO:(daniel.epstein) don't just return a map, print a nicely formatted report (change from get_stats to print_stats)
#TODO:(daniel.epstein) highlight that 5 points is 1 more of something
def get_stats(simulated_next_rolls, current_count_and_number):
    stats = {}
    current_score = SCORES[current_count_and_number]

    stats['current_roll'] = (current_score, current_count_and_number)
    next_roll_summaries = [x[0] for x in simulated_next_rolls]
    next_roll_scores = [SCORES[x] for x in next_roll_summaries]
    next_roll_deltas = [x - SCORES[current_count_and_number] for x in next_roll_scores if current_count_and_number[0] != MAX_NUM_DICE]

    stats['next_roll'] = (mean(next_roll_scores), mode(next_roll_summaries))
    stats['next_roll_delta'] = mean(next_roll_deltas)

    if len(simulated_next_rolls[0]) > 1:
        next_next_roll_summaries = [x[1] for x in simulated_next_rolls]
        next_next_roll_scores = [SCORES[x] for x in next_next_roll_summaries]
        next_next_roll_deltas = [SCORES[x[1]] - SCORES[x[0]] for x in simulated_next_rolls if x[0][0] != MAX_NUM_DICE]

        stats['next_next_roll'] = (mean(next_next_roll_scores), mode(next_next_roll_summaries))
        stats['next_next_roll_delta'] = mean(next_next_roll_deltas)

    return stats

#TODO:(daniel.epstein) suggest if you should stay or roll again based off when your chances of winning increase or decrease
#TODO(daniel.epstein) take num_players into account once you know what percentage of rolls it would beat
def main():
    print('\n'.join(map('  '.join, zip(*[draw_die(6) for i in range(5)]))))
    print("Welcome to Dice Simulator!\n\n")
    first_input = input("Starting a new game.\nType 'random' for random role \nor enter 5 comma separated dice values\n\n")
    if first_input == 'random':
        dice = roll(5)
    else:
        dice = [int(x) for x in first_input.strip().split(",")]


    best_ones_target_next_round, best_next_round_score = get_ones_target_for_best_score_in_num_rounds(1, dice)
    best_ones_target_next_next_round, best_next_next_round_score = get_ones_target_for_best_score_in_num_rounds(2, dice)
    print("For 1 more round go with {} avg score {}".format( best_ones_target_next_round, best_next_round_score))
    print("For 2 more rounds go with {} avg score {}".format(best_ones_target_next_next_round, best_next_next_round_score))

    while True:

        ones_value = int(input("Dice are {} . . . Enter the 1s value you want to test out \n\n".format(dice)).strip())
        current_count_and_number = summarize_roll(dice, ones_value)

        simulated_next_rolls = simulate_next_rolls(ones_value, dice, 2)
        turn_stats = get_stats(simulated_next_rolls, current_count_and_number)
        print("Results are {} \n\n".format(turn_stats))

main()
