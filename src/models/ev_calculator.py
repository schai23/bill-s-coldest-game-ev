def american_odds_to_prob(odds: int) -> float:
    """
    Convert American sportsbook odds to Implied Probability. (-200,-101, +101, +200)
    Returns a value between 0 to 1
    """
    if odds > 0:
        return 100 / (odds + 100)
    else:
        return -odds / (-odds + 100)
    
def expected_value(true_prob: float, odds: int, stake: float = 1.0) -> float:
    """
    Compute the EV of a bet with a given true probability and American sportsbook odds,
    for a given stake (default $1).

    EV = p * profit - (1 - p) * stake
    """
    if odds > 0:
        profit_if_win = stake * (odds / 100)
    else:
        profit_if_win = stake * (100 / -odds)

    return true_prob * profit_if_win - (1 - true_prob) * stake

if __name__ == "__main__":
    # Demo for +150 odds
    example_odds = 150
    break_even = american_odds_to_prob(example_odds)
    print(f"Break-even probability for +{example_odds} is {break_even:.3f}")

    # Demo pretending the model thinks +150 is true probability of 0.45 
    model_prob = 0.45
    ev = expected_value(model_prob, example_odds, stake=1.0)
    print(f"EV for +{example_odds} with true p={model_prob:.2f} is ${ev:.3f}")
