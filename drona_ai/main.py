"""
Drona AI - Main Entry Point

This is a demonstration of a basic RAG (Retrieval-Augmented Generation) system.
We'll show how to:
1. Create a retriever
2. Add knowledge to it
3. Ask questions and get relevant answers
"""

from rag.retriever import Retriever


def demo_basic_rag():
    """
    Demonstrate the basic RAG functionality with sample study content.
    This shows how the system works end-to-end.
    """
    # Step 1: Create a retriever instance
    # This sets up our embedder and vector store
    retriever = Retriever()
    
    # Step 2: Add some sample knowledge
    # In a real application, this would come from documents, PDFs, study materials, etc.
    print("📚 Adding sample study content to knowledge base...")
    print("-" * 60 + "\n")
    
    sample_knowledge = [
        # Python programming facts
        "Python is a high-level, interpreted programming language created by Guido van Rossum. "
        "It emphasizes code readability and supports multiple programming paradigms including "
        "procedural, object-oriented, and functional programming.",
        
        # Data structures
        "Common data structures include arrays, linked lists, stacks, queues, trees, and graphs. "
        "Arrays provide O(1) access time but fixed size, while linked lists allow dynamic sizing "
        "but have O(n) access time.",
        
        # Machine learning
        "Machine Learning is a subset of artificial intelligence that enables systems to learn "
        "and improve from experience without being explicitly programmed. Key types include "
        "supervised learning, unsupervised learning, and reinforcement learning.",
        
        # Interview prep
        "Technical interview preparation should include data structures and algorithms practice, "
        "system design fundamentals, behavioral question preparation, and coding practice on "
        "platforms like LeetCode, HackerRank, or CodeForces.",
        
        # Time complexity
        "Big O notation describes algorithm efficiency. O(1) is constant time, O(log n) is "
        "logarithmic, O(n) is linear, O(n log n) is linearithmic, and O(n²) is quadratic. "
        "Always aim for the most efficient solution possible.",
        
        # Database concepts
        "SQL databases are relational and use structured schemas, while NoSQL databases are "
        "non-relational and offer flexible schemas. Choose SQL for complex queries and ACID "
        "compliance, NoSQL for scalability and flexible data models.",
    ]
    
    # Add all the knowledge to our retriever
    retriever.add_knowledge(sample_knowledge)
    
    # Step 3: Show some example queries
    print("=" * 60)
    print("🎓 DRONA AI - RAG Demo")
    print("=" * 60 + "\n")
    
    # Example queries that demonstrate semantic search
    test_queries = [
        "What is Python programming?",
        "Tell me about algorithm complexity",
        "How should I prepare for coding interviews?",
    ]
    
    # Process each query and show results
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*60}")
        print(f"Question {i}: {query}")
        print('='*60 + "\n")
        
        # The retriever finds relevant info and generates a response
        response = retriever.generate_response(query, top_k=2)
        print(response)
        print("\n")
    
    # Step 4: Show retriever statistics
    print("=" * 60)
    print("📊 Knowledge Base Statistics")
    print("=" * 60)
    stats = retriever.get_stats()
    for key, value in stats.items():
        print(f"  • {key}: {value}")
    print("\n")


def interactive_mode():
    """
    Interactive mode - let users ask their own questions.
    This is a simple command-line interface for testing.
    """
    retriever = Retriever()
    
    # Pre-load some knowledge
    sample_knowledge = [
        "Python is a versatile programming language used for web development, data science, "
        "automation, and artificial intelligence.",
        
        "Machine learning algorithms learn patterns from data. Common algorithms include "
        "linear regression, decision trees, random forests, and neural networks.",
        
        "Data structures organize and store data efficiently. Arrays, linked lists, trees, "
        "and hash tables each have different strengths and use cases.",
        
        "Interview preparation requires consistent practice, understanding fundamentals, "
        "mock interviews, and reviewing common patterns.",
    ]
    
    retriever.add_knowledge(sample_knowledge)
    
    print("\n" + "=" * 60)
    print("🎓 DRONA AI - Interactive Mode")
    print("=" * 60)
    print("\nType 'quit' or 'exit' to stop")
    print("Type 'stats' to see knowledge base statistics\n")
    
    while True:
        try:
            # Get user input
            query = input("Your question: ").strip()
            
            # Handle exit commands
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thanks for using Drona AI!\n")
                break
            
            # Handle stats command
            if query.lower() == 'stats':
                stats = retriever.get_stats()
                print("\n📊 Statistics:")
                for key, value in stats.items():
                    print(f"  • {key}: {value}")
                print()
                continue
            
            # Skip empty queries
            if not query:
                continue
            
            # Generate and display response
            print()
            response = retriever.generate_response(query, top_k=2)
            print(response)
            print("\n" + "-" * 60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Thanks for using Drona AI!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")


def main():
    """
    Main function - entry point for the application.
    You can choose between demo mode or interactive mode.
    """
    print("\n" + "=" * 60)
    print(" " * 15 + "🎓 DRONA AI 🎓")
    print(" " * 10 + "RAG-based Study Assistant")
    print("=" * 60 + "\n")
    
    print("Choose mode:")
    print("1. Demo mode (see how RAG works)")
    print("2. Interactive mode (ask your own questions)")
    print()
    
    choice = input("Enter choice (1 or 2, default=1): ").strip()
    
    if choice == '2':
        interactive_mode()
    else:
        # Default to demo mode
        demo_basic_rag()
        
        # Ask if they want to try interactive mode
        print("\nWould you like to try interactive mode? (y/n): ", end='')
        if input().strip().lower() == 'y':
            print()
            interactive_mode()


if __name__ == "__main__":
    # Run the main function when script is executed
    main()
