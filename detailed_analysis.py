#!/usr/bin/env python3
"""
Detailed analysis of the update_middle_cards_EV function behavior
"""

import sys
import os

# Add the current directory to Python path to import main
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import update_middle_cards_EV, global_vars, get_score_vector

def analyze_ev_calculation():
    """Analyze how the EV calculation works step by step"""
    print("DETAILED ANALYSIS OF EV CALCULATION")
    print("=" * 80)
    
    # Set up initial conditions
    global_vars["n_cards_init"] = 52
    global_vars["middle_cards"] = []
    global_vars["middle_cards_EV"] = 0
    
    # Calculate initial average card value
    score_vector = get_score_vector(1)  # 1 deck
    total_score = sum(score_vector)
    avg_card_value = total_score / len(score_vector)
    
    print(f"Initial setup:")
    print(f"  Total cards in deck: {len(score_vector)}")
    print(f"  Total score of all cards: {total_score}")
    print(f"  Average card value: {avg_card_value:.2f}")
    print(f"  Initial EV for 5 middle cards: {avg_card_value * 5:.2f}")
    print()
    
    # Initialize
    global_vars["middle_cards_EV"] = avg_card_value * 5
    
    # Create test scenario
    player_cards = {
        "optimal": {
            "hand": [[], []],  # 2 optimal players
            "EV_next": [avg_card_value, avg_card_value],
        },
        "insider": {
            "hand": [[]],  # 1 insider player  
            "EV_next": [avg_card_value],
        },
        "sub_optimal": {
            "hand": [],
            "EV_next": [],
        },
    }
    
    # Scenario 1: Add some player cards
    print("STEP 1: Drawing player cards")
    print("-" * 40)
    
    cards_to_add = [10, 5, 20]
    for i, card_val in enumerate(cards_to_add):
        player_cards["optimal"]["hand"][0].append(card_val)
        
        print(f"Adding card {card_val} to optimal player 0")
        print(f"  Before: EV = {global_vars['middle_cards_EV']:.2f}")
        
        # Calculate expected values manually
        cards_seen = len(global_vars["middle_cards"])
        total_player_cards = sum(len(hand) for player_type in player_cards.values() 
                                for hand in player_type["hand"])
        total_cards_seen = cards_seen + total_player_cards
        n_cards_unknown = global_vars["n_cards_init"] - total_cards_seen
        
        print(f"  Cards seen by all: middle={cards_seen}, player={total_player_cards}, total={total_cards_seen}")
        print(f"  Unknown cards remaining: {n_cards_unknown}")
        
        update_middle_cards_EV(card_val, player_cards)
        print(f"  After: EV = {global_vars['middle_cards_EV']:.2f}")
        print()
    
    # Scenario 2: Add middle cards
    print("STEP 2: Drawing middle cards")
    print("-" * 40)
    
    middle_cards_to_add = [15, -50, 0]
    for card_val in middle_cards_to_add:
        global_vars["middle_cards"].append(card_val)
        
        print(f"Adding middle card {card_val}")
        print(f"  Middle cards so far: {global_vars['middle_cards']}")
        print(f"  Cards remaining to be drawn: {5 - len(global_vars['middle_cards'])}")
        print(f"  Before: EV = {global_vars['middle_cards_EV']:.2f}")
        
        update_middle_cards_EV(card_val, player_cards)
        print(f"  After: EV = {global_vars['middle_cards_EV']:.2f}")
        print()
    
    # Scenario 3: Complete the middle cards
    print("STEP 3: Completing all 5 middle cards")
    print("-" * 40)
    
    remaining_cards = [8, 12]  # Add 2 more to complete 5 cards
    for card_val in remaining_cards:
        global_vars["middle_cards"].append(card_val)
        
        print(f"Adding final middle card {card_val}")
        print(f"  Middle cards: {global_vars['middle_cards']}")
        
        if len(global_vars["middle_cards"]) >= 5:
            print("  All 5 cards revealed - EV should be actual sum")
            actual_sum = sum(global_vars["middle_cards"])
            print(f"  Actual sum: {actual_sum}")
        
        print(f"  Before: EV = {global_vars['middle_cards_EV']:.2f}")
        
        update_middle_cards_EV(card_val, player_cards)
        print(f"  After: EV = {global_vars['middle_cards_EV']:.2f}")
        print()

def test_player_visibility():
    """Test how different player types see different cards"""
    print("TESTING PLAYER VISIBILITY DIFFERENCES")
    print("=" * 80)
    
    global_vars["n_cards_init"] = 52
    global_vars["middle_cards"] = [10]  # One middle card revealed
    global_vars["middle_cards_EV"] = 100  # Some starting EV
    
    player_cards = {
        "optimal": {
            "hand": [[5, 15], [20]],  # 2 optimal players with different cards
            "EV_next": [30, 30],
        },
        "insider": {
            "hand": [[0]],  # 1 insider player
            "EV_next": [30],
        },
        "sub_optimal": {
            "hand": [[25]],  # 1 sub-optimal player (can't see others' cards)
            "EV_next": [30],
        },
    }
    
    print("Initial state:")
    print(f"  Middle cards: {global_vars['middle_cards']}")
    print(f"  Optimal players' cards: {player_cards['optimal']['hand']}")
    print(f"  Insider player's cards: {player_cards['insider']['hand']}")
    print(f"  Sub-optimal player's cards: {player_cards['sub_optimal']['hand']}")
    print(f"  Starting EV: {global_vars['middle_cards_EV']}")
    print()
    
    print("Revealing new card: 7")
    update_middle_cards_EV(7, player_cards)
    
    print("After update:")
    print(f"  Global middle EV: {global_vars['middle_cards_EV']:.2f}")
    print(f"  Optimal players' EVs: {player_cards['optimal']['EV_next']}")
    print(f"  Insider player's EV: {player_cards['insider']['EV_next']}")
    print(f"  Sub-optimal player's EV: {player_cards['sub_optimal']['EV_next']}")
    print()
    
    # Calculate what each player type should see
    print("Manual calculation verification:")
    
    # For optimal players (can see all cards)
    cards_optimal_can_see = len(global_vars['middle_cards']) + 2 + 1 + 1 + 1  # middle + own + other optimal + insider + sub_optimal
    print(f"  Optimal players can see {cards_optimal_can_see} cards total")
    
    # For insider players (can see all cards) 
    cards_insider_can_see = len(global_vars['middle_cards']) + 1 + 2 + 1 + 1  # middle + own + optimal1 + optimal2 + sub_optimal
    print(f"  Insider player can see {cards_insider_can_see} cards total")
    
    # For sub-optimal players (can only see own cards and middle cards)
    cards_subopt_can_see = len(global_vars['middle_cards']) + 1  # middle + own only
    print(f"  Sub-optimal player can see {cards_subopt_can_see} cards total")

if __name__ == "__main__":
    analyze_ev_calculation()
    print("\n" + "=" * 80 + "\n")
    test_player_visibility()