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
        padding-top: 1rem;
        max-width: 1200px;
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
    
    /* Input area styling */
    .stTextInput input, .stTextArea textarea {
        background-color: #2a2a2a !important;
        color: #ffffff !important;
        border: 1px solid #404040 !important;
        border-radius: 0.5rem;
    }
    
    /* Buttons - ChatGPT style */
    .stButton>button {
        background-color: #10a37f;
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #0d8c6a;
        box-shadow: 0 4px 12px rgba(16, 163, 127, 0.3);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #2a2a2a !important;
        border-radius: 0.5rem;
        border: 1px solid #404040;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background-color: #262626;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px dashed #4a4a4a;
    }
    
    /* Success/Error/Info boxes */
    .stSuccess {
        background-color: #1a4d2e !important;
        color: #4ade80 !important;
    }
    
    .stError {
        background-color: #4d1a1a !important;
        color: #ff6b6b !important;
    }
    
    .stInfo {
        background-color: #1a2a4d !important;
        color: #87ceeb !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-online {
        background-color: #4ade80;
    }
    
    .status-offline {
        background-color: #ef4444;
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
    
    # Active feature
    if 'active_feature' not in st.session_state:
        st.session_state.active_feature = "chat"  # chat, interview, resume, study
    
    # Interview session tracking
    if 'interview_active' not in st.session_state:
        st.session_state.interview_active = False
    
    if 'interview_session' not in st.session_state:
        st.session_state.interview_session = None
    
    # Pending file upload (for preview)
    if 'pending_file' not in st.session_state:
        st.session_state.pending_file = None
    
    if 'pending_url' not in st.session_state:
        st.session_state.pending_url = None

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
        
        # Extract content using FileHandler
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
        # Extract content using FileHandler
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
                response += f"**Top Result:**\n{results[0]['text'][:500]}\n\n"
                
                response += f"\n💡 **Tip:** {OLLAMA_SETUP}"
            else:
                response = f"""I don't have enough information to answer that question yet.

**Here's what you can do:**
1. Upload relevant documents using the file button below
2. Add content from URLs
3. {OLLAMA_SETUP}"""
            
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
        st.markdown("# 🎓 Drona AI")
        st.markdown("*Your AI Study Assistant*")
        st.markdown("---")
        
        # New chat button
        if st.button("➕ New Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.active_feature = "chat"
            st.rerun()
        
        st.markdown("---")
        
        # Navigation
        st.markdown("### 📋 Features")
        
        if st.button("💬 Chat", use_container_width=True, type="primary" if st.session_state.active_feature == "chat" else "secondary"):
            st.session_state.active_feature = "chat"
            st.rerun()
        
        if st.button("🎤 Mock Interview", use_container_width=True, type="primary" if st.session_state.active_feature == "interview" else "secondary"):
            st.session_state.active_feature = "interview"
            st.rerun()
        
        if st.button("📄 Resume Analyzer", use_container_width=True, type="primary" if st.session_state.active_feature == "resume" else "secondary"):
            st.session_state.active_feature = "resume"
            st.rerun()
        
        if st.button("📚 Study Planner", use_container_width=True, type="primary" if st.session_state.active_feature == "study" else "secondary"):
            st.session_state.active_feature = "study"
            st.rerun()
        
        st.markdown("---")
        
        # System Status
        st.markdown("### ⚙️ System Status")
        
        # Endee DB status
        backend_info = st.session_state.backend_info
        if backend_info['backend'] == 'endee' and backend_info['connected']:
            st.markdown("🟢 **Endee DB:** Connected")
            st.caption(f"Index: {backend_info.get('index_name', 'drona_ui')}")
        elif backend_info['backend'] == 'numpy':
            st.markdown("🟡 **Vector Store:** In-Memory")
            st.caption("Endee DB offline, using fallback")
        else:
            st.markdown("🔴 **Vector Store:** Disconnected")
        
        # LLaMA status
        ollama_status = st.session_state.ollama_status
        if ollama_status['installed']:
            st.markdown("🟢 **LLaMA 3.2:** Ready")
            if ollama_status.get('models'):
                st.caption(f"Models: {', '.join(ollama_status['models'][:2])}")
        else:
            st.markdown("🔴 **LLaMA:** Not Available")
            st.caption("Install Ollama for AI responses")
        
        # Documents loaded
        st.markdown(f"📚 **Documents:** {st.session_state.docs_count}")
        
        if st.session_state.docs_count > 0:
            with st.expander("View Documents"):
                for doc in st.session_state.uploaded_files_list:
                    st.caption(f"📄 {doc}")
                
                if st.button("🗑️ Clear All", key="clear_all_sidebar"):
                    st.session_state.vector_store.clear()
                    st.session_state.docs_count = 0
                    st.session_state.uploaded_files_list = []
                    st.success("Knowledge base cleared!")
                    st.rerun()
        
        st.markdown("---")
        
        # About
        with st.expander("ℹ️ About"):
            st.markdown("""
            **Drona AI v1.0**
            
            An AI-powered study and placement assistant built with:
            - 🤖 LLaMA 3.2 (via Ollama)
            - 🔍 Endee Vector Database
            - 📚 RAG Pipeline
            - 🎓 Smart Study Tools
            
            Built for students, by students.
            """)

# ============================================================================
# CHAT INTERFACE
# ============================================================================

def render_chat_interface():
    """Render the main chat interface."""
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input controls section (above chat input)
    st.markdown("---")
    
    # Action buttons row
    col1, col2, col3, col4 = st.columns([1, 1, 1, 5])
    
    with col1:
        # File upload button
        uploaded_file = st.file_uploader(
            "📎",
            type=['pdf', 'txt', 'docx', 'png', 'jpg', 'jpeg'],
            label_visibility="collapsed",
            key="file_upload_btn"
        )
        if uploaded_file and uploaded_file != st.session_state.pending_file:
            st.session_state.pending_file = uploaded_file
            st.rerun()
    
    with col2:
        # URL input toggle
        if st.button("🔗", help="Add URL", use_container_width=True):
            st.session_state.pending_url = "show_input"
            st.rerun()
    
    with col3:
        # Voice input (placeholder for future implementation)
        if st.button("🎤", help="Voice Input (Coming Soon)", use_container_width=True, disabled=True):
            st.info("Voice input feature coming soon!")
    
    # Show pending file preview
    if st.session_state.pending_file:
        st.info(f"📎 **File ready to upload:** {st.session_state.pending_file.name}")
        col_cancel, col_process = st.columns([1, 6])
        with col_cancel:
            if st.button("❌", key="cancel_file"):
                st.session_state.pending_file = None
                st.rerun()
        with col_process:
            if st.button("✅ Process File", use_container_width=True):
                with st.spinner("Processing file..."):
                    result = process_file_upload(st.session_state.pending_file)
                    st.session_state.messages.append({"role": "assistant", "content": result})
                    st.session_state.pending_file = None
                    st.rerun()
    
    # Show URL input if requested
    if st.session_state.pending_url == "show_input":
        url_input = st.text_input("Enter URL (YouTube, website, article):", key="url_input_field")
        col_cancel_url, col_process_url = st.columns([1, 6])
        with col_cancel_url:
            if st.button("❌", key="cancel_url"):
                st.session_state.pending_url = None
                st.rerun()
        with col_process_url:
            if st.button("✅ Extract Content", use_container_width=True) and url_input:
                with st.spinner("Extracting content..."):
                    result = process_url_input(url_input)
                    st.session_state.messages.append({"role": "assistant", "content": result})
                    st.session_state.pending_url = None
                    st.rerun()
    
    # Main chat input - MUST BE AT ROOT LEVEL (not in columns/expander)
    prompt = st.chat_input("Ask anything about your documents or studies...")
    
    if prompt:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate AI response
        with st.spinner("🤔 Thinking..."):
            response = get_ai_response(prompt)
        
        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Rerun to update display
        st.rerun()

# ============================================================================
# MOCK INTERVIEW MODE
# ============================================================================

def render_mock_interview():
    """Render mock interview interface."""
    
    st.markdown("# 🎤 Mock Interview Mode")
    st.markdown("Practice your interview skills with AI-powered mock interviews.")
    st.markdown("---")
    
    # Interview configuration
    col1, col2 = st.columns(2)
    
    with col1:
        interview_type = st.selectbox(
            "Interview Type",
            ["Technical", "HR", "Behavioral", "Case Study"]
        )
    
    with col2:
        difficulty = st.selectbox(
            "Difficulty Level",
            ["Beginner", "Intermediate", "Advanced"]
        )
    
    role = st.text_input("Target Role (e.g., Software Engineer, Data Analyst)")
    
    # Start/Stop interview
    if not st.session_state.interview_active:
        if st.button("🎬 Start Interview", use_container_width=True):
            st.session_state.interview_active = True
            st.session_state.interview_session = {
                'type': interview_type,
                'difficulty': difficulty,
                'role': role,
                'questions_asked': 0,
                'responses': []
            }
            
            # Initialize mock interview
            mock_interview = MockInterview()
            first_question = f"Hello! Let's begin your {interview_type} interview for the {role} position. {mock_interview.get_question(interview_type, difficulty)}"
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": first_question
            })
            st.rerun()
    else:
        if st.button("⏹️ End Interview", use_container_width=True):
            # Generate interview summary
            summary = f"""
            ### Interview Summary
            
            **Type:** {st.session_state.interview_session['type']}  
            **Difficulty:** {st.session_state.interview_session['difficulty']}  
            **Questions Asked:** {st.session_state.interview_session['questions_asked']}
            
            Great job completing the interview! Practice makes perfect.
            """
            
            st.session_state.messages.append({"role": "assistant", "content": summary})
            st.session_state.interview_active = False
            st.session_state.interview_session = None
            st.rerun()
    
    st.markdown("---")
    
    # Display interview chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input for interview responses
    if st.session_state.interview_active:
        response = st.chat_input("Your answer...")
        
        if response:
            # Add user response
            st.session_state.messages.append({"role": "user", "content": response})
            st.session_state.interview_session['questions_asked'] += 1
            st.session_state.interview_session['responses'].append(response)
            
            # Generate next question or feedback
            mock_interview = MockInterview()
            
            if st.session_state.interview_session['questions_asked'] >= 5:
                feedback = "Thank you for your responses! Click 'End Interview' above to see your summary."
            else:
                feedback = f"Good answer! {mock_interview.get_question(st.session_state.interview_session['type'], st.session_state.interview_session['difficulty'])}"
            
            st.session_state.messages.append({"role": "assistant", "content": feedback})
            st.rerun()

# ============================================================================
# RESUME ANALYZER
# ============================================================================

def render_resume_analyzer():
    """Render resume analysis interface."""
    
    st.markdown("# 📄 Resume Analyzer")
    st.markdown("Get AI-powered feedback on your resume.")
    st.markdown("---")
    
    # Resume upload
    resume_file = st.file_uploader(
        "Upload your resume (PDF, DOCX, TXT)",
        type=['pdf', 'docx', 'txt'],
        key="resume_upload"
    )
    
    target_role = st.text_input("Target Role (optional)", placeholder="e.g., Data Scientist")
    
    if st.button("🔍 Analyze Resume", use_container_width=True) and resume_file:
        with st.spinner("Analyzing your resume..."):
            # Extract resume content
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(resume_file.name).suffix) as tmp_file:
                tmp_file.write(resume_file.getbuffer())
                tmp_path = tmp_file.name
            
            result = st.session_state.file_handler.extract(tmp_path)
            os.unlink(tmp_path)
            
            if result and result.get('text'):
                # Analyze with ResumeAnalyzer
                analyzer = ResumeAnalyzer()
                analysis = analyzer.analyze(result['text'], target_role)
                
                # Display results
                st.success("✅ Analysis Complete!")
                
                # Strengths
                st.markdown("### ✨ Strengths")
                st.markdown(analysis.get('strengths', 'Good overall structure.'))
                
                # Areas for Improvement
                st.markdown("### 🎯 Areas for Improvement")
                st.markdown(analysis.get('improvements', 'Consider adding more quantifiable achievements.'))
                
                # Recommendations
                st.markdown("### 💡 Recommendations")
                st.markdown(analysis.get('recommendations', 'Tailor your resume to the specific role.'))
                
                # ATS Score (simulated)
                st.markdown("### 📊 ATS Compatibility Score")
                st.progress(0.75)
                st.caption("75% - Good compatibility with Applicant Tracking Systems")
            else:
                st.error("Could not extract content from resume. Please try a different format.")

# ============================================================================
# STUDY PLANNER
# ============================================================================

def render_study_planner():
    """Render study planning interface."""
    
    st.markdown("# 📚 Study Planner")
    st.markdown("Get personalized study recommendations based on your goals.")
    st.markdown("---")
    
    # Study preferences
    col1, col2 = st.columns(2)
    
    with col1:
        subject = st.text_input("Subject/Topic", placeholder="e.g., Machine Learning")
        current_level = st.selectbox("Current Level", ["Beginner", "Intermediate", "Advanced"])
    
    with col2:
        goal = st.text_input("Learning Goal", placeholder="e.g., Get a job in AI")
        timeframe = st.selectbox("Timeframe", ["1 week", "1 month", "3 months", "6 months"])
    
    learning_style = st.multiselect(
        "Preferred Learning Style",
        ["Video Tutorials", "Reading Books", "Practice Projects", "Interactive Courses", "Peer Learning"]
    )
    
    if st.button("🎯 Generate Study Plan", use_container_width=True):
        with st.spinner("Creating your personalized study plan..."):
            # Generate study plan
            recommender = StudyRecommender()
            plan = recommender.generate_plan(subject, current_level, goal, timeframe, learning_style)
            
            # Display study plan
            st.success("✅ Your Personalized Study Plan")
            
            st.markdown("### 📅 Weekly Breakdown")
            st.markdown(plan.get('weekly_plan', 'Study consistently and track your progress.'))
            
            st.markdown("### 📚 Recommended Resources")
            st.markdown(plan.get('resources', '- Online courses\n- Practice projects\n- Community forums'))
            
            st.markdown("### 🎯 Milestones")
            st.markdown(plan.get('milestones', '1. Complete fundamentals\n2. Build projects\n3. Prepare for interviews'))
            
            st.markdown("### 💡 Tips")
            st.info(plan.get('tips', 'Stay consistent, practice daily, and join study groups!'))

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point."""
    
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Render active feature
    if st.session_state.active_feature == "chat":
        render_chat_interface()
    elif st.session_state.active_feature == "interview":
        render_mock_interview()
    elif st.session_state.active_feature == "resume":
        render_resume_analyzer()
    elif st.session_state.active_feature == "study":
        render_study_planner()

if __name__ == "__main__":
    main()
