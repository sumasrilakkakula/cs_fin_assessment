from models.openai_handler import OpenAIHandler
from models.anthropic_handler import AnthropicHandler
from app.data_processor import DataProcessor
import json
import os
from typing import Dict, List
from pathlib import Path


class FinancialNewsQA:
    def __init__(self):
        self.data_processor = DataProcessor()
        self.openai = OpenAIHandler()
        self.anthropic = AnthropicHandler()

        # Load prompts
        self.prompts = self._load_prompts()

    def _load_prompts(self) -> Dict[str, str]:
        """Load prompt templates from files"""
        prompts = {}
        prompt_dir = Path(__file__).parent.parent / "prompts"

        for prompt_file in prompt_dir.glob("*.txt"):
            with open(prompt_file, 'r') as f:
                prompts[prompt_file.stem] = f.read()

        return prompts

    def load_and_process_data(self, data_path: str) -> List[Dict]:
        """Load and process raw data"""
        raw_data = self.data_processor.load_data(data_path)
        flattened_data = self.data_processor.flattened_data(raw_data)
        processed_data = self.data_processor.process_articles(flattened_data)
        return processed_data

    def find_relevant_context(self, question: str, processed_data: List[Dict]) -> Dict:
        """
        Simple keyword-based context finder.
        In production, this would use embeddings and vector search.
        """
        # Simple implementation - in reality would use embeddings
        question_lower = question.lower()

        # Prioritize articles with matching tickers
        ticker_match = []
        for article in processed_data:
            if article['ticker'] and article['ticker'].lower() in question_lower:
                ticker_match.append(article)
        print(ticker_match)
        if ticker_match:
            return ticker_match[0]  # Return first match

        # Fall back to title/keyword match
        for article in processed_data:
            if article['title'].lower() in question_lower:
                return article

        # Return first article if no matches (for demo)
        return processed_data[0]

    def answer_question(self, question: str, model: str = "openai", prompt_style: str = "basic_qa") -> Dict:
        """Answer a question using the specified model and prompt style"""
        # Load sample data (in production would use real data)
        processed_data = self.load_and_process_data("data/raw/stock_news.json")

        # Find relevant context
        context_article = self.find_relevant_context(question, processed_data)
        context = f"Title: {context_article['title']}\nTicker: {context_article['ticker']}\nContent: {context_article['chunk']}"

        # Get the selected prompt
        prompt_template = self.prompts.get(prompt_style, self.prompts["basic_qa"])

        # Call the appropriate model
        if model.lower() == "openai":
            response = self.openai.generate_answer(context, question, prompt_template)
        elif model.lower() == "anthropic":
            response = self.anthropic.generate_answer(context, question, prompt_template)
        else:
            raise ValueError(f"Unknown model: {model}")

        # Add context metadata to response
        response.update({
            'context_article_title': context_article['title'],
            'context_article_link': context_article['link'],
            'context_article_ticker': context_article['ticker']
        })

        return response