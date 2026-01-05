# Rock–Paper–Scissors–Plus Referee

## Overview
This project implements a minimal AI referee for a 3-round
Rock–Paper–Scissors–Plus game. The referee enforces game rules,
validates user input, tracks state across rounds, and automatically
ends the game with a clear final result.

Google ADK is used to represent the referee agent abstraction, while
all game logic and state management are handled explicitly in code.

## State Model
Game state is represented using a structured `GameState` object
containing:
- Current round number
- User and bot scores
- Bomb usage flags (once per player)
- Game-over flag

State persists across turns in memory and is never stored in prompts.

## Capability (Tool-like) Functions
The game logic is separated into explicit, named functions that act
as logical tools:

- `validate_move` – validates user input and enforces bomb usage rules
- `resolve_round` – determines the winner of a round
- `update_game_state` – mutates persistent game state
- `explain_outcome` – explains why a round was won or drawn

These functions isolate responsibilities and prevent logic from being
embedded directly in the control flow.

## Agent Role
The Google ADK `Agent` represents the referee conceptually. It does not
contain game logic, but serves as the controlling entity responsible
for coordinating validation, resolution, and response generation.

## Separation of Concerns
| Concern | Implementation |
|------|---------------|
| Intent understanding | User input handling |
| Validation | `validate_move` |
| Game logic | `resolve_round` |
| Explanation | `explain_outcome` |
| State mutation | `update_game_state` |
| Response generation | CLI output |

## Game Flow
- Rules are explained in four lines
- The game runs for a maximum of three rounds
- Invalid input wastes the round
- Bomb usage is limited to once per player
- Each round displays:
  - Round number
  - Moves played
  - Winner
  - Reason for outcome
- The game ends automatically with a final result:
  - User wins / Bot wins / Draw

## Tradeoffs
- CLI interface chosen for simplicity
- Bot uses random move selection
- No persistence beyond a single game session

## Improvements with More Time
- Smarter bot strategy
- Structured JSON input/output
- Unit tests for game logic
- Multi-agent setup (player vs referee)
