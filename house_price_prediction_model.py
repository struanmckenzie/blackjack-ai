import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


#Get the dataset from the csv file
dataset = pd.read_csv("houses/house_price_regression_dataset.csv")
#print(dataset[dataset.duplicated()])

#Get the headings from the data set and separate the house price values as thats the value we are trying to predict
x = dataset[["Square_Footage", "Num_Bedrooms", "Num_Bathrooms", "Year_Built", "Lot_Size", "Garage_Size", "Neighborhood_Quality"]]
y = dataset["House_Price"]

#Spilt the data set into 2 one for the training set and other for testing it is currently set as 80% for training and 20% for testing
X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.2, random_state=42)

#This is a list of hyperparameters that will be used when training the model
#These are here so we can test different combinations of hyperparameters so we can find the combination that gives the best score
param_grid = {
    "n_estimators": [1, 50, 100, 1000],
    "max_depth": [None, 1, 10],
    "min_samples_split": [2, 5],
    "min_samples_leaf": [1, 2,]
}

#Creates a random forest regressor model
forest_model = RandomForestRegressor(random_state=42)
linear_model = LinearRegression()
gradient_model = GradientBoostingRegressor()

#Search's through all the combinations of hyperparameters to find the combination that gives the best mean_absolute error
grid_search = GridSearchCV(
    estimator=forest_model,
    param_grid=param_grid,
    cv=5,
    scoring="neg_mean_absolute_error",
    n_jobs=-1
)

#Trains the model on all the different hyperparameter combinations to find the best combination 
grid_search.fit(X_train, Y_train)
linear_model.fit(X_train, Y_train)
gradient_model.fit(X_train, Y_train)

#Sets the model to the random forest regressor with the best combination of hyperparameters
model = grid_search.best_estimator_

print(f"Best hyperparameters: {grid_search.best_params_}")

#Uses the model to predict the prices of the houses within the test data set
forest_predictions = model.predict(X_test)
linear_predictions = linear_model.predict(X_test)
gradient_predictions = gradient_model.predict(X_test)

#The scores from testing the model
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

#Prints out the calculated values
print("\nRandom forest regressor")
print (f"Mean absolute score: {round(forest_mae, 2)}")
print (f"Root mean squared error: {round(forest_rmse, 2)}")
print (f"r^2 Score: {round(forest_r2, 5)}")

print("\nLinear Regression")
print (f"Mean absolute score: {round(linear_mae, 2)}")
print (f"Root mean squared error: {round(linear_rmse, 2)}")
print (f"r^2 Score: {round(linear_r2, 5)}")

print("\nGradient Boosting Regressor")
print (f"Mean absolute score: {round(gradient_mae, 2)}")
print (f"Root mean squared error: {round(gradient_rmse, 2)}")
print (f"r^2 Score: {round(gradient_r2, 5)}")

#3268,4,2,1983,3.1087902476038645,2,2,742599.2533323644
#add this back to the original file when done

#This is just test code and can be used to input details for a house and the model will predict what the price if the house is
new_house = pd.DataFrame({
    "Square_Footage": [3268], 
    "Num_Bedrooms": [4], 
    "Num_Bathrooms": [2], 
    "Year_Built": 1983, 
    "Lot_Size": [3.1087902476038645],
    "Garage_Size": [2],
    "Neighborhood_Quality": [2] 
    })

predicted_price = linear_model.predict(new_house)

print(f"The model has predicted that the price of this house will be £{round(predicted_price[0], 2)}")