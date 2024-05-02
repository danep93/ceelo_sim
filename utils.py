import ast
import random
from constants import SCORES, MAX_ROLLS
from statistics import mean


def get_counts(dice):
    counts = {}
    for d in dice:
        counts[d] = counts.get(d,0) + 1
    return counts;


# returns array of dice that will not be rerolled based off ones_target
def get_kept_partial_roll(dice, ones_target):
    counts = get_counts(dice)
    return [ones_target] * (counts.get(ones_target,0) + counts.get(1,0))


# generates randomly rolled dice
def roll(num_dice=5):
    return [random.randint(1, 6) for i in range(0, num_dice)]


# returns (x,y,z) summary: (X dice with value Z, Y dice with value 1 (wild), Z)
def summarize_roll(dice, ones_target):
    if ones_target < 0:
        return (0,0)
    counts = get_counts(dice)
    return counts.get(ones_target,0) + counts.get(1,0), ones_target


# avg score over many simulated rolls
def mean_score(summaries):
    scores = [SCORES.get(x,0) for x in summaries if x != (0,0)]
    return mean(scores)


# compare two scores
def compare_summaries(first,second):
    return 1 if SCORES.get(first,0) > SCORES.get(second,0) else -1 if SCORES.get(first,0) < SCORES.get(second,0) else 0


def describe_score(score, ones_target, stop_round):
    # get score of (1,ones_target)
    # keep adding 5 to score until it is greater than score
    comp_score = SCORES.get((1,ones_target),0)
    ones_target_count = 1
    while score >= comp_score:
        if score == comp_score:
            return "best average score (in round {}) is ({},{}) = {} ".format(stop_round, ones_target_count,ones_target,
                                                               SCORES.get((ones_target_count,ones_target),0)
                                                               )
        ones_target_count += 1
        comp_score = SCORES.get((ones_target_count,ones_target),0)
    return "average score (in round {}) between ({},{}) and ({},{}) OR {} and {}".format(
        stop_round,
        ones_target_count-1,ones_target,ones_target_count,ones_target,
        SCORES.get((ones_target_count-1,ones_target),0),SCORES.get((ones_target_count,ones_target),0))


def find_optimal_path(paths, start_roll):
    best_win_ratio, best_ones_target, best_round_idx, best_score, best_percentile = -1, -1, -1, -1, -1
    for path in paths:
        for wr in path['win_ratios']:
            if wr > best_win_ratio:
                best_win_ratio = wr
                best_ones_target = path['ones_target']
                best_round_idx = path['win_ratios'].index(wr)
                best_score = path['scores'][best_round_idx]
                best_percentile = path['percentiles'][best_round_idx]
    return {
        "ones_target": best_ones_target,
        "score_summary": describe_score(best_score, best_ones_target, best_round_idx + 1),
        "win_ratio": best_win_ratio,
        "stop_round": best_round_idx + 1,
        "best_score": best_score,
        "best_percentile": best_percentile
    }


def validate_params(request):
    dice = request.args.get('dice', '[]')
    ones_targets = request.args.get('ones_targets', '[]')
    # type checks
    try:
        dice = ast.literal_eval(dice)
        ones_targets = ast.literal_eval(ones_targets)
    except Exception as e:
        raise ValueError("Params are start_roll (int), ones_target (list), dice (list). Invalid input: {}".format(e))
    if len(dice) != 5 and len(dice) != 0:
        raise ValueError("dice must be either empty or have 5 elements")
    if len(ones_targets) > 6 or any([x < 1 or x > 6 for x in ones_targets]):
        raise ValueError("ones_targets must either be empty or have at most 6 valid dice elements")
    return dice, ones_targets