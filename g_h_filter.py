import time
import numpy as np
import pandas as pd

import altair as alt
import streamlit as st

class GH_Filter():
    def __init__(self, x0, dx, g, h, dt) -> None:
        self.x_est = x0
        self.dx = dx
        self.g = g
        self.h = h
        self.dt = dt
    
    def update(self, z):
        # Prediction
        x_pred = self.x_est + (self.dx * self.dt)

        # Update
        residual = z - x_pred
        self.dx = self.dx + self.h * residual / self.dt
        self.x_est = x_pred + self.g * residual

        return self.x_est

def draw_g_h_filter(start, stop, n_step, sigma, g , h):
    temp_list = np.linspace(start, stop, num=n_step)
    g_h_filter = GH_Filter(start, 0.0, g, h, 1)

    temp_data = pd.DataFrame()
    temp_data['temperature'] = temp_list
    temp_data['类别'] = '环境温度'

    measure_df = pd.DataFrame()
    measure_df['measurement'] = np.nan
    measure_df['类别'] = '测量温度'

    g_h_df = pd.DataFrame()
    g_h_df['estimation'] = np.nan
    g_h_df['类别'] = 'g-h 滤波'

    chart_row = st.empty()

    with st.container():
        for i in range(n_step):
            time.sleep(1)

            # Add new data
            measure = np.random.normal(temp_list[i], sigma)
            measure_df.loc[len(measure_df)] = [measure, '测量温度']
            x_est = g_h_filter.update(np.random.normal(temp_list[i], sigma))
            g_h_df.loc[len(g_h_df)] = [x_est, 'g-h 滤波']

            # print(g_h_df)

            # 绘制环境温度曲线
            temp_chart = (
                alt.Chart(temp_data.reset_index())
                .transform_fold(['环境温度'])
                .mark_line(color='black')
                .encode(x=alt.X("index", title='时间', axis=alt.Axis(tickCount=n_step)), 
                        y=alt.Y("temperature", title='温度', scale=alt.Scale(domain=[start - 10, stop + 10])),
                        # color=alt.value('black'),
                        color='类别:N'
                )
            )
    
            # 绘制测量温度曲线
            measure_chart = (
                alt.Chart(measure_df.reset_index())
                .transform_fold(['测量温度'])
                .mark_point(opacity=1.0, color='red', shape='cross', size=50)
                .encode(x=alt.X("index", title='时间', axis=alt.Axis(tickCount=n_step), scale=alt.Scale(domain=[0, n_step])), 
                        y=alt.Y("measurement", title='温度', scale=alt.Scale(domain=[start - 10, stop + 10])),
                        # color=alt.value('black'),
                        color='类别:N',
                )
            )

            # 绘制 g-h 滤波曲线
            g_h_chart = (
                alt.Chart(g_h_df.reset_index())
                .transform_fold(['g-h 滤波'])
                .mark_line(opacity=0.6, color='black', strokeDash=[10,1], point=alt.OverlayMarkDef(filled=False, fill="white"))
                .encode(x=alt.X("index", title='时间', axis=alt.Axis(tickCount=n_step), scale=alt.Scale(domain=[0, n_step])), 
                        y=alt.Y("estimation", title='温度', scale=alt.Scale(domain=[start - 10, stop + 10])),
                        # color=alt.value('black'),
                        color='类别:N',
                )
            )

            chart_row.altair_chart(g_h_chart + measure_chart + temp_chart, use_container_width=True)
