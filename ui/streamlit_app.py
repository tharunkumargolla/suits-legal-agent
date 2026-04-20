"""
Pearson Specter - Legal AI Interface
A Suits-themed multi-agent legal consultation system
"""
import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv

# Import UI components
from ui.components.styles import get_custom_css

# Agent imports are deferred until initialization to avoid heavy top-level imports
from ui.components.agent_avatar import (
    get_agent_avatar, 
    get_agent_color, 
    get_agent_title,
    agent_message_box,
    loading_indicator
)

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Pearson Specter",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)


# Custom CSS for Suits theme
st.markdown("""
<style>
    /* Pearson Specter Theme */
    .stApp {
        background-color: #0a0a0a;
    }
    
    .main-header {
        color: #c9a84c;
        font-family: 'Georgia', serif;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        border-bottom: 2px solid #c9a84c;
        padding-bottom: 1rem;
        margin-bottom: 2rem;
    }
    
    .agent-message {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .donna-message {
        background: linear-gradient(135deg, #2a1a2e 0%, #1a0a1e 100%);
        border-left: 4px solid #c9a84c;
    }
    
    .mike-message {
        background: linear-gradient(135deg, #1a2a3e 0%, #0a1a2e 100%);
        border-left: 4px solid #4a90d9;
    }
    
    .harvey-message {
        background: linear-gradient(135deg, #2a1a1a 0%, #1a0a0a 100%);
        border-left: 4px solid #c94c4c;
    }
    
    .louis-message {
        background: linear-gradient(135deg, #2a2a1a 0%, #1a1a0a 100%);
        border-left: 4px solid #c9a84c;
    }
    
    .jessica-message {
        background: linear-gradient(135deg, #1a2a2a 0%, #0a1a1a 100%);
        border-left: 4px solid #4cc9c9;
    }
    
    .agent-name {
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .donna-name { color: #c9a84c; }
    .mike-name { color: #4a90d9; }
    .harvey-name { color: #c94c4c; }
    .louis-name { color: #c9a84c; }
    .jessica-name { color: #4cc9c9; }
    
    .sidebar-header {
        color: #c9a84c;
        font-size: 1.2rem;
        font-weight: bold;
        margin-top: 1rem;
    }
    
    .status-badge {
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .status-active {
        background-color: #2e7d32;
        color: white;
    }
    
    .status-pending {
        background-color: #c9a84c;
        color: black;
    }
    
    /* Chat input styling */
    .stChatInput {
        border-top: 1px solid #333;
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


class PearsonSpecterUI:
    def __init__(self):
        # Initialize session state - NO heavy imports here
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'case_active' not in st.session_state:
            st.session_state.case_active = False
        if 'current_agent' not in st.session_state:
            st.session_state.current_agent = None
        if 'firm' not in st.session_state:
            st.session_state.firm = None  # Lazy - initialized on first case
        if 'case_facts' not in st.session_state:
            st.session_state.case_facts = None
        if 'research' not in st.session_state:
            st.session_state.research = None
        if 'strategy' not in st.session_state:
            st.session_state.strategy = None
        if 'compliance' not in st.session_state:
            st.session_state.compliance = None
    
    def init_agents(self):
        """Initialize all firm agents - called lazily on first case"""
        from agents.Donna import Donna
        from agents.mike import Mike
        from agents.harvey import Harvey
        from agents.louis import Louis
        from agents.Jessica import Jessica

        return {
            'donna': Donna(),
            'mike': Mike(),
            'harvey': Harvey(),
            'louis': Louis(),
            'jessica': Jessica()
        }
    
    def get_firm(self):
        """Get or lazily initialize the firm agents"""
        if st.session_state.firm is None:
            with st.spinner("⚖️ Assembling the team at Pearson Specter..."):
                st.session_state.firm = self.init_agents()
        return st.session_state.firm
    
    def add_message(self, agent: str, content: str, agent_class: str):
        """Add a message to the chat history"""
        st.session_state.messages.append({
            'agent': agent,
            'content': content,
            'class': agent_class
        })
    
    def display_message(self, msg: dict):
        """Display a single message with appropriate styling"""
        agent_class = msg['class']
        agent_name = msg['agent']
        content = msg['content']
        
        with st.chat_message(agent_name.lower(), avatar=self.get_avatar(agent_class)):
            st.markdown(f"**{agent_name}**")
            st.markdown(content)
    
    def get_avatar(self, agent_class: str) -> str:
        """Return emoji avatar for each agent"""
        avatars = {
            'donna': '👩‍💼',
            'mike': '📚',
            'harvey': '👔',
            'louis': '📋',
            'jessica': '👑'
        }
        return avatars.get(agent_class, '⚖️')
    
    def run_case(self, client_input: str):
        """Execute the full firm workflow"""
        firm = self.get_firm()
        
        # 1. Donna - Intake
        with st.spinner("👩‍💼 Donna is taking notes..."):
            st.session_state.current_agent = "Donna Paulsen"
            facts = firm['donna'].intake(client_input)
            st.session_state.case_facts = facts
            self.add_message("Donna Paulsen", facts, "donna")
        
        # 2. Mike - Research
        with st.spinner("📚 Mike is searching his memory..."):
            st.session_state.current_agent = "Mike Ross"
            research = firm['mike'].research(
                query=client_input,
                facts=facts
            )
            st.session_state.research = research
            self.add_message("Mike Ross", research, "mike")
        
        # 3. Harvey - Strategy
        with st.spinner("👔 Harvey is crafting the strategy..."):
            st.session_state.current_agent = "Harvey Specter"
            strategy = firm['harvey'].strategize(facts, research)
            st.session_state.strategy = strategy
            self.add_message("Harvey Specter", strategy, "harvey")
        
        # 4. Louis - Compliance
        with st.spinner("📋 Louis is checking compliance..."):
            st.session_state.current_agent = "Louis Litt"
            compliance = firm['louis'].review(facts, strategy)
            st.session_state.compliance = compliance
            self.add_message("Louis Litt", compliance, "louis")
        
        # 5. Jessica - Final Ruling
        with st.spinner("👑 Jessica is making her ruling..."):
            st.session_state.current_agent = "Jessica Pearson"
            ruling = firm['jessica'].decide(facts, strategy, compliance)
            self.add_message("Jessica Pearson", ruling, "jessica")
        
        st.session_state.case_active = False
        st.session_state.current_agent = None
    
    def render_sidebar(self):
        """Render the sidebar with firm information"""
        with st.sidebar:
            st.markdown("## ⚖️ PEARSON SPECTER")
            st.markdown("*New York's Finest*")
            st.markdown("---")
            
            st.markdown("### 👥 The Team")
            
            agents = [
                ("👩‍💼 Donna Paulsen", "COO & Intake Specialist"),
                ("📚 Mike Ross", "Associate & Researcher"),
                ("👔 Harvey Specter", "Name Partner & Strategist"),
                ("📋 Louis Litt", "Junior Partner & Compliance"),
                ("👑 Jessica Pearson", "Managing Partner")
            ]
            
            for name, role in agents:
                st.markdown(f"**{name}**")
                st.markdown(f"*{role}*")
                st.markdown("---")
            
            if st.session_state.current_agent:
                st.markdown("### 🔄 Currently Working")
                st.info(f"**{st.session_state.current_agent}** is on it")
            
            if st.button("🗑️ Clear Conversation"):
                st.session_state.messages = []
                st.session_state.case_active = False
                st.session_state.case_facts = None
                st.session_state.research = None
                st.session_state.strategy = None
                st.session_state.compliance = None
                st.session_state.firm = None
                st.rerun()
    
    def run(self):
        """Main UI loop"""
        
        # Header
        st.markdown('<div class="main-header">⚖️ PEARSON SPECTER</div>', unsafe_allow_html=True)
        
        # Render sidebar
        self.render_sidebar()
        
        # Welcome message
        if len(st.session_state.messages) == 0:
            with st.chat_message("assistant", avatar="⚖️"):
                st.markdown("**Jessica Pearson**")
                st.markdown("*What do we have?*")
                st.markdown("Describe your legal situation, and I'll put the right people on it.")
        
        # Display conversation history
        for msg in st.session_state.messages:
            self.display_message(msg)
        
        # Chat input
        if prompt := st.chat_input("Describe your legal situation..."):
            # Add user message
            st.session_state.messages.append({
                'agent': 'You',
                'content': prompt,
                'class': 'user'
            })
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Run the case
            if not st.session_state.case_active:
                st.session_state.case_active = True
                self.run_case(prompt)
                st.rerun()


# Run the app
app = PearsonSpecterUI()
app.run()