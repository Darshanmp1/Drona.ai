"""
Drona AI - AI-Powered Study Assistant

Main web interface for Drona AI. Built with Streamlit to provide an intuitive
chat-based experience for students preparing for placements and technical interviews.

Key features:
- Interactive chat interface for Q&A
- Document upload and processing (PDFs, images, text files)
- Web content extraction from URLs and YouTube videos
- Voice input/output for hands-free learning
- Placement preparation tools (mock interviews, resume analysis, study plans)
- Powered by Endee vector database for fast semantic search
"""

import streamlit as st
import sys
import os
from pathlib import Path
import tempfile

# Setup module path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from drona_ai.rag import Embedder, VectorStore, Retriever
from drona_ai.extractors import FileHandler
from drona_ai.memory import ConversationMemory
from drona_ai.llm import OllamaLLM, get_ollama_status, OLLAMA_SETUP
from drona_ai.placement import MockInterview, ResumeAnalyzer, StudyRecommender
from drona_ai.placement.advanced_recommender import AdvancedStudyRecommender
from drona_ai.voice import SpeechToText, TextToSpeech

# Page configuration and theme setup

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
    
    # Interview session tracking
    if 'interview_active' not in st.session_state:
        st.session_state.interview_active = False
    
    if 'interview_session' not in st.session_state:
        st.session_state.interview_session = None
    
    # Speech-to-text instance
    if 'speech_to_text' not in st.session_state:
        st.session_state.speech_to_text = SpeechToText(language="en-US")
    
    # Track last processed file to prevent duplicates
    if 'last_processed_file' not in st.session_state:
        st.session_state.last_processed_file = None
    
    # Track last processed URL to prevent duplicates
    if 'last_processed_url' not in st.session_state:
        st.session_state.last_processed_url = None
    
    # Track last processed prompt to prevent duplicate responses
    if 'last_processed_prompt' not in st.session_state:
        st.session_state.last_processed_prompt = None
    
    # Track processing state
    if 'is_processing' not in st.session_state:
        st.session_state.is_processing = False
    
    # Track last study plan request to prevent duplicates
    if 'last_study_plan_request' not in st.session_state:
        st.session_state.last_study_plan_request = None

# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def process_file_upload(uploaded_file):
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_path = tmp_file.name
        
        # Extract content using FileHandler
        result = st.session_state.file_handler.extract(tmp_path)
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        # Check if extraction was successful
        if result is None:
            return f"❌ Could not extract content from **{uploaded_file.name}**\n\n💡 **Image files require Tesseract OCR**\n- See INSTALL_OCR.md for installation instructions\n- Or upload PDF/TXT/DOCX instead"
        
        if not isinstance(result, dict):
            return f"❌ Invalid extraction result from **{uploaded_file.name}**"
        
        if result.get('text'):
            # Add to knowledge base
            st.session_state.retriever.add_document(
                result['text'],
                metadata={'source': uploaded_file.name, 'type': result.get('type', 'file')}
            )
            st.session_state.docs_count += 1
            
            # Add to uploaded files list
            if uploaded_file.name not in st.session_state.uploaded_files_list:
                st.session_state.uploaded_files_list.append(uploaded_file.name)
            
            return f"✅ **Document processed successfully!**\n\n📄 **File:** {uploaded_file.name}\n📊 **Content:** {len(result['text'])} characters extracted\n\n💡 **You can now ask questions about this document.**"
        else:
            return f"❌ No text content found in **{uploaded_file.name}**"
    
    except Exception as e:
        return f"❌ Error processing file: {str(e)}\n\n💡 Try a different file format"

def process_url_input(url):
    try:
        # Validate URL format first
        if not url.startswith('http://') and not url.startswith('https://'):
            return f"❌ Invalid URL format\n\n💡 URL must start with http:// or https://\n\nExample: https://www.youtube.com/watch?v=..."
        
        # Extract content using FileHandler
        result = st.session_state.file_handler.extract(url)
        
        # Check if extraction was successful
        if result is None:
            # Check if it's a YouTube URL
            if 'youtube.com' in url or 'youtu.be' in url:
                return f"""❌ Could not extract YouTube transcript

**Common reasons:**
- 🚫 **YouTube rate limiting** - Too many requests (most common)
- 📵 Video has no captions/subtitles available
- 🔒 Captions are disabled by the creator
- ❓ Invalid video ID or private video

**Solutions:**
1. ⏱️ **Wait 2-5 minutes** and try again (if rate limited)
2. 🌐 Try a different network/WiFi connection
3. 📋 Copy-paste transcript manually from YouTube
4. 🎥 Try a different video with captions

💡 **Note:** YouTube limits automated transcript requests to prevent abuse."""
            else:
                return f"❌ Could not extract content from URL\n\n**Possible reasons:**\n- Website blocks automated access (403 error)\n- Connection timeout (website too slow)\n- Invalid or broken URL\n- Website has no readable text content\n\n💡 Try:\n- Copy-paste the content manually\n- Upload as PDF/text file instead\n- Use a different URL"
        
        if not isinstance(result, dict):
            return f"❌ Invalid extraction result from URL"
        
        if result.get('text'):
            # Add to knowledge base
            st.session_state.retriever.add_document(
                result['text'],
                metadata={'source': url, 'type': result.get('type', 'url')}
            )
            st.session_state.docs_count += 1
            
            # Show success with content preview
            content_preview = result['text'][:200] + "..." if len(result['text']) > 200 else result['text']
            return f"✅ Successfully extracted content from URL\n\n**Extracted:** {len(result['text'])} characters\n\n**Preview:**\n{content_preview}\n\n💡 You can now ask questions about this content."
        else:
            return f"❌ No text content found at URL\n\n💡 The page may be empty or contain only images/videos"
    
    except Exception as e:
        return f"❌ Error processing URL: {str(e)}\n\n💡 Check if URL is valid and accessible"

def get_ai_response(query):
    try:
        # Retrieve relevant documents (returns tuples: (text, score, metadata))
        results = st.session_state.retriever.retrieve(query, top_k=3)
        
        # Build context from retrieved documents
        context = ""
        if results and len(results) > 0:
            context_parts = []
            for i, result in enumerate(results, 1):
                # Result is a tuple: (text, score, metadata)
                if isinstance(result, tuple) and len(result) >= 3:
                    text, score, metadata = result[0], result[1], result[2]
                    source = metadata.get('source', 'Unknown') if isinstance(metadata, dict) else 'Unknown'
                    text_preview = text[:2000] if text else ''  # Increased from 500 to 2000 chars for better context
                    context_parts.append(f"[Source {i}: {source}]\n{text_preview}")
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
                    if isinstance(result, tuple) and len(result) >= 3:
                        metadata = result[2]
                        if isinstance(metadata, dict) and 'source' in metadata:
                            sources.add(metadata['source'])
                if sources:
                    response += f"\n\n📚 **Sources:** {', '.join(sources)}"
            
            return response
        else:
            # Fallback: Just return retrieved documents
            if results and len(results) > 0:
                response = "⚠️ **Ollama not running - showing retrieved documents only**\n\n"
                # Extract text from tuple
                first_result = results[0]
                if isinstance(first_result, tuple) and len(first_result) >= 1:
                    response += f"**Top Result:**\n{first_result[0][:500]}\n\n"
                
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
    with st.sidebar:
        # Header
        st.markdown("# 🎓 Drona AI")
        st.markdown("*Your AI Study Assistant*")
        st.markdown("---")
        
        # New chat button
        if st.button("➕ New Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        
        # File Upload Feature
        with st.expander("📁 Upload Documents", expanded=False):
            st.markdown("Upload PDFs, images, or text files for Q&A")
            
            sidebar_upload = st.file_uploader(
                "Choose file",
                type=['pdf', 'txt', 'docx', 'png', 'jpg', 'jpeg'],
                key="sidebar_file_upload"
            )
            
            if sidebar_upload:
                # Create unique file ID
                file_id = f"{sidebar_upload.name}_{sidebar_upload.size}"
                
                if st.button("📤 Process File", use_container_width=True, type="primary", key="process_file_btn"):
                    # Check if already processed
                    if st.session_state.last_processed_file != file_id and not st.session_state.is_processing:
                        st.session_state.is_processing = True
                        
                        # Add user message to chat showing what file they're uploading
                        st.session_state.messages.append({"role": "user", "content": f"📄 Process file: {sidebar_upload.name}"})
                        
                        # Process file upload with spinner
                        with st.spinner("📄 Processing file..."):
                            result = process_file_upload(sidebar_upload)
                        
                        st.session_state.messages.append({"role": "assistant", "content": result})
                        st.session_state.last_processed_file = file_id
                        
                        st.session_state.is_processing = False
                        st.rerun()  # Force rerun to display messages
                    elif st.session_state.last_processed_file == file_id:
                        st.info("This file has already been processed. Upload a new file to process.")
        
        # URL/Link Processing Feature
        with st.expander("🔗 Extract from URL", expanded=False):
            st.markdown("Extract content from websites or YouTube")
            
            url_input = st.text_input(
                "Enter URL",
                placeholder="https://...",
                key="sidebar_url_input"
            )
            
            if st.button("🌐 Extract Content", use_container_width=True, key="extract_url_btn"):
                if url_input and not st.session_state.is_processing:
                    # Check if we already processed this URL
                    if st.session_state.last_processed_url != url_input:
                        st.session_state.is_processing = True
                        
                        # Add user message to chat showing what URL they're extracting
                        st.session_state.messages.append({"role": "user", "content": f"🌐 Extract content from: {url_input}"})
                        
                        # Process URL extraction with spinner
                        with st.spinner("⏳ Extracting content..."):
                            result = process_url_input(url_input)
                        
                        st.session_state.messages.append({"role": "assistant", "content": result})
                        st.session_state.last_processed_url = url_input
                        
                        st.session_state.is_processing = False
                        st.rerun()  # Force rerun to display messages
                    else:
                        st.info("✅ This URL has already been processed. Check the chat below.")
                elif not url_input:
                    st.warning("⚠️ Please enter a URL first")
        
        # Voice Assistant Feature
        with st.expander("🎤 Voice Input", expanded=False):
            st.markdown("Speak your question instead of typing")
            
            if st.button("🎙️ Start Recording", use_container_width=True, type="primary"):
                try:
                    with st.spinner("🎤 Listening... Speak now!"):
                        recognized_text = st.session_state.speech_to_text.listen(
                            timeout=5,
                            phrase_time_limit=10
                        )
                    
                    if recognized_text:
                        st.success(f"✅ Heard: '{recognized_text}'")
                        
                        # Add to chat and get response
                        st.session_state.messages.append({"role": "user", "content": recognized_text})
                        
                        with st.spinner("🤔 Thinking..."):
                            response = get_ai_response(recognized_text)
                        
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()
                    else:
                        st.warning("⚠️ No speech detected")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            
            st.caption("💡 Works best in quiet environments")
        
        # Mock Interview Feature
        with st.expander("🎤 Mock Interview", expanded=False):
            st.markdown("**Practice Role-Specific Interview Questions**")
            
            # Check if interview is already active
            if st.session_state.interview_active:
                st.info(f"�� Interview in progress for **{st.session_state.interview_session.get('role', 'Unknown Role')}**")
                
                # Show voice answer button if voice mode is enabled
                if st.session_state.interview_session.get('voice_mode', False):
                    st.markdown("**🎙️ Voice Mode Active**")
                    
                    if st.button("🎤 Answer with Voice", use_container_width=True, key="voice_answer_btn"):
                        try:
                            with st.spinner("🎤 Listening for your answer..."):
                                stt = SpeechToText()
                                answer = stt.listen(timeout=10, phrase_time_limit=30)
                            
                            if answer:
                                # Add user's voice answer to chat
                                st.session_state.messages.append({"role": "user", "content": answer})
                                
                                # Get next question
                                mock_interview = MockInterview()
                                st.session_state.interview_session['questions_asked'] += 1
                                question_num = st.session_state.interview_session['questions_asked']
                                
                                if question_num >= 5:
                                    feedback = f"**Excellent answer!**\n\nThat was question {question_num}/5. You've completed the interview session!\n\n✅ Great practice! Click 'End Interview' to see your summary."
                                else:
                                    next_question = mock_interview.get_question(
                                        st.session_state.interview_session['role'],
                                        st.session_state.interview_session['difficulty']
                                    )
                                    feedback = f"**Good answer!**\n\n**Question {question_num}/5:** {next_question}\n\n🎤 Use voice button or type in chat."
                                    
                                    # Speak the question
                                    tts = TextToSpeech()
                                    if tts.enabled:
                                        tts.speak(f"Good answer! Question {question_num}. {next_question}")
                                
                                st.session_state.messages.append({"role": "assistant", "content": feedback})
                        
                        except Exception as e:
                            st.error(f"❌ Voice error: {str(e)}")
                    
                    st.caption("💡 You can also type answers in the chat below")
                else:
                    st.markdown("**💬 Chat Mode Active**")
                    st.caption("💡 Answer questions in the chat below")
                
                if st.button("⏹️ End Interview", use_container_width=True, type="secondary"):
                    role = st.session_state.interview_session.get('role', 'Unknown')
                    questions_answered = st.session_state.interview_session.get('questions_asked', 0)
                    
                    summary = f"""## 🎯 Interview Session Complete!

**Role:** {role}  
**Difficulty:** {st.session_state.interview_session.get('difficulty', 'N/A')}  
**Questions Answered:** {questions_answered}/5

### 💪 Great job practicing!

**Next Steps:**
- Review your answers and identify areas for improvement
- Practice more with different difficulty levels
- Try other roles to broaden your interview skills

**💡 Tip:** Questions won't repeat until you've gone through all available questions for this role!"""
                    
                    st.session_state.messages.append({"role": "assistant", "content": summary})
                    st.session_state.interview_active = False
                    st.session_state.interview_session = None
            else:
                # Get available roles
                mock_interview_instance = MockInterview()
                available_roles = mock_interview_instance.get_available_roles()
                
                # Role selection
                selected_role = st.selectbox(
                    "Select Job Role",
                    available_roles,
                    help="Choose the role you're preparing for. Select 'Other' for custom roles.",
                    key="interview_role_sidebar"
                )
                
                # Custom role input if "Other" is selected
                if selected_role == "Other":
                    custom_role = st.text_input(
                        "Enter Your Role",
                        placeholder="e.g., QA Engineer, Product Manager",
                        key="custom_role_input"
                    )
                    if custom_role:
                        selected_role = custom_role
                
                difficulty = st.selectbox(
                    "Difficulty Level",
                    ["Beginner", "Intermediate", "Advanced"],
                    index=1,  # Default to Intermediate
                    key="difficulty_sidebar"
                )
                
                # Voice mode toggle
                voice_mode = st.checkbox(
                    "🎙️ Enable Voice Mode",
                    value=False,
                    help="Questions will be spoken aloud, and you can answer with voice",
                    key="voice_mode_toggle"
                )
                
                if st.button("🎬 Start Interview", use_container_width=True, type="primary"):
                    mock_interview = MockInterview()
                    question = mock_interview.get_question(selected_role, difficulty)
                    
                    # Initialize interview session with role
                    st.session_state.interview_session = {
                        'role': selected_role,
                        'difficulty': difficulty,
                        'questions_asked': 1,
                        'voice_mode': voice_mode
                    }
                    st.session_state.interview_active = True
                    
                    # Get role-specific tips
                    tips = mock_interview.get_tips_for_role(selected_role)
                    tips_text = "\n".join(tips[:3])  # Top 3 tips
                    
                    mode_text = "🎙️ Voice & Chat" if voice_mode else "💬 Chat"
                    intro = f"""## 🎤 Mock Interview Started!

**Role:** {selected_role}  
**Level:** {difficulty}  
**Mode:** {mode_text}

### 📚 Quick Prep Tips:
{tips_text}

---

**Question 1/5:** {question}

💡 {'Use the Voice button in sidebar or type' if voice_mode else 'Type your answer in the chat below'}."""
                    
                    st.session_state.messages.append({"role": "assistant", "content": intro})
                    
                    # Speak the first question if voice mode
                    if voice_mode:
                        try:
                            tts = TextToSpeech()
                            if tts.enabled:
                                tts.speak(f"Mock interview for {selected_role} role starting now. Question 1. {question}")
                        except Exception as e:
                            print(f"TTS Error: {e}")
        
        # Resume Analyzer Feature
        with st.expander("📄 Resume Analyzer", expanded=False):
            st.markdown("Get AI feedback on your resume")
            
            resume_file = st.file_uploader(
                "Upload Resume",
                type=['pdf', 'docx', 'txt'],
                key="resume_upload_sidebar"
            )
            
            target_role = st.text_input(
                "Target Role (optional)",
                placeholder="e.g., Software Engineer",
                key="target_role_sidebar"
            )
            
            if resume_file and st.button("🔍 Analyze", use_container_width=True, key="analyze_resume_btn"):
                # Check if already analyzed
                if 'last_resume_analyzed' not in st.session_state:
                    st.session_state.last_resume_analyzed = None
                
                # Only analyze if different file or first time
                current_file_id = f"{resume_file.name}_{resume_file.size}"
                
                if st.session_state.last_resume_analyzed != current_file_id:
                    with st.spinner("Analyzing resume..."):
                        # Extract resume content
                        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(resume_file.name).suffix) as tmp_file:
                            tmp_file.write(resume_file.getbuffer())
                            tmp_path = tmp_file.name
                        
                        try:
                            result = st.session_state.file_handler.extract(tmp_path)
                            os.unlink(tmp_path)
                            
                            if result is not None and isinstance(result, dict) and result.get('text'):
                                analyzer = ResumeAnalyzer()
                                analysis = analyzer.analyze(result['text'], target_role)
                                
                                # Extract comprehensive analysis
                                overall_score = analysis.get('overall_score', 70)
                                ats_score = analysis.get('ats_score', 60)
                                sections = analysis.get('sections', {})
                                mistakes = analysis.get('mistakes', [])
                                ats_details = analysis.get('ats_details', {})
                                personalized_tips = analysis.get('personalized_tips', [])
                                quantification = analysis.get('quantification', {})
                                keywords = analysis.get('keywords', {})
                                suggestions = analysis.get('suggestions', [])
                                
                                # Build comprehensive feedback message
                                feedback = f"""## Resume Analysis Complete

### Overall Scores

**Overall Quality:** {overall_score}/100
- {'Excellent - You have a strong resume' if overall_score >= 80 else 'Good with room for improvement' if overall_score >= 60 else 'Needs improvement - significant changes recommended'}

**ATS Compatibility:** {ats_score}/100
- {ats_details.get('recommendation', 'Check ATS compatibility')}

---

### Sections Found
{', '.join(sections.get('found', ['None'])) if sections.get('found') else 'None'}

### Missing Sections
{', '.join(sections.get('missing', ['None'])) if sections.get('missing') else 'All key sections present'}

---

### Detailed Analysis

**Keywords:** {keywords.get('total_count', 0)} technical keywords found
- Categories: {', '.join(keywords.get('categories_covered', [])) if keywords.get('categories_covered') else 'Add more technical skills'}

**Quantified Achievements:** {quantification.get('count', 0)}
- {quantification.get('feedback', 'Add numbers to show impact')}

**Action Verbs:** {'Strong use of action verbs' if analysis.get('action_verbs', {}).get('strong_verbs_count', 0) >= 5 else 'Consider adding more action verbs'}

---"""
                                
                                # Add ATS Details
                                if ats_details.get('strengths'):
                                    feedback += "\n\n### ATS Strengths\n"
                                    for strength in ats_details['strengths'][:5]:
                                        feedback += f"- {strength}\n"
                                
                                if ats_details.get('issues'):
                                    feedback += "\n\n### ATS Issues to Fix\n"
                                    for issue in ats_details['issues'][:5]:
                                        feedback += f"- {issue}\n"
                                
                                # Add Mistakes if found
                                if mistakes:
                                    feedback += "\n\n### Mistakes Detected\n"
                                    for i, mistake in enumerate(mistakes[:8], 1):
                                        feedback += f"\n**{i}. {mistake['issue']}**\n"
                                        feedback += f"   - Fix: {mistake['fix']}\n"
                                        if mistake.get('occurrences', 1) > 1:
                                            feedback += f"   - Found {mistake['occurrences']} times\n"
                                
                                # Add Personalized Tips
                                if personalized_tips:
                                    feedback += "\n\n### Personalized Recommendations"
                                    if target_role:
                                        feedback += f" for {target_role}\n"
                                    else:
                                        feedback += "\n"
                                    for tip in personalized_tips[:10]:
                                        feedback += f"- {tip}\n"
                                
                                # Add Top Suggestions
                                if suggestions:
                                    feedback += "\n\n### Improvement Suggestions\n"
                                    for suggestion in suggestions[:15]:
                                        feedback += f"- {suggestion}\n"
                                
                                feedback += "\n\n---\n\n**Note:** Tailor your resume for each job by adding relevant keywords from the job description."
                                
                                st.session_state.messages.append({"role": "assistant", "content": feedback})
                                st.session_state.last_resume_analyzed = current_file_id
                                st.success("Analysis complete! Check chat for detailed feedback.")
                                # Streamlit automatically reruns on button click
                            else:
                                st.error("Could not extract text from resume")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                            if os.path.exists(tmp_path):
                                os.unlink(tmp_path)
                else:
                    st.info("This resume was already analyzed. Upload a new file to analyze again.")
        
        # Study Planner Feature
        with st.expander("📚 Study Planner", expanded=False):
            st.markdown("Get personalized study plan")
            
            subject = st.text_input(
                "Subject",
                placeholder="e.g., Machine Learning",
                key="subject_sidebar"
            )
            
            level = st.selectbox(
                "Current Level",
                ["Beginner", "Intermediate", "Advanced"],
                key="level_sidebar"
            )
            
            timeframe = st.selectbox(
                "Timeframe",
                ["1 week", "1 month", "3 months"],
                key="timeframe_sidebar"
            )
            
            if st.button("🎯 Generate Plan", use_container_width=True, key="generate_plan_btn"):
                if subject:
                    # Create unique request ID to prevent duplicate processing
                    request_id = f"{subject}|{level}|{timeframe}"
                    
                    # Only process if this is a NEW request
                    if request_id != st.session_state.last_study_plan_request:
                        st.session_state.last_study_plan_request = request_id
                        
                        # Add user message showing the request
                        user_message = f"📚 Generate study plan for: {subject} ({level}, {timeframe})"
                        st.session_state.messages.append({"role": "user", "content": user_message})
                        
                        # Use Advanced Study Recommender for comprehensive personalization
                        advanced_recommender = AdvancedStudyRecommender()
                        plan = advanced_recommender.generate_advanced_plan(subject, level, timeframe)
                        
                        # Format rich comprehensive plan
                        plan_text = f"""**🎓 Personalized Study Plan: {subject}**

📅 **Timeline:** {timeframe} | 📈 **Level:** {level}

---

## 📚 Weekly Curriculum

{plan.get('weekly_plan', 'Study consistently')}

---

## 🎯 Milestones

{plan.get('milestones', 'Focus on steady progress')}

---

{plan.get('daily_schedule', '')}

---

{plan.get('projects', '')}

---

## 💡 Pro Tips

{plan.get('tips', 'Stay consistent!')}

---

{plan.get('total_hours', '')}"""
                        
                        st.session_state.messages.append({"role": "assistant", "content": plan_text})
                        st.rerun()
                else:
                    st.warning("⚠️ Please enter a subject")
        
        st.markdown("---")
        
        # System Status
        st.markdown("### ⚙️ System Status")
        
        # Refresh backend info (check current status)
        backend_info = st.session_state.vector_store.get_backend_info()
        
        # Endee DB status
        if backend_info['backend'] == 'endee' and backend_info.get('connected', False):
            st.markdown("🟢 **Endee DB:** Connected")
            doc_count = backend_info.get('document_count', 0)
            if doc_count > 0:
                st.caption(f"📊 Documents stored: {doc_count}")
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
    # Welcome message (only show if no messages yet)
    if len(st.session_state.messages) == 0:
        st.info("""
        👋 **Welcome to Drona AI!**
        
        **All features are in the sidebar →**
        
        - 📁 Upload documents
        - 🔗 Extract from URLs
        - 🎤 Voice input
        - 🎤 Mock interviews
        - 📄 Resume analysis
        - 📚 Study planning
        
        **Just type your question below or use sidebar features!**
        """)
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Main chat input - MUST BE AT ROOT LEVEL
    prompt = st.chat_input("Ask anything...")
    
    # Clear last processed prompt if user hasn't typed anything
    if not prompt and 'last_processed_prompt' in st.session_state:
        st.session_state.last_processed_prompt = None
    
    # Only process new prompts (not duplicates from rerun)
    if prompt and not st.session_state.is_processing:
        # Check if this is a different prompt than last processed
        if prompt != st.session_state.get('last_processed_prompt', None):
            st.session_state.is_processing = True
            st.session_state.last_processed_prompt = prompt
            
            try:
                # Add user message
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                # Check if in mock interview mode
                if st.session_state.interview_active and st.session_state.interview_session:
                    # Interview mode: provide feedback and next question
                    mock_interview = MockInterview()
                    
                    st.session_state.interview_session['questions_asked'] += 1
                    question_num = st.session_state.interview_session['questions_asked']
                    
                    if question_num >= 5:
                        # End interview after 5 questions
                        feedback = f"**Great answer!**\\n\\nThat was question {question_num}. You've completed the interview session!\\n\\n🎯 Use the sidebar to end the interview and see your summary."
                    else:
                        # Ask next question based on role
                        next_question = mock_interview.get_question(
                            st.session_state.interview_session.get('role', 'Software Engineer'),
                            st.session_state.interview_session['difficulty']
                        )
                        feedback = f"**Good answer!**\\n\\n**Question {question_num}/5:** {next_question}\\n\\n💡 Take your time to answer."
                        
                        # Speak the question if voice mode is enabled
                        if st.session_state.interview_session.get('voice_mode', False):
                            try:
                                tts = TextToSpeech()
                                if tts.enabled:
                                    tts.speak(f"Good answer! Question {question_num}. {next_question}")
                            except Exception as e:
                                print(f"TTS Error: {e}")
                    
                    st.session_state.messages.append({"role": "assistant", "content": feedback})
                else:
                    # Normal chat mode: Generate AI response
                    with st.spinner("🤔 Thinking..."):
                        response = get_ai_response(prompt)
                    
                    # Add assistant response
                    st.session_state.messages.append({"role": "assistant", "content": response})
            
            except Exception as e:
                # Handle any errors and reset processing flag
                error_msg = f"❌ Error: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
            finally:
                # Always reset processing flag
                st.session_state.is_processing = False
                st.rerun()

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar with ALL features
    render_sidebar()
    
    # Render clean chat interface in main area
    render_chat_interface()

if __name__ == "__main__":
    main()
