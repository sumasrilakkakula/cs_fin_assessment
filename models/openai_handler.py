from openai import OpenAI
from typing import List, Dict
import time
from config import Config


class OpenAIHandler:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL

    def generate_answer(self, context: str, question: str, prompt_template: str) -> str:
        """Generate answer using OpenAI model"""
        prompt = prompt_template.format(context=context, question=question)

        start_time = time.time()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a knowledgeable financial assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        latency = time.time() - start_time

        return {
            'answer': response.choices[0].message.content,
            'latency': latency,
            'model': self.model,
            'prompt': prompt
        }