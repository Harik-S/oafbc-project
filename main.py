import random

global_vars = {
    "n_cards_init": 0,
    "middle_cards": [],
    "user_position": 0,
    "user_cash": 0,
    "middle_cards_EV": 0,  # EV of the 5 middle cards to be drawn
}


def setup_game_tracker_dicts(n_optimal, n_insider, n_sub_optimal):
    return (
        # POSITIONS DICT
        {
            "optimal": [0] * n_optimal,
            "insider": [0] * n_insider,
            "sub_optimal": [0] * n_sub_optimal,
        },
        # CASH DICT
        {
            "optimal": [0] * n_optimal,
            "insider": [0] * n_insider,
            "sub_optimal": [0] * n_sub_optimal,
        },
        # PLAYER CARDS DICT
        {
            "optimal": {
                "hand": [[] for _ in range(n_optimal)],
                "EV_next": [0] * n_optimal,
            },
            "insider": {
                "hand": [[] for _ in range(n_insider)],
                "EV_next": [0] * n_insider,
            },
            "sub_optimal": {
                "hand": [[] for _ in range(n_sub_optimal)],
                "EV_next": [0] * n_sub_optimal,
            },
        },
    )


def update_middle_cards_EV(new_card_val, player_cards=None):
    """Update the expected value of the remaining middle cards for each player based on their visible cards"""
    n_middle_cards_remaining = 5 - len(global_vars["middle_cards"])
    
    if n_middle_cards_remaining <= 0:
        # When all 5 cards are revealed, EV is the actual sum for everyone
        actual_sum = sum(global_vars["middle_cards"])
        if player_cards:
            for player_type in player_cards:
                for i in range(len(player_cards[player_type]["EV_next"])):
                    player_cards[player_type]["EV_next"][i] = actual_sum
        global_vars["middle_cards_EV"] = actual_sum
        return
    
    if not player_cards:
        return
    
    # Update EV for each player based on cards they can see
    for player_type in player_cards:
        for i in range(len(player_cards[player_type]["EV_next"])):
            # Calculate cards this player can see
            cards_seen_by_player = len(global_vars["middle_cards"])
            
            # Add cards from this player's hand
            cards_seen_by_player += len(player_cards[player_type]["hand"][i])
            
            # For optimal and insider players, they can also see other players' cards
            if player_type in {"optimal", "insider"}:
                for other_type in player_cards:
                    for j, hand in enumerate(player_cards[other_type]["hand"]):
                        if other_type != player_type or j != i:  # Don't double count own hand
                            cards_seen_by_player += len(hand)
            
            n_cards_unknown_to_player = global_vars["n_cards_init"] - cards_seen_by_player
            
            # Update this player's EV
            if n_cards_unknown_to_player > 0:
                player_cards[player_type]["EV_next"][i] = (
                    (n_cards_unknown_to_player + 1) * player_cards[player_type]["EV_next"][i] - new_card_val
                ) / n_cards_unknown_to_player
    
    # Update global middle cards EV (can be average of optimal players or use total cards seen)
    total_cards_seen = len(global_vars["middle_cards"])
    for player_type in player_cards:
        for hand in player_cards[player_type]["hand"]:
            total_cards_seen += len(hand)
    
    n_cards_unknown = global_vars["n_cards_init"] - total_cards_seen
    if n_cards_unknown > 0:
        global_vars["middle_cards_EV"] = (
            (n_cards_unknown + 1) * global_vars["middle_cards_EV"] - new_card_val
        ) / n_cards_unknown


def get_score_vector(n_card_decks):
    scores = [
        (i % 13 + 1) if (i % 13) < 10 else 20
        for _ in range(n_card_decks)
        for i in range(52)
    ]

    for i in range(n_card_decks):
        scores[i * 52] = scores[i * 52 + 13] = -50
        scores[i * 52 + 26] = scores[i * 52 + 39] = 0

    return scores


def draw_one_card(score_vector):
    return score_vector.pop(random.randint(0, len(score_vector) - 1))


def draw_cards_for_players(player_cards, score_vector):
    for player_type in player_cards:
        for i in range(len(player_cards[player_type]["hand"])):
            player_cards[player_type]["hand"][i].append(draw_one_card(score_vector))

            if player_type in {"optimal", "insider"}:
                update_middle_cards_EV(
                    player_cards[player_type]["hand"][i][-1], player_cards
                )


def draw_middle_card(score_vector, player_cards):
    global_vars["middle_cards"].append(draw_one_card(score_vector))

    # Update middle cards EV once after drawing the middle card
    update_middle_cards_EV(global_vars["middle_cards"][-1], player_cards)


def get_user_round_decision():
    print("=" * 53)
    print(f"{'=' * 20} PLAYER MOVE {'=' * 20}")
    print("=" * 53, "\n")

    bid = int(input(f"Enter your bid: "))
    ask = int(input(f"Enter your ask: "))

    print("=" * 53)
    print(f"{'=' * 18} PLAYER MOVE END {'=' * 18}")
    print("=" * 53, "\n")

    return bid, ask


def make_player_sell(player_type, player_idx, positions, cash, bid):
    positions[player_type][player_idx] -= 1
    cash[player_type][player_idx] += bid

    global_vars["user_position"] += 1
    global_vars["user_cash"] -= bid


def make_player_buy(player_type, player_idx, positions, cash, ask):
    positions[player_type][player_idx] += 1
    cash[player_type][player_idx] -= ask

    global_vars["user_position"] -= 1
    global_vars["user_cash"] += ask


def simulate_taker_moves(player_cards, positions, cash, user_bid, user_ask):
    for player_type in player_cards:
        for i in range(len(player_cards[player_type]["hand"])):
            if player_cards[player_type]["EV_next"][i] < user_bid:
                # BOT SELLS
                make_player_sell(player_type, i, positions, cash, user_bid)

            if player_cards[player_type]["EV_next"][i] > user_ask:
                # BOT BUYS
                make_player_buy(player_type, i, positions, cash, user_ask)


def play_round(score_vector, positions, cash, player_cards):
    draw_cards_for_players(player_cards, score_vector)
    draw_middle_card(score_vector, player_cards)

    print(
        f"\n\nMiddle scores:\n\n== {' == '.join(map(str, global_vars['middle_cards']))} ==\n\n"
    )

    bid, ask = get_user_round_decision()

    simulate_taker_moves(player_cards, positions, cash, bid, ask)
    print(f"Turn completed. Middle cards: {global_vars['middle_cards']}")
    print(f"Expected value of remaining middle cards: {global_vars['middle_cards_EV']:.2f}")
    print(player_cards)


def play_game(n_card_decks, n_rounds, n_optimal, n_insider, n_sub_optimal):
    score_vector = get_score_vector(n_card_decks)
    total_score = sum(score_vector)

    positions, cash, player_cards = setup_game_tracker_dicts(
        n_optimal, n_insider, n_sub_optimal
    )
    # Initialize middle cards EV to average card value
    global_vars["middle_cards_EV"] = total_score / (n_card_decks * 52) * 5  # EV for 5 middle cards
    
    for player_type in player_cards:
        if player_type == "sub_optimal":
            continue

        for i in range(len(player_cards[player_type]["EV_next"])):
            player_cards[player_type]["EV_next"][i] = total_score / (n_card_decks * 52)

    for _ in range(n_rounds):
        play_round(score_vector, positions, cash, player_cards)


if __name__ == "__main__":
    n_card_decks, n_rounds = 1, 2
    n_optimal, n_insider, n_sub_optimal = 5, 5, 0

    global_vars["n_cards_init"] = n_card_decks * 52

    play_game(n_card_decks, n_rounds, n_optimal, n_insider, n_sub_optimal)
