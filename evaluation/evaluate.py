from app.main import FinancialNewsQA
import json
from pathlib import Path
from typing import Dict, List
import time


class Evaluator:
    def __init__(self):
        self.qa_system = FinancialNewsQA()

    def load_test_questions(self, path: str) -> List[Dict]:
        """Load test questions with expected answers"""
        with open(path, 'r') as f:
            return json.load(f)

    def evaluate_model(self, model: str, prompt_style: str, test_questions: List[Dict]) -> Dict:
        """Evaluate a model/prompt combination"""
        results = []
        total_latency = 0

        for question_data in test_questions:
            start_time = time.time()
            response = self.qa_system.answer_question(
                question=question_data['question'],
                model=model,
                prompt_style=prompt_style
            )
            latency = time.time() - start_time
            total_latency += latency

            results.append({
                'question': question_data['question'],
                'expected_answer': question_data.get('expected_answer'),
                'actual_answer': response['answer'],
                'latency': latency,
                'context_used': response['context_article_title'],
                'is_correct': self._check_answer(
                    question_data.get('expected_answer'),
                    response['answer']
                )
            })

        accuracy = sum(1 for r in results if r['is_correct']) / len(results)
        avg_latency = total_latency / len(results)

        return {
            'model': model,
            'prompt_style': prompt_style,
            'accuracy': accuracy,
            'average_latency': avg_latency,
            'results': results
        }

    def _check_answer(self, expected: str, actual: str) -> bool:
        """Simple answer checking (would be more sophisticated in production)"""
        if not expected:
            return True  # No expected answer to compare against

        expected_lower = expected.lower()
        actual_lower = actual.lower()

        # Simple check if expected answer is contained in actual answer
        return expected_lower in actual_lower

    def run_full_evaluation(self, test_questions_path: str, output_path: str):
        """Run evaluation across all models and prompts"""
        test_questions = self.load_test_questions(test_questions_path)

        models = ['openai', 'anthropic']
        prompts = ['basic_qa', 'financial_expert', 'cautious_answer']

        evaluation_results = []

        for model in models:
            for prompt in prompts:
                print(f"Evaluating {model} with {prompt} prompt...")
                result = self.evaluate_model(model, prompt, test_questions)
                evaluation_results.append(result)

        # Save results
        with open(output_path, 'w') as f:
            json.dump(evaluation_results, f, indent=2)

        return evaluation_results