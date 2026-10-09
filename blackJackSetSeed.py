import gymnasium as gym

# --- SEED SETUP ---
print("=" * 40)
print("          BLACKJACK GAME SETUP          ")
print("=" * 40)
seed_input = input("Enter a specific number seed (or press Enter for a random game): ").strip()

# If the user typed a number, convert it to an integer; otherwise, leave it as None
my_seed = int(seed_input) if seed_input.isdigit() else None

# Setup the environment
env = gym.make("Blackjack-v1", sab=True)

# Pass the seed into the reset function here
observation, info = env.reset(seed=my_seed)
terminated = False

print("\n" + "=" * 40)
print("       WELCOME TO GYMNASIUM BLACKJACK   ")
print("=" * 40)

if my_seed is not None:
    print(f"🎮 Playing with fixed Seed: {my_seed}")

# Main game loop
while not terminated:
    player_sum, dealer_card, usable_ace = observation
    
    print(f"\nYour Hand Total: {player_sum}")
    print(f"Dealer's Up-Card: {dealer_card}")
    print(f"Usable Ace?: {'Yes' if usable_ace else 'No'}")
    
    # Get player choice
    choice = input("Type 'h' to HIT or 's' to STAND: ").strip().lower()
    
    if choice == 'h':
        action = 1  # 1 means Hit
    elif choice == 's':
        action = 0  # 0 means Stand
    else:
        print("Invalid input! Please type 'h' or 's'.")
        continue

    # Take the step in the game
    observation, reward, terminated, truncated, info = env.step(action)

# --- GAME OVER SECTION ---
player_sum, dealer_card, usable_ace = observation
print("\n" + "=" * 40)
print("               GAME OVER                ")
print("=" * 40)

# Manually calculate the dealer's score to avoid import errors
dealer_full_hand = env.unwrapped.dealer

# Calculate the sum, giving Aces a value of 11 if it doesn't bust them
dealer_total = sum(dealer_full_hand)
if 1 in dealer_full_hand and dealer_total + 10 <= 21:
    dealer_total += 10

print(f"Your Final Hand Total: {player_sum}")
print(f"Dealer's Full Hand   : {dealer_full_hand} (Total: {dealer_total})")
print("-" * 40)

if reward > 0:
    print("YOU WIN!")
elif reward < 0:
    print("YOU LOSE!")
else:
    print("IT'S A PUSH! (Tie game)")

env.close()
