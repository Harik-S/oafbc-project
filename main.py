# oxford alpha fund quant boot camp project
# game: suppose there are m teams, n rounds, in each round, each team gets a card and there is one card revealed in the middle
# optimal traders will calculate the EV based on available information to them. then they will trade based on the bid and offer provided by the market maker
# insider traders will have information from the next round in advance
# other traders will behave in a way that is as of now not determined
# POSSIBLE IMPROVEMENT: current idea is for market maker to offer a market with a set spread s = 0.2 around their EV. each trader takes k turns at mm so that n=km. open to other suggestions

import math
import random

def scorer(cards, score_matrix):
    # this returns the score of a set of cards
    x = 0
    for i in range(len(cards)):
        score = score_matrix[cards[i] % 52]
        x+=score
    return x

def EV(known_middle, known_team, all_card, score_matrix, n):
    # known_middle is the cards that are in the middle
    # known team is the cards that cannot be in the middle because they're with you
    leftover = list(set(all_card) - set(known_team) - set(known_middle))
    return scorer(known_middle, score_matrix) + (n-len(known_middle))/(len(leftover)) * scorer(leftover, score_matrix)

m = 10
m_optimal = 5
m_insider = 5
m_sub_optimal = m - m_optimal - m_insider

k = 2
n = k * m

n_cards = n * (m + 1) # since each team gets one card and there is one card in the middle
n_decks = math.ceil(n_cards/52)

# score matrix gives the score for each card
score = [(i%13 + 1) if (i%13)<10 else 20 for i in range(52)] # red first, A-K, A-K, A-K, A-K
score[0] = score[13] = -50
score[26] = score[39] = 0

all_cards_clone = [i for i in range(52 * n_decks)] # defined separately to avoid reference issues
all_cards = [i for i in range(52 * n_decks)]

middle = random.sample(all_cards, n)

final_score = scorer(middle, score)

all_cards = list(set(all_cards) - set(middle))
teams_cards = [[] for i in range(m)]
for i in range(m):
    teams_cards[i] = random.sample(all_cards, n)
    all_cards = list(set(all_cards) - set(teams_cards[i]))

