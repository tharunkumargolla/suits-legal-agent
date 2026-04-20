"""
Agent avatar components for Streamlit UI
"""
import streamlit as st
from typing import Optional


def get_agent_avatar(agent_name: str) -> str:
    """Return emoji avatar for each agent"""
    avatars = {
        'donna': '👩‍💼',
        'mike': '📚',
        'harvey': '👔',
        'louis': '📋',
        'jessica': '👑',
        'jessica_supervisor': '👑',
        'user': '👤'
    }
    return avatars.get(agent_name.lower(), '⚖️')


def get_agent_color(agent_name: str) -> str:
    """Return color code for each agent"""
    colors = {
        'donna': '#c9a84c',      # Gold
        'mike': '#4a90d9',       # Blue
        'harvey': '#c94c4c',     # Red
        'louis': '#c9a84c',      # Gold
        'jessica': '#4cc9c9',    # Teal
        'jessica_supervisor': '#4cc9c9'  # Teal
    }
    return colors.get(agent_name.lower(), '#888888')


def get_agent_title(agent_name: str) -> str:
    """Return full title for each agent"""
    titles = {
        'donna': 'Donna Paulsen - COO',
        'mike': 'Mike Ross - Associate',
        'harvey': 'Harvey Specter - Name Partner',
        'louis': 'Louis Litt - Junior Partner',
        'jessica': 'Jessica Pearson - Managing Partner',
        'jessica_supervisor': 'Jessica Pearson - Managing Partner'
    }
    return titles.get(agent_name.lower(), agent_name)


def agent_message_box(content: str, agent_name: str) -> None:
    """
    Display a styled message box for an agent
    """
    color = get_agent_color(agent_name)
    avatar = get_agent_avatar(agent_name)
    title = get_agent_title(agent_name)
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {color}15 0%, {color}05 100%);
        border-left: 4px solid {color};
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    ">
        <div style="
            display: flex;
            align-items: center;
            margin-bottom: 0.5rem;
        ">
            <span style="font-size: 1.5rem; margin-right: 0.5rem;">{avatar}</span>
            <span style="
                font-weight: bold;
                color: {color};
                font-size: 1.1rem;
            ">{title}</span>
        </div>
        <div style="
            color: #e0e0e0;
            line-height: 1.6;
            white-space: pre-wrap;
        ">{content}</div>
    </div>
    """, unsafe_allow_html=True)


def loading_indicator(agent_name: str) -> None:
    """Display a loading indicator for an agent"""
    avatar = get_agent_avatar(agent_name)
    color = get_agent_color(agent_name)
    
    st.markdown(f"""
    <div style="
        display: flex;
        align-items: center;
        padding: 0.5rem 1rem;
        background: #1a1a2e;
        border-radius: 20px;
        margin: 0.5rem 0;
        width: fit-content;
    ">
        <span style="font-size: 1.2rem; margin-right: 0.5rem;">{avatar}</span>
        <span style="color: {color};">{agent_name} is typing</span>
        <span class="loading-dots">
            <span>.</span><span>.</span><span>.</span>
        </span>
    </div>
    <style>
        .loading-dots span {{
            animation: blink 1.4s infinite both;
            color: {color};
        }}
        .loading-dots span:nth-child(2) {{ animation-delay: 0.2s; }}
        .loading-dots span:nth-child(3) {{ animation-delay: 0.4s; }}
        @keyframes blink {{
            0%, 80%, 100% {{ opacity: 0; }}
            40% {{ opacity: 1; }}
        }}
    </style>
    """, unsafe_allow_html=True)
