# Oxford Alpha Fund Quant Boot Camp Project

A simulated market-making and trading game developed during the **Oxford Alpha Fund Quant Boot Camp**.

The project models a multi-round card-based market in which traders receive private information, observe information revealed to the market, and trade against a market maker. The simulation explores how **information asymmetry, expected-value pricing and trader behaviour** affect trading outcomes.

## Overview

The game consists of:

* multiple trading teams;
* multiple rounds;
* one card distributed to each team each round;
* one card revealed publicly in each round;
* traders with different information sets;
* a market maker quoting a bid and ask;
* trading based on each trader's estimated expected value;
* final mark-to-market profit and loss.

Three trader types are represented:

* **Optimal traders** use the information currently available to estimate expected value.
* **Insider traders** have access to information from the following round.
* **Sub-optimal traders** provide a less-informed benchmark.

The aim is to create a simplified environment for studying how traders with different information interact with a market maker.

## Market Model

Each game generates a shuffled collection of card scores. Cards are distributed between teams and the public middle, with the middle cards revealed sequentially throughout the game.

A trader's value depends on the cards that are already known and the expected value of the remaining cards.

The project separates the calculation of expected value from the game engine through `EV_funcs.py`.

### Expected-value pricing

For each trader, the simulation maintains an estimate of the expected value of the eventual middle-card payoff.

The estimate is updated as new information becomes available:

1. cards are distributed privately;
2. the next public card is revealed;
3. trader information sets change;
4. expected values are recalculated;
5. traders decide whether to trade against the market maker.

This creates a simple information-driven trading environment.

## Trading Simulation

The game implementation includes:

### Market maker

The user acts as the market maker and submits a bid and ask each round.

Other traders compare their estimated expected value against these quotes.

A trader with an estimated value below the bid sells to the market maker, while a trader with an estimated value above the ask buys.

The simulation tracks:

* trader positions;
* trader cash;
* market-maker position;
* market-maker cash;
* trading volume;
* final profit and loss.

The trading logic is implemented in `main.py`.

### Trader information

The simulation distinguishes between traders with different information sets. In particular, insider traders receive information about the subsequent round in advance, allowing their behaviour to be compared with traders operating only on currently available information.

## Game Structure

The simulation follows the sequence:

```text
Generate card scores
        ↓
Shuffle deck
        ↓
Distribute private cards
        ↓
Reveal public information
        ↓
Calculate trader expected values
        ↓
Market maker posts bid / ask
        ↓
Traders decide whether to trade
        ↓
Update cash and positions
        ↓
Reveal additional information
        ↓
Repeat
        ↓
Mark final positions to market
```

The game engine handles card allocation, trader state, market interaction and final P&L calculation.

## Code Structure

```text
.
├── main.py
├── EV_funcs.py
├── constants.py
└── OAFBC-Presentation.pptx
```

### `main.py`

Contains the game engine, including:

* player/trader state;
* card distribution;
* round execution;
* market-making interaction;
* trading decisions;
* position and cash accounting;
* final P&L calculation.

### `EV_funcs.py`

Contains expected-value calculations used by the simulation.

### `constants.py`

Stores global game state and configuration.

## Trader P&L

At the end of a game, the simulation calculates the value of each trader's final position together with accumulated cash:

$$
\text{P\&L}
=
\text{Position}\times\text{Final payoff}
+
\text{Cash}.
$$

Average position, cash and net profit are reported separately for each trader type, allowing the performance of different information levels to be compared.

## Motivation

The project was designed as a simplified quantitative market environment rather than a realistic pricing model.

The central question is:

> **How does information advantage translate into trading behaviour and P&L when participants interact through a market maker?**

This makes it possible to experiment with:

* different trader populations;
* different market-maker spreads;
* different information advantages;
* different payoff structures;
* different trading rules.

## Possible Extensions

Several natural extensions would make the model more realistic and allow more systematic experimentation:

* dynamically determine the market-maker spread from estimated uncertainty;
* introduce inventory constraints;
* allow the market maker to update quotes after each trade;
* model trader-specific risk preferences;
* add stochastic or strategic sub-optimal traders;
* run many independent simulations and analyse P&L distributions;
* measure the P&L advantage generated by insider information;
* study market efficiency as the proportion of informed traders changes;
* analyse the relationship between spread, trade frequency and market-maker profitability.

## Project Context

Developed as part of the **Oxford Alpha Fund Quant Boot Camp** as an introduction to quantitative trading, expected-value pricing, market making and information asymmetry.
