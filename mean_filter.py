import time
import uuid
import numpy as np
import pandas as pd

import altair as alt
import streamlit as st

@st.fragment
def draw_mean_filter(mean, sigma, n_step, animation=False):
    chart_row = st.empty()

    temp_data = pd.DataFrame()
    temp_data['temperature'] = np.array([mean] * (n_step))
    temp_data['类别'] = '环境温度'

    measure_df = pd.DataFrame()
    measure_df['measurement'] = np.nan
    measure_df['类别'] = '测量温度'

    average_df = pd.DataFrame()
    average_df['average'] = np.nan
    average_df['类别'] = '均值滤波'

    # 绘制环境温度曲线
    temp_chart = (
        alt.Chart(temp_data.reset_index())
        .transform_fold(['环境温度'])
        .mark_line(color='black')
        .encode(x=alt.X("index", title='时间', axis=alt.Axis(tickCount=n_step)), 
                y=alt.Y("temperature", title='温度', scale=alt.Scale(domain=[mean - 10, mean + 10])),
                # color=alt.value('black'),
                color='类别:N'
        )
    )

    with st.container():
        for i in range(n_step):
            if animation:
                time.sleep(1)

            # Add new data
            measure_df.loc[len(measure_df)] = [np.random.normal(mean, sigma), '测量温度']
            average_df.loc[len(average_df)] = [measure_df['measurement'].sum() / len(measure_df), '均值滤波']

            # 绘制测量温度曲线
            measure_chart = (
                alt.Chart(measure_df.reset_index())
                .transform_fold(['测量温度'])
                .mark_point(opacity=1.0, color='red', shape='cross', size=50)
                .encode(x=alt.X("index", title='时间', axis=alt.Axis(tickCount=n_step)), 
                        y=alt.Y("measurement", title='温度', scale=alt.Scale(domain=[mean - 10, mean + 10])),
                        # color=alt.value('black'),
                        color='类别:N',
                )
            )

            # 绘制均值温度曲线
            average_chart = (
                alt.Chart(average_df.reset_index())
                .transform_fold(['均值温度'])
                .mark_line(opacity=0.6, color='black', strokeDash=[10,1], point=alt.OverlayMarkDef(filled=False, fill="white"))
                .encode(x=alt.X("index", title='时间', axis=alt.Axis(tickCount=n_step)), 
                        y=alt.Y("average", title='温度', scale=alt.Scale(domain=[mean - 10, mean + 10])),
                        # color=alt.value('black'),
                        color='类别:N'
                )
            )

            chart_row.altair_chart(measure_chart + temp_chart + average_chart, use_container_width=True)
