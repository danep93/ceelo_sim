import random
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

def mean_score(summaries):
    scores = [SCORES.get(x,0) for x in summaries]
    return mean(scores)

def compare_summaries(first,second):
    return 1 if SCORES[first] > SCORES[second] else -1 if SCORES[first] < SCORES[second] else 0

def summary_to_partial_roll(summary):
    return [summary[1]] * summary[0]

#TODO:(daniel.epstein) make it take current roll and tell you the rest of the rolls. SO you can plug into get_win_ratios for all remaining rounds
def simulate_next_rolls(ones_target, dice, og_num_rolls_left = 2):
    #NOTE: runs num_simulations times
    next_roll_summaries = []
    for i in range(0, NUM_SIMULATIONS):
        num_rolls_left = og_num_rolls_left
        turn = []

        partial_roll = get_kept_partial_roll(dice, ones_target)

        while num_rolls_left > 0:
            new_partial_roll = roll(MAX_NUM_DICE - len(partial_roll))
            partial_roll += get_kept_partial_roll(new_partial_roll, ones_target)
            summary = summarize_roll(partial_roll, ones_target)
            turn.append(summary)
            num_rolls_left -= 1
        next_roll_summaries.append(turn)
    return next_roll_summaries

def simulate_remaining_rolls(dice, og_num_rolls_left = 2):
    #NOTE: runs num_simulations times
    all_rolls = {}
    next_roll_summaries = []
    if len(dice) == 0:
        dice = roll(MAX_NUM_DICE)
    ones_target, summaries = get_ones_target_and_summaries_for_best_score_in_num_rounds(og_num_rolls_left, dice)
    return ones_target, summaries


def _get_best_ones_target_for_current_roll(dice):
    scores = {}
    for ones_target in dice:
        if ones_target == 1:
            continue
        scores[ones_target] = SCORES[summarize_roll(dice, ones_target)]
    return max(scores, key=scores.get)

def get_potential_best_ones_targets(dice):
    # gets number with the highest concordance or highest value (at most 2)
    dice = [x for x in dice if x != 1] # 1 cannot be a 1s target
    if len(dice) == 0:
        return [2,3,4,5,6]
    counts = get_counts(dice)
    values = [max(dice), max(counts, key=counts.get)]
    return list(set(values))

def get_ones_target_for_best_score_in_num_rounds(num_rounds_left, dice):
    # NOTE: runs num simulations through simulate_next_rolls
    summaries = {}
    scores = {}
    if num_rounds_left == 0:
        ones_target = _get_best_ones_target_for_current_roll(dice)
        return ones_target, [summarize_roll(dice, ones_target)] * NUM_SIMULATIONS
    potential_ones_targets = get_potential_best_ones_targets(dice)
    for ones_target in potential_ones_targets:
        simulated_rolls = simulate_next_rolls(ones_target, dice, num_rounds_left)
        round_simulated_rolls = [x[num_rounds_left-1] for x in simulated_rolls] #-1 because 0 offset arrays
        summaries[ones_target] = round_simulated_rolls
        scores[ones_target] = mean_score(round_simulated_rolls)
    best_ones_target = max(scores, key=scores.get)
    return best_ones_target, summaries[best_ones_target]

def get_ones_target_and_summaries_for_best_score_in_num_rounds(num_rounds_left, dice):
    # NOTE: runs num simulations through simulate_next_rolls
    summaries = {}
    scores = {}
    if num_rounds_left == 0:
        ones_target = _get_best_ones_target_for_current_roll(dice)
        return ones_target, [summarize_roll(dice, ones_target)] * NUM_SIMULATIONS
    potential_ones_targets = get_potential_best_ones_targets(dice)
    for ones_target in potential_ones_targets:
        simulated_rolls = simulate_next_rolls(ones_target, dice, num_rounds_left)
        # round_simulated_rolls = [x[num_rounds_left-1] for x in simulated_rolls] #-1 because 0 offset arrays
        summaries[ones_target] = simulated_rolls
        scores[ones_target] = mean_score([x for x in simulated_rolls[-1]])
    best_ones_target = max(scores, key=scores.get)
    return best_ones_target, summaries[best_ones_target]


# get best ones targets takes a map (from run_simulations) and just adds the score



#TODO:(daniel.epstein) fix the bug with max
#TODO:(daniel.epstein) investigate why you never go 3 rounds even with 2 6s
#TODO:(daniel.epstein): change get_potential_ones_target to use highest if theres a tie on concordance
def get_win_ratio(curr_round, fp_summaries, ones_target):
    wins = 0
    losses = 0

    #cpu competitors
    for i in range(0,NUM_SIMULATIONS):
        cpu_dice = roll(MAX_NUM_DICE)
        cpu_ones_target, cpu_summaries = get_ones_target_for_best_score_in_num_rounds(curr_round-1, cpu_dice)
        # bp()
        compare_result = compare_summaries(fp_summaries[i], cpu_summaries[i])
        # print("round is {} and cpu_dice is {} and cpu_summary is {} and fp_summary is {} and compare_results {}".format(
        #     curr_round, cpu_dice, cpu_summaries[i], fp_summaries[i], compare_result))

        if compare_result > 0:
            wins += 1
        elif compare_result < 0:
            losses += 1
        else: # we don't count ties
            continue
    return str(wins) + ":" + str(losses)

print(get_win_ratio(1, [2,2,3,5,6], ))
# def get_remaining_rounds_win_ratios(curr_round, fp_summaries, ones_target):
#     wins = 0
#     losses = 0
#
#     #cpu competitors
#     for i in range(0,NUM_SIMULATIONS):
#         cpu_dice = roll(MAX_NUM_DICE)
#         cpu_ones_target, cpu_summaries = get_ones_target_for_best_score_in_num_rounds(curr_round-1, cpu_dice)
#         # bp()
#         compare_result = compare_summaries(fp_summaries[i], cpu_summaries[i])
#         # print("round is {} and cpu_dice is {} and cpu_summary is {} and fp_summary is {} and compare_results {}".format(
#         #     curr_round, cpu_dice, cpu_summaries[i], fp_summaries[i], compare_result))
#
#         if compare_result > 0:
#             wins += 1
#         elif compare_result < 0:
#             losses += 1
#         else: # we don't count ties
#             continue
#     return str(wins) + ":" + str(losses)
#

#TODO:(daniel.epstein) compute if mode is round up or down from mean
#TODO:(daniel.epstein) don't just return a map, print a nicely formatted report (change from get_stats to print_stats)
#TODO:(daniel.epstein) highlight that 5 points is 1 more of something
#TODO:(daniel.epstein) get_stats computes win_ratio from win_percentage. 90% means 9 wins to 1 loss
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


def main():
    print(simulate_remaining_rolls([], 3))

#TODO:(daniel.epstein) suggest if you should stay or roll again based off when your chances of winning increase or decrease

# def main():
#     print('\n'.join(map('  '.join, zip(*[draw_die(6) for i in range(5)]))))
#     print("Welcome to Dice Simulator!\n\n")
#     first_input = input("Starting a new game.\nType 'random' for random role \nor enter 5 comma separated dice values\n\n")
#     if first_input == 'random':
#         dice = roll(5)
#     else:
#         dice = [int(x) for x in first_input.strip().split(",")]
#
#     current_round = 1
#     # current roll (1)
#     best_ones_target_r1, summaries_r1 = get_ones_target_for_best_score_in_num_rounds(0, dice)
#     win_ratio_r1 = get_win_ratio(1, summaries_r1, best_ones_target_r1)
#
#     # next rolls (2 and 3)
#     best_ones_target_r2, summaries_r2 = get_ones_target_for_best_score_in_num_rounds(1, dice)
#     win_ratio_r2 = get_win_ratio(2, summaries_r2, best_ones_target_r2)
#
#     best_ones_target_r3, summaries_r3 = get_ones_target_for_best_score_in_num_rounds(1, dice)
#     win_ratio_r3 = get_win_ratio(3, summaries_r3, best_ones_target_r3)
#
#     print("Round 1: Best score is with 1s target {} giving you win ratio is {}".format(best_ones_target_r1, win_ratio_r1))
#     print("Predictions for Round 2: Best score would be with 1s target {} giving you a win ratio of {}".format(best_ones_target_r2, win_ratio_r2))
#     print("Predictions for Round 3: Best score would be with 1s target {} giving you a win ratio of {}".format(best_ones_target_r3, win_ratio_r3))

    #optional round 2
    # print("\n\n")
    # second_round_input = input("Dice are {} . . .\n Input a ones value (2-6) for your dice you want to keep \nor enter 5 comma separated dice as if that was your second roll".format(dice).strip())
    # print("\n\n")
    # if len(second_round_input) == 1:
    #     chosen_ones_value = int(second_round_input)
    #     partial_roll = get_kept_partial_roll(dice, chosen_ones_value)
    #     dice = partial_roll + roll(MAX_NUM_DICE - len(partial_roll))
    # else:
    #     dice = [int(x) for x in second_round_input.strip().split(",")]
    #
    #     best_ones_target_r2, summaries_r2 = get_ones_target_for_best_score_in_num_rounds(0, dice)
    #     win_ratio_r2 = get_win_ratio(2, summaries_r2, best_ones_target_r2)




    # turn_stats = get_stats(simulated_next_rolls, current_count_and_number)
    # print("Results are {} \n\n".format(turn_stats))

main()
