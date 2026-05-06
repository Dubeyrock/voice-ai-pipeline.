import streamlit as st
import os
import tempfile
from pipeline.stt import transcribe_audio
from pipeline.llm import get_llm_response
from pipeline.tts import text_to_speech
from pipeline.memory import SessionManager

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VoiceIQ — AI Voice Assistant",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Hide Streamlit Branding ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; }

/* ── Hero Banner ── */
.hero-wrap {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1040 50%, #0d1f3c 100%);
    border-radius: 20px;
    padding: 48px 48px 40px 48px;
    margin-bottom: 2rem;
    border: 1px solid rgba(255,255,255,0.08);
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(99,102,241,0.3) 0%, transparent 70%);
    pointer-events: none;
}
.hero-wrap::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(34,197,94,0.2) 0%, transparent 70%);
    pointer-events: none;
}
.hero-badge {
    display: inline-block;
    background: rgba(99,102,241,0.2);
    border: 1px solid rgba(99,102,241,0.5);
    color: #a5b4fc;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 4px 14px;
    border-radius: 99px;
    margin-bottom: 16px;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 52px;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.05;
    margin: 0 0 8px 0;
    letter-spacing: -1px;
}
.hero-title span {
    background: linear-gradient(90deg, #818cf8, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 17px;
    color: rgba(255,255,255,0.55);
    font-weight: 300;
    margin: 0 0 28px 0;
    max-width: 560px;
    line-height: 1.6;
}
.hero-stats {
    display: flex;
    gap: 32px;
    flex-wrap: wrap;
}
.hero-stat {
    text-align: left;
}
.hero-stat-num {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
}
.hero-stat-label {
    font-size: 12px;
    color: rgba(255,255,255,0.4);
    letter-spacing: 0.05em;
}

/* ── Feature Cards ── */
.features-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 2rem;
}
.feat-card {
    background: #f8faff;
    border: 1px solid #e5e7f0;
    border-radius: 14px;
    padding: 20px;
    transition: border-color 0.2s;
}
.feat-card:hover { border-color: #818cf8; }
.feat-icon {
    font-size: 26px;
    margin-bottom: 10px;
    display: block;
}
.feat-title {
    font-family: 'Syne', sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 6px;
}
.feat-desc {
    font-size: 13px;
    color: #6b7280;
    line-height: 1.55;
}

/* ── How To Use Section ── */
.howto-wrap {
    background: #fafafa;
    border: 1px solid #e5e7f0;
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 2rem;
}
.howto-title {
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 16px;
}
.howto-steps {
    display: flex;
    gap: 0;
    align-items: flex-start;
    flex-wrap: wrap;
}
.howto-step {
    flex: 1;
    min-width: 140px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    position: relative;
    padding: 0 12px;
}
.howto-step:not(:last-child)::after {
    content: '→';
    position: absolute;
    right: -8px;
    top: 14px;
    color: #d1d5db;
    font-size: 18px;
}
.step-circle {
    width: 40px; height: 40px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    margin-bottom: 8px;
}
.step-text {
    font-size: 12px;
    font-weight: 600;
    color: #374151;
}
.step-sub {
    font-size: 11px;
    color: #9ca3af;
    margin-top: 2px;
}

/* ── Section Heading ── */
.section-heading {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #111827;
    margin: 0 0 4px 0;
}
.section-sub {
    font-size: 13px;
    color: #9ca3af;
    margin-bottom: 16px;
}

/* ── Step Labels ── */
.step-label {
    font-size: 11px;
    font-weight: 700;
    color: #9ca3af;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin: 20px 0 6px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}
.step-label-dot {
    width: 18px; height: 18px;
    border-radius: 50%;
    background: #6366f1;
    color: white;
    font-size: 10px;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}

/* ── Output Boxes ── */
.transcript-box {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-left: 4px solid #3b82f6;
    padding: 14px 18px;
    border-radius: 10px;
    font-size: 15px;
    color: #1e3a5f;
    margin: 8px 0 16px 0;
    line-height: 1.6;
}
.response-box {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-left: 4px solid #22c55e;
    padding: 14px 18px;
    border-radius: 10px;
    font-size: 15px;
    color: #14532d;
    margin: 8px 0 16px 0;
    line-height: 1.6;
}

/* ── Topic Pills ── */
.topic-pill {
    display: inline-block;
    background: #ede9fe;
    color: #5b21b6;
    font-size: 11px;
    padding: 3px 10px;
    border-radius: 99px;
    margin: 2px 3px;
    font-weight: 600;
}

/* ── Chat Bubbles ── */
.chat-user {
    background: #f1f5f9;
    border-radius: 14px 14px 14px 4px;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 14px;
    color: #1e293b;
    border: 1px solid #e2e8f0;
}
.chat-ai {
    background: #f0fdf4;
    border-radius: 14px 14px 4px 14px;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 14px;
    color: #14532d;
    border: 1px solid #dcfce7;
    margin-left: 20px;
}
.chat-turn-num {
    font-size: 11px;
    color: #9ca3af;
    text-align: center;
    margin: 12px 0 4px 0;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* ── Sidebar ── */
.sidebar-brand {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 800;
    color: #111827;
    letter-spacing: -0.5px;
    margin-bottom: 4px;
}
.sidebar-brand span { color: #6366f1; }
.sidebar-tagline {
    font-size: 11px;
    color: #9ca3af;
    margin-bottom: 16px;
}
.session-info-card {
    background: #f8faff;
    border: 1px solid #e0e7ff;
    border-radius: 12px;
    padding: 14px;
    margin-top: 8px;
}
.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    color: #6b7280;
    margin-bottom: 6px;
}
.info-val {
    font-weight: 700;
    color: #111827;
}

/* ── Pipeline status tag ── */
.pipeline-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    color: #15803d;
    font-size: 12px;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 99px;
}
</style>
""", unsafe_allow_html=True)

# ─── Session Manager Init ──────────────────────────────────────────────────────
if "session_manager" not in st.session_state:
    sm = SessionManager()
    sm.create_session("Session 1")
    st.session_state.session_manager = sm
if "show_intro" not in st.session_state:
    st.session_state.show_intro = True

sm: SessionManager = st.session_state.session_manager

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="sidebar-brand">Voice<span>IQ</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">AI-Powered Voice Pipeline</div>', unsafe_allow_html=True)
    st.divider()

    st.markdown("**💬 Conversations**")
    st.caption("Each session has its own memory & history.")

    if st.button("➕ New Conversation", use_container_width=True, type="primary"):
        count = sm.get_session_count() + 1
        name = f"Session {count}"
        sm.create_session(name)
        sm.switch_session(name)
        st.session_state.show_intro = False
        st.rerun()

    st.markdown("")

    for sname in sm.list_sessions():
        session = sm.get_session(sname)
        turns = len(session["chat_log"])
        is_active = (sname == sm.active_session)
        col_a, col_b = st.columns([4, 1])
        with col_a:
            label = f"{'● ' if is_active else '○ '}{sname}  ({turns}t)"
            if st.button(label, key=f"sw_{sname}", use_container_width=True):
                sm.switch_session(sname)
                st.session_state.show_intro = False
                st.rerun()
        with col_b:
            if not is_active:
                if st.button("✕", key=f"del_{sname}", help="Delete"):
                    sm.delete_session(sname)
                    st.rerun()

    st.divider()

    # Active session details
    active = sm.get_active_session()
    if active and not st.session_state.show_intro:
        memory = active["memory"]
        turns = memory.get_turn_count()
        topics = memory.get_topics()

        st.markdown(f"""
        <div class="session-info-card">
            <div class="info-row"><span>Active Session</span><span class="info-val">{sm.active_session}</span></div>
            <div class="info-row"><span>Turns Used</span><span class="info-val">{turns} / 8</span></div>
            <div class="info-row"><span>Model</span><span class="info-val">LLaMA 3.1</span></div>
            <div class="info-row"><span>STT</span><span class="info-val">Whisper v3</span></div>
        </div>
        """, unsafe_allow_html=True)

        if topics:
            st.markdown("<br>**🏷️ Topics Covered**", unsafe_allow_html=True)
            pills = "".join([f'<span class="topic-pill">{t[:22]}</span>' for t in topics[-6:]])
            st.markdown(pills, unsafe_allow_html=True)

        st.markdown("")
        if st.button("🗑️ Clear Session History", use_container_width=True):
            active["memory"].clear()
            active["chat_log"] = []
            st.rerun()

    st.divider()
    st.caption("Built with Groq · Whisper · LLaMA · gTTS")

# ══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════════════════════════════

# ── Hero Banner ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">🎙️ Voice AI Pipeline — Assignment Build</div>
    <div class="hero-title">Voice<span>IQ</span></div>
    <div class="hero-sub">
        Speak naturally — VoiceIQ transcribes your voice, understands context, 
        and responds with a human-like voice. Powered by Groq's ultra-fast inference.
    </div>
    <div class="hero-stats">
        <div class="hero-stat">
            <div class="hero-stat-num">~1s</div>
            <div class="hero-stat-label">Avg Response Time</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-num">Whisper v3</div>
            <div class="hero-stat-label">STT Engine</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-num">LLaMA 3.1</div>
            <div class="hero-stat-label">Language Model</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-num">Multi-turn</div>
            <div class="hero-stat-label">Memory Support</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Features Grid ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="features-grid">
    <div class="feat-card">
        <span class="feat-icon">🎤</span>
        <div class="feat-title">Live Voice Recording</div>
        <div class="feat-desc">Record directly from your browser mic or upload any audio file (WAV, MP3, M4A). No setup required.</div>
    </div>
    <div class="feat-card">
        <span class="feat-icon">⚡</span>
        <div class="feat-title">Groq-Powered Speed</div>
        <div class="feat-desc">Whisper Large v3 transcribes your audio in milliseconds via Groq's LPU inference engine.</div>
    </div>
    <div class="feat-card">
        <span class="feat-icon">🧠</span>
        <div class="feat-title">Contextual Memory</div>
        <div class="feat-desc">LLaMA 3.1 remembers your entire conversation. Ask follow-ups — it builds on previous answers.</div>
    </div>
    <div class="feat-card">
        <span class="feat-icon">🔊</span>
        <div class="feat-title">Voice Response</div>
        <div class="feat-desc">AI responses are converted to natural speech using gTTS. Listen directly in the browser.</div>
    </div>
    <div class="feat-card">
        <span class="feat-icon">💬</span>
        <div class="feat-title">Multiple Sessions</div>
        <div class="feat-desc">Create separate conversation sessions. Each has its own history, memory, and topic tracking.</div>
    </div>
    <div class="feat-card">
        <span class="feat-icon">🏷️</span>
        <div class="feat-title">Topic Awareness</div>
        <div class="feat-desc">VoiceIQ tracks discussed topics and goes deeper on revisited subjects instead of repeating basics.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── How To Use ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="howto-wrap">
    <div class="howto-title">📖 How to Use VoiceIQ</div>
    <div class="howto-steps">
        <div class="howto-step">
            <div class="step-circle" style="background:#ede9fe;">🎤</div>
            <div class="step-text">Record or Upload</div>
            <div class="step-sub">Speak or drop an audio file</div>
        </div>
        <div class="howto-step">
            <div class="step-circle" style="background:#dbeafe;">📝</div>
            <div class="step-text">Auto Transcribe</div>
            <div class="step-sub">Whisper converts speech to text</div>
        </div>
        <div class="howto-step">
            <div class="step-circle" style="background:#dcfce7;">🧠</div>
            <div class="step-text">AI Understands</div>
            <div class="step-sub">LLaMA 3.1 processes with memory</div>
        </div>
        <div class="howto-step">
            <div class="step-circle" style="background:#fef9c3;">🔊</div>
            <div class="step-text">Listen to Reply</div>
            <div class="step-sub">Response converted to speech</div>
        </div>
        <div class="howto-step">
            <div class="step-circle" style="background:#fee2e2;">🔁</div>
            <div class="step-text">Keep Talking</div>
            <div class="step-sub">Ask follow-ups — it remembers!</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# PIPELINE SECTION
# ══════════════════════════════════════════════════════════════════════════════
active = sm.get_active_session()
session_name = sm.active_session

col_title, col_tag = st.columns([4, 1])
with col_title:
    st.markdown(f'<div class="section-heading">🎙️ {session_name}</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Record your voice and run the full AI pipeline below.</div>', unsafe_allow_html=True)
with col_tag:
    st.markdown('<div class="pipeline-tag">✓ Pipeline Ready</div>', unsafe_allow_html=True)

# ── Step 1: Audio Input ────────────────────────────────────────────────────────
st.markdown('<div class="step-label"><span class="step-label-dot">1</span> Audio Input</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🎤 Record from Mic", "📁 Upload Audio File"])
audio_bytes = None

with tab1:
    st.caption("Click the microphone icon below to start recording. Click again to stop.")
    recorded = st.audio_input("Record your voice", key=f"mic_{session_name}")
    if recorded:
        audio_bytes = recorded

with tab2:
    st.caption("Supports WAV, MP3, M4A, OGG. Max ~25MB.")
    uploaded = st.file_uploader(
        "Drop your audio file here",
        type=["wav", "mp3", "m4a", "ogg"],
        key=f"upload_{session_name}",
        label_visibility="collapsed"
    )
    if uploaded:
        audio_bytes = uploaded
        st.success(f"✅ Uploaded: `{uploaded.name}`")

if audio_bytes:
    st.caption("**Preview your audio:**")
    st.audio(audio_bytes)
    st.markdown("")

    run = st.button("🚀 Run VoiceIQ Pipeline", type="primary", use_container_width=True)

    if run:
        # Save temp file
        suffix = ".wav"
        if hasattr(audio_bytes, "name"):
            ext = os.path.splitext(audio_bytes.name)[-1]
            if ext: suffix = ext

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            data = audio_bytes.read() if hasattr(audio_bytes, 'read') else audio_bytes.getvalue()
            tmp.write(data)
            tmp_path = tmp.name

        # ── Step 2: STT ────────────────────────────────────────────────────────
        st.markdown('<div class="step-label"><span class="step-label-dot">2</span> Speech → Text (Whisper via Groq)</div>', unsafe_allow_html=True)
        with st.spinner("Transcribing your audio with Whisper Large v3..."):
            try:
                transcript = transcribe_audio(tmp_path)
                os.unlink(tmp_path)
                st.markdown(
                    f'<div class="transcript-box">📝 <b>Transcription Result:</b><br><br>{transcript}</div>',
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"❌ Transcription failed: {e}")
                os.unlink(tmp_path)
                st.stop()

        # ── Step 3: LLM ────────────────────────────────────────────────────────
        st.markdown('<div class="step-label"><span class="step-label-dot">3</span> LLM Response (LLaMA 3.1 via Groq)</div>', unsafe_allow_html=True)
        with st.spinner("LLaMA 3.1 is processing with conversation context..."):
            try:
                history = active["memory"].get_history()
                topics  = active["memory"].get_topics()
                response = get_llm_response(transcript, history, topics_discussed=topics)
                active["memory"].add_exchange(transcript, response)
                st.markdown(
                    f'<div class="response-box">🤖 <b>AI Response:</b><br><br>{response}</div>',
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"❌ LLM Error: {e}")
                st.stop()

        # ── Step 4: TTS ────────────────────────────────────────────────────────
        st.markdown('<div class="step-label"><span class="step-label-dot">4</span> Text → Speech (gTTS Output)</div>', unsafe_allow_html=True)
        with st.spinner("Converting response to audio..."):
            try:
                output_path = text_to_speech(response)
                st.caption("**Listen to AI's voice response:**")
                st.audio(output_path, format="audio/mp3")
                st.success("✅ Pipeline complete! You can record another message to continue the conversation.")
            except Exception as e:
                st.error(f"❌ TTS Error: {e}")
                st.stop()

        active["chat_log"].append({"user": transcript, "ai": response})
        st.session_state.show_intro = False

else:
    st.info("👆 Use the tabs above to record your voice or upload an audio file, then click **Run VoiceIQ Pipeline**.")

# ── Conversation History ───────────────────────────────────────────────────────
if active and active["chat_log"]:
    st.divider()
    st.markdown(f'<div class="section-heading">💬 Conversation History</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-sub">{len(active["chat_log"])} turn(s) in {session_name} — AI remembers all of these.</div>', unsafe_allow_html=True)

    for i, turn in enumerate(active["chat_log"]):
        st.markdown(f'<div class="chat-turn-num">— Turn {i+1} —</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="chat-user">🧑 <b>You:</b> {turn["user"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="chat-ai">🤖 <b>VoiceIQ:</b> {turn["ai"]}</div>', unsafe_allow_html=True)