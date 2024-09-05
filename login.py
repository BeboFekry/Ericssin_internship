import streamlit as st

password2 = "Ericsson2024"
email2 = "Abdallah"

log = False
st.write("---")
col1, col2, col3 = st.columns([3,1,3])
with col1:
    st.write("  \n");st.write("  \n")
    st.image(r"images/Login.gif")
with col2:
    pass
with col3:
    st.title("Login")
    email = st.text_input(label="Name", max_chars=50)
    password = st.text_input(label="Password", max_chars=20, type='password')
    if email==email2 and password==password2 and password is not "" and email is not "":
        log = True
    bt = st.button("Login", use_container_width=1)
    if bt:
        if email is "" or password is "":
            st.error("Please enter your data!")
        if log==True:
            st.success("Success")
            st.session_state.logged_in = True
            st.rerun()
        elif password is not "" and email is not "":
            st.error("Wrong name or password!")

st.write("---")
