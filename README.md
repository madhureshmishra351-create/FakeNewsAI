# Fake News Detection using Hybrid Deep Learning and Online Verification

This project aims to detect fake news using a combination of a fine-tuned DistilBERT model and real-time online verification from trusted sources. The goal is to build a system that not only predicts news authenticity using machine learning but also cross-checks the claim using live data from Wikipedia, GNews, and Google Fact Check APIs.

The project includes offline training, testing, evaluation, hybrid prediction logic, and a Streamlit web interface for manual testing.

## 1. Project Overview

Fake news detection is a challenging problem because AI models often fail with new or unseen news. To address this, the project uses a hybrid approach:

1. An offline trained DistilBERT model for fake/real classification.
2. Online verification of the user-entered news using:

   * Wikipedia summary
   * GNews live articles
   * Google Fact Check API

The hybrid logic combines all three sources to produce a more reliable final verdict.

## 2. Dataset Used

The model is trained using the **WELFake Dataset**, which consists of both real and fake news articles.

* Total dataset size: 72,000+ records
* Includes title, text, and label
* Label 1 = Fake, Label 0 = Real

The dataset was split into training and testing using an 80:20 ratio.

## 3. Model Used

The project uses:

* DistilBERT (distilbert-base-uncased)
* Fine-tuned for binary classification
* Training was done for one epoch with AdamW optimizer and learning rate of 2e-5

The trained model is saved in `models/best_model/`.

## 4. Evaluation Results

The model was evaluated on 14,427 test samples.

**Results:**

* Accuracy: 98.93%
* Precision: 98.76%
* Recall: 99.13%
* F1-Score: 98.95%

**Confusion Matrix:**

|             | Predicted Real | Predicted Fake |
| ----------- | -------------- | -------------- |
| Actual Real | 6998           | 91             |
| Actual Fake | 64             | 7274           |

The model performs strongly on both classes with minimal false positives and false negatives.

---

## 5. Hybrid Verification System

Since offline models can still make mistakes on new topics, the project includes a hybrid verification stage.

For user-entered news:

1. The offline model predicts FAKE or REAL with confidence.
2. The system checks the claim online through:

   * Wikipedia API search
   * GNews API for recent news articles
   * Google Fact Check Tools API

Hybrid logic:

* If any fact-check source marks the claim as false → Final result is FAKE.
* If Wikipedia strongly matches the topic → Mark as TRUE.
* If live news articles support the claim → Mark as TRUE.
* If offline model says fake but no evidence online → Mark as UNCERTAIN.
* Otherwise, fallback to the AI prediction.

This hybrid approach significantly increases overall reliability.

## 6. Folder Structure

FakeNews-main/
│
├── data/
│   ├── WELFake_Dataset.csv
│   ├── train.csv
│   └── test.csv
│
├── models/
│   └── best_model/
│
├── dataset.py
├── train_distilbert.py
├── evaluate_model.py
├── local_test.py
├── fact_check.py
├── online_sources.py
├── hybrid_predict.py
├── online_verify.py
├── preprocess.py
├── streamlit_app.py
├── make_test_split.py
├── utils.py
└── test_api.py

## 7. How to Run the Project

### Step 1: Create and activate a virtual environment

Windows:

python -m venv venv
.\venv\Scripts\activate

### Step 2: Install required libraries

pip install -r requirements.txt

### Step 3: Train the model (optional)

python train_distilbert.py

### Step 4: Evaluate the model

python make_test_split.py
python evaluate_model.py

### Step 5: Run the hybrid verification system

python online_verify.py

### Step 6: Run the Streamlit app

streamlit run streamlit_app.py

## 8. Features Implemented

* Text preprocessing and cleaning
* Dataset merging
* Train/test splitting
* Fine-tuning DistilBERT for classification
* Model evaluation with accuracy, precision, recall, F1
* Hybrid online verification using three APIs
* Streamlit interface for end-users
* Modular and clean code structure

## 9. Limitations

* Offline model accuracy depends on dataset quality.
* Wikipedia and GNews can sometimes return unrelated pages.
* Free API rate limits may restrict the number of online checks per day.
* Hybrid system relies on internet connectivity.

## 10. Future Improvements

* Replace DistilBERT with a stronger model like DeBERTa-v3.
* Add semantic similarity (sentence transformers) for better Wikipedia matching.
* Include more news APIs for better verification.
* Add better UI/UX for the Streamlit application.
* Deploy the system online.


