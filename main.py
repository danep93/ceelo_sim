from statistics import mean
from constants import draw_die, MAX_ROLLS, MAX_NUM_DICE, NUM_SIMULATIONS, SCORES
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
    scores = [SCORES.get(x,0) for x in summaries if x != (0,0)]
    return mean(scores)


def compare_summaries(first,second):
    return 1 if SCORES[first] > SCORES[second] else -1 if SCORES[first] < SCORES[second] else 0


def summary_to_partial_roll(summary):
    return [summary[1]] * summary[0]


def round_score_to_summary(score):
    summary = "(0,0)"
    rounded_score = round(score)
    for k,v in SCORES.items():
        if rounded_score == v:
            summary = str(k)
    if rounded_score < score:
        summary = "rounded down " + summary
    elif rounded_score > score:
        summary = "rounded up " + summary
    return summary


def _simulate_all_rolls(ones_target, dice, starting_roll):
    # NOTE: runs num_simulations times
    next_roll_summaries = []

    for i in range(0, NUM_SIMULATIONS):
        curr = 1
        turn = []

        partial_roll = get_kept_partial_roll(dice, ones_target)

        while curr <= MAX_ROLLS:
            if curr < starting_roll:
                summary = (0,0)
            elif curr == starting_roll:
                summary = summarize_roll(dice, ones_target)
            else:
                new_partial_roll = roll(MAX_NUM_DICE - len(partial_roll))
                partial_roll += get_kept_partial_roll(new_partial_roll, ones_target)
                summary = summarize_roll(partial_roll, ones_target)
            turn.append(summary)
            curr += 1
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
        bp()
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
        ones_target_simulated_rolls[ones_target] = _simulate_all_rolls(ones_target, dice, curr_roll)
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


def print_win_ratios(fp_dice, curr_roll):
    og_curr_roll = curr_roll
    win_lose_ratios = {}
    win_lose_ones_targets = {}
    cpu_avg_scores = {}
    fp_avg_scores = {}
    for i in range(curr_roll,MAX_ROLLS+1):
        win_lose_ratios[i] = [0, 0]  # wins and losses
        win_lose_ones_targets[i] = 0
        cpu_avg_scores[i] = []
        fp_avg_scores[i] = []

    # fp current and future rolls
    fp_ones_targets_to_rolls = simulate_remaining_rolls_for_probable_ones_targets(fp_dice, curr_roll)

    # make cpu competitors and compare to current and future first player rolls
    for i in range(0, NUM_SIMULATIONS):
        curr_roll = og_curr_roll
        # CPU always starts from round 1, even if first player is comparing a 3rd round roll
        cpu_dice = roll(MAX_NUM_DICE)
        cpu_ones_targets_to_rolls = simulate_remaining_rolls_for_probable_ones_targets(cpu_dice, curr_roll=1)
        while curr_roll <= MAX_ROLLS:
            fp_ones_target_future_roll = get_best_ones_target_for_simulated_remaining_rolls(fp_ones_targets_to_rolls,
                                                                                            curr_roll)
            fp_round_summaries = get_round_simulated_summaries(fp_ones_targets_to_rolls, fp_ones_target_future_roll,
                                                               curr_roll)

            cpu_ones_target = get_best_ones_target_for_simulated_remaining_rolls(cpu_ones_targets_to_rolls, curr_roll)
            cpu_round_summaries = get_round_simulated_summaries(cpu_ones_targets_to_rolls, cpu_ones_target, curr_roll)
            for j in range(0, len(fp_round_summaries)):
                result = compare_summaries(fp_round_summaries[j], cpu_round_summaries[j])
                if result > 0:
                    win_lose_ratios[curr_roll][0] += 1  # win
                elif result < 0:
                    win_lose_ratios[curr_roll][1] += 1  # loss
            win_lose_ones_targets[curr_roll] = fp_ones_target_future_roll
            cpu_avg_scores[curr_roll] = cpu_avg_scores[curr_roll] + cpu_round_summaries
            fp_avg_scores[curr_roll] = fp_avg_scores[curr_roll] + fp_round_summaries
            curr_roll += 1

    print("Computer competitor (CPU) scores per round -- mostly static --")
    for k, v in cpu_avg_scores.items():
        cpu_avg_score = round(mean_score(cpu_avg_scores[k]), 2)
        cpu_rounded_score = round_score_to_summary(cpu_avg_score)
        print("Round: {} . . . CPU_avg_score: {} or {}".format(k, cpu_avg_score, cpu_rounded_score))
    print("\n")

    print('\n'.join(map('  '.join, zip(*[draw_die(i) for i in fp_dice]))))
    print("dice are {} in round {}".format(fp_dice, og_curr_roll))
    print("First Player (FP) scores per round -- highly dependent on your initial dice --")
    for k, v in win_lose_ratios.items():
        if v[1] == 0:
            percentile = 100
            ratio = NUM_SIMULATIONS ** 2
        else:
            percentile = round(v[0] / (v[0] + v[1]), 2) * 100
            ratio = round(v[0] / v[1], 2)

        fp_avg_score = round(mean_score(fp_avg_scores[k]), 2)
        fp_rounded_score = round_score_to_summary(fp_avg_score)
        ones_target = win_lose_ones_targets[k]
        print("Round: {} ... \t 1s_target: {} ... \t FP_avg_score: {} or {} ... \t Percentile: {} ... \t Win-lose-ratio: {}".format(
            k, ones_target, format(fp_avg_score, '.2f'), fp_rounded_score, format(percentile, '.0f'),
            format(ratio, '.2f')).expandtabs(25))





# When should you take the higher-concordance-lower-value dice over the lower-concordance-higher-value dice?
dice = [4,4,1,5,6]
curr_roll = 1
print_win_ratios(dice, curr_roll)
