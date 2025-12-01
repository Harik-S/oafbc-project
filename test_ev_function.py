#!/usr/bin/env python3
"""
Test script for the update_middle_cards_EV function
"""

import sys
import os

# Add the current directory to Python path to import main
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import update_middle_cards_EV, global_vars, setup_game_tracker_dicts

def reset_globals():
    """Reset global variables for each test"""
    global_vars["n_cards_init"] = 52
    global_vars["middle_cards"] = []
    global_vars["middle_cards_EV"] = 34.23  # Average card value for 1 deck * 5 cards
    global_vars["user_position"] = 0
    global_vars["user_cash"] = 0

def create_test_player_cards():
    """Create a simple player cards structure for testing"""
    return {
        "optimal": {
            "hand": [[], []],  # 2 optimal players
            "EV_next": [34.23, 34.23],
        },
        "insider": {
            "hand": [[]],  # 1 insider player  
            "EV_next": [34.23],
        },
        "sub_optimal": {
            "hand": [],
            "EV_next": [],
        },
    }

def test_scenario_1():
    """Test: No middle cards revealed yet, add first player card"""
    print("=" * 60)
    print("TEST 1: First card drawn (no middle cards yet)")
    print("=" * 60)
    
    reset_globals()
    player_cards = create_test_player_cards()
    
    # Add first card to first optimal player
    player_cards["optimal"]["hand"][0] = [10]
    
    print(f"Before: middle_cards_EV = {global_vars['middle_cards_EV']:.2f}")
    print(f"Middle cards: {global_vars['middle_cards']}")
    print(f"Player 0 cards: {player_cards['optimal']['hand'][0]}")
    
    update_middle_cards_EV(10, player_cards)
    
    print(f"After: middle_cards_EV = {global_vars['middle_cards_EV']:.2f}")
    print(f"Player EVs: {player_cards['optimal']['EV_next']}")
    print()

def test_scenario_2():
    """Test: One middle card revealed"""
    print("=" * 60)
    print("TEST 2: First middle card revealed")
    print("=" * 60)
    
    reset_globals()
    player_cards = create_test_player_cards()
    
    # Add some player cards first
    player_cards["optimal"]["hand"][0] = [10, 5]
    player_cards["optimal"]["hand"][1] = [20]
    player_cards["insider"]["hand"][0] = [2]
    
    # Add first middle card
    global_vars["middle_cards"] = [15]
    
    print(f"Before: middle_cards_EV = {global_vars['middle_cards_EV']:.2f}")
    print(f"Middle cards: {global_vars['middle_cards']}")
    print(f"Player cards: {player_cards['optimal']['hand']} + {player_cards['insider']['hand']}")
    
    update_middle_cards_EV(15, player_cards)
    
    print(f"After: middle_cards_EV = {global_vars['middle_cards_EV']:.2f}")
    print(f"Player EVs: optimal={player_cards['optimal']['EV_next']}, insider={player_cards['insider']['EV_next']}")
    print()

def test_scenario_3():
    """Test: All 5 middle cards revealed (end game)"""
    print("=" * 60)
    print("TEST 3: All 5 middle cards revealed (end game)")
    print("=" * 60)
    
    reset_globals()
    player_cards = create_test_player_cards()
    
    # All middle cards revealed
    global_vars["middle_cards"] = [10, 5, 20, 0, -50]
    expected_sum = sum(global_vars["middle_cards"])  # = -15
    
    print(f"Before: middle_cards_EV = {global_vars['middle_cards_EV']:.2f}")
    print(f"Middle cards: {global_vars['middle_cards']}")
    print(f"Expected sum: {expected_sum}")
    
    update_middle_cards_EV(-50, player_cards)  # The last card revealed
    
    print(f"After: middle_cards_EV = {global_vars['middle_cards_EV']:.2f}")
    print(f"Should equal sum of middle cards: {expected_sum}")
    print(f"Player EVs (should all equal {expected_sum}): optimal={player_cards['optimal']['EV_next']}, insider={player_cards['insider']['EV_next']}")
    print()

def test_scenario_4():
    """Test: No player_cards provided"""
    print("=" * 60)
    print("TEST 4: No player_cards provided (should exit early)")
    print("=" * 60)
    
    reset_globals()
    
    print(f"Before: middle_cards_EV = {global_vars['middle_cards_EV']:.2f}")
    
    update_middle_cards_EV(10, None)
    
    print(f"After: middle_cards_EV = {global_vars['middle_cards_EV']:.2f} (should be unchanged)")
    print()

def test_scenario_5():
    """Test: Different visibility for different player types"""
    print("=" * 60)
    print("TEST 5: Different player types see different cards")
    print("=" * 60)
    
    reset_globals()
    player_cards = create_test_player_cards()
    
    # Add cards to players
    player_cards["optimal"]["hand"][0] = [10, 5]    # Optimal player 0 sees these
    player_cards["optimal"]["hand"][1] = [20, 2]    # Optimal player 1 sees these
    player_cards["insider"]["hand"][0] = [0]        # Insider sees this
    
    global_vars["middle_cards"] = [15, 8]  # 2 middle cards revealed
    
    print(f"Before: middle_cards_EV = {global_vars['middle_cards_EV']:.2f}")
    print(f"Middle cards: {global_vars['middle_cards']}")
    print(f"Optimal players see all cards, insider sees all cards")
    print(f"Player cards: optimal={player_cards['optimal']['hand']}, insider={player_cards['insider']['hand']}")
    
    update_middle_cards_EV(8, player_cards)  # The last middle card added
    
    print(f"After: middle_cards_EV = {global_vars['middle_cards_EV']:.2f}")
    print(f"Player EVs should be different based on what each player type can see:")
    print(f"  Optimal: {player_cards['optimal']['EV_next']}")
    print(f"  Insider: {player_cards['insider']['EV_next']}")
    print()

if __name__ == "__main__":
    print("Testing update_middle_cards_EV function")
    print("=" * 80)
    
    test_scenario_1()
    test_scenario_2() 
    test_scenario_3()
    test_scenario_4()
    test_scenario_5()
    
    print("=" * 80)
    print("All tests completed!")