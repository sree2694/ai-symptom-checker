import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder
import joblib
import numpy as np

# Load the dataset
def load_data():
    return pd.read_csv('data/symptom_disease_dataset.csv',encoding='latin1')


# Preprocessing and training the model
def train_model():
    df = load_data()

    # Separate features and target
    X = df.drop(columns=['Disease'])  # All symptom columns
    y = df['Disease']                 # Target Disease

    # Encode Disease labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # Train a RandomForestClassifier
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y_encoded)

    # Save the model and the encoder
    joblib.dump(model, 'symptom_disease_model.pkl')
    joblib.dump(label_encoder, 'disease_encoder.pkl')

def preprocess_data(df):
    # Make a copy to avoid changes to original
    df_copy = df.copy()

    # If columns are multi-symptom strings, we create binary indicators
    symptom_columns = df_copy.columns.drop('Disease')

    for col in symptom_columns:
        # If cell is a string and contains the symptom name -> 1 else 0
        df_copy[col] = df_copy[col].apply(
            lambda x: 1 if isinstance(x, str) and col in x else 0
        )

    return df_copy

# Function to predict disease from symptoms
def predict_disease(symptoms: list[str]):
    try:
        model = joblib.load('symptom_disease_model.pkl')
        label_encoder = joblib.load('disease_encoder.pkl')

        df = load_data()
        symptom_columns = df.columns.drop('Disease')

        input_data = {col: 1 if col in symptoms else 0 for col in symptom_columns}
        input_vector = pd.DataFrame([input_data])

        prediction = model.predict(input_vector)
        predicted_disease = label_encoder.inverse_transform(prediction)

        return predicted_disease[0]

    except Exception as e:
        print(f"Error in prediction: {e}")
        return None

    
    
# Add this to the end of ml_model.py to train the model once

if __name__ == "__main__":
    train_model()  # Call the function to train the model
