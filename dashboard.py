import streamlit as st
import streamlit.components.v1 as components

# --- Power BI Embed Code ---
# Using fixed pixel height for iframe, adjust as needed
PBI_IFRAME = """
<iframe title="CC_Database_Prod_v6.14" width="100%" height="700" src="https://app.powerbi.com/view?r=eyJrIjoiYWZmYmI2MDUtNzQxMC00ZDBjLTgwYWEtOGQ4NGQ5MjNkMTg4IiwidCI6IjU5YTIyMTkwLTMzZDQtNGM1NC1iM2VlLTc4ZGMzMDhlNzY3YiJ9" frameborder="0" allowFullScreen="true"></iframe>
"""

def dashboard_page():
    """Displays the member dashboard with the Power BI report."""
    # --- Authentication Check ---
    if not st.session_state.get('logged_in', False):
        st.warning("🔒 Please log in to view the dashboard.")
        st.stop() # Stop execution if not logged in

    # --- Header Section ---
    # Use markdown for centered title
    st.markdown("<h1 style='text-align: center;'>📊 Member Dashboard</h1>", unsafe_allow_html=True)

    # Display welcome message in a separate column or below
    # If keeping side-by-side, adjust columns or use st.container
    # For simplicity, placing welcome message below the title:
    #st.markdown(f"<div style='text-align: right;'>Welcome, <b>{st.session_state.get('username', 'Member')}</b>!</div>", unsafe_allow_html=True)

    st.divider() # Visual separator

    # --- Power BI Section ---
    st.markdown("<h2 style='text-align: center;'>County Championship Ultimate Database</h2>", unsafe_allow_html=True)

    # Embed the Power BI report
    # Set component height slightly larger than iframe height for padding/scrolling
    components.html(PBI_IFRAME, height=720, scrolling=True)

    st.divider() # Add a divider before the buttons

    # --- Footer Buttons (Centered) ---
    # Use columns to create padding on the sides and center the middle column
    col_left_pad, col_center, col_right_pad = st.columns([1, 2, 1]) # Adjust ratio e.g., [1,1,1] or [2,1,2]

    with col_center: # Place buttons in the central column
        col_btn1, col_btn2 = st.columns(2) # Create two columns inside the central one for the buttons
        with col_btn1:
            # Bug Report Button
            if st.button("🐞 Report a Bug", key="footer_bug_report", use_container_width=True):
                st.session_state.page = 'bug_report' # Set state to navigate
                st.rerun()
 
        with col_btn2:
            # Contact Support Button (using mailto link)
            if "email_recipient" in st.secrets:
                support_email = st.secrets["email_recipient"]
            else:
                support_email = "r.taylor289@gmail.com" # Fallback email if secret is missing

            st.link_button("📧 Contact Support", f"mailto:{support_email}", use_container_width=True)


    # --- Sidebar Content ---
    with st.sidebar:
        st.header("Navigation") # Changed header
        if st.button("Logout", key="dashboard_logout"):
            # Clear relevant session state keys
            keys_to_clear = ['logged_in', 'username', 'page'] # Ensure 'page' is cleared
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            # Set page to home explicitly after logout if needed, rerun handles it often
            # st.session_state.page = 'home'
            st.rerun() # Rerun the app to go back to the login/home page

        st.divider()
        # Removed the generic st.info("Need help? Contact support or check the FAQ.")

# Example of running this page directly (optional, for testing)
# if __name__ == "__main__":
#     # Mock session state for testing
#     if 'logged_in' not in st.session_state:
#         st.session_state.logged_in = True
#         st.session_state.username = "TestUser"
#     st.set_page_config(layout="wide")
#     dashboard_page()