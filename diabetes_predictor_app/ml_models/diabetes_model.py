# predictions/ml_models/diabetes_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle

# Load the dataset
def train_model():
    url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
    column_names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
    data = pd.read_csv(url, names=column_names)

    # Split dataset into features and target
    X = data.drop("Outcome", axis=1)
    y = data["Outcome"]

    # Split into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the logistic regression model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # Save the trained model
    with open("diabetes_predictor_app/ml_models/diabetes_model.pkl", "wb") as file:
        pickle.dump(model, file)

    return "Model trained and saved successfully!"

if __name__ == '__main__':
    print(train_model())
