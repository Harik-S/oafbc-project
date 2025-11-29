import random

global_vars = {
    "n_cards_init": 0,
    "middle_cards": [],
    "user_position": 0,
    "user_cash": 0,
    "n_rounds": 0,
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
                "EV_middle": [0] * n_optimal,
            },
            "insider": {
                "hand": [[] for _ in range(n_insider)],
                "EV_middle": [0] * n_insider,
            },
            "sub_optimal": {
                "hand": [[] for _ in range(n_sub_optimal)],
                "EV_middle": [0] * n_sub_optimal,
            },
        },
    )


def update_player_EV(player_type_dict, idx_player, new_card_val):
    n_cards_unknown = (
        global_vars["n_cards_init"]
        - len(player_type_dict["hand"][idx_player])
        - len(global_vars["middle_cards"])
    )
    player_type_dict["EV_middle"][idx_player] = (
        (
            (n_cards_unknown + 1) * player_type_dict["EV_middle"][idx_player]
            - new_card_val
        )
        / n_cards_unknown
    ) * (global_vars["n_rounds"] - len(global_vars["middle_cards"])) + sum(
        global_vars["middle_cards"]
    )


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
                update_player_EV(
                    player_cards[player_type],
                    i,
                    player_cards[player_type]["hand"][i][-1],
                )


def draw_middle_card(score_vector, player_cards):
    global_vars["middle_cards"].append(draw_one_card(score_vector))

    for player_type in player_cards:
        if player_type == "sub_optimal":
            continue

        for i in range(len(player_cards[player_type]["hand"])):
            update_player_EV(
                player_cards[player_type], i, global_vars["middle_cards"][-1]
            )


def get_user_round_decision():
    print("=" * 53)
    print(f"{"=" * 20} PLAYER MOVE {"=" * 20}")
    print("=" * 53, "\n")

    bid = int(input(f"Enter your bid: "))
    ask = int(input(f"Enter your ask: "))

    print("=" * 53)
    print(f"{"=" * 18} PLAYER MOVE END {"=" * 18}")
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
    n_user_buys, n_user_sells = 0, 0
    net_cash = 0

    for player_type in player_cards:
        for i in range(len(player_cards[player_type]["hand"])):
            if player_cards[player_type]["EV_middle"][i] < user_bid:
                # BOT SELLS
                make_player_sell(player_type, i, positions, cash, user_bid)
                n_users_buys += 1
                net_cash -= user_bid

            if player_cards[player_type]["EV_middle"][i] > user_ask:
                # BOT BUYS
                make_player_buy(player_type, i, positions, cash, user_ask)
                n_user_sells += 1
                net_cash += user_ask

    print("ROUND STATS:")
    print(
        f"Bought: {n_user_buys} @ {user_bid}\nSold: {n_user_sells} @ {user_ask}\nNet cash: {net_cash}"
    )


def play_round(score_vector, positions, cash, player_cards):
    draw_cards_for_players(player_cards, score_vector)

    print(
        f"\n\nMiddle scores:\n\n== {" == ".join(map(str, global_vars["middle_cards"]))} ==\n\n"
    )

    bid, ask = get_user_round_decision()
    simulate_taker_moves(player_cards, positions, cash, bid, ask)

    draw_middle_card(score_vector, player_cards)


def print_final_results():
    print(
        f"\n\nFinal middle scores:\n\n== {" == ".join(map(str, global_vars["middle_cards"]))} ==\n\n"
    )

    print(f"Final user position: {global_vars["user_position"]}")
    print(f"Final user cash: {global_vars["user_cash"]}")

    print(
        f"Net profit: {global_vars["user_position"] * sum(global_vars["middle_cards"]) + global_vars["user_cash"]}"
    )


def play_game(n_card_decks, n_rounds, n_optimal, n_insider, n_sub_optimal):
    score_vector = get_score_vector(n_card_decks)
    total_score = sum(score_vector)

    positions, cash, player_cards = setup_game_tracker_dicts(
        n_optimal, n_insider, n_sub_optimal
    )
    for player_type in player_cards:
        if player_type == "sub_optimal":
            continue

        for i in range(len(player_cards[player_type]["EV_middle"])):
            player_cards[player_type]["EV_middle"][i] = total_score / (
                n_card_decks * 52
            )

    for _ in range(n_rounds):
        play_round(score_vector, positions, cash, player_cards)

    print_final_results()


if __name__ == "__main__":
    n_card_decks, n_rounds = 1, 2
    n_optimal, n_insider, n_sub_optimal = 5, 5, 0

    global_vars["n_cards_init"] = n_card_decks * 52
    global_vars["n_rounds"] = n_rounds

    play_game(n_card_decks, n_rounds, n_optimal, n_insider, n_sub_optimal)
