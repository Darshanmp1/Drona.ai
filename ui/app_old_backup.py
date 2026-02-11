"""
Drona AI - Professional ChatGPT-style Web Interface

A modern, professional web interface for the Drona AI study assistant.
Features ChatGPT-like chat interface with integrated file upload, URL extraction, and voice support.
"""

import streamlit as st
import sys
import os
from pathlib import Path
import tempfile

# Add parent directory to path so we can import drona_ai modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from drona_ai.rag import Embedder, VectorStore, Retriever
from drona_ai.extractors import FileHandler
from drona_ai.memory import ConversationMemory
from drona_ai.llm import OllamaLLM, get_ollama_status, OLLAMA_SETUP
from drona_ai.placement import MockInterview, ResumeAnalyzer, StudyRecommender

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Drona AI - Your AI Study Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional dark theme CSS - ChatGPT style
st.markdown("""
<style>
    /* Main app background - Dark theme */
    .stApp {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    /* Main content area */
    .main .block-container {
        background-color: #1a1a1a;
        padding-top: 2rem;
    }
    
    /* Sidebar - Dark professional */
    [data-testid="stSidebar"] {
        background-color: #0d0d0d;
        border-right: 1px solid #333;
    }
    
    [data-testid="stSidebar"] * {
        color: #e8e8e8 !important;
    }
    
    /* Chat messages - ChatGPT style */
    .stChatMessage {
        background-color: #2a2a2a;
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin-bottom: 1rem;
        color: #ffffff;
    }
    
    .stChatMessage[data-testid="user-message"] {
        background-color: #2d2d2d;
    }
    
    .stChatMessage[data-testid="assistant-message"] {
        background-color: #1e1e1e;
    }
    
    /* File uploader - Dark with good contrast */
    [data-testid="stFileUploader"] {
        background-color: #262626;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 2px dashed #4a4a4a;
    }
    
    [data-testid="stFileUploader"] label {
        color: #ffffff !important;
        font-weight: 600;
        font-size: 1rem;
    }
    
    [data-testid="stFileUploader"] small {
        color: #b8b8b8 !important;
    }
    
    [data-testid="stFileUploader"] section {
        border-color: #4a4a4a !important;
    }
    
    /* Text inputs - Dark theme */
    .stTextInput input {
        background-color: #2a2a2a !important;
        color: #ffffff !important;
        border: 1px solid #404040 !important;
        border-radius: 0.5rem;
    }
    
    .stTextInput input:focus {
        border-color: #10a37f !important;
        box-shadow: 0 0 0 1px #10a37f !important;
    }
    
    /* Chat input - Bottom bar */
    .stChatInput {
        border-radius: 1.5rem;
        background-color: #2a2a2a;
    }
    
    .stChatInput textarea {
        background-color: #2a2a2a !important;
        color: #ffffff !important;
        border: 1px solid #404040 !important;
    }
    
    /* Buttons - Professional style */
    .stButton>button {
        width: 100%;
        border-radius: 0.5rem;
        font-weight: 500;
        background-color: #10a37f;
        color: #ffffff;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #0d8c6a;
        transform: translateY(-1px);
    }
    
    /* Headers - White text */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 600;
    }
    
    /* Paragraphs and text */
    p, span, div {
        color: #e8e8e8 !important;
    }
    
    /* Expander - Dark theme */
    .streamlit-expanderHeader {
        background-color: #2a2a2a;
        color: #ffffff !important;
        border-radius: 0.5rem;
    }
    
    /* Metrics - Dark cards */
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #b8b8b8 !important;
    }
    
    /* Success/Warning/Error messages */
    .stSuccess {
        background-color: #1a4d2e !important;
        color: #90ee90 !important;
    }
    
    .stWarning {
        background-color: #4d3a1a !important;
        color: #ffd700 !important;
    }
    
    .stError {
        background-color: #4d1a1a !important;
        color: #ff6b6b !important;
    }
    
    .stInfo {
        background-color: #1a2a4d !important;
        color: #87ceeb !important;
    }
    
    /* Code blocks */
    code {
        background-color: #2a2a2a !important;
        color: #10a37f !important;
        padding: 0.2rem 0.4rem;
        border-radius: 0.25rem;
    }
    
    pre {
        background-color: #1a1a1a !important;
        border: 1px solid #404040 !important;
    }
    
    /* Markdown text */
    .stMarkdown {
        color: #e8e8e8 !important;
    }
    
    /* Tables */
    table {
        color: #e8e8e8 !important;
        background-color: #1a1a1a !important;
    }
    
    /* Links */
    a {
        color: #10a37f !important;
    }
    
    a:hover {
        color: #0d8c6a !important;
    }
    
    /* Feature menu button */
    .stButton>button[kind="primary"] {
        background-color: #2a2a2a;
        color: #ffffff;
        border: 1px solid #404040;
    }
    
    /* Columns */
    [data-testid="column"] {
        background-color: transparent;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #10a37f !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def initialize_session_state():
    """Initialize all session state variables."""
    
    # Chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # RAG components (initialize once)
    if 'embedder' not in st.session_state:
        with st.spinner("🔄 Loading AI models..."):
            st.session_state.embedder = Embedder()
    
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = VectorStore(
            dimension=384, 
            index_name="drona_ui",
            use_endee=True,
            endee_url="http://localhost:8080"
        )
    
    if 'retriever' not in st.session_state:
        st.session_state.retriever = Retriever(
            st.session_state.embedder,
            st.session_state.vector_store
        )
    
    # File handler
    if 'file_handler' not in st.session_state:
        st.session_state.file_handler = FileHandler()
    
    # Memory
    if 'conversation_memory' not in st.session_state:
        st.session_state.conversation_memory = ConversationMemory()
    
    # Backend info
    if 'backend_info' not in st.session_state:
        st.session_state.backend_info = st.session_state.vector_store.get_backend_info()
    
    # Document counter
    if 'docs_count' not in st.session_state:
        st.session_state.docs_count = 0
    
    # Uploaded files tracking
    if 'uploaded_files_list' not in st.session_state:
        st.session_state.uploaded_files_list = []
    
    # LLM integration
    if 'ollama_llm' not in st.session_state:
        st.session_state.ollama_llm = OllamaLLM(model="llama3.2")
    
    if 'ollama_status' not in st.session_state:
        st.session_state.ollama_status = get_ollama_status()
    
    # Feature menu state
    if 'show_feature_menu' not in st.session_state:
        st.session_state.show_feature_menu = False
    
    # Active feature
    if 'active_feature' not in st.session_state:
        st.session_state.active_feature = None
    
    # Interview session tracking
    if 'interview_active' not in st.session_state:
        st.session_state.interview_active = False
    
    if 'interview_session' not in st.session_state:
        st.session_state.interview_session = None

# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def process_file_upload(uploaded_file):
    """Process uploaded file and add to knowledge base."""
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_path = tmp_file.name
        
        # Extract content using FileHandler (CORRECT METHOD: extract())
        result = st.session_state.file_handler.extract(tmp_path)
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        if result and result.get('text'):
            # Add to knowledge base
            st.session_state.retriever.add_document(
                result['text'],
                metadata={'source': uploaded_file.name, 'type': result.get('type', 'file')}
            )
            st.session_state.docs_count += 1
            
            # Add to uploaded files list
            if uploaded_file.name not in st.session_state.uploaded_files_list:
                st.session_state.uploaded_files_list.append(uploaded_file.name)
            
            return f"✅ Successfully processed **{uploaded_file.name}**\n\nExtracted {len(result['text'])} characters."
        else:
            return f"❌ Could not extract content from **{uploaded_file.name}**"
    
    except Exception as e:
        return f"❌ Error processing file: {str(e)}"

def process_url_input(url):
    """Process URL and add to knowledge base."""
    try:
        # Extract content using FileHandler (CORRECT METHOD: extract())
        result = st.session_state.file_handler.extract(url)
        
        if result and result.get('text'):
            # Add to knowledge base
            st.session_state.retriever.add_document(
                result['text'],
                metadata={'source': url, 'type': result.get('type', 'url')}
            )
            st.session_state.docs_count += 1
            return f"✅ Successfully extracted content from URL\n\nExtracted {len(result['text'])} characters."
        else:
            return f"❌ Could not extract content from URL"
    
    except Exception as e:
        return f"❌ Error processing URL: {str(e)}"

def get_ai_response(query):
    """Generate AI response using RAG + LLM."""
    try:
        # Retrieve relevant documents
        results = st.session_state.retriever.retrieve(query, top_k=3)
        
        # Build context from retrieved documents
        context = ""
        if results and len(results) > 0:
            context_parts = []
            for i, result in enumerate(results, 1):
                source = result.get('metadata', {}).get('source', 'Unknown')
                text = result['text'][:500]  # Limit context size
                context_parts.append(f"[Source {i}: {source}]\n{text}")
            context = "\n\n".join(context_parts)
        
        # Check if Ollama is available
        if st.session_state.ollama_status['installed']:
            # Use LLM with RAG context
            if context:
                response = st.session_state.ollama_llm.generate(
                    prompt=query,
                    context=context,
                    max_tokens=500,
                    temperature=0.7
                )
            else:
                # No context, use LLM directly
                response = st.session_state.ollama_llm.generate(
                    prompt=query,
                    max_tokens=500,
                    temperature=0.7
                )
            
            # Add source information
            if results:
                sources = set()
                for result in results:
                    if 'metadata' in result and 'source' in result['metadata']:
                        sources.add(result['metadata']['source'])
                if sources:
                    response += f"\n\n📚 **Sources:** {', '.join(sources)}"
            
            return response
        else:
            # Fallback: Just return retrieved documents
            if results and len(results) > 0:
                response = "⚠️ **Ollama not running - showing retrieved documents only**\n\n"
                response += f"**Top Result:**\n{results[0]['text']}\n\n"
                
                if len(results) > 1:
                    response += "**Additional Results:**\n"
                    for i, result in enumerate(results[1:], 1):
                        response += f"{i}. {result['text'][:200]}...\n\n"
                
                response += "\n💡 **Tip:** Install Ollama to get AI-generated responses!"
            else:
                response = """I don't have enough information to answer that question yet.

**Here's what you can do:**
1. Upload relevant documents
2. Add content from URLs
3. Install Ollama for AI responses"""
            
            return response
    
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ============================================================================
# SIDEBAR
# ============================================================================

def render_sidebar():
    """Render professional sidebar with controls."""
    
    with st.sidebar:
        # Header
        st.title("🎓 Drona AI")
        st.caption("Your AI-Powered Study Assistant")
        st.markdown("---")
        
        # System Status
        with st.expander("📊 System Status", expanded=True):
            backend = st.session_state.backend_info['backend']
            docs = st.session_state.vector_store.count()
            
            # Endee / Docker Status
            st.markdown("**🗄️ Vector Database:**")
            if backend == 'Endee':
                st.success("✅ Endee Running (Persistent Storage)")
                st.caption("Using production vector database")
            else:
                st.error("❌ Endee offline - Using in-memory fallback")
                st.caption("⚠️ Docker not installed or Endee not started")
                with st.expander("🐳 How to start Endee"):
                    st.code("""# Install Docker Desktop first
# Then run:
cd endee
docker compose up -d""", language="bash")
            
            # LLM Status  
            st.markdown("**🤖 AI Model:**")
            ollama_status = st.session_state.ollama_status
            if ollama_status.get('installed'):
                st.success("✅ LLaMA 3.2 Connected")
                st.caption("Generating intelligent responses")
            else:
                st.warning("⚠️ Ollama offline - Retrieval-only mode")
                with st.expander("🚀 How to enable LLaMA 3.2"):
                    st.code("""# Install Ollama, then:
ollama pull llama3.2
ollama serve""", language="bash")
            
            # Stats
            st.markdown("---")
            st.metric("📚 Documents", docs)
            st.metric("💬 Messages", len(st.session_state.messages))
        
        st.markdown("---")
        
        # Actions
        st.subheader("⚡ Quick Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        
        with col2:
            if st.button("🔄 Refresh", use_container_width=True):
                st.rerun()
        
        st.markdown("---")
        
        # LLM Status
        with st.expander("🤖 AI Model Status", expanded=True):
            if st.session_state.ollama_status['installed']:
                st.success("✅ **Ollama:** Running")
                st.info(f"**Model:** Llama 3.2")
                available_models = st.session_state.ollama_status.get('models', [])
                if available_models:
                    st.caption(f"Available: {', '.join(available_models)}")
            else:
                st.error("❌ **Ollama:** Not running")
                if st.button("📝 Show Setup Instructions"):
                    st.session_state.show_ollama_setup = True
        
        st.markdown("---")
        
        # Voice Mode
        st.subheader("🎤 Voice Mode")
        st.info("""To use voice assistant, run:
```bash
python drona_ai/main.py
```
Select option 4 for voice mode.""")
        
        st.markdown("---")
        
        # Help
        with st.expander("❓ Help & Tips"):
            st.markdown("""
**Getting Started:**
1. Upload documents or add URLs
2. Ask questions in the chat
3. Get AI-powered answers

**Supported Formats:**
- 📄 PDF documents
- 🖼️ Images (with OCR)
- 🎥 YouTube videos
- 🌐 Web pages
- 📝 Text files

**Tips:**
- Be specific in your questions
- Upload relevant materials first
- Check system status regularly
            """)

# ============================================================================
# MAIN CHAT INTERFACE
# ============================================================================

def render_chat_interface():
    """Render the main ChatGPT-style chat interface."""
    
    # Welcome message
    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div style='text-align: center; padding: 2rem;'>
            <h1>🎓 Welcome to Drona AI</h1>
            <p style='font-size: 1.2rem; color: #666;'>Your intelligent study assistant powered by RAG technology</p>
            <p>Upload documents, add URLs, or start asking questions!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick start suggestions
        st.markdown("### 💡 Try asking:")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📚 What can you help me with?", key="q1"):
                st.session_state.messages.append({"role": "user", "content": "What can you help me with?"})
                st.rerun()
        
        with col2:
            if st.button("🎯 How do I upload documents?", key="q2"):
                st.session_state.messages.append({"role": "user", "content": "How do I upload documents?"})
                st.rerun()
        
        with col3:
            if st.button("🚀 Tell me about RAG", key="q3"):
                st.session_state.messages.append({"role": "user", "content": "Tell me about RAG technology"})
                st.rerun()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Show uploaded files above chat input (if any)
    if st.session_state.docs_count > 0:
        st.markdown("---")
        with st.expander(f"📚 {st.session_state.docs_count} document(s) uploaded", expanded=True):
            # Display uploaded file names
            if st.session_state.uploaded_files_list:
                for file_name in st.session_state.uploaded_files_list:
                    st.markdown(f"📄 **{file_name}**")
            
            # Clear button
            if st.button("🗑️ Clear Knowledge Base", key="clear_kb"):
                st.session_state.vector_store.clear()
                st.session_state.docs_count = 0
                st.session_state.uploaded_files_list = []
                st.success("Knowledge base cleared!")
                st.rerun()
    
    # Chat input with + button beside it
    col_plus, col_input = st.columns([1, 11])
    
    with col_plus:
        if st.button("➕", key="plus_btn", help="Features Menu", use_container_width=True):
            st.session_state.show_feature_menu = not st.session_state.get('show_feature_menu', False)
            st.rerun()
    
    with col_input:
        prompt = st.chat_input("Ask anything")
    
    # Show feature menu popup if active
    if st.session_state.get('show_feature_menu', False):
        st.markdown("---")
        st.markdown("### ⚡ Features")
        
        menu_cols = st.columns(3)
        
        with menu_cols[0]:
            if st.button("📄 Add Files", key="menu_files", use_container_width=True):
                st.session_state.active_feature = "files"
                st.session_state.show_feature_menu = False
                st.rerun()
            
            if st.button("🔗 Add URL", key="menu_url", use_container_width=True):
                st.session_state.active_feature = "url_feature"
                st.session_state.show_feature_menu = False
                st.rerun()
        
        with menu_cols[1]:
            if st.button("🎯 Mock Interview", key="menu_interview", use_container_width=True):
                st.session_state.active_feature = "interview"
                st.session_state.show_feature_menu = False
                st.rerun()
            
            if st.button("📝 Resume Analysis", key="menu_resume", use_container_width=True):
                st.session_state.active_feature = "resume"
                st.session_state.show_feature_menu = False
                st.rerun()
        
        with menu_cols[2]:
            if st.button("📚 Study Planner", key="menu_study", use_container_width=True):
                st.session_state.active_feature = "study"
                st.session_state.show_feature_menu = False
                st.rerun()
            
            if st.button("🤖 About LLM", key="menu_llm", use_container_width=True):
                st.session_state.active_feature = "llm_info"
                st.session_state.show_feature_menu = False
                st.rerun()
    
    # Process chat input
    if prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_ai_response(prompt)
                st.markdown(response)
        
        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Save to memory (correct method: add_conversation)
        st.session_state.conversation_memory.add_conversation(prompt, response)
        
        # Rerun to show updated chat
        st.rerun()

# ============================================================================
# FEATURE PANELS
# ============================================================================

def render_mock_interview():
    """Render Mock Interview feature."""
    st.title("🎯 Mock Interview Practice")
    
    st.markdown("### Prepare for your next technical interview!")
    
    col1, col2 = st.columns(2)
    with col1:
        role = st.selectbox(
            "Select Role",
            ["Python Developer", "Data Scientist", "ML Engineer", "Full Stack Developer", "DevOps Engineer"]
        )
    
    with col2:
        difficulty = st.selectbox(
            "Difficulty",
            ["Beginner", "Intermediate", "Advanced"]
        )
    
    focus_areas = st.multiselect(
        "Focus Areas",
        ["Data Structures", "Algorithms", "System Design", "Python", "Machine Learning", "Databases"]
    )
    
    num_questions = st.slider("Number of Questions", 3, 10, 5)
    
    if st.button("🚀 Start Interview", use_container_width=True):
        try:
            mock_interview = MockInterview()
            mock_interview.start_interview(
                role=role.lower().replace(" ", "_"),
                difficulty=difficulty.lower(),
                focus_areas=focus_areas,
                num_questions=num_questions
            )
            st.session_state.interview_session = mock_interview
            st.session_state.interview_active = True
            st.rerun()
        except Exception as e:
            st.error(f"Error starting interview: {e}")
    
    # Show active interview
    if st.session_state.get('interview_active', False):
        interview = st.session_state.interview_session
        
        if not interview.is_interview_complete():
            question = interview.get_next_question()
            
            st.markdown(f"### Question {question.get('number', 1)}")
            st.info(question.get('question', ''))
            
            answer = st.text_area("Your Answer", height=150)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Submit Answer"):
                    interview.submit_answer(answer)
                    st.rerun()
            with col2:
                if st.button("Skip"):
                    interview.submit_answer("")
                    st.rerun()
            with col3:
                if st.button("End Interview"):
                    st.session_state.interview_active = False
                    st.rerun()
        else:
            summary = interview.get_interview_summary()
            st.success("🎉 Interview Complete!")
            st.markdown(summary)
            if st.button("Close"):
                st.session_state.interview_active = False
                del st.session_state.interview_session
                st.rerun()
    
    if st.button("← Back to Chat"):
        st.session_state.active_feature = None
        st.rerun()

def render_resume_analyzer():
    """Render Resume Analysis feature."""
    st.title("📝 Resume Analyzer")
    
    st.markdown("### Upload your resume for detailed analysis")
    
    uploaded_resume = st.file_uploader(
        "Upload Resume (PDF or TXT)",
        type=['pdf', 'txt'],
        key="resume_uploader"
    )
    
    if uploaded_resume:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_resume.name).suffix) as tmp:
            tmp.write(uploaded_resume.getbuffer())
            tmp_path = tmp.name
        
        result = st.session_state.file_handler.extract(tmp_path)
        os.unlink(tmp_path)
        
        if result and result.get('text'):
            st.success(f"✅ Resume loaded: {len(result['text'])} characters")
            
            if st.button("🔍 Analyze Resume", use_container_width=True):
                with st.spinner("Analyzing..."):
                    try:
                        analyzer = ResumeAnalyzer()
                        analysis = analyzer.analyze_resume(result['text'])
                        
                        st.markdown("### Analysis Results")
                        st.markdown(analysis)
                    except Exception as e:
                        st.error(f"Error: {e}")
    
    if st.button("← Back to Chat"):
        st.session_state.active_feature = None
        st.rerun()

def render_study_planner():
    """Render Study Plan feature."""
    st.title("📚 Study Plan Generator")
    
    st.markdown("### Create a personalized study roadmap")
    
    goal = st.text_input(
        "Learning Goal",
        placeholder="e.g., Master Python for Data Science"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        duration_weeks = st.slider("Duration (weeks)", 1, 16, 8)
    with col2:
        hours_per_week = st.slider("Hours per week", 5, 40, 10)
    
    topics = st.text_area(
        "Specific Topics (optional)",
        placeholder="e.g., NumPy, Pandas, Matplotlib, Machine Learning",
        height=100
    )
    
    if st.button("🎯 Generate Study Plan", use_container_width=True):
        if goal:
            with st.spinner("Creating personalized plan..."):
                try:
                    recommender = StudyRecommender()
                    plan = recommender.generate_study_plan(
                        goal=goal,
                        duration_weeks=duration_weeks,
                        hours_per_week=hours_per_week
                    )
                    
                    st.markdown("### Your Personalized Study Plan")
                    st.markdown(plan)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a learning goal")
    
    if st.button("← Back to Chat"):
        st.session_state.active_feature = None
        st.rerun()

def render_ollama_setup():
    """Render Ollama setup instructions."""
    st.title("🚀 Ollama Setup")
    st.markdown(OLLAMA_SETUP)
    
    if st.button("🔄 Check Status"):
        st.session_state.ollama_status = get_ollama_status()
        st.rerun()
    
    if st.button("← Back"):
        st.session_state.show_ollama_setup = False
        st.rerun()

def render_llm_info():
    """Show information about the AI model being used."""
    st.title("🤖 AI Model Information")
    
    st.markdown("""
    ### Drona AI uses **LLaMA 3.2** for intelligent response generation!
    
    #### 🔄 How It Works (RAG Pipeline):
    
    1. **📥 Your Question** → You ask a question
    2. **📊 Embedding** → Question converted to 384-dimensional vector
    3. **🔍 Endee Search** → Finds relevant documents from vector database
    4. **🤖 LLaMA 3.2** → Generates natural response using retrieved context
    5. **✅ Response** → You get an intelligent, contextual answer
    
    ---
    
    #### 🗄️ Vector Database: **Endee**
    - High-performance C++ vector database
    - Uses HNSW algorithm for fast similarity search
    - Persistent storage across sessions
    - Automatic fallback to in-memory if offline
    
    #### 🧠 LLM: **LLaMA 3.2 via Ollama**
    - Runs locally on your machine (privacy-first!)
    - No data sent to external servers
    - Fast response times
    - Customizable temperature and parameters
    
    ---
    
    #### 📊 Current Status:
    """)
    
    # Show Ollama status
    status = st.session_state.ollama_status
    
    if status['installed']:
        st.success("✅ **Ollama is installed and running!**")
        st.info(f"📍 **Endpoint:** {status.get('url', 'http://localhost:11434')}")
        
        if status.get('models'):
            st.write("**Available Models:**")
            for model in status['models']:
                if 'llama3.2' in model.lower():
                    st.write(f"  🟢 {model} (Active)")
                else:
                    st.write(f"  ⚪ {model}")
    else:
        st.warning("⚠️ **Ollama not detected**")
        st.markdown("""
        **To enable LLaMA 3.2:**
        1. Install Ollama: https://ollama.ai
        2. Run: `ollama pull llama3.2`
        3. Start server: `ollama serve`
        4. Refresh this page
        
        *Drona AI will still work with retrieval-only mode!*
        """)
    
    # Show Endee status
    backend_info = st.session_state.backend_info
    st.markdown("---")
    st.markdown("#### 🗄️ Vector Database Status:")
    
    if backend_info['backend'] == 'Endee':
        st.success(f"✅ **Endee is running!** (http://localhost:8080)")
        st.write(f"📦 **Documents stored:** {st.session_state.vector_store.count()}")
    else:
        st.warning("⚠️ **Using in-memory storage** (Endee offline)")
        st.markdown("""
        **To enable persistent storage:**
        ```bash
        cd endee
        docker compose up -d
        ```
        """)
        st.write(f"📦 **Documents in memory:** {st.session_state.vector_store.count()}")

def render_file_upload():
    """Render file upload feature panel."""
    st.title("📄 Upload Documents")
    
    st.markdown("""
    ### Upload your study materials to the knowledge base
    
    **Supported formats:**
    - 📄 PDF documents
    - 🖼️ Images (PNG, JPG) - OCR enabled
    - 📝 Text files
    """)
    
    uploaded_files = st.file_uploader(
        "Drag and drop files here or click to browse",
        type=['pdf', 'png', 'jpg', 'jpeg', 'txt'],
        accept_multiple_files=True,
        key="bulk_file_uploader"
    )
    
    if uploaded_files:
        st.write(f"📦 **{len(uploaded_files)} file(s) selected**")
        
        if st.button("📥 Process All Files", key="process_bulk_files", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            successful = 0
            failed = 0
            
            for idx, file in enumerate(uploaded_files):
                status_text.text(f"Processing {idx + 1}/{len(uploaded_files)}: {file.name}")
                
                result = process_file_upload(file)
                
                if "✅" in result:
                    successful += 1
                    st.success(result)
                else:
                    failed += 1
                    st.error(result)
                
                progress_bar.progress((idx + 1) / len(uploaded_files))
            
            status_text.empty()
            progress_bar.empty()
            
            st.success(f"🎉 Processing complete! {successful} successful, {failed} failed")
    
    st.markdown("---")
    
    if st.button("← Back to Chat", key="close_files"):
        st.session_state.active_feature = None
        st.rerun()

def render_url_extractor():
    """Render URL content extraction feature panel."""
    st.title("🔗 Extract from URL")
    
    st.markdown("""
    ### Extract content from web pages and YouTube videos
    
    **Supported sources:**
    - 🌐 Web pages and articles
    - 🎥 YouTube videos (transcript)
    - 📰 Blog posts and documentation
    """)
    
    url_input = st.text_input(
        "Enter URL",
        placeholder="https://example.com or https://youtube.com/watch?v=...",
        key="url_extraction_input"
    )
    
    if url_input:
        if st.button("🌐 Extract Content", key="extract_url", use_container_width=True):
            with st.spinner("Fetching and processing content..."):
                result = process_url_input(url_input)
            
            if "✅" in result:
                st.success(result)
            else:
                st.error(result)
    
    st.markdown("---")
    st.markdown("""
    ### 💡 Tips:
    - YouTube videos must have captions available
    - Some websites may block scraping
    - Content is automatically chunked and embedded
    """)
    
    if st.button("← Back to Chat", key="close_url"):
        st.session_state.active_feature = None
        st.rerun()

def render_llm_info():
    """Show information about the AI model being used."""
    st.title("🤖 AI Model Information")
    
    st.markdown("""
    ### Drona AI uses **LLaMA 3.2** for intelligent response generation!
    
    #### 🔄 How It Works (RAG Pipeline):
    
    1. **📥 Your Question** → You ask a question
    2. **📊 Embedding** → Question converted to 384-dimensional vector
    3. **🔍 Endee Search** → Finds relevant documents from vector database
    4. **🤖 LLaMA 3.2** → Generates natural response using retrieved context
    5. **✅ Response** → You get an intelligent, contextual answer
    
    ---
    
    #### 🗄️ Vector Database: **Endee**
    - High-performance C++ vector database
    - Uses HNSW algorithm for fast similarity search
    - Persistent storage across sessions
    - Automatic fallback to in-memory if offline
    
    #### 🧠 LLM: **LLaMA 3.2 via Ollama**
    - Runs locally on your machine (privacy-first!)
    - No data sent to external servers
    - Fast response times
    - Customizable temperature and parameters
    
    ---
    
    #### 📊 Current Status:
    """)
    
    # Show Ollama status
    status = st.session_state.ollama_status
    
    if status['installed']:
        st.success("✅ **Ollama is installed and running!**")
        st.info(f"📍 **Endpoint:** {status.get('url', 'http://localhost:11434')}")
        
        if status.get('models'):
            st.write("**Available Models:**")
            for model in status['models']:
                if 'llama3.2' in model.lower():
                    st.write(f"  🟢 {model} (Active)")
                else:
                    st.write(f"  ⚪ {model}")
    else:
        st.warning("⚠️ **Ollama not detected**")
        st.markdown("""
        **To enable LLaMA 3.2:**
        1. Install Ollama: https://ollama.ai
        2. Run: `ollama pull llama3.2`
        3. Start server: `ollama serve`
        4. Refresh this page
        
        *Drona AI will still work with retrieval-only mode!*
        """)
    
    # Show Endee status
    backend_info = st.session_state.backend_info
    st.markdown("---")
    st.markdown("#### 🗄️ Vector Database Status:")
    
    if backend_info['backend'] == 'Endee':
        st.success(f"✅ **Endee is running!** ({backend_info.get('url', 'http://localhost:8080')})")
        st.write(f"📦 **Documents stored:** {st.session_state.vector_store.count()}")
    else:
        st.warning("⚠️ **Using in-memory storage** (Endee offline)")
        st.markdown("""
        **To enable persistent storage:**
        ```bash
        cd endee
        docker compose up -d
        ```
        """)
        st.write(f"📦 **Documents in memory:** {st.session_state.vector_store.count()}")

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    """Main application entry point."""
    
    # Initialize
    initialize_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Show Ollama setup if requested
    if st.session_state.get('show_ollama_setup', False):
        render_ollama_setup()
    # Show active feature based on selection
    elif st.session_state.active_feature == 'interview':
        render_mock_interview()
    elif st.session_state.active_feature == 'resume':
        render_resume_analyzer()
    elif st.session_state.active_feature in ['study_plan', 'study']:
        render_study_planner()
    elif st.session_state.active_feature == 'llm_info':
        render_llm_info()
        if st.button("✖ Close", key="close_llm_main"):
            st.session_state.active_feature = None
            st.rerun()
    elif st.session_state.active_feature == 'files':
        render_file_upload()
    elif st.session_state.active_feature == 'url_feature':
        render_url_extractor()
    elif st.session_state.active_feature in ['upload', 'url']:
        st.info(f"💡 Use the sidebar to {st.session_state.active_feature} content!")
        render_chat_interface()
    elif st.session_state.active_feature == 'voice':
        st.info("🎤 Voice mode is available via command line. Run: `python drona_ai/main.py`")
        render_chat_interface()
    else:
        # Default: Show chat interface
        render_chat_interface()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #999; font-size: 0.9rem;'>
        <p>Drona AI - Intelligent Study Assistant | Powered by Llama 3.2 + RAG Technology</p>
        <p>💡 <strong>Tip:</strong> Upload documents and ask questions to get AI-powered answers!</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# RUN APP
# ============================================================================

if __name__ == "__main__":
    main()
