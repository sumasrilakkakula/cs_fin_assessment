import anthropic
from typing import Dict
import time
from config import Config


class AnthropicHandler:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        self.model = Config.ANTHROPIC_MODEL

    def generate_answer(self, context: str, question: str, prompt_template: str) -> Dict:
        """Generate answer using Anthropic model"""
        prompt = prompt_template.format(context=context, question=question)

        start_time = time.time()
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        latency = time.time() - start_time

        return {
            'answer': response.content[0].text,
            'latency': latency,
            'model': self.model,
            'prompt': prompt
        }