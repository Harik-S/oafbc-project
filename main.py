import random

from constants import global_vars
from EV_funcs import *


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


def get_score_vector(n_card_decks):
    scores = [
        (i % 13 + 1) if (i % 13) < 10 else 20
        for _ in range(n_card_decks)
        for i in range(52)
    ]

    for i in range(n_card_decks):
        scores[i * 52] = scores[i * 52 + 13] = -50
        scores[i * 52 + 26] = scores[i * 52 + 39] = 0

    random.shuffle(scores)

    return scores


def draw_one_card(score_vector):
    return score_vector.pop()


def draw_cards_for_players(player_cards, score_vector):
    for player_type in player_cards:
        for i in range(len(player_cards[player_type]["hand"])):
            player_cards[player_type]["hand"][i].append(draw_one_card(score_vector))

            update_player_EV(player_type, player_cards, i)


def reveal_middle_card(player_cards):
    for player_type in player_cards:
        for i in range(len(player_cards[player_type]["hand"])):
            update_player_EV(player_type, player_cards, i)


def get_user_round_decision():
    print("=" * 53)
    print(f"{"=" * 20} PLAYER MOVE {"=" * 20}")
    print("=" * 53, "\n")

    bid = int(input(f"Enter your bid: "))
    ask = int(input(f"Enter your ask: "))

    print("")
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
                n_user_buys += 1
                net_cash -= user_bid

            if player_cards[player_type]["EV_middle"][i] > user_ask:
                # BOT BUYS
                make_player_buy(player_type, i, positions, cash, user_ask)
                n_user_sells += 1
                net_cash += user_ask

    print(f"ROUND {global_vars["curr_round"]} STATS:")
    print(
        f"Bought: {n_user_buys} @ {user_bid}\nSold: {n_user_sells} @ {user_ask}\nNet cash: {net_cash}"
    )


def play_round(score_vector, positions, cash, player_cards):
    draw_cards_for_players(player_cards, score_vector)

    print(
        f"\n\nMiddle scores:\n\n== {" == ".join(map(str, global_vars["middle_cards"][:global_vars["curr_round"]]))} ==\n\n"
    )

    bid, ask = get_user_round_decision()
    simulate_taker_moves(player_cards, positions, cash, bid, ask)

    reveal_middle_card(player_cards)

    global_vars["curr_round"] += 1


def print_taker_bot_results(positions, cash, player_type):
    print("=" * 53)
    print(f"Average {player_type} result\n")

    print(
        f"Average {player_type} position: {sum(positions[player_type]) / len(positions[player_type])}"
    )
    print(
        f"Average {player_type} cash: {sum(cash[player_type]) / len(cash[player_type])}"
    )

    final_value = sum(global_vars["middle_cards"])
    net_profit = [
        positions[player_type][i] * final_value + cash[player_type][i]
        for i in range(len(positions[player_type]))
    ]

    print(
        f"Average {player_type} net profit: " + f"{sum(net_profit) / len(net_profit)}"
    )


def print_user_results():
    print("=" * 53)
    print(f"{"=" * 16} FINAL USER RESULTS {"=" * 17}")
    print("=" * 53, "\n")

    print(f"Final user position: {global_vars["user_position"]}")
    print(f"Final user cash: {global_vars["user_cash"]}")

    print(
        f"Net profit: {global_vars["user_position"] * sum(global_vars["middle_cards"]) + global_vars["user_cash"]}"
    )


def print_final_results(positions, cash):
    print("\n\n\n")
    print(
        f"\n\nFinal middle scores:\n\n== {" == ".join(map(str, global_vars["middle_cards"]))} ==\n\n"
    )

    print_taker_bot_results(positions, cash, "insider")
    print_taker_bot_results(positions, cash, "optimal")
    print_taker_bot_results(positions, cash, "sub_optimal")

    print_user_results()


def set_initial_EVs(player_cards, score_vector):
    total_score = sum(score_vector)

    for player_type in player_cards:
        for i in range(len(player_cards[player_type]["EV_middle"])):
            player_cards[player_type]["EV_middle"][i] = (
                total_score / (n_card_decks * 52) * global_vars["n_rounds"]
            )


def draw_middle_cards(score_vector):
    for _ in range(global_vars["n_rounds"]):
        global_vars["middle_cards"].append(draw_one_card(score_vector))


def play_game(n_card_decks, n_optimal, n_insider, n_sub_optimal):
    score_vector = get_score_vector(n_card_decks)
    global_vars["total_score_sum"] = sum(score_vector)

    positions, cash, player_cards = setup_game_tracker_dicts(
        n_optimal, n_insider, n_sub_optimal
    )

    set_initial_EVs(player_cards, score_vector)
    draw_middle_cards(score_vector)

    for _ in range(global_vars["n_rounds"]):
        play_round(score_vector, positions, cash, player_cards)

    print(positions)
    print(cash)

    print_final_results(positions, cash)


if __name__ == "__main__":
    n_card_decks, n_rounds = 1000, 3
    n_optimal, n_insider, n_sub_optimal = 100, 50, 1000

    global_vars["n_cards_init"] = n_card_decks * 52
    global_vars["n_rounds"] = n_rounds

    play_game(n_card_decks, n_optimal, n_insider, n_sub_optimal)
