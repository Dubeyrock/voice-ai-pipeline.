class ConversationMemory:
    """
    Enhanced sliding window memory with topic tracking.
    - Stores last N turns
    - Tracks topics discussed in the session
    - Provides context summary for LLM
    """

    def __init__(self, max_turns: int = 8):
        self.history = []
        self.max_turns = max_turns
        self.topics = []  # Track what topics user has asked about

    def add_exchange(self, user_msg: str, assistant_msg: str):
        self.history.append({"role": "user", "content": user_msg})
        self.history.append({"role": "assistant", "content": assistant_msg})

        # Sliding window — prevent overflow
        if len(self.history) > self.max_turns * 2:
            self.history = self.history[-(self.max_turns * 2):]

        # Track topic (first 6 words of user message as topic label)
        topic = " ".join(user_msg.split()[:6])
        if topic not in self.topics:
            self.topics.append(topic)

    def get_history(self) -> list:
        return self.history.copy()

    def get_topics(self) -> list:
        return self.topics.copy()

    def get_turn_count(self) -> int:
        return len(self.history) // 2

    def clear(self):
        self.history = []
        self.topics = []


class SessionManager:
    """
    Manages multiple named chat sessions.
    Each session has its own ConversationMemory.
    """

    def __init__(self):
        self.sessions: dict[str, dict] = {}
        self.active_session: str = None

    def create_session(self, name: str):
        """Create a new named session"""
        if name not in self.sessions:
            self.sessions[name] = {
                "memory": ConversationMemory(max_turns=8),
                "chat_log": [],
                "name": name
            }
        self.active_session = name

    def get_session(self, name: str) -> dict:
        return self.sessions.get(name)

    def get_active_session(self) -> dict:
        if self.active_session:
            return self.sessions.get(self.active_session)
        return None

    def switch_session(self, name: str):
        if name in self.sessions:
            self.active_session = name

    def delete_session(self, name: str):
        if name in self.sessions:
            del self.sessions[name]
        if self.active_session == name:
            self.active_session = list(self.sessions.keys())[0] if self.sessions else None

    def list_sessions(self) -> list:
        return list(self.sessions.keys())

    def get_session_count(self) -> int:
        return len(self.sessions)