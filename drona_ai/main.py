"""
Drona AI - Main Entry Point

This is a demonstration of a RAG (Retrieval-Augmented Generation) system with content extraction.
Features:
1. Extract knowledge from PDFs, images, YouTube videos, and web pages
2. Store extracted content in vector database
3. Ask questions and get relevant answers
"""

from rag.retriever import Retriever
from extractors.file_handler import FileHandler


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


def extraction_mode():
    """
    Extraction mode - extract knowledge from files and URLs, then query them.
    Supports: PDFs, Images (OCR), YouTube videos, Web pages
    """
    print("\n" + "=" * 60)
    print("📂 DRONA AI - Content Extraction Mode")
    print("=" * 60)
    print("\nSupported sources:")
    print("  • PDF files (.pdf)")
    print("  • Images (.png, .jpg, etc.) - uses OCR")
    print("  • YouTube videos (full URL)")
    print("  • Web pages (any URL)")
    print("\nType 'done' when finished adding sources")
    print("Type 'quit' to exit\n")
    
    # Initialize handlers
    file_handler = FileHandler()
    retriever = Retriever()
    
    # Track what has been extracted
    extracted_sources = []
    
    # Step 1: Collect sources to extract
    while True:
        source = input("Enter file path or URL: ").strip()
        
        if source.lower() == 'quit':
            print("\n👋 Goodbye!\n")
            return
        
        if source.lower() == 'done':
            if not extracted_sources:
                print("⚠️  No sources added yet. Please add at least one source.")
                continue
            break
        
        if not source:
            continue
        
        # Extract content from the source
        print()
        result = file_handler.extract(source)
        
        if result:
            # Add extracted text to retriever
            # Split into chunks if text is very long
            text = result['text']
            
            # For very long texts, split into manageable chunks
            if len(text) > 5000:
                print("  Text is long, splitting into chunks...")
                chunks = split_text_into_chunks(text, chunk_size=1000)
                retriever.add_knowledge(chunks)
                print(f"  Added {len(chunks)} chunks to knowledge base")
            else:
                retriever.add_knowledge([text])
                print("  Added to knowledge base")
            
            extracted_sources.append({
                'source': result['source'],
                'type': result['type']
            })
        else:
            print("  Failed to extract. Try another source.\n")
    
    # Step 2: Display summary
    print("\n" + "=" * 60)
    print("📊 Extraction Summary")
    print("=" * 60)
    print(f"Sources processed: {len(extracted_sources)}")
    for idx, source in enumerate(extracted_sources, 1):
        print(f"  {idx}. [{source['type']}] {source['source']}")
    
    stats = retriever.get_stats()
    print(f"\nKnowledge chunks stored: {stats['total_documents']}")
    print("=" * 60 + "\n")
    
    # Step 3: Interactive Q&A over extracted content
    print("💬 Now you can ask questions about the extracted content!")
    print("Type 'quit' to exit, 'stats' for statistics\n")
    
    while True:
        try:
            query = input("Your question: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thanks for using Drona AI!\n")
                break
            
            if query.lower() == 'stats':
                stats = retriever.get_stats()
                print("\n📊 Statistics:")
                for key, value in stats.items():
                    print(f"  • {key}: {value}")
                print()
                continue
            
            if not query:
                continue
            
            # Generate response based on extracted content
            print()
            response = retriever.generate_response(query, top_k=3)
            print(response)
            print("\n" + "-" * 60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Thanks for using Drona AI!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")


def split_text_into_chunks(text: str, chunk_size: int = 1000, overlap: int = 100) -> list:
    """
    Split long text into smaller chunks for better retrieval.
    
    Args:
        text: Text to split
        chunk_size: Size of each chunk in characters
        overlap: Number of characters to overlap between chunks
        
    Returns:
        List of text chunks
    """
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        # Get chunk
        end = start + chunk_size
        chunk = text[start:end]
        
        # Try to break at sentence boundary if possible
        if end < text_length:
            # Look for last period in chunk
            last_period = chunk.rfind('.')
            if last_period > chunk_size // 2:  # Only if period is in latter half
                end = start + last_period + 1
                chunk = text[start:end]
        
        chunks.append(chunk.strip())
        
        # Move start position with overlap
        start = end - overlap
        
        # Ensure we make progress
        if start <= 0:
            start = end
    
    return chunks


def main():
    """
    Main function - entry point for the application.
    Choose between demo mode, interactive mode, or extraction mode.
    """
    print("\n" + "=" * 60)
    print(" " * 15 + "🎓 DRONA AI 🎓")
    print(" " * 10 + "RAG-based Study Assistant")
    print("=" * 60 + "\n")
    
    print("Choose mode:")
    print("1. Demo mode (see how RAG works)")
    print("2. Interactive mode (ask your own questions)")
    print("3. Extraction mode (extract from PDFs, images, YouTube, web)")
    print()
    
    choice = input("Enter choice (1/2/3, default=1): ").strip()
    
    if choice == '2':
        interactive_mode()
    elif choice == '3':
        extraction_mode()
    else:
        # Default to demo mode
        demo_basic_rag()
        
        # Ask if they want to try other modes
        print("\nWhat would you like to try next?")
        print("1. Interactive mode")
        print("2. Extraction mode")
        print("3. Exit")
        next_choice = input("Enter choice (1/2/3): ").strip()
        
        if next_choice == '1':
            print()
            interactive_mode()
        elif next_choice == '2':
            print()
            extraction_mode()


if __name__ == "__main__":
    # Run the main function when script is executed
    main()
