import streamlit as st
import streamlit.components.v1 as components

# --- Power BI Embed URL ---
# Using a taller default height can prevent Power BI from over-shrinking the view.
PBI_URL = (
    "https://app.powerbi.com/view?r=eyJrIjoiYWM0YmNiZDMtZjMxOC00MWMyLTg4NjAtOTQ0NGE5Y2Q1NmJhIiwidCI6IjU5YTIyMTkwLTMzZDQtNGM1NC1iM2VlLTc4ZGMzMDhlNzY3YiJ9&pageName=ReportSection06cd1cda4509ede10730"
)

def dashboard_page():
    """Displays the member dashboard with the Power BI report."""
    # --- Authentication Check ---
    if not st.session_state.get('logged_in', False):
        st.warning("🔒 Please log in to view the dashboard.")
        st.stop() # Stop execution if not logged in

    # --- Header Section ---
    # Expand usable width a bit more than Streamlit's default "wide" layout
    st.markdown(
        """
        <style>
        .main .block-container {max-width: 95vw;}
        </style>
        """,
        unsafe_allow_html=True,
    )
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
    # Let users tweak height if the report appears tiny due to "fit to page" scaling.
    default_height = st.session_state.get("pbi_iframe_height", 1100)
    components.iframe(PBI_URL, height=default_height, scrolling=True)

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
        # Optional display-size controls for the embedded report
        with st.expander("Display size", expanded=False):
            new_height = st.slider(
                "Report height (px)", min_value=700, max_value=2000, value=int(default_height), step=50
            )
            if new_height != default_height:
                st.session_state["pbi_iframe_height"] = int(new_height)
                st.rerun()

        # Removed the generic st.info("Need help? Contact support or check the FAQ.")

# Example of running this page directly (optional, for testing)
# if __name__ == "__main__":
#     # Mock session state for testing
#     if 'logged_in' not in st.session_state:
#         st.session_state.logged_in = True
#         st.session_state.username = "TestUser"
#     st.set_page_config(layout="wide")
#     dashboard_page()