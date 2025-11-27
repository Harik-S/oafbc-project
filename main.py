# oxford alpha fund quant boot camp project
# game: suppose there are m teams, n rounds, in each round, each team gets a card and there is one card revealed in the middle
# optimal traders will calculate the EV based on available information to them. then they will trade based on the bid and offer provided by the market maker
# insider traders will have information from the next round in advance
# other traders will behave in a way that is as of now not determined
# POSSIBLE IMPROVEMENT: current idea is for market maker to offer a market with a set spread s = 0.2 around their EV. each trader takes k turns at mm so that n=km. open to other suggestions

import random

global_vars = {
    "n_cards_init": 0,
    "middle_cards": [],
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
                "hand": [[]] * n_optimal,
                "EV_next": 0,
            },
            "insider": {
                "hand": [[]] * n_insider,
                "EV_next": 0,
            },
            "sub_optimal": {
                "hand": [[]] * n_sub_optimal,
                "EV_next": 0,
            },
        },
    )


def update_player_EV(player):
    n_cards_unknown = (
        global_vars["n_cards_init"]
        - len(player["hand"])
        - len(global_vars["middle_cards"])
    )
    player["EV"] = (
        (n_cards_unknown + 1) * player["EV"] - player["hand"][-1]
    ) / n_cards_unknown


def get_score_vector(n_card_decks):
    scores = [
        (i % 13 + 1) if (i % 13) < 10 else 20
        for i in range(52)
        for _ in range(n_card_decks)
    ]

    for i in range(n_card_decks):
        scores[i * 52] = scores[i * 52 + 13] = -50
        scores[i * 52 + 26] = scores[i * 52 + 39] = 0

    return scores


def draw_one_card(score_vector):
    return score_vector.pop(random.randint(0, len(score_vector) - 1))


def draw_cards_for_players(player_cards, score_vector):
    for player_type in player_cards:
        for player in player_cards[player_type]:
            player["hand"].append(draw_one_card(score_vector))

            if player_type in {"optimal", "insider"}:
                update_player_EV(player)


def draw_middle_card(score_vector, player_cards):
    global_vars["middle_cards"].append(draw_one_card(score_vector))

    for player_type in player_cards:
        if player_type == "sub_optimal":
            continue

        for player in player_cards[player_type]:
            update_player_EV(player)


def play_round(score_vector, positions, cash, player_cards):
    draw_cards_for_players(player_cards, score_vector)

    # TODO: implement game playing logic

    draw_middle_card(score_vector, player_cards)


def play_game(n_card_decks, n_rounds, n_optimal, n_insider, n_sub_optimal):
    score_vector = get_score_vector(n_card_decks)
    total_score = sum(score_vector)

    positions, cash, player_cards = setup_game_tracker_dicts(
        n_optimal, n_insider, n_sub_optimal
    )
    for player_type in player_cards:
        if player_type == "sub_optimal":
            continue

        for player in player_cards[player_type]:
            player["EV_next"] = total_score / (n_card_decks * 52)

    for _ in range(n_rounds):
        play_round(score_vector, positions, cash, player_cards)


if __name__ == "__main__":
    n_card_decks, n_rounds = 3, 5
    n_optimal, n_insider, n_sub_optimal = 5, 5, 0

    global_vars["n_cards_init"] = n_card_decks * 52

    play_game(n_card_decks, n_rounds, n_optimal, n_insider, n_sub_optimal)
