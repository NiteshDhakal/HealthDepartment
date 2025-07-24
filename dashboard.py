
import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import plotly.express as  px
import matplotlib.pyplot as plt
from health_department import load_data, get_metrices,barGraph, timeTrend, heatMap, scatterPlot, pieChart, staffUsed, bubbleChart,lineChart


# --- Page config ---
st.set_page_config(page_title="Health Department", layout="wide")
# --- Top Header ---
logo = Image.open("assets/logo.png")  

# load data
health_dept = load_data()
#st.dataframe(health_dept, use_container_width=True)

# load css from markdown file(st_style)
with open("st_style.md", "r", encoding="utf-8") as file:
    md_content = file.read()
# inject CSS
st.markdown(md_content, unsafe_allow_html=True)


def render_header():
    with st.container():
        st.markdown('<div class="custom-header">', unsafe_allow_html=True)

        col_logo, col_name, col_search = st.columns([0.1, 0.7, 0.2])

        with col_logo:
            st.image("assets/logo.png", width=50)

        with col_name:
            st.markdown(
                "<h2 style='margin: 0; padding-top: 8px;'>Health Department Dashboard</h2>",
                unsafe_allow_html=True
            )

        with col_search:
            st.text_input("", placeholder="Search...", label_visibility="collapsed")

        st.markdown('</div>', unsafe_allow_html=True)

render_header()

st.markdown("---")  # Divider line


#----- fetching data ---------
# load data
health_dept = load_data()


# --- Sidebar Menu ---
with st.sidebar:
    # ✅ Logo at the very top (local file or remote URL)
    st.markdown("<div style='margin-top: -100px;'></div>", unsafe_allow_html=True)
    st.image("assets/logo.png", width=50)
    st.title("📂 Navigation")

    with st.expander("⚙️ Filters"):
        year = health_dept.index.month_name().unique()
        selectedYear = st.selectbox("Select Year", year)

        department = sorted(health_dept['CostCentre'].unique())
        selectedDepartment = st.multiselect("Select Department", department)

#--------Function call when filter is used ---------------
def apply_filters(health_dept):
    filtered_df =  health_dept.copy()
    if selectedYear:
        filtered_df = filtered_df[filtered_df.index.month_name()==selectedYear]
    if selectedDepartment:
        filtered_df = filtered_df[filtered_df['CostCentre'].isin(selectedDepartment)]
    return filtered_df

#----- Get values returned as filtered dataframe and use it to find information on selection basis
filtered_df = apply_filters(health_dept)
matricesInfo = get_metrices(filtered_df)

# To convert large number to short 
def format_number(value):
    if value >= 1_00_000:
        return f"{value/1_00_000:.2f}M"
    elif value >= 1_000:
        return f"{value/1_000:.1f}K"
    else:
        return f"{value:.2f}"


##-------------- Compute KPIS -----------------------------
#st.subheader("📌 Key Metrics")
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
   
    st.markdown(
        f'''
       <div class="participants-metric">
            <h5 style="margin: 0;">Participants</h5>
            <p style="font-size: 32px; font-weight: bold; margin: 0;">
                {format_number(matricesInfo["PatientsTreated"])}
            </p>
        </div>''',
       unsafe_allow_html=True
    )
with col2:
    st.markdown(
        f'''
       <div class="participants-metric">
            <h5 style="margin: 0;">Expenditure</h5>
            <p style="font-size: 32px; font-weight: bold; margin: 0;">
                {format_number(matricesInfo["Expenditure"])}
            </p>
        </div>''',
       unsafe_allow_html=True
    )
with col3:
    st.markdown(
       f'''
       <div class="participants-metric">
            <h5 style="margin: 0;">Revenue</h5>
            <p style="font-size: 32px; font-weight: bold; margin: 0;">
                {format_number(matricesInfo["Revenue"])}
            </p>
        </div>''',
       unsafe_allow_html=True
    )

with col4:
    st.markdown(
       f'''
       <div class="participants-metric">
            <h5 style="margin: 0;">StaffFTE</h5>
            <p style="font-size: 32px; font-weight: bold; margin: 0;">
                {format_number(matricesInfo["StaffFTE"])}
            </p>
        </div>''',
       unsafe_allow_html=True
    )

with col5:
    st.markdown(
      f'''
       <div class="participants-metric">
            <h5 style="margin: 0;"> Cancellation</h5>
            <p style="font-size: 32px; font-weight: bold; margin: 0;">
                {format_number(matricesInfo["Cancellations"])}
            </p>
        </div>''',
       unsafe_allow_html=True
    )

with col6:
    st.markdown(
       f'''
       <div class="participants-metric">
            <h5 style="margin: 0;">Staff Per Patient</h5>
            <p style="font-size: 32px; font-weight: bold; margin: 0;">
                {format_number(matricesInfo["StaffPerPatient"])}
            </p>
        </div>''',
       unsafe_allow_html=True
    )

##-------- End Computing KPIS ---------------------------------------------------


#--------- Data Visualization ---------------------------------------
# Expenditure and Revenue per department---------------------------
# Grouping
graph1, graph2 = st.columns(2)
with graph1:
    expenditure_revenue_per_dept = filtered_df.groupby('CostCentre')[['Expenditure', 'Revenue']].sum().reset_index()
    barGraph(expenditure_revenue_per_dept)
with graph2:
    heatMap(filtered_df)


graph3, graph4 = st.columns(2)
with graph3:
    scatterPlot(filtered_df)
with graph4:
    pieChart(filtered_df)

graph5, graph6 = st.columns(2)
with graph5:
    staffUsed(filtered_df)
with graph6:
    bubbleChart(filtered_df)

graph7 = st.columns(1)[0]
with graph7:
    lineChart(filtered_df)

