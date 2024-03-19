import yfinance as yf
import streamlit as st 
from period_mapping import period_mapping,period_interval_mapping
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import datetime as dt
import plotly.express as px
import numpy as np 

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
            data = stock.history(interval=f"{interval_var}",period=f"{period_var}")
            # data = data.drop(columns=["Dividends", "Stock Splits"],axis=1)
            if data.empty:
                st.warning(f"{label} couldn't find please check your stock label")

    



main_col1,main_col2 = st.columns(2)

with main_col1:            
    if len(data)>1:
        try:
            data.index = data.index.dt.strftime("%Y/%b/%d, %H:%M:%S")
            data.index  = pd.to_datetime(data.index)

            st.dataframe(data.sort_values(by="Date",ascending=False),height=800)
            data=data.sort_index(ascending=False)
            graph=data

        except:
            data.index = pd.to_datetime(data.index)
            # data.index = data.index.dt.strftime("%Y/%b/%d, %H:%M:%S")
            # data.index  = pd.to_datetime(data.index)
            
            # data= data.sort_index(ascending=False)
            data=data.sort_index(ascending=False)
            st.dataframe(data,use_container_width=True,height=800)



import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import pandas as pd
import numpy as np

def fill_green(data,name,ax1):
    ymin = min(data[name])
    ymax = max(data[name])
    padding = 0.05 * (ymax - ymin)  # 5% padding
    ax1.set_ylim(ymin - padding, ymax + padding)

    # Fill the area between the curve and the x-axis

    return ax1.fill_between(data.index, data[name], color='green', alpha=0.3)


def create_plot(name: str, label: str, title_info: str, data, period_var: str):
    fig, ax1 = plt.subplots(figsize=(24, 6), sharex=True)

    data.index = pd.to_datetime(data.index)
    ax1.set_ylabel(name)
    plt.xlabel('Datetime')
    plt.ylabel(label)
    plt.title(title_info)

    if period_var in ["1d"]:
        date_formatter = DateFormatter('%H:%M')
        ax1.xaxis.set_major_formatter(date_formatter)
        ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=30))
        ax1.plot(data.index, data[name], label=name, marker='o', markersize=2)
        fill_green(data=data,name=name,ax1=ax1)

    elif period_var in ["3d", "5d"]:
        date_formatter = DateFormatter("%d-%H")
        ax1.xaxis.set_major_formatter(date_formatter)
        ax1.xaxis.set_major_locator(mdates.HourLocator(byhour=range(9, 16), interval=30))
        ax1.plot(range(data.index.size), data[name], label=name, marker='o', markersize=2)
        ymin = min(data[name])
        ymax = max(data[name])
        padding = 0.05 * (ymax - ymin) 
        ax1.set_ylim(ymin - padding, ymax + padding)


        ax1.fill_between(range(data.index.size), data[name], color='green', alpha=0.3)

        new_date = data.index.indexer_at_time('08:00')
        new_time = np.arange(data.index.size)[data.index.minute == 0][::2] 
        ax1.set_xticks(new_date)
        ax1.set_xticks(new_time, minor=True)

        new_date_label = [major_tick.strftime('\n%d-%b').replace('\n0', '\n') for major_tick in data.index[new_date]]
        new_time_label = [minor_tick.strftime('%d %I %p').lstrip('0').lower()    for minor_tick in data.index[new_time]]
        ax1.set_xticklabels(new_date_label)
        ax1.set_xticklabels(new_time_label, minor=True)

    elif period_var in ["1mo", "3mo", "6mo"]:
        date_formatter = DateFormatter("%Y - %b")
        ax1.xaxis.set_major_formatter(date_formatter)
        ax1.plot(data.index, data[name], label=name, marker='o', markersize=2)
        ax1.xaxis.set_major_locator(mdates.DayLocator(interval=int(period_var[0]) * 3))
        fill_green(data=data,name=name,ax1=ax1)
    elif period_var in ["1y", "2y", "5y"]:
        date_formatter = DateFormatter("%Y-%b")
        ax1.xaxis.set_major_formatter(date_formatter)
        ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=int(period_var[0])))
        ax1.plot(data.index, data[name], label=name, marker='o', markersize=2)
        fill_green(data=data,name=name,ax1=ax1)
    else:
        date_formatter = DateFormatter("%Y")
        ax1.xaxis.set_major_formatter(date_formatter)
        ax1.xaxis.set_major_locator(mdates.YearLocator())
        ax1.plot(data.index, data[name], label=name, marker='o', markersize=2)
        fill_green(data=data,name=name,ax1=ax1)
    
    plt.xticks(rotation=45)
    plt.grid(False)
    plt.tight_layout()
    fig.patch.set_facecolor('#0E1117')
    ax1.set_facecolor('#0E1117')
    ax1.tick_params(axis='x', colors='gray',labelsize=18,width=2)  # Set x-axis tick color to gray
    ax1.tick_params(axis='y', colors='gray',labelsize=18,width=2)  # Set y-axis tick color to gray
    for label in ax1.get_xticklabels() + ax1.get_yticklabels():
        label.set_fontweight('bold')  
    ax1.xaxis.label.set_color('gray')  
    ax1.yaxis.label.set_color('gray') 
    ax1.title.set_color('gray')
    
    return fig

with main_col2:
    if len(data)>1:
        open_fig = create_plot(name="Open",label="Price",title_info="Open Prices",data=data,period_var=period_var)
        close_fig = create_plot(name="Close",label="Price",title_info="Close Prices",data=data,period_var=period_var)
        volume_fig = create_plot(name="Volume",label="Count",title_info="Volume Count",data=data,period_var=period_var)

        st.pyplot(open_fig,use_container_width=True)
        st.pyplot(close_fig,use_container_width=True)
        st.pyplot(volume_fig,use_container_width=True)


