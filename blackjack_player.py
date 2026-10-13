
import pandas as pd
import blackjack_decision_tree_training
import random


player_cards = random.randint(4, 21)
dealer_card = random.randint(2, 11)
hand = pd.DataFrame([{
    "player_total": player_cards,
    "dealer_upcard": dealer_card,
    "usable_ace": 0,
}])

model = blackjack_decision_tree_training.train()
action = model.predict(hand)[0]

print(f"Player total = {player_cards}")
print(f"Dealer card: {dealer_card}")
print("Recommended action:", action)