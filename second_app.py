import streamlit as st
# importing numpy and pandas for to work with sample data.
import numpy as np
import pandas as pd 
import time
import matplotlib.pyplot as plt
import seaborn as sns; sns.set_theme()


st.title('Dashboard with Uber dataset 🚗')

st.caption('Lucie Bottin 20180304')


st.sidebar.title("Choose the dataset you want to work with :")

choice = st.sidebar.selectbox(
    "Uber Data or NY trips ?",
    ("--Select--", "Uber Data", "NY Trips")
)

if (choice == "Uber Data") :

    df = pd.read_csv("uber-raw-data-apr14.csv")

    left_column, right_column = st.columns(2)
    pressed = left_column.button('Display full Dataset')
    if pressed:
        right_column.write("Here it is !")
        expander = st.expander("Dataset")
        expander.write(df)



    dt = pd.to_datetime(df['Date/Time'], format='%m/%d/%Y %H:%M:%S')
    dt_frame = dt.to_frame()


    def get_dom(dt): 
        return dt.day 
    dt_frame['dom'] = dt_frame['Date/Time'].map(get_dom)


    def get_weekday(dt): 
        return dt.weekday() 
    dt_frame['weekday']= dt_frame['Date/Time'].map(get_weekday)

    def get_hour(dt): 
        return dt.hour
    dt_frame['hour']= dt_frame['Date/Time'].map(get_hour)

    option = '--Select--'
    option = st.selectbox(
        'What specific dataframe do you need ?',
        ('--Select--', 'Day of month', 'Weekday', 'Hour'))


    if (option == '--Select--') :
        st.write('Choose a dataframe to display')

    else :

        st.write('You selected:', option)

        if (option == 'Day of month') :
            st.write(dt_frame[['Date/Time', 'dom']])

        if (option == 'Weekday') :
            st.write(dt_frame[['Date/Time','weekday']])

        if (option == 'Hour') :
            st.write(dt_frame[['Date/Time','hour']])
            

    arr = dt_frame['hour']
    fig, ax = plt.subplots()
    ax.hist(arr, bins=24)
    plt.title('Frequency by hour - Uber - April 2014')
    plt.xlabel('Hour')
    plt.ylabel('Frequency')




    arr2 = dt_frame['weekday']
    fig2, ax2 = plt.subplots()
    ax2.hist(arr2, bins=7,range = (-.5,6.5), rwidth=0.8)
    plt.xlabel('Weekday')
    plt.ylabel('Frequency')
    plt.title('Frequency by weekday - Uber - April 2014')
    plt.xticks([0, 1, 2, 3, 4, 5, 6], [ 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])



    def count_rows(rows): 
        return len(rows)

    grouped_data = dt_frame.groupby(['weekday', 'hour']).apply(count_rows).unstack(level=0)


    if st.button('Group the data'):
        latest_iteration = st.empty()
        bar = st.progress(0)
        for i in range(100):
            # Update the progress bar with each iteration.
            latest_iteration.text(f'Grouping the data... : {i+1}')
            bar.progress(i + 1)
            time.sleep(0.05)
        st.text("Grouped data : ")
        st.write(grouped_data)


    fig3, ax3 = plt.subplots()
    ax3 = sns.heatmap(grouped_data)
    plt.title('Uber trip frequency in a week')
    plt.xlabel('Weekday')
    plt.ylabel('Hour')

    left_column, right_column = st.columns(2)
    pressed = left_column.button('Here are some plots ! Press me')
    if pressed:
        right_column.write("Here they are !")
        expander = st.expander("Frequency by hour plot")
        expander.write(fig)
        expander = st.expander("Frequency by weekday plot")
        expander.write(fig2)
        expander = st.expander("Heat Map")
        expander.write(fig3)

elif (choice == "NY Trips") :
    
    df = pd.read_csv("ny-trips-data.csv")

    left_column, right_column = st.columns(2)
    pressed = left_column.button('Display full Dataset')
    if pressed:
        right_column.write("Here it is !")
        expander = st.expander("Dataset")
        expander.write(df)


    df[['tpep_pickup_datetime','tpep_dropoff_datetime']] = df[['tpep_pickup_datetime','tpep_dropoff_datetime']].apply(pd.to_datetime);



    def get_hours(dt): 
        return dt.hour
    df['hour_pickup'] = df['tpep_pickup_datetime'].map(get_hours)
    df['hour_dropoff'] = df['tpep_dropoff_datetime'].map(get_hours)

    def get_weekday(dt):
        return dt.weekday()
    df['weekday_pickup']= df['tpep_pickup_datetime'].map(get_weekday)
    df['weekday_dropoff']= df['tpep_dropoff_datetime'].map(get_weekday)
                

    fig, ax = plt.subplots()
    ax.hist(df['VendorID'], bins = 30, rwidth=1, range=(1,3))
    plt.title('Number of sales by vendor')
    plt.xlabel('Vendor ID')
    plt.ylabel('Sales')

    fig2, ax2 = plt.subplots()
    ax2.hist(df['passenger_count'], bins = 20, rwidth=1, range=(1,7))
    plt.xlabel('Passengers')
    plt.ylabel('Trips')
    plt.title('Number of passenger by trip')

    fig3, ax2 = plt.subplots()
    ax2.hist(df["hour_pickup"], bins = 20, rwidth=1, range=(1,7))
    ax2.hist(df["hour_dropoff"], bins = 20, rwidth=1, range=(1,7))
    plt.xlabel('Hour')
    plt.ylabel('Frequency')
    plt.title('Frequency by hour - Trips - January 2015')
    
    fig4, ax2 = plt.subplots()
    ax2.hist(df["weekday_pickup"], bins = 20, rwidth=1, range=(1,7))
    ax2.hist(df["weekday_dropoff"], bins = 20, rwidth=1, range=(1,7))
    plt.xlabel('Weekday')
    plt.ylabel('Frequency')
    plt.title('Frequency by weekday - Trips - January 2015')
    plt.xticks([ 2, 3, 4], [ 'Wed', 'Thu', 'Fri'])


    def count_rows(rows): 
        return len(rows)

    grouped_data = df.groupby(['weekday_pickup', 'hour_pickup']).apply(count_rows).unstack(level=0)
    grouped_data =  df.groupby(['weekday_dropoff', 'hour_dropoff']).apply(count_rows).unstack(level=0)


    if st.button('Group the data'):
        latest_iteration = st.empty()
        bar = st.progress(0)
        for i in range(100):
            latest_iteration.text(f'Grouping the data... : {i+1}')
            bar.progress(i + 1)
            time.sleep(0.05)
        st.text("Grouped data : ")
        st.write(grouped_data)


    fig5, ax3 = plt.subplots()
    ax3 = sns.heatmap(grouped_data)
    plt.title('Uber trip frequency in a week')
    plt.xlabel('Weekday')
    plt.ylabel('Hour')

    left_column, right_column = st.columns(2)
    pressed = left_column.button('Here are some plots ! Press me')

    if pressed:
        right_column.write("Here they are !")
        expander = st.expander("Number of sales by vendor")
        expander.write(fig)
        expander = st.expander("Number of passengers by trip")
        expander.write(fig2)
        expander = st.expander("Frequency by hour - Trips - January 2015")
        expander.write(fig3)
        expander = st.expander("Frequency by weekday - Trips - January 2015")
        expander.write(fig4)
        expander = st.expander("Heat Map")
        expander.write(fig5)
   