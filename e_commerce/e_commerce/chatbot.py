import nltk 
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from django.db.models import F
from inventory.models import *

# Download required nltk resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')


class CollectDatas:
    def __init__(self):
        try:
            self.product_details = list(
                ProductDetails.objects.select_related("category")
                .annotate(
                    product_id=F("id"),  # alias id as product_id
                    category_name=F("category__category_name")
                )
                .values(
                    "product_id",
                    "product_name",
                    "description",
                    "price",
                    "offer",
                    "category_name"
                )
            )
            print(self.product_details)
        except Exception as e:
            print("Error in Collect Database ", e)
            self.product_details = None

    def dataset_processing(self):
        """Return dataset with structured fields"""
        try:
            if not self.product_details:
                return False
            dataset = []
            for items in self.product_details:
                dataset.append({
                    "product_id": items['product_id'],
                    "product_name": items['product_name'],
                    "description": items['description'],
                    "price": float(items['price']),
                    "offer": items['offer'],
                    "category_name": items['category_name']
                })
            return dataset
        except Exception as e:
            print("Error in dataset_processing:", e)
            return []


class ChatBot(CollectDatas):
    def __init__(self):
        super().__init__()
        self.stop_words = stopwords.words('english')
        self.lemmatizer = WordNetLemmatizer()
        self.vectorizer = TfidfVectorizer()    
        self.tfidf_matrix = None
        self.dataset = None
        self.texts = None

    def preprocessing(self, text):
        """Clean and tokenize text"""
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return text
    
    def apply_lemmatization(self, sentence):
        split_words = sentence.split()
        return [self.lemmatizer.lemmatize(word, pos=self.apply_pos_tag(word))  
                for word in split_words if word not in self.stop_words]
        
    def apply_pos_tag(self, word):
        pos_tag = nltk.pos_tag([word])
        _, tag = pos_tag[0]
        if tag.startswith('NN'):
            return 'n'
        elif tag.startswith('VB'):
            return 'v'
        elif tag.startswith('JJ'):
            return 'a'
        elif tag.startswith('RB'):
            return 'r'
        else:
            return 'n'

    def build_corpus(self, dataset):
        """Build corpus of product_name + description"""
        texts = []
        for item in dataset:
            combined = f"{item['product_name']} {item['description']} {item['category_name']} "
            cleaned = self.preprocessing(combined)
            lemmatized = self.apply_lemmatization(cleaned)
            texts.append(" ".join(lemmatized))
        return texts

    def train_model(self):
        """Prepare TF-IDF matrix"""
        self.dataset = self.dataset_processing()
        if not self.dataset:
            return None
        
        self.texts = self.build_corpus(self.dataset)
        self.tfidf_matrix = self.vectorizer.fit_transform(self.texts)
        

    def calculate_similarity(self, user_query, tfidf_matrix):
        """Vectorize query and compute similarity scores"""
        query = self.preprocessing(user_query)
        lemmatized_query = " ".join(self.apply_lemmatization(query))
        query_tfidf = self.vectorizer.transform([lemmatized_query])
        similarity_scores = cosine_similarity(query_tfidf, tfidf_matrix)
        return similarity_scores[0]

    def extract_price_constraint(self, query):
        """Extract price condition from query (e.g. under 5000, above 10000)"""
        match = re.search(r'(\d+)', query)
        if not match:
            return None, None
        
        price = int(match.group(1))
        if "under" in query or "below" in query or "less" in query:
            return "under", price
        elif "above" in query or "over" in query or "greater" in query:
            return "above", price
        else:
                return None, None
    def search_products(self, user_query, n=5, threshold=0.2):
        similarity_scores = self.calculate_similarity(user_query, self.tfidf_matrix)
        top_indices = np.argsort(similarity_scores)[::-1]

        condition, limit = self.extract_price_constraint(user_query)

        results = []
        for idx in top_indices:
            score = similarity_scores[idx]
            if score < threshold:   # Ignore irrelevant results
                continue

            product = self.dataset[idx]

            if condition == "under" and product["price"] > limit:
                continue
            if condition == "above" and product["price"] < limit:
                continue

            results.append(product)
            if len(results) == n:
                break

        if not results:
            return [{"product_id": None, "product_name": "No relevant products found", "price": "-", "offer": "-"}]

        return results

    def run(self,user_query):

        if self.tfidf_matrix is None or self.dataset is None:
            if not self.train_model():
                return None

        search_results = self.search_products(user_query, n=5)

        print(f"Search results for '{user_query}':")
        product_details=[]
        for result in search_results:
            product_details.append({"product_id":result['product_id']})

        return product_details

