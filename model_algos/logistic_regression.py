import streamlit as st
import pandas as pd
import numpy as np
from math import floor, ceil
import plotly.graph_objects as go

config = {'displayModeBar': False}
st.title("Logistic Regression")

df = pd.DataFrame({
    'Sex': ['Male']*10 + ['Female']*10,
    'Height': [
        171, 173.29, 176.52, 177.1, 177.70, 177.9, 178.3, 178.87, 180.3, 181.9,  # Male
        159.89, 161.42, 162.32, 162.6, 162.98, 163.2, 163.41, 164.53, 167.2, 168.4,  # Female
    ],
})
x_min = floor(df['Height'].min())
x_max = ceil(df['Height'].max())
x_range = range(x_min, x_max+1)

col1, col2 = st.columns(2, gap='large')

with col1:
    st.slider(
        'Slope', 
        min_value = 0., 
        max_value = 1., 
        step = 0.05, 
        value = 0.5, 
        key = 'log_m'
    )
    st.slider(
        'Center', 
        min_value = x_min, 
        max_value = x_max, 
        value = x_min + (x_max - x_min) // 2, 
        key = 'log_c'
    )
    log_b = -st.session_state['log_m'] * st.session_state['log_c']

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x = list(x_range),
        y = [st.session_state['log_m'] * i + log_b for i in x_range],
        mode = 'lines',
        marker_color = '#bfc5d3',
        hoverinfo = 'skip',
    ))
    fig.add_trace(go.Scatter(
        x = df['Height'][:10],
        y = [1] * 10,
        mode = 'markers',
        marker_color = '#0068c9',
        marker_symbol = 'square',
        name = 'Male',
    ))
    fig.add_trace(go.Scatter(
        x = df['Height'][10:],
        y = [-1] * 10,
        mode = 'markers',
        marker_color = '#ff2b2b',
        name = 'Female',
    ))
    fig.update_layout(
        margin = dict(t=50, r=0),
        height = 400,
        showlegend = False,
        xaxis_title = 'Height (cm)',
        yaxis = dict(
            title = 'log(p/(1-p))',
            tickvals = [-1, 1],
            ticktext = ['-inf', 'inf'],
            range = [-1.1, 1.1]
        ),
        title = f"log(p/(1-p)) = {st.session_state['log_m']} * Height + {round(log_b, 2)}",
    )
    st.plotly_chart(fig, config=config)

with col2: 
    st.number_input(
        'Height', 
        min_value = 0., 
        max_value = 1000., 
        step = 0.5, 
        value = 170., 
        key = 'log_x'
    )

    p = 1 / (1 + np.exp(-(log_b + st.session_state['log_m'] * st.session_state['log_x'])))
    sex = 'Male' if  p > 0.5 else 'Female' if p < 0.5 else 'Unknown'
    st.write(f"Predicted Sex: {sex}")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x = list(x_range),
        y = [1 / (1 + np.exp(-(log_b + st.session_state['log_m'] * i))) for i in x_range],
        mode = 'lines',
        marker_color = '#bfc5d3',
        hoverinfo = 'skip',
    ))
    fig.add_hrect(
        y0 = 0.5, 
        y1 = 1, 
        line_width = 0, 
        fillcolor = '#0068c9', 
        opacity = 0.1
    )
    fig.add_hrect(
        y0 = 0, 
        y1 = 0.5, 
        line_width = 0, 
        fillcolor = '#ff2b2b', 
        opacity = 0.1
    )
    fig.add_trace(go.Scatter(
        x = df['Height'][:10],
        y = [1 / (1 + np.exp(-(log_b + st.session_state['log_m'] * i))) for i in df['Height'][:10]],
        mode = 'markers',
        marker_color = '#0068c9',
        marker_symbol = 'square',
        name = 'Male',
    ))
    fig.add_trace(go.Scatter(
        x = df['Height'][10:],
        y = [1 / (1 + np.exp(-(log_b + st.session_state['log_m'] * i))) for i in df['Height'][10:]],
        mode = 'markers',
        marker_color = '#ff2b2b',
        name = 'Female',
    ))
    if 'log_x' in st.session_state:
        fig.add_trace(go.Scatter(
            x = [st.session_state['log_x']],
            y = [1 / (1 + np.exp(-(log_b + st.session_state['log_m'] * st.session_state['log_x'])))],
            mode = 'markers',
            marker_color = 'black',
            marker_size = 10,
            marker_symbol = 'x',
            name = 'Prediction',
        ))
    fig.update_layout(
        margin = dict(t=115, r=0),
        height = 475,
        showlegend = False,
        xaxis_title = 'Height (cm)',
        yaxis_title = 'Probability',
    )
    st.plotly_chart(fig, config=config)
