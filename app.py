import streamlit as st
import json
import os
import os
import bcrypt
import toml

# Page configuration
st.set_page_config(
    page_title="CoolKonyha Assistant",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded",
)

def load_config():
    """Loads the UI configuration."""
    try:
        with open("ui_config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Configuration file 'ui_config.json' not found.")
        return {}

def main():
    config = load_config()
    
    # st.title("CoolKonyha AI Assistant 🤖")  <-- Moved to sidebar
    
    if config.get("UI_LOCKED", False):
        st.info("UI Layout is LOCKED by Admin.")
    
    # Auto-login for testing
    if "auto_login" in st.query_params:
        auto_user = st.query_params["auto_login"]
        if auto_user in ["admin", "user"]:
            st.session_state.authenticated = True
            st.session_state.username = auto_user
            st.toast(f"Auto-logged in as {auto_user} for testing!", icon="🧪")

    # Authentication check
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.warning("Please log in to access the dashboard.")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                if username in st.secrets["passwords"] and \
                   bcrypt.checkpw(password.encode('utf-8'), st.secrets["passwords"][username].encode('utf-8')):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        # Initial Password Setup
        with st.expander("Initial Password Setup"):
            st.warning("Use this only for initial setup or password reset.")
            try:
                # Load secrets directly to get the structure
                secrets_path = ".streamlit/secrets.toml"
                if os.path.exists(secrets_path):
                    with open(secrets_path, "r", encoding="utf-8") as f:
                        secrets_data = toml.load(f)
                else:
                    secrets_data = {"passwords": {}}

                # Get list of users who need setup (empty password or "placeholder")
                all_users = secrets_data.get("passwords", {})
                users_to_setup = [u for u, p in all_users.items() if p == "" or p == "placeholder"]
                
                if not all_users:
                     st.info(f"No users found. Please add a `[passwords]` section to your `{secrets_path}` file.")
                     st.code("""
[passwords]
admin = ""
user = ""
""", language="toml")
                elif not users_to_setup:
                    st.success(f"All users have passwords set! To reset, clear the password in `{secrets_path}`.")
                else:
                    selected_user = st.selectbox("Select User to Setup", users_to_setup)
                    new_password = st.text_input("New Password", type="password", key="new_pass")
                    confirm_password = st.text_input("Confirm Password", type="password", key="conf_pass")
                    
                    if st.button("Set Password"):
                        if new_password != confirm_password:
                            st.error("Passwords do not match.")
                        elif not new_password:
                            st.error("Password cannot be empty.")
                        else:
                            # Hash the password
                            salt = bcrypt.gensalt()
                            hashed = bcrypt.hashpw(new_password.encode('utf-8'), salt)
                            
                            # Update the secrets data
                            if "passwords" not in secrets_data:
                                secrets_data["passwords"] = {}
                            secrets_data["passwords"][selected_user] = hashed.decode("utf-8")
                            
                            # Write back to secrets.toml
                            with open(secrets_path, "w", encoding="utf-8") as f:
                                toml.dump(secrets_data, f)
                                
                            st.success(f"Password updated for {selected_user}!")
            except Exception as e:
                st.error(f"Error updating password: {e}")

    else:
        # Initialize Team Lead Agent
        from agents.team_lead import TeamLeadAgent
        if 'agent' not in st.session_state:
            st.session_state.agent = TeamLeadAgent()
        
        agent = st.session_state.agent
        # data = agent.get_dashboard_data()  <-- Removed, fetching later with date

        # --- Custom CSS for Spacing ---
        st.markdown("""
            <style>
               .block-container {
                    padding-top: 2rem;
                    padding-bottom: 0rem;
                    margin-top: 0rem;
                }
                /* Hide the default Streamlit header decoration line if desired, 
                   but keeping the toolbar visible */
                header {
                    visibility: visible;
                }
            </style>
        """, unsafe_allow_html=True)

        # --- Header Layout (Logo + Title) ---
        # Using columns to align Logo and Title
        # Trying to align visually with the top area
        h_col1, h_col2, h_col3 = st.columns([1, 6, 1])
        with h_col1:
            st.image("assets/logo.png", width=80)
        with h_col2:
            st.markdown("<h1 style='text-align: center; margin: 0; padding: 0;'>Dashboard</h1>", unsafe_allow_html=True)
        with h_col3:
            # Spacer or placeholder to balance the logo width
            st.write("")

        # --- Sidebar Chat ---
        with st.sidebar:
            st.title("CoolKonyha AI Assistant 🤖")
            st.header("Chat with Team Lead")
            if "messages" not in st.session_state:
                st.session_state.messages = []

            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if prompt := st.chat_input("What can I help you with?"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                response = agent.handle_chat_input(prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.markdown(response)

        # --- Main Dashboard Content ---
        # st.markdown("<h1 style='text-align: center;'>Dashboard</h1>", unsafe_allow_html=True) # Moved to header
        
        # Date Navigation State
        from datetime import datetime, timedelta
        if "selected_date" not in st.session_state:
            st.session_state.selected_date = datetime.now().date()

        # Layout Columns
        col1, col2 = st.columns([2, 1])

        # 1. Delta Log Panel (Left Column)
        with col1:
            if config.get("layout", {}).get("show_delta_log", True):
                # Date Navigation Header
                nav_col1, nav_col2, nav_col3 = st.columns([1, 4, 1])
                
                with nav_col1:
                    if st.button("◀", key="prev_day"):
                        st.session_state.selected_date -= timedelta(days=1)
                        st.rerun()
                
                with nav_col2:
                    current_date = st.session_state.selected_date
                    if current_date == datetime.now().date():
                        display_date = "What happened since yesterday?"
                    else:
                        display_date = current_date.strftime("%Y-%m-%d (%A)")
                    st.markdown(f"<h3 style='text-align: center; margin: 0;'>{display_date}</h3>", unsafe_allow_html=True)
                
                with nav_col3:
                    if st.button("▶", key="next_day"):
                        st.session_state.selected_date += timedelta(days=1)
                        st.rerun()

                # Fetch data for selected date
                data = agent.get_dashboard_data(st.session_state.selected_date)
                
                st.write("") # Spacer
                delta_container = st.container(border=True)
                if not data["delta_log"]:
                     delta_container.info("No events recorded for this day.")
                else:
                    for log_item in data["delta_log"]:
                        delta_container.markdown(f"- {log_item}")

        # 2. Action Center (Right Column)
        with col2:
            if config.get("layout", {}).get("show_action_center", True):
                st.subheader("⚡ Action Center")
                # Vertical layout for action center in the side column
                for action in data["pending_actions"]:
                    with st.container(border=True):
                        st.markdown(f"**{action['task']}**")
                        if st.button("Process", key=f"btn_{action['id']}"):
                            st.success(f"Action '{action['task']}' processed!")
                            # In a real app, this would update the backend and rerun

        # 3. Status Dashboard (Full Width)
        st.divider()
        st.subheader("📊 Active Cases")
        st.dataframe(
            data["active_cases"],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Status": st.column_config.TextColumn("Status", help="Current phase of the workflow"),
                "Last Update": st.column_config.DateColumn("Last Update"),
            }
        )

        # --- Admin Settings (Only for Admin) ---
        if st.session_state.get("username") == "admin":
            st.divider()
            with st.expander("⚙️ Admin Settings (Configuration)"):
                st.info("These settings control the global UI layout.")
                
                # Load current config to ensure freshness
                current_config = config
                
                with st.form("admin_config_form"):
                    # UI Lock
                    ui_locked = st.checkbox("🔒 Lock UI Layout (Prevent further changes)", value=current_config.get("UI_LOCKED", False))
                    
                    st.subheader("Layout Options")
                    # Disable options if UI is locked (unless unlocking)
                    disabled = ui_locked and current_config.get("UI_LOCKED", False)
                    
                    show_delta = st.checkbox("Show 'Delta Log' Panel", value=current_config.get("layout", {}).get("show_delta_log", True), disabled=disabled)
                    show_action = st.checkbox("Show 'Action Center' Panel", value=current_config.get("layout", {}).get("show_action_center", True), disabled=disabled)
                    sidebar_expanded = st.checkbox("Start with Sidebar Expanded", value=current_config.get("layout", {}).get("sidebar_expanded", True), disabled=disabled)
                    
                    if st.form_submit_button("Save Configuration"):
                        new_config = current_config.copy()
                        new_config["UI_LOCKED"] = ui_locked
                        if "layout" not in new_config:
                            new_config["layout"] = {}
                        
                        new_config["layout"]["show_delta_log"] = show_delta
                        new_config["layout"]["show_action_center"] = show_action
                        new_config["layout"]["sidebar_expanded"] = sidebar_expanded
                        
                        try:
                            with open("ui_config.json", "w", encoding="utf-8") as f:
                                json.dump(new_config, f, indent=4)
                            st.success("Configuration saved successfully! Reloading...")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to save config: {e}")

if __name__ == "__main__":
    main()
