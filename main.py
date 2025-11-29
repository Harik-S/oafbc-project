import random

global_vars = {
    "n_cards_init": 0,
    "middle_cards": [],
    "middle_cards_EV": 0,  # EV of the 5 middle cards to be drawn
}


def setup_game_tracker_dicts(n_optimal, n_insider, n_sub_optimal):
    return (
        {
            "optimal": [0] * n_optimal,
            "insider": [0] * n_insider,
            "sub_optimal": [0] * n_sub_optimal,
        },
        {
            "optimal": [0] * n_optimal,
            "insider": [0] * n_insider,
            "sub_optimal": [0] * n_sub_optimal,
        },
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
    """Update the expected value of the remaining middle cards after revealing a new card"""
    n_middle_cards_remaining = 5 - len(global_vars["middle_cards"])
    
    if n_middle_cards_remaining <= 0:
        # When all 5 cards are revealed, EV is the actual sum of the 5 middle cards
        global_vars["middle_cards_EV"] = sum(global_vars["middle_cards"])
        return
    
    # Calculate total cards seen (middle cards + all player cards)
    total_cards_seen = len(global_vars["middle_cards"])
    
    # Count cards in all players' hands if player_cards is provided
    if player_cards:
        for player_type in player_cards:
            for hand in player_cards[player_type]["hand"]:
                total_cards_seen += len(hand)
    
    n_cards_unknown = global_vars["n_cards_init"] - total_cards_seen
    
    # Update EV by removing the revealed card's contribution
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


def play_round(score_vector, positions, cash, player_cards):
    draw_cards_for_players(player_cards, score_vector)

    # TODO: implement game playing logic

    draw_middle_card(score_vector, player_cards)

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
    n_card_decks, n_rounds = 2, 5
    n_optimal, n_insider, n_sub_optimal = 5, 5, 0

    global_vars["n_cards_init"] = n_card_decks * 52

    play_game(n_card_decks, n_rounds, n_optimal, n_insider, n_sub_optimal)
