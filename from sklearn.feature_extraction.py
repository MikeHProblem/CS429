from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

class DocumentIndexer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = None

    def create_index(self, documents):
        # Fit the model and transform the documents
        self.tfidf_matrix = self.vectorizer.fit_transform(documents)

    def save_index(self, path='tfidf_index.pkl'):
        # Save the vectorizer and the matrix to a file
        with open(path, 'wb') as f:
            pickle.dump((self.vectorizer, self.tfidf_matrix), f)

    def load_index(self, path='tfidf_index.pkl'):
        # Load the vectorizer and the matrix from the file
        with open(path, 'rb') as f:
            self.vectorizer, self.tfidf_matrix = pickle.load(f)

    def query_index(self, query):
        # Convert the query to the same vector space as the documents
        query_vector = self.vectorizer.transform([query])
        # Compute the cosine similarities
        cosine_similarities = (query_vector * self.tfidf_matrix.T).toarray()[0]
        return cosine_similarities

# Example usage
if __name__ == '__main__':
    documents = [
        "The quick brown fox jumps over the lazy dog",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
        "Python developers use Scikit-Learn for machine learning"
    ]

    indexer = DocumentIndexer()
    indexer.create_index(documents)
    indexer.save_index()

    # Load the index (if starting from a saved state)
    indexer.load_index()

    # Query the index
    query = "machine learning"
    scores = indexer.query_index(query)
    print(scores)
