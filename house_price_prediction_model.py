import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


#Get the dataset from the csv file
dataset = pd.read_csv("houses/house_price_regression_dataset.csv")

#Get the headings from the data set and separate the house price values as thats the value we are trying to predict
x = dataset[["Square_Footage", "Num_Bedrooms", "Num_Bathrooms", "Year_Built", "Lot_Size", "Garage_Size", "Neighborhood_Quality"]]
y = dataset["House_Price"]

#Spilt the data set into 2 one for the training set and other for testing it is currently set as 80% for training and 20% for testing
X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.2, random_state=42)

#This is a list of hyperparameters that will be used when training the model
#These are here so we can test different combinations of hyperparameters for each model so we can find the combination that gives the best score
param_grid_forest = {
    "n_estimators": [50, 100, 1000],
    "max_depth": [None, 10],
    "min_samples_split": [2, 5],
    "min_samples_leaf": [1, 2,]
}

param_grid_linear = {
    "fit_intercept": [True, False],
    "positive": [True, False]
}

param_grid_gradient = {
    "n_estimators": [100, 200],
    "learning_rate": [0.05, 0.1],
    "min_samples_split": [2, 5],
    "min_samples_leaf": [1, 2,],
    "subsample": [0.8, 1]
}

#Creates random forest regressor, linear regression and gradient boosting regressor models
forest_model = RandomForestRegressor()
linear_model = LinearRegression()
gradient_model = GradientBoostingRegressor()

#Search's through all the combinations of hyperparameters to find the combination that gives the best mean_absolute error does this for all the models
grid_search_forest = GridSearchCV(
    estimator=forest_model,
    param_grid=param_grid_forest,
    cv=5,
    scoring="neg_mean_absolute_error",
    n_jobs=-1
)

grid_search_linear = GridSearchCV(
    estimator=linear_model,
    param_grid=param_grid_linear,
    cv=5,
    scoring="neg_mean_absolute_error",
    n_jobs=-1
)

grid_search_gradient = GridSearchCV(
    estimator=gradient_model,
    param_grid=param_grid_gradient,
    cv=5,
    scoring="neg_mean_absolute_error",
    n_jobs=-1
)

#Trains the models on all the different hyperparameter combinations to find the best combination for each model 
grid_search_forest.fit(X_train, Y_train)
grid_search_linear.fit(X_train, Y_train)
grid_search_gradient.fit(X_train, Y_train)

#Sets the models to the ones with the best combination of hyperparameters
forest_model = grid_search_forest.best_estimator_
linear_model = grid_search_linear.best_estimator_
gradient_model = grid_search_gradient.best_estimator_

#Prints the best hyperparameter combination for each individual model
print(f"Best hyperparameters forest: {grid_search_forest.best_params_}")
print(f"Best hyperparameters linear: {grid_search_linear.best_params_}")
print(f"Best hyperparameters gradient: {grid_search_gradient.best_params_}")

#Predicts the house price for each data set in the test set for each model 
forest_predictions = forest_model.predict(X_test)
linear_predictions = linear_model.predict(X_test)
gradient_predictions = gradient_model.predict(X_test)

#The scores from testing the models
#mae - is the average error in the price that the model predicts
#mse - is the average squared difference in the prices that the model predicts (THIS IS IMPORTANT AS BIGGER ERRORS IN THE PRICES HAVE MORE OF AN IMPACT ON THE SCORE)
#rmse - is the square root of the mse value and it measures the prediction error in pounds making it easier to understand
#r2 - this is how well the model determines the houses prices compared with just predicting the average of all the house prices (A VALUE OF 1 IS THE BEST HERE)
forest_mae = mean_absolute_error(Y_test, forest_predictions)
forest_mse = mean_squared_error(Y_test, forest_predictions)
forest_rmse = np.sqrt(forest_mse)
forest_r2 = r2_score(Y_test, forest_predictions)

linear_mae = mean_absolute_error(Y_test, linear_predictions)
linear_mse = mean_squared_error(Y_test, linear_predictions)
linear_rmse = np.sqrt(linear_mse)
linear_r2 = r2_score(Y_test, linear_predictions)

gradient_mae = mean_absolute_error(Y_test, gradient_predictions)
gradient_mse = mean_squared_error(Y_test, gradient_predictions)
gradient_rmse = np.sqrt(gradient_mse)
gradient_r2 = r2_score(Y_test, gradient_predictions)

#Prints out the calculated values/scores
print("\nRandom forest regressor")
print (f"Mean absolute error: {round(forest_mae, 2)}")
print (f"Root mean squared error: {round(forest_rmse, 2)}")
print (f"r^2 Score: {round(forest_r2, 5)}")

print("\nLinear Regression")
print (f"Mean absolute error: {round(linear_mae, 2)}")
print (f"Root mean squared error: {round(linear_rmse, 2)}")
print (f"r^2 Score: {round(linear_r2, 5)}")

print("\nGradient Boosting Regressor")
print (f"Mean absolute error: {round(gradient_mae, 2)}")
print (f"Root mean squared error: {round(gradient_rmse, 2)}")
print (f"r^2 Score: {round(gradient_r2, 5)}")