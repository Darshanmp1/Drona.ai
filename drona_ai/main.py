"""
Drona AI - Core Application Module

Main entry point for Drona AI functionality. This module demonstrates how the
RAG (Retrieval-Augmented Generation) pipeline works with content extraction.

The system can:
- Extract and process knowledge from various sources (PDFs, images, YouTube, web)
- Store content efficiently in Endee vector database
- Retrieve relevant context for answering questions
- Provide voice-based interaction for accessibility
- Remember conversation context for personalized responses
- Help with placement prep through mock interviews, resume feedback, and study plans
"""

from .rag.retriever import Retriever
from .extractors.file_handler import FileHandler
from .voice.voice_chat import VoiceChat
from .memory.context_manager import ContextManager
from .placement.mock_interview import MockInterview
from .placement.resume_analyzer import ResumeAnalyzer
from .placement.study_recommender import StudyRecommender


def demo_basic_rag():
    # Initialize retriever (sets up embeddings and vector storage)
    retriever = Retriever()
    
    # Load some sample content into the knowledge base
    # Real usage would pull from uploaded docs, PDFs, or scraped web content
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


def voice_mode():
    print("\n" + "=" * 60)
    print("🎤 DRONA AI - Voice Assistant Mode")
    print("=" * 60)
    print("\nInitializing voice assistant...")
    
    # Create retriever with some sample knowledge
    retriever = Retriever()
    
    # Load some sample knowledge for demo
    print("\n📚 Loading sample knowledge base...")
    sample_knowledge = [
        "Python is a versatile programming language used for web development, data science, "
        "automation, and artificial intelligence. It emphasizes code readability.",
        
        "Machine learning is a subset of artificial intelligence that enables systems to learn "
        "from data without being explicitly programmed. Common types include supervised learning, "
        "unsupervised learning, and reinforcement learning.",
        
        "Data structures organize and store data efficiently. Common ones include arrays, linked lists, "
        "stacks, queues, trees, hash tables, and graphs. Each has different performance characteristics.",
        
        "Algorithm complexity describes how performance changes with input size. Big O notation is used. "
        "O(1) is constant time, O(log n) is logarithmic, O(n) is linear, and O(n²) is quadratic.",
        
        "Interview preparation requires consistent practice of coding problems, understanding of data "
        "structures and algorithms, system design knowledge, and behavioral question preparation.",
        
        "Artificial intelligence includes machine learning, natural language processing, computer vision, "
        "and robotics. AI systems can learn patterns, make decisions, and automate tasks.",
    ]
    
    retriever.add_knowledge(sample_knowledge)
    print("✓ Knowledge base ready")
    
    # Initialize voice chat
    voice_chat = VoiceChat(retriever, speech_rate=175)
    
    # Option to preload custom content
    print("\n" + "=" * 60)
    print("Would you like to add custom content first? (y/n): ", end='')
    add_content = input().strip().lower()
    
    if add_content == 'y':
        print("\nYou can add:")
        print("  1. Text directly")
        print("  2. From a file/URL (using extraction mode)")
        content_choice = input("Choose (1/2): ").strip()
        
        if content_choice == '1':
            print("\nEnter your text (press Enter twice when done):")
            lines = []
            while True:
                line = input()
                if not line and lines and not lines[-1]:
                    break
                lines.append(line)
            
            custom_text = ' '.join(lines).strip()
            if custom_text:
                retriever.add_knowledge([custom_text])
                print("✓ Custom content added!")
        
        elif content_choice == '2':
            file_handler = FileHandler()
            print("\nEnter file path or URL: ", end='')
            source = input().strip()
            
            if source:
                result = file_handler.extract(source)
                if result:
                    text = result['text']
                    if len(text) > 5000:
                        chunks = split_text_into_chunks(text, chunk_size=1000)
                        retriever.add_knowledge(chunks)
                    else:
                        retriever.add_knowledge([text])
                    print("✓ Content extracted and added!")
    
    # Start voice conversation
    print("\n" + "=" * 60)
    print("Starting voice conversation...")
    print("=" * 60)
    
    voice_chat.start_conversation()


def mock_interview_mode():
    print("\n" + "=" * 60)
    print("🎯 DRONA AI - Mock Interview Mode")
    print("=" * 60)
    
    interviewer = MockInterview()
    
    # Get user preferences
    print("\nLet's set up your mock interview!\n")
    
    print("Target role options:")
    print("1. Software Engineer (default)")
    print("2. Frontend Developer")
    print("3. Backend Developer")
    print("4. Data Scientist")
    role_choice = input("Choose role (1-4, default=1): ").strip()
    
    roles = {
        '1': 'Software Engineer',
        '2': 'Frontend Developer',
        '3': 'Backend Developer',
        '4': 'Data Scientist'
    }
    role = roles.get(role_choice, 'Software Engineer')
    
    print("\nDifficulty level:")
    print("1. Beginner")
    print("2. Intermediate (default)")
    print("3. Advanced")
    difficulty_choice = input("Choose difficulty (1-3, default=2): ").strip()
    
    difficulties = {'1': 'beginner', '2': 'intermediate', '3': 'advanced'}
    difficulty = difficulties.get(difficulty_choice, 'intermediate')
    
    num_questions = input("\nNumber of questions (default=5): ").strip()
    num_questions = int(num_questions) if num_questions.isdigit() else 5
    
    # Start interview
    print("\n" + "=" * 60)
    print(f"Starting Mock Interview: {role} - {difficulty.capitalize()} Level")
    print("=" * 60 + "\n")
    
    session = interviewer.start_interview(
        role=role,
        difficulty=difficulty,
        num_questions=num_questions
    )
    
    print("💡 Answer each question to the best of your ability.")
    print("   Type 'skip' to skip a question.\n")
    print("=" * 60 + "\n")
    
    # Interview loop
    while not interviewer.is_interview_complete():
        question = interviewer.get_next_question()
        
        if not question:
            break
        
        print(f"\nQuestion {question['number']}/{question['total']}")
        print(f"Category: {question['category'].replace('_', ' ').title()}")
        print(f"Difficulty: {question['difficulty'].capitalize()}")
        print("\n" + "-" * 60)
        print(f"Q: {question['question']}")
        print("-" * 60 + "\n")
        
        # Get answer
        answer = input("Your answer (or 'skip'): ").strip()
        
        if answer.lower() == 'skip':
            answer = "[Skipped]"
        
        interviewer.submit_answer(answer)
        print()
    
    # Show summary
    print("\n" + "=" * 60)
    print("✓ Interview Complete!")
    print("=" * 60 + "\n")
    
    summary = interviewer.get_interview_summary()
    print(f"Role: {summary['role']}")
    print(f"Difficulty: {summary['difficulty'].capitalize()}")
    print(f"Questions Answered: {summary['questions_answered']}/{summary['total_questions']}")
    print(f"Categories Covered: {', '.join(c.replace('_', ' ').title() for c in summary['categories_covered'])}")
    
    # Show tips
    print("\n📚 Preparation Tips:")
    for category in summary['categories_covered']:
        tips = interviewer.get_tips_for_category(category)
        if tips:
            print(f"\n{category.replace('_', ' ').title()}:")
            for tip in tips[:2]:  # Show top 2 tips
                print(f"  • {tip}")
    
    print("\n" + "=" * 60 + "\n")


def resume_analysis_mode():
    print("\n" + "=" * 60)
    print("📄 DRONA AI - Resume Analyzer")
    print("=" * 60 + "\n")
    
    analyzer = ResumeAnalyzer()
    
    print("How would you like to input your resume?")
    print("1. Paste resume text")
    print("2. Load from file")
    choice = input("Choose (1/2, default=1): ").strip()
    
    resume_text = ""
    
    if choice == '2':
        file_path = input("\nEnter path to resume text file: ").strip()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                resume_text = f.read()
            print("✓ Resume loaded successfully\n")
        except Exception as e:
            print(f"Error loading file: {e}")
            return
    else:
        print("\nPaste your resume text below (press Ctrl+Z then Enter when done on Windows,")
        print("or Ctrl+D on Mac/Linux):\n")
        
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            resume_text = '\n'.join(lines)
    
    if not resume_text.strip():
        print("No resume text provided.")
        return
    
    # Analyze resume
    print("\n" + "=" * 60)
    print("Analyzing your resume...")
    print("=" * 60 + "\n")
    
    analysis = analyzer.analyze(resume_text)
    
    # Display results
    print(f"\n📊 Overall Score: {analysis['overall_score']}/100\n")
    
    # Sections analysis
    print("✓ Sections Found:", ", ".join(analysis['sections']['found']) if analysis['sections']['found'] else "None")
    if analysis['sections']['missing']:
        print("⚠️  Missing Sections:", ", ".join(analysis['sections']['missing']))
    
    # Keywords
    print(f"\n🔍 Technical Keywords: {analysis['keywords']['total_count']} found")
    if analysis['keywords']['categories_covered']:
        print("   Categories:", ", ".join(analysis['keywords']['categories_covered']))
    
    # Length
    print(f"\n📏 Length: {analysis['length']['word_count']} words")
    print(f"   {analysis['length']['feedback']}")
    
    # Action verbs
    print(f"\n💪 Action Verbs: {analysis['action_verbs']['strong_verbs_count']} strong verbs found")
    print(f"   {analysis['action_verbs']['recommendation']}")
    
    # Formatting issues
    if analysis['formatting']['issues']:
        print("\n⚠️  Formatting Issues:")
        for issue in analysis['formatting']['issues']:
            print(f"   • {issue}")
    
    # Suggestions
    print("\n📝 Improvement Suggestions:")
    for i, suggestion in enumerate(analysis['suggestions'][:5], 1):
        print(f"   {i}. {suggestion}")
    
    # Quick tips
    print("\n💡 Quick Tips:")
    for tip in analyzer.get_quick_tips()[:5]:
        print(f"   {tip}")
    
    print("\n" + "=" * 60 + "\n")


def study_plan_mode():
    print("\n" + "=" * 60)
    print("📚 DRONA AI - Study Planner")
    print("=" * 60 + "\n")
    
    recommender = StudyRecommender()
    
    # Get user information
    print("Let's create your personalized study plan!\n")
    
    target_role = input("Target role (e.g., Software Engineer): ").strip()
    
    print("\nWeak areas (comma-separated, e.g., algorithms, system_design):")
    weak_input = input("> ").strip()
    weak_areas = [area.strip() for area in weak_input.split(',') if area.strip()]
    
    print("\nHow much time do you have?")
    print("1. 1 month")
    print("2. 2 months")
    print("3. 3 months")
    time_choice = input("Choose (1-3, default=2): ").strip()
    
    timeframes = {'1': '1_month', '2': '2_months', '3': '3_months'}
    timeframe = timeframes.get(time_choice, '2_months')
    
    # Generate study plan
    print("\n" + "=" * 60)
    print("Generating your personalized study plan...")
    print("=" * 60 + "\n")
    
    plan = recommender.create_study_plan(timeframe, weak_areas, target_role)
    
    print(f"📅 Study Plan: {timeframe.replace('_', ' ').title()}")
    if target_role:
        print(f"🎯 Target Role: {target_role}")
    print(f"⏰ Daily Commitment: {plan['daily_commitment']}")
    print(f"📖 Topics to Cover: {plan['total_topics']}\n")
    
    print("=" * 60)
    print("Week-by-Week Schedule")
    print("=" * 60 + "\n")
    
    for week_plan in plan['weekly_schedule']:
        print(f"\nWeek {week_plan['week']}: {week_plan['topic'].replace('_', ' ').title()}")
        print(f"Estimated Time: {week_plan['estimated_time']}")
        
        print("\n📚 Resources:")
        for resource in week_plan['resources']:
            print(f"   • {resource}")
        
        print("\n✏️  Practice:")
        for practice in week_plan['practice']:
            print(f"   • {practice}")
        
        print("-" * 60)
    
    # Get topic recommendations
    print("\n" + "=" * 60)
    print("Additional Recommendations")
    print("=" * 60 + "\n")
    
    recommendations = recommender.recommend_topics(weak_areas, target_role)
    
    if recommendations['high_priority']:
        print("🔴 High Priority Topics:")
        for rec in recommendations['high_priority'][:3]:
            print(f"   • {rec['topic'].replace('_', ' ').title()} - {rec['reason']}")
    
    if recommendations['role_specific']:
        print("\n🎯 Role-Specific Topics:")
        for rec in recommendations['role_specific'][:3]:
            print(f"   • {rec['topic'].replace('_', ' ').title()} - {rec['reason']}")
    
    print("\n" + "=" * 60 + "\n")


def main():
    print("\n" + "=" * 60)
    print(" " * 15 + "🎓 DRONA AI 🎓")
    print(" " * 10 + "RAG-based Study Assistant")
    print("=" * 60 + "\n")
    
    print("Choose mode:")
    print("1. Demo mode (see how RAG works)")
    print("2. Interactive mode (ask your own questions)")
    print("3. Extraction mode (extract from PDFs, images, YouTube, web)")
    print("4. Voice mode (voice assistant - speak your questions)")
    print("\nPlacement Preparation:")
    print("5. Mock Interview (practice interview questions)")
    print("6. Resume Analyzer (get feedback on your resume)")
    print("7. Study Planner (create personalized study plan)")
    print()
    
    choice = input("Enter choice (1-7, default=1): ").strip()
    
    if choice == '2':
        interactive_mode()
    elif choice == '3':
        extraction_mode()
    elif choice == '4':
        voice_mode()
    elif choice == '5':
        mock_interview_mode()
    elif choice == '6':
        resume_analysis_mode()
    elif choice == '7':
        study_plan_mode()
    else:
        # Default to demo mode
        demo_basic_rag()
        
        # Ask if they want to try other modes
        print("\nWhat would you like to try next?")
        print("1. Interactive mode")
        print("2. Extraction mode")
        print("3. Voice mode")
        print("4. Mock Interview")
        print("5. Resume Analyzer")
        print("6. Study Planner")
        print("7. Exit")
        next_choice = input("Enter choice (1-7): ").strip()
        
        if next_choice == '1':
            print()
            interactive_mode()
        elif next_choice == '2':
            print()
            extraction_mode()
        elif next_choice == '3':
            print()
            voice_mode()
        elif next_choice == '4':
            print()
            mock_interview_mode()
        elif next_choice == '5':
            print()
            resume_analysis_mode()
        elif next_choice == '6':
            print()
            study_plan_mode()


if __name__ == "__main__":
    # Run the main function when script is executed
    main()
