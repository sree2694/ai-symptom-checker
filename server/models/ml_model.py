import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import os

# Define paths
MODEL_DIR = os.path.join(os.path.dirname(__file__), '../data')

# Load the dataset
def load_data():
    df = pd.read_csv(os.path.join(MODEL_DIR, 'symptom_disease_dataset.csv'), encoding='latin1')
    df.columns = df.columns.str.strip().str.lower()
    return df

# Preprocess data: encode categorical and normalize
def preprocess_data(df):
    df_copy = df.copy()

    # Encode gender
    df_copy['gender'] = df_copy['gender'].str.lower()
    gender_encoder = LabelEncoder()
    df_copy['gender'] = gender_encoder.fit_transform(df_copy['gender'])

    # Encode disease
    disease_encoder = LabelEncoder()
    df_copy['disease'] = disease_encoder.fit_transform(df_copy['disease'])

    # Get symptom columns (excluding age, gender, disease)
    symptom_cols = df_copy.columns.difference(['age', 'gender', 'disease'])

    # Convert symptom row to text: "fever headache" etc.
    df_copy['symptom_text'] = df_copy[symptom_cols].apply(
        lambda row: ' '.join(row.index[row == 1]), axis=1
    )

    # Vectorize symptom text
    vectorizer = TfidfVectorizer()
    symptom_vectors = vectorizer.fit_transform(df_copy['symptom_text'])

    # Convert to DataFrame
    X_symptom = pd.DataFrame(symptom_vectors.toarray())

    # Combine with age and gender
    X = pd.concat([
        pd.DataFrame(df_copy[['age', 'gender']].values, columns=['age', 'gender']),
        X_symptom
    ], axis=1)

    X.columns = X.columns.astype(str)
    y = df_copy['disease']

    return X, y, gender_encoder, disease_encoder, vectorizer

# Train the model
def train_model():
    df = load_data()
    X, y, gender_encoder, disease_encoder, vectorizer = preprocess_data(df)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Save model and transformers
    joblib.dump(model, os.path.join(MODEL_DIR, 'symptom_disease_model.pkl'))
    joblib.dump(gender_encoder, os.path.join(MODEL_DIR, 'gender_encoder.pkl'))
    joblib.dump(disease_encoder, os.path.join(MODEL_DIR, 'disease_encoder.pkl'))
    joblib.dump(vectorizer, os.path.join(MODEL_DIR, 'symptom_vectorizer.pkl'))

# Predict disease using the model
def predict_disease(symptoms: list[str], age: int, gender: str):
    try:
        # Load model and encoders
        model = joblib.load(os.path.join(MODEL_DIR, 'symptom_disease_model.pkl'))
        vectorizer = joblib.load(os.path.join(MODEL_DIR, 'symptom_vectorizer.pkl'))
        gender_encoder = joblib.load(os.path.join(MODEL_DIR, 'gender_encoder.pkl'))
        disease_encoder = joblib.load(os.path.join(MODEL_DIR, 'disease_encoder.pkl'))

        # Encode gender
        gender_encoded = gender_encoder.transform([gender.lower()])[0]

        # Vectorize symptoms
        symptom_str = ' '.join(symptoms)
        symptom_vector = vectorizer.transform([symptom_str]).toarray()[0]

        # Combine age, gender, and symptoms into a single input
        input_vector = [age, gender_encoded] + list(symptom_vector)

        # Predict
        prediction = model.predict([input_vector])
        predicted_disease = disease_encoder.inverse_transform(prediction)

        return predicted_disease[0]

    except Exception as e:
        print(f"Error in prediction: {e}")
        return None

# Test cases for the ML model functions
if __name__ == "__main__":
    # Test training model
    try:
        print("Training model...")
        train_model()
        print("Model trained and saved.")
    except Exception as e:
        print(f"Error in model training: {e}")
    
    # Test prediction function
    try:
        test_symptoms = ['fever', 'headache']
        test_age = 25
        test_gender = 'male'
        print(f"Predicting disease for {test_symptoms}...")
        prediction = predict_disease(test_symptoms, test_age, test_gender)
        if prediction:
            print(f"Predicted disease: {prediction}")
        else:
            print("Prediction failed.")
    except Exception as e:
        print(f"Error in prediction test: {e}")
