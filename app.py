import yfinance as yf
import streamlit as st 


st.set_page_config(page_title="MSO FINANCE",layout="wide")

#BUILD MY OWN CSS
ticker = "a"
search_period = None
form_width =400
st.markdown("""
            <style>
            .h1-text-style{
                font-size : 48px;
                color:orange;
                font-family: Tahoma, Verdana, sans-serif;
                font-weight: bold;
                text-align: center ;
            }
            form-title-text {
                font-size : 24px;
                color:orange;
                font-family: Tahoma, Verdana, sans-serif;
                font-weight: bold;
                text-align: center ;
                margin-left : 25%;
                margin-right:25%;

            }
                    
        .st-emotion-cache-1jz4sbv .e1f1d6gn2 {
            width:200px;
        }
            
            </style>
            """,unsafe_allow_html=True)

st.markdown(f"<h1 class=h1-text-style> MSO FINANCE</h1>",unsafe_allow_html=True)
form_width = 400
input_width = 300  # Adjust this value as needed

# Apply CSS to adjust the form width and text input width


# Display the for
# form_col1,form_col2,form_col3 = st.columns([0.3,0.4,0.3])
# with form_col1:
with st.sidebar.form("ticker_form"):
    st.markdown("<p class='form-title-text'>Setuo Your Data</p>", unsafe_allow_html=True)
    label=st.text_input("Stock Label")
    period =st.selectbox("Period",options=["24 Hour","5 Days","1 Month","3 Months","6 Months","1 Year","2 Year","5 Years","10 Years"])
    search=st.form_submit_button("Search")

    if search:
        ticker = label
        
        search_period = period
        if search_period =="24 Hour":
            search_period="1d"
        stock= yf.Ticker(f"{ticker}")
        data = stock.history(interval="1m",period=f"{search_period}")
        if data.empty:
                st.warning(f"{label} couldn't find please check your stock label")
    
            

    




# st.sidebar()


#Daily Graphs


#Weekly Graphs



#Monthly Graphs



#Yearly Graphs