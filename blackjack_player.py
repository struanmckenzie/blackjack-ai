
import pandas as pd
import blackjack_decision_tree_training

hand = pd.DataFrame([{
    "player_total": 16,
    "dealer_upcard": 10,
    "usable_ace": 0,
    "true_count": 4.0,
}])

model = blackjack_decision_tree_training.train()
action = model.predict(hand)[0]

print("Recommended action:", action)