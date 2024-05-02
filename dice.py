from constants import draw_die, MAX_ROLLS, MAX_NUM_DICE, NUM_SIMULATIONS
from utils import roll, get_kept_partial_roll, get_counts, mean_score, compare_summaries, summarize_roll


# Get the best ones target for a CPU given first player ones target that is the floor
def get_cpu_ones_target(dice: list[int], min_ones_target: int) -> int:
    # filter out everything below min_ones_target
    dice = [x for x in dice if x >= min_ones_target or x == 1]
    # if there are only 1s left, choose to make them 6
    if not dice:
        return -1 # reroll everything, still don't need to pick 1s target this round
    elif all([d == 1 for d in dice]):
        return 6
    else:
        # find 1s target with highest concordance and highest number.
        dice = [x for x in dice if x != 1]
        counts = get_counts(dice)
        max_concord_value = max(counts, key=lambda x: (counts[x], x))
        return max_concord_value


# Uses 1s target strategy of the highest concordance above min_ones_target, tie going to highest number
# 1s target might not be set after first (or second) roll if all rolled dice are below min 1s target, reroll all of them
def simulate_all_cpu_rolls(min_ones_target):
    # NOTE: runs num_simulations times
    next_roll_summaries = []
    for num_sim in range(0, NUM_SIMULATIONS):
        # first turn
        dice = roll()
        curr_roll = 1
        ones_target = get_cpu_ones_target(dice, min_ones_target)  # could be -1 if no dice are above min 1s target
        turn = [summarize_roll(dice, ones_target)]
        partial_roll = get_kept_partial_roll(dice, ones_target)

        # rest of turns
        while curr_roll < MAX_ROLLS:
            new_partial_roll = roll(MAX_NUM_DICE - len(partial_roll))
            # in case you are in a later round still without a 1s target due to all dice being below min 1s target
            if ones_target < 0:
                ones_target = get_cpu_ones_target(new_partial_roll, min_ones_target)
            partial_roll = get_kept_partial_roll(partial_roll + new_partial_roll, ones_target)
            turn.append(summarize_roll(partial_roll, ones_target))
            curr_roll += 1

        next_roll_summaries.append(turn)
    return next_roll_summaries


# Simulate remaining rounds with a specified ones target
def _simulate_all_remaining_rolls(ones_target, dice, starting_roll_number, include_current_roll=False):
    # NOTE: runs num_simulations times
    next_roll_summaries = []

    for num_sim in range(0, NUM_SIMULATIONS):
        curr_roll = starting_roll_number
        turn = [summarize_roll(dice, ones_target)] if include_current_roll else []

        partial_roll = get_kept_partial_roll(dice, ones_target)

        while curr_roll < MAX_ROLLS:
            new_partial_roll = roll(MAX_NUM_DICE - len(partial_roll))
            partial_roll += get_kept_partial_roll(new_partial_roll, ones_target)
            turn.append(summarize_roll(partial_roll, ones_target))
            curr_roll += 1

        next_roll_summaries.append(turn)
    return next_roll_summaries


# gets number with the highest concordance and highest number. Most always a decision between 2 options
def get_probable_best_ones_targets(dice: list[int]) -> list[int]:
    dice = [x for x in dice if x != 1]  # 1 cannot be a 1s target
    if len(dice) == 0:
        return [6]  # turn all wilds into 6s for best possible roll
    counts = get_counts(dice)
    max_concord_value = max(counts, key=lambda x: (counts[x], x))
    best_ones_targets = list(set([max(dice), max_concord_value]))
    return best_ones_targets


# Simulate remaining rounds with either a list of specified ones targets or the ones most likely to succeed
def simulate_remaining_rolls_for_probable_ones_targets(dice, curr_roll_number, ones_targets=[], include_current_roll=False):
    if not ones_targets:
        ones_targets = get_probable_best_ones_targets(dice)
    ones_target_simulated_rolls = {}
    for ones_target in ones_targets:
        ones_target_simulated_rolls[ones_target] = _simulate_all_remaining_rolls(
            ones_target, dice, curr_roll_number, include_current_roll)
    return ones_target_simulated_rolls


# Get win ratios, percentiles, and scores for each round
def get_performance_stats(fp_rolls, cpu_rolls):
    # how many rounds are there
    num_rounds = len(fp_rolls[0])  # how many rounds between starting and end roll
    win_ratios = []
    scores = []
    percentiles = []

    # Separate out the rolls for each round
    for round_num in range(0, num_rounds):
        wins = 0
        losses = 0
        fp_round_rolls = [x[round_num] for x in fp_rolls]
        cpu_round_rolls = [x[round_num] for x in cpu_rolls]
        print("hey")
        for sim_number in range(0, len(fp_round_rolls)):
            result = compare_summaries(fp_round_rolls[sim_number], cpu_round_rolls[sim_number])
            if result > 0:
                wins += 1
            elif result < 0:
                losses += 1

        # store win ratios
        win_ratio = (wins / losses) if losses != 0 else 100
        win_ratios.append(round(win_ratio, 2))
        # store percentiles
        percentiles.append(round((100 * wins) / (wins + losses), 2))
        # store scores
        scores.append(round(mean_score(fp_round_rolls), 2))
    return {"win_ratios": win_ratios, "scores": scores, "percentiles": percentiles}


def simulate_competition(dice, curr_roll, ones_targets):
    # Do param validation
    # Get dice
    results = []

    # If they passed in dice but not a ones target, get best ones
    if dice and not ones_targets:
        ones_targets = get_probable_best_ones_targets(dice)
        
    for fp_ones_target in ones_targets:
        # Get simulated rolls for each possible ones target
        fp_ones_targets_to_rolls = simulate_remaining_rolls_for_probable_ones_targets(
            dice=dice,
            curr_roll_number=curr_roll,
            ones_targets=[fp_ones_target],
            include_current_roll=True
        )
        cpu = simulate_all_cpu_rolls(min_ones_target=fp_ones_target)

        # CPU might not have the same 1s targets.

        perf_stats = get_performance_stats(fp_rolls=fp_ones_targets_to_rolls[fp_ones_target], cpu_rolls=cpu)
        path = {**{"ones_target": fp_ones_target}, **perf_stats}
        results.append(path)
    return results
