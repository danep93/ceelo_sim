from statistics import mean
from constants import MAX_ROLLS, MAX_NUM_DICE, NUM_SIMULATIONS, SCORES
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
    return [random.randint(1, 6) for i in range(0, num_dice)]


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


def _simulate_remaining_rolls(ones_target, dice, og_current_roll):
    # NOTE: runs num_simulations times
    next_roll_summaries = []

    for i in range(0, NUM_SIMULATIONS):
        current_roll = og_current_roll
        turn = []

        partial_roll = get_kept_partial_roll(dice, ones_target)

        while current_roll < MAX_ROLLS:
            new_partial_roll = roll(MAX_NUM_DICE - len(partial_roll))
            partial_roll += get_kept_partial_roll(new_partial_roll, ones_target)
            summary = summarize_roll(partial_roll, ones_target)
            turn.append(summary)
            current_roll += 1
        next_roll_summaries.append(turn)
    return next_roll_summaries


def get_best_ones_target_for_current_roll(dice):
    scores = {}
    for ones_target in dice:
        if ones_target == 1:
            continue
        scores[ones_target] = SCORES[summarize_roll(dice, ones_target)]
    max_key = 6
    try:
        max_key = max(scores, key=scores.get)
    except:
        # bp()
        print("exception in get best ones target, dice are ".format(dice))
    finally:
        return max_key


def get_probable_best_ones_targets(dice):
    # gets number with the highest concordance or highest value (at most 2)
    dice = [x for x in dice if x != 1]  # 1 cannot be a 1s target
    if len(dice) == 0:
        return [2, 3, 4, 5, 6]
    counts = get_counts(dice)
    max_count = max(counts.values())
    max_val = [key for key, value in counts.items() if value == max_count]
    return list(set([max(dice), max(max_val)]))


def simulate_remaining_rolls_for_probable_ones_targets(dice, curr_roll):
    probable_best_ones_targets = get_probable_best_ones_targets(dice)
    ones_target_simulated_rolls = {}
    for ones_target in probable_best_ones_targets:
        ones_target_simulated_rolls[ones_target] = _simulate_remaining_rolls(ones_target, dice, curr_roll)
    return ones_target_simulated_rolls

def get_round_simulated_summaries(ones_targets_to_simulated_rolls, ones_target, roll):
    round_simulated_rolls = {}
    # bp()
    for k,v in ones_targets_to_simulated_rolls.items():
        x_round_rolls = [x[roll-1] for x in v]
        round_simulated_rolls[k] = x_round_rolls
    return round_simulated_rolls[ones_target]


def get_best_ones_target_for_simulated_remaining_rolls(ones_targets_to_simulated_rolls, in_num_rolls):

    round_simulated_rolls = {}
    for k,v in ones_targets_to_simulated_rolls.items():
        x_round_rolls = [x[in_num_rolls-1] for x in v]
        round_simulated_rolls[k] = x_round_rolls
    round_simulated_scores = {k: mean_score(v) for k,v in round_simulated_rolls.items()}
    # print("scores are {}".format(round_simulated_scores))
    return max(round_simulated_scores, key=round_simulated_scores.get)

#todo:(daniel.epstein) get win ratio of 2nd best ones target for FP if there is one
def print_win_ratios(fp_dice, curr_roll):
    win_lose_ratios = {}
    for i in range(curr_roll,MAX_ROLLS+1):
        win_lose_ratios[i] = [0, 0]  # wins and losses


    #fp current and future rolls
    fp_ones_target_current_round = get_best_ones_target_for_current_roll(fp_dice)
    fp_ones_targets_to_rolls = simulate_remaining_rolls_for_probable_ones_targets(fp_dice, curr_roll)
    fp_current_roll_summary = summarize_roll(fp_dice, fp_ones_target_current_round)


    #make cpu competitors and compare to current and future first player rolls
    for i in range(0, NUM_SIMULATIONS):
        # CPU always starts from round 1, even if first player is comparing a 3rd round roll
        cpu_dice = roll(MAX_NUM_DICE)
        cpu_ones_targets_to_rolls = simulate_remaining_rolls_for_probable_ones_targets(cpu_dice, curr_roll=1)

        # -1 because we just did our first CPU roll above
        in_num_rolls = curr_roll - 1
        cpu_ones_target = get_best_ones_target_for_simulated_remaining_rolls(cpu_ones_targets_to_rolls, in_num_rolls)

        # bp()
        cpu_round_summaries = get_round_simulated_summaries(cpu_ones_targets_to_rolls, cpu_ones_target, in_num_rolls)
        for i in range(0, len(cpu_round_summaries)):
            first_result = compare_summaries(fp_current_roll_summary, cpu_round_summaries[i])
            wl_ratio = win_lose_ratios[curr_roll]
            if first_result > 0:
                wl_ratio[0] += 1
            elif first_result < 0:
                wl_ratio[1] += 1
            win_lose_ratios[curr_roll] = wl_ratio

    # win lose stats for remaining rounds (if applicable)
        j = curr_roll + 1
        in_num_rolls += 1
        while j <= MAX_ROLLS:

            cpu_ones_target_future_roll = get_best_ones_target_for_simulated_remaining_rolls(cpu_ones_targets_to_rolls, in_num_rolls)
            # bp()
            cpu_round_summaries = get_round_simulated_summaries(cpu_ones_targets_to_rolls, cpu_ones_target_future_roll, j-1)

            fp_ones_target_future_roll = get_best_ones_target_for_simulated_remaining_rolls(fp_ones_targets_to_rolls, in_num_rolls)
            fp_round_summaries = get_round_simulated_summaries(fp_ones_targets_to_rolls, fp_ones_target_future_roll, j-1)

            for i in range(0, len(fp_round_summaries)):
                wl_ratio = win_lose_ratios[j]
                round_result = compare_summaries(fp_round_summaries[i], cpu_round_summaries[i])
                if round_result > 0:
                    wl_ratio[0] += 1
                elif round_result < 0:
                    wl_ratio[1] += 1
                win_lose_ratios[j] = wl_ratio
            j += 1
            in_num_rolls += 1

    print("win lose ratio is {}".format(win_lose_ratios))
    for k, v in win_lose_ratios.items():
        #todo:(daniel.epstein) print the avg summary/score at each round
        if v[1] == 0:
            percentile = 1.00
            ratio = NUM_SIMULATIONS
        else:
            percentile = round(v[0] / (v[0] + v[1]), 2) * 100
            ratio = round(v[0] / v[1], 2)
        print("In round {} your dice are in the {} percentile with a win-lose ratio of {}".format(k, percentile, ratio))






# 1) prove why its better to go first
dice = [1,2,2,2,2]
curr_roll = 1
final_roll = 3
simulated_rolls = simulate_remaining_rolls_for_probable_ones_targets(dice, curr_roll)

print("dice are {} in round {}".format(dice, curr_roll))
print("best ones target in round {} is {}".format(final_roll,
    get_best_ones_target_for_simulated_remaining_rolls(simulated_rolls, in_num_rolls=final_roll - curr_roll)))
# print(simulated_rolls)
print_win_ratios(dice, curr_roll)


# proves when you should use more of lesser number vs less of higher number for 1, 2, and 3 rounds
# dice = [1,2,2,5,6]
# simulated_rolls = simulate_remaining_rolls_for_probable_ones_targets(dice, current_roll=1, end_roll=3)
# print(get_best_ones_target_for_simulated_remaining_rolls(simulated_rolls, 2))


# prove assumption that 3 4s wins about half the time and that goes down in later rounds
# talk about percentiles and win ratios and what that means relative to how many people you play with

# two questions to answer. Why is it better to go first? When should I choose less of something vs more of something else
# prove why it is an advantage to go first. You can quit when you have the best projected win percentage.
# show how that is 1st round with 4 sixes. But if you need to beat (5,5,3) then you must keep rolling, decreasing your relative advantage

# todo list
#todo:(daniel.epstein): fix next/current roll debacle so we can get win ratio of a roll in a certain round.
#todo:(daniel.epstein) i suspect when you enter a roll in X round you're competing against cpu at 1st round. FIX THIS

#todo:(daniel.epstein) print avg score (and what it translates to) in print_ratios. Also do this for 2nd best scores
#todo:(daniel.epstein) factor in ones where you hit 5 of something before 3rd round


# todo list DONE
#todo:(daniel.epstein) show that 5,5,3 has a lower win-lose ratio and is in a lower percentile than 4,6,1
