import numpy as np
import streamlit as st

from mean_filter import draw_mean_filter
from g_h_filter import GH_Filter_Plot

# Mean Filter
st.header("均值滤波 (Mean Filter)", divider=True)

animation = st.toggle("Activate animation", key='animation_mean')
draw_mean_filter(mean=20, sigma=2, n_step=51, animation=animation)

# g-h Filter
st.header("g-h Filter", divider=True)

data = np.linspace(15, 55, num=51)
if "g_h_linear" not in st.session_state:
  st.session_state.g_h_linear = GH_Filter_Plot(data, sigma=2)

st.session_state.g_h_linear.draw()

data = np.concatenate((np.linspace(15, 55, num=20), np.array([55]*30)))
if "g_h_slope" not in st.session_state:
    st.session_state.g_h_slope = GH_Filter_Plot(data, sigma=2)

st.session_state.g_h_slope.draw()
