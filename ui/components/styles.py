"""
Custom CSS styles for Pearson Specter UI
"""

def get_custom_css() -> str:
    """Return the complete custom CSS for the app"""
    return """
    <style>
        /* Pearson Specter Theme - Main Styles */
        
        /* Global background */
        .stApp {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
        }
        
        /* Main header styling */
        .main-header {
            color: #c9a84c;
            font-family: 'Georgia', 'Times New Roman', serif;
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 4px;
            border-bottom: 2px solid #c9a84c;
            padding-bottom: 1.5rem;
            margin-bottom: 2rem;
            text-shadow: 0 0 20px rgba(201, 168, 76, 0.3);
        }
        
        /* Subheader styling */
        .sub-header {
            color: #c9a84c;
            font-family: 'Georgia', serif;
            font-size: 1.5rem;
            margin-top: 1rem;
            margin-bottom: 0.5rem;
        }
        
        /* Sidebar customization */
        .css-1d391kg, .css-1lcbmhc {
            background: linear-gradient(180deg, #0a0a0a 0%, #1a1a2e 100%);
        }
        
        /* Sidebar headers */
        .sidebar-header {
            color: #c9a84c;
            font-size: 1.3rem;
            font-weight: bold;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            border-bottom: 1px solid #c9a84c;
            padding-bottom: 0.5rem;
        }
        
        /* Agent list items */
        .agent-item {
            padding: 0.5rem;
            margin: 0.25rem 0;
            border-radius: 4px;
            transition: background 0.3s;
        }
        
        .agent-item:hover {
            background: rgba(201, 168, 76, 0.1);
        }
        
        /* Status badge */
        .status-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: bold;
            text-transform: uppercase;
        }
        
        .status-active {
            background: linear-gradient(135deg, #2e7d32, #1b5e20);
            color: white;
            box-shadow: 0 0 10px rgba(46, 125, 50, 0.5);
        }
        
        .status-pending {
            background: linear-gradient(135deg, #c9a84c, #9a7a2a);
            color: black;
        }
        
        .status-complete {
            background: linear-gradient(135deg, #1565c0, #0d47a1);
            color: white;
        }
        
        /* Chat message container */
        .chat-container {
            max-width: 900px;
            margin: 0 auto;
        }
        
        /* Chat input styling */
        .stChatInput {
            border-top: 1px solid #333;
            padding-top: 1rem;
            margin-top: 1rem;
        }
        
        .stChatInput input {
            background: #1a1a2e;
            border: 1px solid #c9a84c;
            border-radius: 25px;
            color: white;
            padding: 0.75rem 1.5rem;
        }
        
        .stChatInput input:focus {
            border-color: #c9a84c;
            box-shadow: 0 0 10px rgba(201, 168, 76, 0.3);
        }
        
        /* Button styling */
        .stButton button {
            background: linear-gradient(135deg, #c9a84c, #9a7a2a);
            color: black;
            font-weight: bold;
            border: none;
            border-radius: 4px;
            padding: 0.5rem 1rem;
            transition: all 0.3s;
            width: 100%;
        }
        
        .stButton button:hover {
            background: linear-gradient(135deg, #d9b85c, #aa8a3a);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(201, 168, 76, 0.3);
        }
        
        /* Spinner customization */
        .stSpinner > div {
            border-color: #c9a84c !important;
        }
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #0a0a0a;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #c9a84c;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #d9b85c;
        }
        
        /* Info/Warning/Success boxes */
        .info-box {
            background: rgba(74, 144, 217, 0.1);
            border-left: 4px solid #4a90d9;
            padding: 1rem;
            border-radius: 4px;
            margin: 1rem 0;
        }
        
        .warning-box {
            background: rgba(201, 168, 76, 0.1);
            border-left: 4px solid #c9a84c;
            padding: 1rem;
            border-radius: 4px;
            margin: 1rem 0;
        }
        
        .success-box {
            background: rgba(46, 125, 50, 0.1);
            border-left: 4px solid #2e7d32;
            padding: 1rem;
            border-radius: 4px;
            margin: 1rem 0;
        }
        
        /* Agent-specific message bubbles (fallback if not using component) */
        .agent-message {
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            animation: fadeIn 0.5s;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Donna message styling */
        .donna-message {
            background: linear-gradient(135deg, #2a1a2e 0%, #1a0a1e 100%);
            border-left: 4px solid #c9a84c;
        }
        
        /* Mike message styling */
        .mike-message {
            background: linear-gradient(135deg, #1a2a3e 0%, #0a1a2e 100%);
            border-left: 4px solid #4a90d9;
        }
        
        /* Harvey message styling */
        .harvey-message {
            background: linear-gradient(135deg, #2a1a1a 0%, #1a0a0a 100%);
            border-left: 4px solid #c94c4c;
        }
        
        /* Louis message styling */
        .louis-message {
            background: linear-gradient(135deg, #2a2a1a 0%, #1a1a0a 100%);
            border-left: 4px solid #c9a84c;
        }
        
        /* Jessica message styling */
        .jessica-message {
            background: linear-gradient(135deg, #1a2a2a 0%, #0a1a1a 100%);
            border-left: 4px solid #4cc9c9;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            color: #666;
            font-size: 0.8rem;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid #333;
        }
        
        /* Citation styling for Mike's responses */
        .legal-citation {
            color: #4a90d9;
            font-style: italic;
            border-bottom: 1px dotted #4a90d9;
        }
        
        /* Case reference */
        .case-ref {
            background: rgba(201, 168, 76, 0.1);
            padding: 0.5rem;
            border-radius: 4px;
            font-family: monospace;
            margin: 0.5rem 0;
        }
    </style>
    """


def inject_css():
    """Inject all custom CSS into the Streamlit app"""
    import streamlit as st
    st.markdown(get_custom_css(), unsafe_allow_html=True)
