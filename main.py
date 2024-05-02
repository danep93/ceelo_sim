from dice import get_probable_best_ones_targets, simulate_competition
from utils import find_optimal_path, roll, validate_params
from flask import Flask, jsonify, request


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.json.sort_keys = False


def format_results(results, dice, start_roll, ones_target):
    # find best win ratio for optimal path
    formatted_results = {
        "starting_dice": dice,
        "start_roll": start_roll,
        "ones_targets": ones_target,
        "optimal_path": find_optimal_path(results, start_roll),
        "paths": results,
    }
    return formatted_results


def get_results(dice, curr_roll, ones_targets):
    results = simulate_competition(dice, curr_roll, ones_targets)
    return format_results(results, dice, curr_roll, ones_targets)


@app.route('/roll', methods=['GET'])
def compute():
    dice, ones_targets = validate_params(request)
    curr_roll = 1
    if not dice:
        dice = roll()
    if not ones_targets:
        ones_targets = get_probable_best_ones_targets(dice)

    results = get_results(dice, curr_roll, ones_targets)
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5001)




