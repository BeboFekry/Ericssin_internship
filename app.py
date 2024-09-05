import streamlit as st

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def logoutt():
    # if st.button("Log out"):
    st.session_state.logged_in = False
    st.rerun()


login = st.Page(r"login.py", title="Login", icon=":material/login:")
home = st.Page(r"home.py", title="Home", icon=":material/home:", default=True)
logout = st.Page(logoutt, title="Logout", icon=":material/logout:")
page1 = st.Page(r"page1.py", title="Mobile Network", icon=":material/share:")
page2 = st.Page(r"page2.py", title="Text2Panda Engine", icon=":material/description:")

pages2 = {
    "":[login]
}

pages = {
    "Tasks": [home,page1, page2],
    "": [logout]
}

if st.session_state.logged_in == True:
    pg = st.navigation(pages)
    pg.run()

else:
    pg2 = st.navigation(pages2)
    pg2.run()