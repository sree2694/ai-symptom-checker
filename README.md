# 🩺 MedAssist AI – Symptom Checker & Suggestion Tool

A full-stack AI-powered healthcare assistant that uses both Machine Learning and Generative AI (Cohere) to analyze user symptoms and suggest possible conditions and care tips.

---

## 🧠 What is MedAssist AI?

MedAssist AI is a real-time AI/ML application designed to provide accessible and intelligent symptom analysis. It helps users understand potential health conditions based on entered symptoms using:
- **Cohere AI (LLM)** for natural language health suggestions.
- **Supervised ML (Random Forest)** for disease classification based on encoded features.

---

## 🎯 Problem Statement

Many individuals resort to self-diagnosis via search engines, leading to fear or misinformation. This tool aims to:
- Simplify the symptom-to-diagnosis journey.
- Provide more trustworthy, AI-assisted condition suggestions.
- Improve accessibility to basic health insights in real-time.

---

## 🧩 Features

- 🧾 Symptom input form (age, gender, symptoms)
- 🤖 AI-generated care suggestions via Cohere
- 🧠 Traditional ML-based disease prediction
- 🔄 Switch between AI and ML modes
- 💬 Real-time responses with user-friendly interface

---

## 🛠️ Tech Stack

| Layer        | Technology                    |
|--------------|-------------------------------|
| Frontend     | React + Material UI           |
| Backend      | FastAPI (Python)              |
| AI Model     | Cohere (LLM)                  |
| ML Model     | Random Forest (scikit-learn)  |
| Data         | Public health symptom datasets |

---

## 🔍 Architecture Overview

```
flowchart TD
    A[User Inputs: Age, Gender, Symptoms] --> B[Frontend (React Form)]
    B --> C[API Request to FastAPI Backend]
    C --> D{Model Type?}
    D -- Cohere AI --> E[Cohere LLM generates suggestions]
    D -- ML Model --> F[Symptom vectorization + RF prediction]
    E --> G[Return AI Suggestions]
    F --> G[Return Predicted Disease]
    G --> H[Frontend Displays Results]
```

---

## 🧪 Test Cases

### ✅ Valid Submission
- Input: Age = 30, Gender = Male, Symptoms = [headache, fever]
- Output: Condition suggestions or disease classification.

### ❌ Missing Data
- Input: Missing age/gender/symptoms
- Output: Alert prompting user to complete all fields.

### 🚫 Invalid Symptoms
- Input: Age = 25, Gender = Female, Symptoms = [xyz]
- Output: Message: “Unable to recognize symptoms.”

---

## 📦 How to Run Locally

### Backend (FastAPI)
```bash
cd server
venv\Scripts\activate
pip install -r requirements.txt
python models/ml_model.py  # Trains the ML model
uvicorn main:app --reload
```

### Frontend (React)
```bash
cd client
npm install
npm start
```

---

## 📂 Dataset Sources

- [SymCat Symptom-Disease Dataset](https://www.symcat.com/)
- [CDC ICD-10 Code List](https://www.cdc.gov/nchs/icd/icd10.htm)
- [HealthData.gov Public Health Datasets](https://healthdata.gov/)

---

## 🤖 ML Details

| Aspect        | Value                          |
|---------------|---------------------------------|
| Type          | Supervised Learning             |
| Algorithm     | Random Forest Classifier        |
| Features      | Age, Gender, Symptom Vectors    |
| Labels        | Disease Categories              |
| Text Encoding | TF-IDF Vectorization            |

---

## 📌 Project Goals ✅

- ✔️ Use AI/ML for symptom-based prediction
- ✔️ Provide real-time, deployable web application
- ✔️ Address the problem of online self-diagnosis
- ✔️ Apply supervised learning effectively

---

## 📤 Deployment

- APIs secured via environment keys (e.g., Cohere API key)

---

## 🙋 FAQ

- **Q:** Is this an AI/ML project?  
  **A:** Yes. It uses both supervised ML and generative AI.

- **Q:** Is this a real-time app?  
  **A:** Yes. It gives real-time feedback via frontend APIs.

- **Q:** What ML model is used?  
  **A:** Random Forest Classifier (Supervised Learning)

---

## 👨‍💻 Author

**Your Name**  
[GitHub](https://github.com/sree2694) | [LinkedIn](https://www.linkedin.com/in/sreekanth-j-developer/)

---

## 📃 License

Apache-2.0 License – free to use, modify, and share.