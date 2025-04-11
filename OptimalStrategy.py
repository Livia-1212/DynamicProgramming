def optimal_value(coins, i, j, memo):
    """
    Returns the net advantage (current player's total minus opponent's total)
    for the subarray coins[i...j] when both players play optimally.
    """
    if i > j:
        return 0
    if (i, j) in memo:
        return memo[(i, j)]
    if i == j:
        memo[(i, j)] = coins[i]
        return coins[i]
    
    # If current player picks left coin, opponent will then force optimal play on coins[i+1...j]
    left_choice = coins[i] - optimal_value(coins, i + 1, j, memo)
    # If current player picks right coin, opponent then plays optimally on coins[i...j-1]
    right_choice = coins[j] - optimal_value(coins, i, j - 1, memo)
    
    best = max(left_choice, right_choice)
    memo[(i, j)] = best
    return best

def optimal_move(coins):
    """
    Returns the move decision for the current player using the optimal strategy.
    Returns 0 if picking the left coin yields an advantage at least as good as picking
    the right coin, otherwise returns -1 (meaning choose the right coin).
    """
    n = len(coins)
    if n == 0:
        return None
    memo = {}
    # If we take the left coin, our net advantage is:
    left_advantage = coins[0] - optimal_value(coins, 1, n - 1, memo) if n > 0 else float('-inf')
    # If we take the right coin, our net advantage is:
    right_advantage = coins[-1] - optimal_value(coins, 0, n - 2, memo) if n > 0 else float('-inf')
    
    if left_advantage >= right_advantage:
        return 0  # Choose left coin
    else:
        return -1  # Choose right coin

def simulate_game():
    # Initial coin line
    coins = [2, 6, 5, 2, 7, 3, 5, 4]
    
    # Prompt user to choose which player is Player 1.
    player1 = input("Choose who will be Player 1 (Alice/Bob): ").strip()
    if player1 not in ["Alice", "Bob"]:
        print("Invalid choice. Defaulting to Alice as Player 1.")
        player1 = "Alice"
    player2 = "Alice" if player1 == "Bob" else "Bob"
    
    print(f"\nPlayer 1: {player1} (Optimal Strategy)")
    print(f"Player 2: {player2} (Optimal Strategy)\n")
    
    # Initialize scores for both players.
    scores = {player1: 0, player2: 0}
    
    current_player = player1
    turn = 1
    
    # Game simulation: loop until no coins remain.
    while coins:
        move = optimal_move(coins)
        if move == 0:
            chosen_coin = coins.pop(0)
            side = "left"
        else:
            chosen_coin = coins.pop(-1)
            side = "right"
        
        scores[current_player] += chosen_coin
        
        # Display the move details.
        print(f"Turn {turn}: {current_player} chooses {chosen_coin} from the {side}.")
        print(f"Remaining coins: {coins}")
        print(f"Scores => {player1}: {scores[player1]}, {player2}: {scores[player2]}\n")
        
        # Switch the turn.
        current_player = player2 if current_player == player1 else player1
        turn += 1
    
    # Game over: output final scores.
    print("Game over!")
    print(f"Final Scores => {player1}: {scores[player1]}, {player2}: {scores[player2]}")

if __name__ == "__main__":
    simulate_game()
