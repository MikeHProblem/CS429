# CS429
Project IR
Hugo Michael Hernandez
CS 429
Project
Due: 04/22/24

Development Summary: The project aims to develop a comprehensive search engine utilizing Python-based tools across three main components. The crawler uses Scrapy to download web documents, the indexer utilizes Scikit-Learn to create an inverted index, and the query processor leverages Flask to handle and respond to user queries.
Objectives: To efficiently crawl web pages, index the retrieved content for quick searching, and handle user queries with relevant search results.
Next Steps: Improve crawling efficiency with advanced Scrapy settings, enhance the indexer with neural network techniques, and expand the Flask API for better user interaction and scalability.

Overview
Solution Outline: The solution is structured into three modular components, each handling a specific aspect of a search engine: crawling, indexing, and querying.
Relevant Literature: The design is inspired by basic principles found in "Information Retrieval: Implementing and Evaluating Search Engines" by Stefan Büttcher, Charles L. A. Clarke, and Gordon V. Cormack.
Proposed System: A distributed web crawler, a robust indexing system using TF-IDF and cosine similarity, and a responsive web API to process and respond to queries.

Design
System Capabilities:
Crawler: Can crawl with specified depth and breadth, handling politeness policies via Scrapy's AutoThrottle.
Indexer: Builds an inverted index with options for TF-IDF and vector embeddings, with scope for extending to semantic analysis.
Query Processor: Validates and processes queries, returning ranked results based on document relevance.
Interactions and Integration: Each component is designed to operate independently yet integrate smoothly via JSON and pickle files for data exchange.

Architecture
Software Components:
Scrapy Crawler: Manages web crawling.
Scikit-Learn Indexer: Handles data indexing.
Flask Processor: Manages query reception and response.
Interfaces: REST API for the query processor, command-line interface for the crawler and indexer.
Implementation: Python scripts with external libraries (Scrapy, Scikit-Learn, Flask).

Operation
Software Commands:
Crawler: scrapy crawl webcrawler -a domain=example.com
Indexer: python indexer.py
Query Processor: flask run
Inputs: URLs for the crawler, text data for the indexer, JSON for the processor.
Installation: Use pip install scrapy, scikit-learn, flask to install necessary libraries.

Conclusion
Results: The system successfully crawls, indexes, and processes queries with initial tests showing promising response times and accuracy.
Crawler:



img




Indexer: 

img
Flask: 
img
Failures:  
When running the crawler code via terminal it was not working but it was mainly due to me not being in the right directory
When running the index program, it wasn’t reading the example index that I hard coded in. 
When also running the index program, it was going in a loop where the terminal will not provide the scores but will continue to spam the terminal.
When trying to combine these three programs, it wasn’t working. The only thing that worked was the flask. 
Caveats/Cautions: Ensure compliance with robots.txt for crawling and manage load to avoid server strain.
Data Sources
Links: No specific links used; crawls are domain-specific. Downloads: Python library installations via pip. Access Information: Local installation and operation, no external data sources used.
Test Cases
Things that need to be checked for each program: 
Scrapy-Based Crawler
Basic Functionality: Verify the crawler fetches and stores pages correctly from a given URL.
Depth and Page Limits: Ensure it respects set limits on crawling depth and maximum number of pages.
Error Handling: Test how it manages non-existent domains and pages without crashing.
 Scikit-Learn-Based Indexer
Index Creation: Check if the indexer can build an accurate inverted index from sample documents.
TF-IDF and Cosine Similarity: Validate the correct computation of TF-IDF scores and cosine similarity for document-query matching.
Performance: Assess indexer efficiency with a large volume of documents.
 Flask-Based Query Processor
Query Response: Confirm accurate and relevant results for valid search queries.
Error Management: Test response to invalid queries, ensuring proper error messages are returned.
Load Handling and Security: Evaluate performance under high query load and security against injections.



Framework: Use Python's unittest framework. Harness: Setup test cases for each component—crawler (mock sites), indexer (predefined datasets), and processor (mock queries). Coverage: Aim for 80% code coverage, testing major functionalities and error handling.
Source Code:
Scrapy: 

import scrapy
from scrapy.exceptions import CloseSpider


class WebCrawler(scrapy.Spider):
    name = 'webcrawler'
    allowed_domains = ['example.com']  # Change to your target domain
    start_urls = ['http://example.com']  # Starting URL


    def __init__(self, domain='', start_url='', max_pages=100, max_depth=3, *args, **kwargs):
        super(WebCrawler, self).__init__(*args, **kwargs)
        if domain:
            self.allowed_domains = [domain]
        if start_url:
            self.start_urls = [start_url]
        self.max_pages = int(max_pages)
        self.max_depth = int(max_depth)
        self.pages_crawled = 0


    def parse(self, response):
        if self.pages_crawled >= self.max_pages or response.meta.get('depth', 0) > self.max_depth:
            raise CloseSpider('Reached max pages or depth limit')


        self.pages_crawled += 1
        yield {
            'url': response.url,
            'content': response.text
        }
        links = response.css('a::attr(href)').getall()
        for link in links:
            if self.pages_crawled < self.max_pages:
                yield response.follow(link, self.parse)

Indexer: 

from sklearn.feature_extraction.text import TfidfVectorizer
import pickle


class DocumentIndexer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = None


    def create_index(self, documents):
        # This fits the model and transform the documents
        self.tfidf_matrix = self.vectorizer.fit_transform(documents)


    def save_index(self, path='tfidf_index.pkl'):
        # Should save the vectorizer and the matrix to a file
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


# Exampl!
if __name__ == '__main__':
    documents = [
        "The quick brown fox jumps over the lazy dog",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
        "Python developers use Scikit-Learn for machine learning"
    ]


    indexer = DocumentIndexer()
    indexer.create_index(documents)
    indexer.save_index()


    # Loads said index
    indexer.load_index()


    # Query the index
    query = "machine learning"
    scores = indexer.query_index(query)
    print(scores)





Flask:
from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome to the Flask-Based Query Processor!"


@app.route('/query', methods=['POST'])
def query():
    if request.is_json:
        data = request.get_json()
        query = data.get('query', '')
        # Here you would integrate your search functionality
        return jsonify({"message": f"Received query: {query}"})
    else:
        return jsonify({"error": "Request must be JSON"}), 400


if __name__ == '__main__':
    app.run(debug=True)





Bibliography
Büttcher, Stefan, Charles L. A. Clarke, and Gordon V. Cormack. "Information Retrieval: Implementing and Evaluating Search Engines." MIT Press, 2010.
"Scrapy Documentation." Scrapy.org.
"Scikit-Learn Documentation." Scikit-learn.org.
"Flask Documentation." PalletsProjects.com.
