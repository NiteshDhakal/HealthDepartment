import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


def load_data():
    health_dept = pd.read_csv("csv/Business_Analyst_Healthcare_Data.csv")
    health_dept.astype({
    "CostCentre": "string",
    "Month": "datetime64[ns]",
    })
    health_dept = health_dept.assign(
        Date = pd.to_datetime(health_dept["Month"])
    ).set_index("Date")
    health_dept = health_dept.drop('Month', axis=1)
    return health_dept


def get_metrices(filtered_df):
    health_dept = filtered_df
    totalExpenditure = health_dept['Expenditure'].sum()
    totalRevenue = health_dept['Revenue'].sum()
    totalPatient = health_dept['PatientsTreated'].sum()
    staffFTE = health_dept['StaffFTE'].sum()
    totalCancellation = health_dept['Cancellations'].sum()
    avgLengthOfStay	 = health_dept['AvgLengthOfStay'].sum()
    staffPerPatient = totalPatient/staffFTE
    return ({
        'Expenditure': totalExpenditure,
        'Revenue': totalRevenue,
        'PatientsTreated': totalPatient,
        'StaffFTE': staffFTE,
        'Cancellations': totalCancellation,
        'AvgLengthOfStay': avgLengthOfStay,
        'StaffPerPatient': staffPerPatient
    })
    

def barGraph(data):
    expenditure_revenue_per_dept = data
    # Bar positions
    x = np.arange(len(expenditure_revenue_per_dept['CostCentre']))
    width = 0.35

    ## Initialize a Matplotlib figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))

    # Draw expenditure bars shifted left and revenue on right
    ax.bar(x - width/2, expenditure_revenue_per_dept['Expenditure'], width, label='Expenditure', color='royalblue')
    ax.bar(x + width/2, expenditure_revenue_per_dept['Revenue'], width, label='Revenue', color='limegreen')

    # Labels & formatting
    ax.set_xticks(x)
    ax.set_xticklabels(expenditure_revenue_per_dept['CostCentre'], rotation=45, ha='right')
    ax.set_title("Expenditure and Revenue per Department")
    ax.set_ylabel("Amount ($)")
    ax.legend()

    # Show plot in Streamlit
    st.pyplot(fig)


def timeTrend(data):
    pass
            

def heatMap(data):
    heat_data = data.copy()
    #st.write(heat_data)
    heat_data['MonthYear'] = heat_data.index.strftime('%Y-%m')
    #pivot data
    pivot = heat_data.pivot_table(index='CostCentre', columns='MonthYear', values='TheatreUtilisation')
    #plot heatmap
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(pivot, annot=True, fmt=".1f", cmap='coolwarm', ax=ax)
    st.pyplot(fig)

def scatterPlot(data):
    scatter = data.copy()
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.scatterplot(data=scatter, x='OvertimeHours', y='Expenditure', hue='CostCentre', ax=ax)
    st.pyplot(fig)


def pieChart(data):
    pie = data.copy()
    patient_share = pie.groupby('CostCentre')['PatientsTreated'].sum()
    fig, ax = plt.subplots(figsize=(12,8))
    ax.pie(patient_share, labels=patient_share.index, autopct='%1.1f%%', startangle=140)
    ax.set_title("Share of Patients Treated by Cost Centre")
    ax.axis('equal')  # Equal aspect ratio makes it a perfect circle
    st.pyplot(fig)

def staffUsed(data):
    staff = data.copy()
    staff_by_dept = staff.groupby('CostCentre')['StaffFTE'].sum().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(12,15))
    staff_by_dept.plot(kind='barh', ax=ax, color='skyblue')
    ax.set_title('Total Staff FTE used by Department')
    ax.set_label('Total Staff FTE')
    st.pyplot(fig)

def bubbleChart(data):
    bubble = data.copy()
    month = bubble.index.month_name().unique()
    fig = px.scatter(
        bubble,
        x='StaffFTE',
        y='OvertimeHours',
        size='Expenditure',
        color='CostCentre',
        size_max=60,
    )
    st.plotly_chart(fig)
    

def lineChart(data):
    line = data.copy()
    line['Month'] = line.index.strftime('%Y-%m')
    #melt the df for multiple y variables
    melted = line.melt(
        id_vars='Month',
        value_vars=['StaffFTE', 'OvertimeHours', 'PatientsTreated', 'Cancellations'],
        var_name='Metric',
        value_name='Value'
        )
    fig = px.line(
        melted,
        x='Month',
        y='Value',
        color='Metric',
        markers=True,
        title = 'Monthly Trends of Staff, Overtime, Patients & Cancellations'
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)
    


