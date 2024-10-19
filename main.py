import streamlit as st

from mean_filter import draw_mean_filter
from g_h_filter import draw_g_h_filter

st.header("均值滤波 (Mean Filter)", divider=True)

draw_mean_filter(mean=20, sigma=2, n_step=21)

st.header("g-h Filter", divider=True)

g = st.slider("g value", min_value=0.0, max_value=1.0, value=0.1, step=0.1)
h = st.slider("h value", min_value=0.0, max_value=1.0, value=0.1, step=0.1)

draw_g_h_filter(start=15, stop=55, n_step=21, sigma=2, g=g, h=h)

