import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import io

web_apps = st.sidebar.selectbox("Select Web Apps",
                                ("Exploratory Data Analysis", "Distributions"))


if web_apps == "Exploratory Data Analysis":

  uploaded_file = st.sidebar.file_uploader("Choose a file")

  if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    df = pd.read_csv(uploaded_file)
    show_df = st.checkbox("Show Data Frame", key="disabled")
    
    data_types = df.dtypes
    data_shape = df.shape

    if show_df:
      st.write(df)
    
    st.sidebar.write('Summary of Datatypes')
    #st.sidebar.metric(label = " Number of Numerical Values", value = data_types.value_counts()[0] + data_types.value_counts()[2])
    #st.sidebar.metric(label = " Number of Categorical Values", value = data_types.value_counts()[1])

    st.sidebar.table(data_types)
    st.sidebar.metric(label="Number of Columns", value=data_shape[1])
    st.sidebar.metric(label="Number of Rows", value=data_shape[0])


    column_type = st.sidebar.selectbox('Select Data Type',
                                       ("Numerical", "Categorical"))

    if column_type == "Numerical":
      numerical_column = st.sidebar.selectbox(
          'Select a Column', df.select_dtypes(include=['int64', 'float64']).columns)

      # histogram
      choose_color = st.color_picker('Pick a Color', "#69b3a2")
      choose_opacity = st.slider(
          'Color Opacity', min_value=0.0, max_value=1.0, step=0.05, value=1.0)

      hist_bins = st.slider('Number of bins', min_value=5,
                            max_value=150, value=30)
      hist_title = st.text_input('Set Title', 'Histogram')
      hist_xtitle = st.text_input('Set x-axis Title', numerical_column)

      fig, ax = plt.subplots()
      ax.hist(df[numerical_column], bins=hist_bins,
              edgecolor="black", color=choose_color, alpha=choose_opacity)
      ax.set_title(hist_title)
      ax.set_xlabel(hist_xtitle)
      ax.set_ylabel('Count')

      st.pyplot(fig)
      filename = "plot.png"
      fig.savefig(filename,dpi = 300)

      summary_stats = df[numerical_column].describe()
      st.subheader('Summary Statistics')
      st.table(summary_stats)



      # Display the download button
      with open("plot.png", "rb") as file:
        btn = st.download_button(
            label="Download image",
            data=file,
            file_name="flower.png",
            mime="image/png"
        )


    if column_type == "Categorical":
      categorical_column = st.sidebar.selectbox(
          'Select a Column', df.select_dtypes(include=['object']).columns)
      
      # histogram
      choose_color = st.color_picker('Pick a Color', "#69b3a2")
      choose_opacity = st.slider(
          'Color Opacity', min_value=0.0, max_value=1.0, step=0.05, value = 1.0)

      hist_title = st.text_input('Set Title', 'Histogram')
      hist_xtitle = st.text_input('Set x-axis Title', categorical_column)

      fig, ax = plt.subplots()
      ax.hist(df[categorical_column].astype(str),
              edgecolor="black", color=choose_color, alpha=choose_opacity)
      ax.set_title(hist_title)
      ax.set_xlabel(hist_xtitle)
      ax.set_ylabel('Count')

      st.pyplot(fig)
      filename = "plot.png"
      fig.savefig(filename,dpi = 300)

      proportion_stats = (df[categorical_column].value_counts() / df[categorical_column].count())*100

      st.subheader('Proportion in each category (by percent)')
      st.table(proportion_stats)

      # Display the download button
      with open("plot.png", "rb") as file:
        btn = st.download_button(
            label="Download image",
            data=file,
            file_name="flower.png",
            mime="image/png"
        )
    

    