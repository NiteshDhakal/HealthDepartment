<style>

    .stApp{
        background-image: url("https://images.pexels.com/photos/3847486/pexels-photo-3847486.jpeg");
        background-size: cover;
    }
/* Hide sidebar collapse control */
[data-testid="collapsedControl"] {
    display: none;
}

/* Adjust main content spacing */
.block-container {
    padding-top: 10px; /* Push content below fixed header */
}

/* Hide Streamlit default menu, footer, and header */
#MainMenu{
    visibility: hidden;
}
footer {
    visibility: hidden;
}
header {
    display: none;
}

/* Adjust sidebar padding */
section[data-testid="stSidebar"] > div:first-child {
    padding-top: 1rem;
}

/* Scrollable sidebar */
section[data-testid="stSidebar"] {
    height: 100vh;
    overflow-y: auto;
}

/* Add space below the logo */
.sidebar-logo {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 20px;
}

/* participants matrics */

.participants-metric {
    background-color: #f9c74f;
    padding: 10px;
    border-radius: 8px;
    color: black;
    margin: 10px 0;
    }
</style>
