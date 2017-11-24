from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import time

categories = ['alt.atheism', 'sci.space', 'comp.graphics',
              'rec.motorcycles', 'sci.electronics']
news = fetch_20newsgroups(remove=("headers", "footers", "quotes"),
                          categories=categories)

vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(news.data)
clf = MultinomialNB(alpha=0.01)
clf.fit(vectors, news.target)
pickle.dump({"vectorizer": vectorizer, "model": clf}, open("nb_model", "wb"))

# pred = clf.predict(vectorizer.transform([news.data[-1]]))
# print news.target_names[pred[0]]
