import json
import os
from typing import List, Dict
import hashlib


class DataProcessor:
    def __init__(self, max_chunk_size: int = 1000, chunk_overlap: int = 200):
        self.max_chunk_size = max_chunk_size
        self.chunk_overlap = chunk_overlap

    def load_data(self, file_path: str) -> List[Dict]:
        """Load JSON data from file"""
        with open(file_path, 'r', encoding='utf-8') as f:  # Add encoding here
            data = json.load(f)
        return data

    def flattened_data(self, raw_data):
        flat_articles = []
        for ticker, articles in raw_data.items():
            for article in articles:
                article['ticker'] = ticker
                flat_articles.append(article)
        return flat_articles

    def chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0

        while start < len(text):
            end = min(start + self.max_chunk_size, len(text))
            chunk = text[start:end]
            chunks.append(chunk)

            if end == len(text):
                break

            start = end - self.chunk_overlap

        return chunks

    def process_articles(self, articles: List[Dict]) -> List[Dict]:
        """Process articles into chunks with metadata"""
        processed = []
        for article in articles:
            chunks = self.chunk_text(article['full_text'])

            for i, chunk in enumerate(chunks):
                processed.append({
                    'id': f"{hashlib.md5(article['link'].encode()).hexdigest()}_{i}",
                    'title': article['title'],
                    'ticker': article.get('ticker', ''),
                    'link': article['link'],
                    'chunk': chunk,
                    'chunk_num': i,
                    'total_chunks': len(chunks)
                })
        return processed

    def save_processed_data(self, data: List[Dict], output_path: str):
        """Save processed data to JSON file"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)