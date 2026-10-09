from sklearn import tree
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt

def train():

    data = pd.read_csv("black_jack_training.csv")

    features = ["player_total", "dealer_upcard", "usable_ace", "true_count"]

    x = data[features]
    y = data["action"]

    X_train, X_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = DecisionTreeClassifier(
        max_depth=5,
        min_samples_leaf=20,
        random_state=42,
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, predictions))
    print(classification_report(y_test, predictions))

    # Visualize the learned rules
    plt.figure(figsize=(18, 9))
    plot_tree(
        model,
        feature_names=features,
        class_names=model.classes_,
        filled=True,
        rounded=True,
    )

    plt.show()

    return model