import streamlit as st
import pandas as pd
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('https://images.unsplash.com/photo-1474487548417-781cb71495f3?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8M3x8dHJhaW58ZW58MHx8MHx8&auto=format&fit=crop&w=500&q=60');
    background-size: cover;
}
[data-testid="stSidebar"] {
    background-color: rgba(0,0,0,0.0);
}
h1{
    color: indianred;
}

</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)
st.title("Railway Route Optimization System")
option1 = st.selectbox('Select Source Station',('Kolkata','Delhi','Mumbai','Chennai','Bangalore','Hyderabad','Ahmedabad','Pune','Jaipur','Surat','Lucknow','Kanpur','Nagpur','Visakhapatnam','Indore','Thane'))
option2 = st.selectbox('Select Destination Station',('Kolkata','Delhi','Mumbai','Chennai','Bangalore','Hyderabad','Ahmedabad','Pune','Jaipur','Surat','Lucknow','Kanpur','Nagpur','Visakhapatnam','Indore','Thane'))

st.button('Find Route')
