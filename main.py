# oxford alpha fund quant boot camp project
# game: suppose there are m teams, n rounds, in each round, each team gets a card and there is one card revealed in the middle
# optimal traders will calculate the EV based on available information to them. then they will trade based on the bid and offer provided by the market maker
# insider traders will have information from the next round in advance
# other traders will behave in a way that is as of now not determined
# POSSIBLE IMPROVEMENT: current idea is for market maker to offer a market with a set spread s = 0.2 around their EV. each trader takes k turns at mm so that n=km. open to other suggestions

import math

m = 10
m_optimal = 5
m_insider = 5
m_sub_optimal = m - m_optimal - m_insider

k = 2
n = k * m

n_cards = n * (
    m + 1
)  # since each team gets one card and there is one card in the middle
n_decks = math.ceil(n_cards / 52)

score = [
    (i % 13 + 1) if (i % 13) < 10 else 20 for i in range(52)
]  # red first, A-K, A-K, A-K, A-K
score[0] = score[13] = -50
score[26] = score[39] = 0
print(score)
