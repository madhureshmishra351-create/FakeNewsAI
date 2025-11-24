# Problem Statement

The rapid spread of misinformation and fake news across digital platforms has become a major challenge in recent years. Social media users frequently share unverified news, leading to widespread misinformation and negative societal impact. Traditional machine learning models struggle to detect newly emerging or evolving fake news topics, and fully manual verification is slow, unreliable, and not scalable.

This project aims to address these challenges by building a hybrid fake news detection system that combines an offline deep learning model with online verification from trusted sources. The intent is to create a system that not only classifies news using a fine-tuned language model but also cross-checks the claim in real time using live information from the internet.

# Objective

The main objectives of this project are as follows:

1. Develop a machine learning model capable of classifying news articles as real or fake.
2. Fine-tune a DistilBERT transformer model on the WELFake dataset.
3. Evaluate the performance of the model using accuracy, precision, recall, and F1-score.
4. Integrate online verification via:

   * Wikipedia API
   * GNews API
   * Google Fact Check Tools API
5. Build a hybrid prediction system that combines AI classification with real-time fact verification.
6. Provide a Streamlit-based user interface for end-users to test and verify news.

# Scope of the Project

The project focuses on detecting fake textual news articles. It does not cover images, videos, or multimodal misinformation. The system is limited to English language news and relies on third-party APIs for real-time fact-checking. The hybrid system increases reliability but works within the constraints of free-tier API limits.

# Expected Outcomes

1. A trained DistilBERT model capable of classifying news with high accuracy.
2. A hybrid verification system that cross-checks news authenticity using online sources.
3. A user-friendly Streamlit application that allows real-time testing.
4. A performance report including accuracy, precision, recall, F1-score, and confusion matrix.
5. Improved reliability in detecting fake news compared to a standalone machine learning model.
