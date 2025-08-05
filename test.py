from app.main import FinancialNewsQA


def main():
    qa = FinancialNewsQA()

    questions = [
            "What was AAPL 's Q4 revenue?",
            "How did Apple's stock react to the earnings report?",
            "What did the Fed minutes suggest about future rate hikes?",
            "Whats the name of the actor that played spiderman?",
            "&&&&&&&&&&"
    ]

    for question in questions:
        print(f"\nQuestion: {question}")
        response = qa.answer_question(question)
        print(f"Answer: {response['answer']}")
        print(f"Source: {response['context_article_title']}")
        print(f"Model: {response['model']}")
        print(f"Latency: {response['latency']:.2f}s")


if __name__ == "__main__":
    main()