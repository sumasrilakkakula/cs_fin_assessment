from app.main import FinancialNewsQA


def main():
    qa = FinancialNewsQA()

    questions = [
            "What was AAPL 's Q2 revenue?",
            "How did Apple's stock react to the earnings report?",
            "What did the Fed minutes suggest about future rate hikes?",
            "How did Golden gate bridge get that name?",
            "What is driving AMZN sales for Q1?",
            "What impacted Tesla's profits in last quarter",
            "Compare the revenue growth of AAPL and AMZN"
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