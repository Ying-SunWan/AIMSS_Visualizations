import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures

st.set_page_config(layout="centered")
config = {'displayModeBar': False}
st.title('Model Fitting')

if 'degrees' not in st.session_state:
    st.session_state['degrees'] = 5

data = pd.read_csv('./data/fitting.csv')

time_X = np.atleast_2d(data["day"].values).T
temp = data["temperature"].values

X = time_X
y = temp

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.4, random_state=10)

sorted_indices = X_test.flatten().argsort()
X_test_sorted = X_test[sorted_indices]
y_test_sorted = y_test[sorted_indices]

st.number_input('Polynomial Degrees', min_value=1, max_value=50, key='degrees')
poly = PolynomialFeatures(degree=st.session_state['degrees'], include_bias=False)
poly_X_train = poly.fit_transform(X_train)
poly_X_test = poly.transform(X_test)

model = LinearRegression()
model.fit(poly_X_train, y_train)
y_pred = model.predict(poly_X_test)

col1, col2 = st.columns(2)

with col1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=X_train.flatten()*366, y=y_train, mode='markers', name='Training'))
    fig.add_trace(go.Scatter(x=X_test_sorted.flatten() * 366, y=y_pred[sorted_indices], mode='lines', name='Fitted Curve', line=dict(color='black')))

    fig.update_layout(
        title = 'Training', 
        xaxis_title='Day of the Year',
        yaxis_title='Temperature',
        margin=dict(t=30, b=10),
        height=300,
        showlegend=False
    )
    st.plotly_chart(fig, config=config)

with col2:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=X_test_sorted.flatten()*366, y=y_test_sorted, mode='markers', name='Testing', marker=dict(color='red')))
    fig.add_trace(go.Scatter(x=X_test_sorted.flatten() * 366, y=y_pred[sorted_indices], mode='lines', name='Fitted Curve', line=dict(color='black')))

    fig.update_layout(
        title='Testing', 
        xaxis_title='Day of the Year',
        yaxis_title='Temperature',
        margin=dict(t=30, b=10),
        height=300,
        showlegend=False
    )
    st.plotly_chart(fig, config=config)

train_losses = []
test_losses = []

for degree in range(1, st.session_state['degrees'] + 1):
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    poly_X_train = poly.fit_transform(X_train)
    poly_X_test = poly.transform(X_test)

    model = LinearRegression()
    model.fit(poly_X_train, y_train)
    
    # Predict and calculate mean squared error
    y_train_pred = model.predict(poly_X_train)
    y_test_pred = model.predict(poly_X_test)
    
    train_mse = mean_squared_error(y_train, y_train_pred)
    test_mse = mean_squared_error(y_test, y_test_pred)
    
    train_losses.append(train_mse)
    test_losses.append(test_mse)

fig_loss = go.Figure()
fig_loss.add_trace(go.Scatter(x=list(range(1, st.session_state['degrees'] + 1)), y=train_losses, mode='lines+markers', name='Training Loss'))
fig_loss.add_trace(go.Scatter(x=list(range(1, st.session_state['degrees'] + 1)), y=test_losses, mode='lines+markers', name='Test Loss'))
fig_loss.update_layout(
    title = f'Mean Squared Error: {test_losses[-1]:.2f}', 
    xaxis_title='Polynomial Degree',
    yaxis_title='MSE',
    showlegend=False,
    margin=dict(t=30),
    height=200,
    hovermode='x unified'
)
st.plotly_chart(fig_loss, config=config)