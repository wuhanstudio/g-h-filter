import time
import uuid
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

class GH_Filter_Plot():
    def __init__(self, data, sigma) -> None:

        self.data = data
        self.sigma = sigma

        self.g_uuid = uuid.uuid4()
        self.h_uuid = uuid.uuid4()
        self.animation_uuid = uuid.uuid4()

    @st.fragment
    def draw(self, g=0.6, h=0.1):
        self.animation = st.toggle("Activate animation", key=self.animation_uuid)
        self.g = st.slider("g value", min_value=0.0, max_value=1.0, value=g, step=0.01, key=self.g_uuid)
        self.h = st.slider("h value", min_value=0.0, max_value=1.0, value=h, step=0.01, key=self.h_uuid)

        self.g_h_filter = GH_Filter(self.data[0], 0.0, self.g, self.h, 1)

        n_step = len(self.data)

        temp_data = pd.DataFrame()
        temp_data['temperature'] = self.data
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

                if self.animation:
                    time.sleep(1)

                # Add new data
                measure = np.random.normal(self.data[i], self.sigma)
                measure_df.loc[len(measure_df)] = [measure, '测量温度']

                x_est = self.g_h_filter.update(measure)
                g_h_df.loc[len(g_h_df)] = [x_est, 'g-h 滤波']

                # print(g_h_df)

                # 绘制环境温度曲线
                temp_chart = (
                    alt.Chart(temp_data.reset_index())
                    .transform_fold(['环境温度'])
                    .mark_line(color='black')
                    .encode(x=alt.X("index", title='时间', axis=alt.Axis(tickCount=n_step), scale=alt.Scale(domain=[0, n_step])), 
                            y=alt.Y("temperature", title='温度', scale=alt.Scale(domain=[np.min(self.data) - 3*self.sigma, np.max(self.data) + 3*self.sigma])),
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
                            y=alt.Y("measurement", title='温度', scale=alt.Scale(domain=[np.min(self.data) - 3*self.sigma, np.max(self.data) + 3*self.sigma])),
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
                            y=alt.Y("estimation", title='温度', scale=alt.Scale(domain=[np.min(self.data) - 3*self.sigma, np.max(self.data) + 3*self.sigma])),
                            # color=alt.value('black'),
                            color='类别:N',
                    )
                )

                chart_row.altair_chart(g_h_chart + measure_chart + temp_chart, use_container_width=True)
