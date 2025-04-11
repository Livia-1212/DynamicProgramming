def optimal_value(coins, i, j, memo):
    """
    Computes the net advantage (current player's score minus opponent's score)
    from the subarray coins[i...j] when both players play optimally.
    """
    if i > j:
        return 0
    if (i, j) in memo:
        return memo[(i, j)]
    if i == j:
        memo[(i, j)] = coins[i]
        return coins[i]
    
    # If the current player picks the left coin, then the opponent gets optimal play on coins[i+1...j]
    left_choice = coins[i] - optimal_value(coins, i + 1, j, memo)
    # Similarly for the right coin
    right_choice = coins[j] - optimal_value(coins, i, j - 1, memo)
    
    best = max(left_choice, right_choice)
    memo[(i, j)] = best
    return best

def optimal_move(coins):
    """
    Returns the move decision for an optimal strategy.
    Returns 0 if taking the left coin gives at least as much advantage as taking the right,
    otherwise returns -1 (which means take the right coin).
    """
    n = len(coins)
    if n == 0:
        return None
    memo = {}
    left_advantage = coins[0] - optimal_value(coins, 1, n - 1, memo) if n > 0 else float('-inf')
    right_advantage = coins[-1] - optimal_value(coins, 0, n - 2, memo) if n > 0 else float('-inf')
    if left_advantage >= right_advantage:
        return 0  # choose left coin
    else:
        return -1  # choose right coin

def largest_coin_move(coins):
    """
    Returns the move decision based solely on the coin values.
    Returns 0 if the left coin is greater than or equal to the right coin,
    otherwise returns -1.
    """
    if not coins:
        return None
    return 0 if coins[0] >= coins[-1] else -1

def simulate_game():
    # Initial coins
    coins = [2, 6, 5, 2, 7, 3, 5, 4]
    
    # Prompt user for Player 1 choice
    player1 = input("Choose who will be Player 1 (Alice/Bob): ").strip()
    if player1 not in ["Alice", "Bob"]:
        print("Invalid choice. Defaulting to Alice as Player 1.")
        player1 = "Alice"
    # In this scenario, we know that:
    # - Alice uses the optimal strategy.
    # - Bob uses the largest coin strategy.
    # So if the user chooses Player 1 as "Alice", then Alice is optimal and Bob is largest coin.
    # If the user chooses "Bob" as Player 1, then Bob goes first using the largest coin rule and Alice is optimal.
    player2 = "Alice" if player1 == "Bob" else "Bob"
    
    print(f"\nPlayer 1: {player1}")
    print(f"Player 2: {player2}")
    print("Scenario: Alice (optimal) vs. Bob (largest coin)\n")
    
    # Initialize scores
    scores = {"Alice": 0, "Bob": 0}
    
    # Determine strategy functions for each player.
    # According to the scenario:
    #   - Alice always uses the optimal strategy.
    #   - Bob always uses the largest coin strategy.
    strategy = {
        "Alice": optimal_move,
        "Bob": largest_coin_move
    }
    
    # Set the current player to Player 1
    current_player = player1
    turn = 1
    
    # Game simulation: run until no coins remain.
    while coins:
        # Determine which strategy to use for the current move.
        move_func = strategy[current_player]
        move = move_func(coins)
        
        # Apply the move: 0 means take from left, -1 means take from right.
        if move == 0:
            chosen_coin = coins.pop(0)
            side = "left"
        else:
            chosen_coin = coins.pop(-1)
            side = "right"
        
        # Update the score for the current player.
        scores[current_player] += chosen_coin
        
        # Output the current turn's move details.
        print(f"Turn {turn}: {current_player} chooses {chosen_coin} from the {side}.")
        print(f"Remaining coins: {coins}")
        print(f"Scores -> Alice: {scores['Alice']} , Bob: {scores['Bob']}\n")
        
        # Switch turn to the other player.
        current_player = player2 if current_player == player1 else player1
        turn += 1
    
    # Final output.
    print("Game over!")
    print(f"Final Scores -> Alice: {scores['Alice']} , Bob: {scores['Bob']}")

if __name__ == "__main__":
    simulate_game()
