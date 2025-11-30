import numpy as np

from constants import global_vars


def update_player_EV(player_type, player_cards, player_idx):
    if player_type == "optimal":
        update_optimal_player_EV(player_cards[player_type], player_idx)
    if player_type == "insider":
        update_insider_player_EV(player_cards[player_type], player_idx)
    if player_type == "sub_optimal":
        update_sub_optimal_player_EV(player_cards[player_type], player_idx)


def update_optimal_player_EV(player_type_dict, idx_player):
    N = (
        global_vars["n_cards_init"]
        - global_vars["curr_round"]
        - len(player_type_dict["hand"][idx_player])
    )
    R = global_vars["n_rounds"] - global_vars["curr_round"]
    Y = sum(global_vars["middle_cards"][: global_vars["curr_round"]])
    Z = sum(player_type_dict["hand"][idx_player])
    S = global_vars["total_score_sum"]

    player_type_dict["EV_middle"][idx_player] = Y + R / N * (S - Z - Y)


def update_insider_player_EV(player_type_dict, idx_player):
    round_with_advantage = min(global_vars["curr_round"] + 1, global_vars["n_rounds"])

    N = (
        global_vars["n_cards_init"]
        - round_with_advantage
        - len(player_type_dict["hand"][idx_player])
    )
    R = global_vars["n_rounds"] - round_with_advantage
    Y = sum(global_vars["middle_cards"][:round_with_advantage])
    Z = sum(player_type_dict["hand"][idx_player])
    S = global_vars["total_score_sum"]

    player_type_dict["EV_middle"][idx_player] = Y + R / N * (S - Z - Y)


def update_sub_optimal_player_EV(player_type_dict, idx_player):
    N = (
        global_vars["n_cards_init"]
        - global_vars["curr_round"]
        - len(player_type_dict["hand"][idx_player])
    )
    R = global_vars["n_rounds"] - global_vars["curr_round"]
    Y = sum(global_vars["middle_cards"][: global_vars["curr_round"]])
    Z = sum(player_type_dict["hand"][idx_player])
    S = global_vars["total_score_sum"]

    player_type_dict["EV_middle"][idx_player] = (
        Y + R / N * (S - Z - Y)
    ) + np.random.normal(0, global_vars["sub_optimal_noise_std"])
