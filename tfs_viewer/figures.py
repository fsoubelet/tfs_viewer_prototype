from typing import Sequence, Tuple

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ----- Parameters Querying ----- #


def get_scatter_plot_params(data_frame: pd.DataFrame) -> Tuple[str, Sequence[str], str]:
    plot_versus, plot_columns, plot_mode = st.beta_columns([1, 3, 1])
    with plot_versus:
        versus: str = st.selectbox(
            "Property to Plot Against",
            options=data_frame.columns.to_numpy(),
            help="Select the column that will be on the horizontal axis",
        )
    with plot_columns:
        to_plot: Sequence[str] = st.multiselect(
            "Columns to Plot",
            options=data_frame.columns.to_numpy(),
            help="Select the columns to plot in this chart",
            key="columns_for_scatterplot",
        )
    with plot_mode:
        mode: str = st.selectbox(
            "Styling of the line chart",
            options=["lines", "markers", "lines+markers"],
            help="The styling of the scatter plot data",
        )
    return versus, to_plot, mode


def get_histplot_params(data_frame: pd.DataFrame) -> Tuple[Sequence[str], str, str]:
    plot_columns, marginal_mode, normalization_mode, nbins_query = st.beta_columns([2, 1, 1, 1])
    with plot_columns:
        to_plot: Sequence[str] = st.multiselect(
            "Columns to Plot",
            options=data_frame.columns.to_numpy(),
            help="Select the columns to plot in this chart",
            key="columns_for_histogram",
        )
    with marginal_mode:
        mode: str = st.selectbox(
            "Styling of distribution plot",
            options=["box", "violin", "rug"],
            help="The type of distribution representation used for the upper axis",
        )
    with normalization_mode:
        histnorm: str = st.selectbox(
            "Normalization Routine",
            options=["None", "percent", "probability", "density", "probability density"],
            help="Bin normalization method. If None is selected, then the simple value counts are used",
        )
    with nbins_query:
        nbins: int = st.number_input(
            "Number of Bins",
            value=100,
            step=25,
            min_value=5,
            max_value=1000,
            help="Number of bins in the histogram",
        )
    return to_plot, mode, histnorm, nbins


def get_density_plot_params(data_frame: pd.DataFrame) -> Tuple[str, str]:
    xaxis, yaxis = st.beta_columns([1, 1])
    with xaxis:
        xaxis_var: str = st.selectbox(
            "Property on the Horizontal Axis",
            options=data_frame.columns.to_numpy(),
            help="Select the column that will be on the horizontal axis",
        )
    with yaxis:
        yaxis_var: str = st.selectbox(
            "Property on the Vertical Axis",
            options=data_frame.columns.to_numpy(),
            help="Select the column that will be on the vertical axis",
        )
    return xaxis_var, yaxis_var


# ----- Plotting Functions ----- #


def plotly_line_chart(data_frame: pd.DataFrame, height: int = 600) -> None:
    versus, plot_quantities, mode = get_scatter_plot_params(data_frame)
    fig = go.Figure(layout=go.Layout(height=height))
    for variable in plot_quantities:
        fig.add_trace(
            go.Scattergl(
                x=data_frame[versus].to_numpy(),
                y=data_frame[variable].to_numpy(),
                mode=mode,
                name=variable,
            )
        )
    st.plotly_chart(fig, use_container_width=True)
    # if st.button("Export to HTML"):
    #     fig.write_html("scatterplot.html")


def plotly_histogram(data_frame: pd.DataFrame, height: int = 600) -> None:
    plot_quantities, marginal_mode, histnorm, n_bins = get_histplot_params(data_frame)
    if plot_quantities:  # errors if not
        norm_method = None if histnorm == "None" else histnorm
        fig = px.histogram(
            data_frame,
            x=plot_quantities,
            marginal=marginal_mode,
            histnorm=norm_method,
            barmode="overlay",
            height=height,
            nbins=n_bins,
        )
        st.plotly_chart(fig, use_container_width=True)
    # if st.button("Export to HTML"):
    #     fig.write_html("histogram.html")


def plotly_density_contour(data_frame: pd.DataFrame, height: int = 600) -> None:
    xcol, ycol = get_density_plot_params(data_frame)
    fig = px.density_contour(data_frame, x=xcol, y=ycol, height=height)
    fig.update_traces(contours_coloring="fill", contours_showlabels=True)
    st.plotly_chart(fig, use_container_width=True)
