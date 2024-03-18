import yfinance as yf
import streamlit as st 
from period_mapping import period_mapping,period_interval_mapping
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import datetime as dt
st.set_page_config(layout="wide")

#BUILD MY OWN CSS
ticker = "a"
search_period = None
form_width =400
data = []
def period_interval_setup(period):
    interval_count = period_interval_mapping[period]
    period_count = period_mapping[period]
    return period_count,interval_count



st.markdown("""
            <style>
            header{
                visibility:hidden;
            }
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
        .glideDataEditor .gdg-wmyidgi  {
            height:900px;
            
        }
        
        .dvn-scroller .glideDataEditor
 {
     height:900px;}        
     
     
     </style>
            """,unsafe_allow_html=True)

st.markdown(f"<h1 class=h1-text-style> MSO FINANCE</h1>",unsafe_allow_html=True)


with st.sidebar.form("ticker_form"):
    st.markdown("<p class='form-title-text'>Setuo Your Data</p>", unsafe_allow_html=True)
    label=st.text_input("Stock Label")

    period =st.selectbox("Period",options=["24 Hour","3 Days","5 Days","1 Month","3 Months","6 Months","1 Year","2 Year","5 Years","10 Years"])
    search=st.form_submit_button("Search")
    if search:
        if not label:
            st.warning(f"Please Fill All Field")
        else:
            ticker = label
            period_var,interval_var = period_interval_setup(period=period)
            stock= yf.Ticker(f"{ticker}")
            data = stock.history(interval=f"{interval_var}",period=f"{period_var}").reset_index()
            data = data.drop(columns=["Dividends", "Stock Splits"],axis=1)
            pd.set_option("min_rows",30)
            if data.empty:
                st.warning(f"{label} couldn't find please check your stock label")

    



main_col1,main_col2 = st.columns(2)

with main_col1:            
    if len(data)>1:
        try:
            data["Datetime"] = data["Datetime"].dt.strftime("%Y/%b/%d, %H:%M:%S")

            st.dataframe(data.sort_values(by="Datetime",ascending=False),height=800)
            data=data.sort_values(by="Datetime",ascending=False)
            graph=data

        except:
            data.index = pd.to_datetime(data.index)
            data= data.sort_index(ascending=False)
            graph = data
            num_row = data.shape[0]
            st.dataframe(data,use_container_width=True,height=800)





def create_plot(name:str,label:str,title_info:str,data):
        fig, ax1 = plt.subplots(figsize=(16,8))

        # ax2 = ax1.twinx()
        ax1.set_ylabel(name)
        # ax2.set_ylabel("Close")        
        plt.xlabel('Datetime')
        plt.ylabel(label)
        plt.title(title_info)

        # Format x-axis labels
        if period_var in ["1d", "3d"]:
            date_formatter = DateFormatter('%H:%M')
            ax1.xaxis.set_major_formatter(date_formatter)
            ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=30))
        elif period_var == "5d":
            date_formatter = DateFormatter("%d - %H")
            ax1.xaxis.set_major_locator(mdates.HourLocator(interval=5))
        elif period_var in ["1mo", "3mo", "6mo"]:
            date_formatter = DateFormatter("%b")
            ax1.xaxis.set_major_locator(mdates.DayLocator(interval=int(period_var[0])*3))
        elif period_var in ["1y", "2y", "5y"]:
            date_formatter = DateFormatter("%b")
            ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=int(period_var[0]*2)))
        else:
            date_formatter = DateFormatter("%Y")
            ax1.xaxis.set_major_locator(mdates.YearLocator())

        ax1.xaxis.set_major_formatter(date_formatter)

        ax1.plot(data.index, data[name], label=name, marker='o', markersize=1)
        # ax2.plot(data.index, data['Close'], label='Close', marker='s', markersize=1)
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        return fig

with main_col2:
    if len(data)>1:
        st.markdown("Open")
        open_fig = create_plot(name="Open",label="Price",title_info="Open Prices",data=graph)
        close_fig = create_plot(name="Close",label="Price",title_info="Close Prices",data=graph)
        volume_fig = create_plot(name="Volume",label="Count",title_info="Volume Count",data=graph)

        st.pyplot(open_fig,use_container_width=True)
        st.pyplot(close_fig,use_container_width=True)
        st.pyplot(volume_fig,use_container_width=True)


