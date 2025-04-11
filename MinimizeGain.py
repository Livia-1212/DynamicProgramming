def optimal_value(coins, i, j, memo):
    """
    Computes the net advantage (current player's score minus opponent's score)
    from coins[i...j] when both players play optimally.
    """
    if i > j:
        return 0
    if (i, j) in memo:
        return memo[(i, j)]
    if i == j:
        memo[(i, j)] = coins[i]
        return coins[i]
    left_choice = coins[i] - optimal_value(coins, i + 1, j, memo)
    right_choice = coins[j] - optimal_value(coins, i, j - 1, memo)
    best = max(left_choice, right_choice)
    memo[(i, j)] = best
    return best

def move_optimal(player, coins, scores, strategies):
    """Optimal strategy: uses dynamic programming to choose move."""
    n = len(coins)
    if n == 0:
        return None
    memo = {}
    left_advantage = coins[0] - optimal_value(coins, 1, n - 1, memo) if n > 0 else float('-inf')
    right_advantage = coins[-1] - optimal_value(coins, 0, n - 2, memo) if n > 0 else float('-inf')
    if left_advantage >= right_advantage:
        return 0  # pick left
    else:
        return -1  # pick right

def move_largest(player, coins, scores, strategies):
    """Largest coin strategy: pick the end with the larger immediate coin."""
    if not coins:
        return None
    return 0 if coins[0] >= coins[-1] else -1

def simulate_future(coins, current_player, scores, strategies):
    """
    Recursively simulate the remainder of the game (without printing)
    given the current state and return the final scores.
    """
    if not coins:
        return scores.copy()
    move = strategies[current_player](current_player, coins, scores, strategies)
    new_scores = scores.copy()
    new_coins = coins.copy()
    if move == 0:
        coin = new_coins.pop(0)
        new_scores[current_player] += coin
    else:
        coin = new_coins.pop(-1)
        new_scores[current_player] += coin
    next_player = "Alice" if current_player == "Bob" else "Bob"
    return simulate_future(new_coins, next_player, new_scores, strategies)

def move_minimize(player, coins, scores, strategies):
    """
    Minimize opponent's gain strategy.
    The current player simulates both moves and chooses the one that yields a lower final score for the opponent.
    """
    if not coins:
        return None
    opponent = "Alice" if player == "Bob" else "Bob"
    
    # Simulate taking the left coin
    coins_left = coins.copy()
    coin_left = coins_left.pop(0)
    scores_left = scores.copy()
    scores_left[player] += coin_left
    outcome_left = simulate_future(coins_left, opponent, scores_left, strategies)
    
    # Simulate taking the right coin
    coins_right = coins.copy()
    coin_right = coins_right.pop(-1)
    scores_right = scores.copy()
    scores_right[player] += coin_right
    outcome_right = simulate_future(coins_right, opponent, scores_right, strategies)
    
    # Compare the opponent's final score for each move.
    if outcome_left[opponent] < outcome_right[opponent]:
        return 0  # choose left
    elif outcome_left[opponent] > outcome_right[opponent]:
        return -1  # choose right
    else:
        return 0  # if tie, choose left by default

def simulate_game_interactive(strategies, scenario_label):
    """
    Simulate the game interactively using the given strategies.
    strategies is a dictionary mapping player names ("Alice" and "Bob")
    to the corresponding move functions.
    The function prints each move (step-by-step) and shows current scores.
    """
    coins = [2, 6, 5, 2, 7, 3, 5, 4]
    
    # Prompt user to choose who is Player 1.
    player1 = input("Choose who will be Player 1 (Alice/Bob): ").strip()
    if player1 not in ["Alice", "Bob"]:
        print("Invalid choice. Defaulting to Alice as Player 1.")
        player1 = "Alice"
    player2 = "Alice" if player1 == "Bob" else "Bob"
    
    print(f"\nScenario {scenario_label}")
    print(f"Player 1: {player1}")
    print(f"Player 2: {player2}\n")
    
    # Initialize scores.
    scores = {"Alice": 0, "Bob": 0}
    current_player = player1
    turn = 1
    
    while coins:
        move_func = strategies[current_player]
        move = move_func(current_player, coins, scores, strategies)
        if move == 0:
            chosen_coin = coins.pop(0)
            side = "left"
        else:
            chosen_coin = coins.pop(-1)
            side = "right"
        scores[current_player] += chosen_coin
        print(f"Turn {turn}: {current_player} chooses {chosen_coin} from the {side}.")
        print(f"Remaining coins: {coins}")
        print(f"Scores => Alice: {scores['Alice']} , Bob: {scores['Bob']}\n")
        current_player = player2 if current_player == player1 else player1
        turn += 1
    
    print("Game over!")
    print(f"Final Scores => Alice: {scores['Alice']} , Bob: {scores['Bob']}")

def main():
    print("Choose scenario to simulate:")
    print("  5: Bob (optimal) vs. Alice (minimize Bob's gain)")
    print("  6: Alice (optimal) vs. Bob (minimize Alice's gain)")
    scenario = input("Enter scenario number (5 or 6): ").strip()
    
    if scenario == "5":
        # Scenario 5: Bob uses optimal, Alice uses minimize (minimize Bob's gain)
        strategies = {
            "Alice": move_minimize,  # When Alice moves, she simulates outcomes to minimize Bob's final score.
            "Bob": move_optimal      # Bob plays optimally.
        }
        simulate_game_interactive(strategies, "5: Bob (optimal) vs. Alice (minimize Bob's gain)")
    elif scenario == "6":
        # Scenario 6: Alice uses optimal, Bob uses minimize (minimize Alice's gain)
        strategies = {
            "Alice": move_optimal,   # Alice plays optimally.
            "Bob": move_minimize     # Bob uses minimize strategy to reduce Alice's eventual score.
        }
        simulate_game_interactive(strategies, "6: Alice (optimal) vs. Bob (minimize Alice's gain)")
    else:
        print("Invalid scenario choice.")

if __name__ == "__main__":
    main()
