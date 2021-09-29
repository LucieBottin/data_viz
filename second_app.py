import streamlit as st
# importing numpy and pandas for to work with sample data.
import numpy as np
import pandas as pd 
import time
import matplotlib.pyplot as plt
import seaborn as sns; sns.set_theme()
import datetime
import streamlit.components.v1 as components


st.title('Dashboard with Uber dataset 🚗')

st.caption('Lucie Bottin 20180304')

#D E C O R A T O R S
#log execution time
@st.cache(suppress_st_warning=True) 
def log(func):
    def wrapper(*args,**kwargs):
        with open("logs.txt","a") as f:
            f.write("Called function with " + " ".join([str(arg) for arg in args]) + " at " + str(datetime.datetime.now()) + "\n")
        val = func(*args,**kwargs)
        return val
    return wrapper

@log
def run(a,b,c=9):
    print(a+b+c)

run(1,3,c=9)


st.sidebar.title("Choose the dataset you want to work with :")

components.iframe("https://cdn.futura-sciences.com/buildsv6/images/largeoriginal/a/0/f/a0fc73919d_50166390_chaton.jpg")

############
import os
import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = False

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(

        "my_component",
        url="http://localhost:8501",
    )
else:
    
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("my_component", path=build_dir)

def my_component(name, key=None):
    
    component_value = _component_func(name=name, key=key, default=0)

    return component_value

if not _RELEASE:
    import streamlit as st

    st.subheader("Component with constant args")

    num_clicks = my_component("World")
    st.markdown("You've clicked %s times!" % int(num_clicks))

    st.markdown("---")
    st.subheader("Component with variable args")

    name_input = st.text_input("Enter a name", value="Streamlit")
    num_clicks = my_component(name_input, key="foo")
    st.markdown("You've clicked %s times!" % int(num_clicks))
############

@st.cache(suppress_st_warning=True) 
def choice_uber(c) :
    df = pd.read_csv("uber-raw-data-apr14.csv")

    left_column, right_column = st.columns(2)
    pressed = left_column.button('Display full Dataset')
    if pressed:
        right_column.write("Here it is !")
        expander = st.expander("Dataset")
        expander.write(df)
    return df

def to_time_uber(df) :
    dt = pd.to_datetime(df['Date/Time'], format='%m/%d/%Y %H:%M:%S')
    return dt.to_frame()

def get_dom(dt): 
    return dt.day 

def get_weekday(dt): 
    return dt.weekday() 

def get_hour(dt): 
    return dt.hour

@st.cache(suppress_st_warning=True) 
def full_df(dt) : 

    dt['dom'] = dt['Date/Time'].map(get_dom)
    dt['weekday']= dt['Date/Time'].map(get_weekday)
    dt['hour']= dt['Date/Time'].map(get_hour)
    return dt

def display_data(option) :

    if (option == '--Select--') :
        st.write('')

    else :

        st.write('You selected:', option)

        if (option == 'Day of month') :
            st.write(dt[['Date/Time', 'dom']])

        if (option == 'Weekday') :
            st.write(dt[['Date/Time','weekday']])

        if (option == 'Hour') :
            st.write(dt[['Date/Time','hour']])

def count_rows(rows): 
        return len(rows)

@st.cache(suppress_st_warning=True) 
def group_data(option) :
    dt_grouped = dt.groupby(['weekday', 'hour']).apply(count_rows).unstack(level=0)

    if (option == '--Select--') :
        st.write('')

    else :

        st.write('You selected:', option)

        if (option == 'Yes') :
            latest_iteration = st.empty()
            bar = st.progress(0)
            for i in range(100):
                # Update the progress bar with each iteration.
                latest_iteration.text(f'Grouping the data... : {i+1}')
                bar.progress(i + 1)
                time.sleep(0.05)
            st.text("Grouped data : ")
            st.write(dt_grouped)

        if (option == 'No') :
            st.write("Ok, then")
    return dt_grouped

choix = st.sidebar.selectbox(
    "Uber Data or NY trips ?",
    ("--Select--", "Uber Data", "NY Trips")
)

option = '--Select--'
option = st.selectbox(
    'What specific dataframe do you need ?',
    ('--Select--', 'Day of month', 'Weekday', 'Hour'))

option2 = '--Select--'
option2 = st.selectbox(
    'Group the data ?',
    ('--Select--', 'Yes', 'No'))

def freq_hour(dt) :

    arr = dt['hour']
    fig, ax = plt.subplots()
    ax.hist(arr, bins=24)
    plt.title('Frequency by hour - Uber - April 2014')
    plt.xlabel('Hour')
    plt.ylabel('Frequency')
    return fig

def freq_weekday(dt) :

    arr2 = dt['weekday']
    fig2, ax2 = plt.subplots()
    ax2.hist(arr2, bins=7,range = (-.5,6.5), rwidth=0.8)
    plt.xlabel('Weekday')
    plt.ylabel('Frequency')
    plt.title('Frequency by weekday - Uber - April 2014')
    plt.xticks([0, 1, 2, 3, 4, 5, 6], [ 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    return fig2

def heatmap(group_data) :
    fig3, ax3 = plt.subplots()
    ax3 = sns.heatmap(group_data)
    plt.title('Uber trip frequency in a week')
    plt.xlabel('Weekday')
    plt.ylabel('Hour')
    return fig3

def display_plots(fig, fig1, fig2) :

    left_column, right_column = st.columns(2)
    pressed = left_column.button('Here are some plots ! Press me')
    if pressed:
        right_column.write("Here they are !")
        expander = st.expander("Frequency by hour plot")
        expander.write(fig)
        expander = st.expander("Frequency by weekday plot")
        expander.write(fig1)
        expander = st.expander("Heat Map")
        expander.write(fig2)

#################################################################################################################

@st.cache(suppress_st_warning=True) 
def choice_trips(c) :
    df = pd.read_csv("ny-trips-data.csv")

    left_column, right_column = st.columns(2)
    pressed = left_column.button('Display full Dataset')
    if pressed:
        right_column.write("Here it is !")
        expander = st.expander("Dataset")
        expander.write(df)
    return df

  
def to_time_trips(df) :
    return df[['tpep_pickup_datetime','tpep_dropoff_datetime']].apply(pd.to_datetime)
    
def get_hours(dt): 
    return dt.hour

def get_weekday(dt):
    return dt.weekday()

@st.cache(suppress_st_warning=True) 
def full_df_trips(dt) : 

    dt['hour_pickup'] = dt['tpep_pickup_datetime'].map(get_hours)
    dt['hour_dropoff'] = dt['tpep_dropoff_datetime'].map(get_hours)
    dt['weekday_pickup']= dt['tpep_pickup_datetime'].map(get_weekday)
    dt['weekday_dropoff']= dt['tpep_dropoff_datetime'].map(get_weekday)
    return dt


def count_rows(rows): 
    return len(rows)

def sales_plot(dt) :

    fig, ax = plt.subplots()
    print(dt['VendorID'])
    ax.hist(dt['VendorID'], bins = 30, rwidth=1, range=(1,3))
    plt.title('Number of sales by vendor')
    plt.xlabel('Vendor ID')
    plt.ylabel('Sales')
    return fig

def passengers_plot(dt) :

    fig2, ax2 = plt.subplots()
    ax2.hist(dt['passenger_count'], bins = 20, rwidth=1, range=(1,7))
    plt.xlabel('Passengers')
    plt.ylabel('Trips')
    plt.title('Number of passenger by trip')
    return fig2

def hour_plot(dt) :

    fig3, ax2 = plt.subplots()
    ax2.hist(dt["hour_pickup"], bins = 20, rwidth=1, range=(1,7))
    ax2.hist(dt["hour_dropoff"], bins = 20, rwidth=1, range=(1,7))
    plt.xlabel('Hour')
    plt.ylabel('Frequency')
    plt.title('Frequency by hour - Trips - January 2015')
    return fig3

def weekday_plot(dt) :

    fig4, ax2 = plt.subplots()
    ax2.hist(dt["weekday_pickup"], bins = 20, rwidth=1, range=(1,7))
    ax2.hist(dt["weekday_dropoff"], bins = 20, rwidth=1, range=(1,7))
    plt.xlabel('Weekday')
    plt.ylabel('Frequency')
    plt.title('Frequency by weekday - Trips - January 2015')
    plt.xticks([ 2, 3, 4], [ 'Wed', 'Thu', 'Fri'])
    return fig4

def show_plots(f1,f2,f3,f4) :
    left_column, right_column = st.columns(2)
    pressed = left_column.button('Here are some plots ! Press me')

    if pressed:
        right_column.write("Here they are !")
        expander = st.expander("Number of sales by vendor")
        expander.write(f1)
        expander = st.expander("Number of passengers by trip")
        expander.write(f2)
        expander = st.expander("Frequency by hour - Trips - January 2015")
        expander.write(f3)
        expander = st.expander("Frequency by weekday - Trips - January 2015")
        expander.write(f4)
                

if choix == "Uber Data" : 
    df = choice_uber(choix)
    dt_init = to_time_uber(df)
    dt = full_df(dt_init)
    display_data(option)
    grouped_data = group_data(option2)
    fig = freq_hour(dt)
    fig1 = freq_weekday(dt)
    fig2 = heatmap(grouped_data)
    display_plots(fig,fig1,fig2)
    


elif choix == "NY Trips" : 
    df = choice_trips(choix)
    dt_init = to_time_trips(df)
    dt = full_df_trips(dt_init)
    f1 = sales_plot(df)
    f2 = passengers_plot(df)
    f3 = hour_plot(dt)
    f4 = weekday_plot(dt)
    show_plots(f1,f2,f3,f4)








