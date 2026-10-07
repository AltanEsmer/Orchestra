import platform

import sklearn
from scipy.sparse import issparse
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

train_queries = [
    "What is the capital of Denmark?",
    "Explain how rain forms.",
    "What is the capital of France?",
]
train_labels = ["simple", "complex", "simple"]
held_out_queries = ["Explain quasar formation.", "What is the capital of Sweden?"]

vectorizer = TfidfVectorizer()
train_features = vectorizer.fit_transform(train_queries)
held_out_features = vectorizer.transform(held_out_queries)

assert issparse(train_features)
assert issparse(held_out_features)
assert train_features.shape[0] == len(train_labels)
assert held_out_features.shape == (2, train_features.shape[1])
assert train_features.nnz > 0
assert held_out_features.nnz > 0
assert "quasar" not in vectorizer.vocabulary_

classifier = DummyClassifier(strategy="most_frequent")
classifier.fit(train_features, train_labels)
assert classifier.predict(held_out_features).tolist() == ["simple", "simple"]

print(
    "PASS: environment-smoke-only; sparse TF-IDF, held-out vocabulary isolation, "
    "and toy DummyClassifier predictions verified."
)
print(f"Python {platform.python_version()}; scikit-learn {sklearn.__version__}")
