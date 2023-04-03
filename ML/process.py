import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import joblib


class ProcessData:

    def process(text):
        text = text.lower()

        text = ''.join(char for char in text if char.isalnum()
                       or char.isspace())
        tokens = text.split()
        stop_words = set(['a', 'an', 'the', 'in', 'on', 'at', 'to',
                          'from', 'by', 'for', 'of', 'was', 'were', 'is', 'am'])
        tokens = [token for token in tokens if token not in stop_words]
        text = ' '.join(tokens)
        return text
    df = pd.read_csv('./ML/dataset/emails.csv')

    df['text'] = df['text'].apply(process)

    X_train, X_test, y_train, y_test = train_test_split(
        df['text'], df['spam'], random_state=0)

    vectorizer = CountVectorizer()

    X_train_vector = vectorizer.fit_transform(X_train)
    X_test_vector = vectorizer.transform(X_test)

    def messages(email):
        model = joblib.load("./ML/trainedModel/spam_classifier_model.joblib")
        new_email = email
        processed_text = ProcessData.process(new_email)
        new_email_vector = ProcessData.vectorizer.transform(
            [processed_text])

        # Use the trained model to predict whether the new email is spam or not
        prediction = model.predict(new_email_vector)[0]
        print("Prediction:", prediction)
        
        return prediction
