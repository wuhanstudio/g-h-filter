import numpy as np
import streamlit as st

from mean_filter import draw_mean_filter
from g_h_filter import GH_Filter_Plot

def gen_linear(start, stop, step):
    return np.linspace(start, stop, num=step)

def gen_slope(start, stop, step):
    return np.concatenate((np.linspace(start, stop, num=int(step*0.4)), np.array([stop]*int(step*0.6))))

def gen_sin(step):
    time = np.linspace(0, 4 * np.pi, step, endpoint=False)
    return 30 * np.sin(time)

def gen_accl(start, step, accel):
    data = []
    dx = 0
    for i in range(step):
        data.append(start + accel * (i**2) / 2 + dx * i)
        dx += accel
    return data

# Mean Filter
st.header("均值滤波 (Mean Filter)", divider=True)

animation = st.toggle("Activate animation", key='animation_mean')
draw_mean_filter(mean=20, sigma=2, n_step=51, animation=animation)

# g-h Filter
st.header("g-h Filter", divider=True)

data = gen_linear(15, 55, 50)
if "g_h_linear" not in st.session_state:
  st.session_state.g_h_linear = GH_Filter_Plot(data, sigma=2)

st.session_state.g_h_linear.draw()

data = gen_slope(15, 55, 50)
if "g_h_slope" not in st.session_state:
    st.session_state.g_h_slope = GH_Filter_Plot(data, sigma=2)

st.session_state.g_h_slope.draw()

data = gen_sin(50)
if "g_h_sin" not in st.session_state:
    st.session_state.g_h_sin = GH_Filter_Plot(data, sigma=10)

st.session_state.g_h_sin.draw()

data = gen_accl(0, 20, 90)
if "g_h_accel" not in st.session_state:
    st.session_state.g_h_accel = GH_Filter_Plot(data, sigma=10, g=0.2, h=0.02)

st.session_state.g_h_accel.draw()
