import random
from dataclasses import dataclass
from google.adk import Agent

# -----------------------------
# Game State (persistent)
# -----------------------------
@dataclass
class GameState:
    round: int = 1
    user_score: int = 0
    bot_score: int = 0
    user_bomb_used: bool = False
    bot_bomb_used: bool = False
    game_over: bool = False


# -----------------------------
# "TOOLS" (explicit capabilities)
# -----------------------------
def validate_move(move: str, bomb_used: bool) -> dict:
    move = move.lower().strip()
    valid_moves = {"rock", "paper", "scissors", "bomb"}

    if move not in valid_moves:
        return {"valid": False, "reason": "Invalid move"}

    if move == "bomb" and bomb_used:
        return {"valid": False, "reason": "Bomb already used"}

    return {"valid": True, "move": move}


def resolve_round(user_move: str, bot_move: str) -> str:
    if user_move == bot_move:
        return "draw"

    if user_move == "bomb":
        return "user"

    if bot_move == "bomb":
        return "bot"

    beats = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock"
    }

    return "user" if beats[user_move] == bot_move else "bot"

def explain_outcome(user_move: str, bot_move: str, result: str) -> str:
    if result == "draw":
        return f"Both chose {user_move}. It's a draw."

    if user_move == "bomb" or bot_move == "bomb":
        return "Bomb beats all other moves."

    return f"{user_move.capitalize()} beats {bot_move}."



def update_game_state(
    state: GameState,
    result: str,
    user_move: str,
    bot_move: str
) -> GameState:
    if result == "user":
        state.user_score += 1
    elif result == "bot":
        state.bot_score += 1

    if user_move == "bomb":
        state.user_bomb_used = True
    if bot_move == "bomb":
        state.bot_bomb_used = True

    state.round += 1
    if state.round > 3:
        state.game_over = True

    return state


# -----------------------------
# Agent (capability declaration)
# -----------------------------
referee_agent = Agent(
    name="RPSPlusReferee",
    description="Referee agent for Rock–Paper–Scissors–Plus"
)
# -----------------------------
# Game Loop (CLI-style)
# -----------------------------
def run_game():
    state = GameState()

    print(
        "Rules:\n"
        "• Best of 3 rounds\n"
        "• Moves: rock, paper, scissors, bomb\n"
        "• Bomb beats all, once per player\n"
        "• Invalid input wastes the round\n"
    )

    while not state.game_over:
        print(f"\nRound {state.round}/3")
        user_input = input("Your move: ")

        validation = validate_move(user_input, state.user_bomb_used)
        if not validation["valid"]:
            print(f"Invalid move: {validation['reason']}")
            state.round += 1
            if state.round > 3:
                state.game_over = True
            continue

        user_move = validation["move"]

        bot_moves = ["rock", "paper", "scissors"]
        if not state.bot_bomb_used:
            bot_moves.append("bomb")

        bot_move = random.choice(bot_moves)

        result = resolve_round(user_move, bot_move)
        state = update_game_state(state, result, user_move, bot_move)
        

        print(f"You played: {user_move}")
        print(f"Bot played: {bot_move}")
        print(f"Round winner: {result.upper()}")
        print("Reason:", explain_outcome(user_move, bot_move, result))

    print("\nFinal Result")
    print(f"User score: {state.user_score}")
    print(f"Bot score: {state.bot_score}")

    if state.user_score > state.bot_score:
        print("WINNER: USER")
    elif state.bot_score > state.user_score:
        print("WINNER: BOT")
    else:
        print("RESULT: DRAW")


if __name__ == "__main__":
    run_game()
