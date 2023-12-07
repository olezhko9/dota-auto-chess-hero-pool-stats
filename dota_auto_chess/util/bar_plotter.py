import plotly.graph_objs as go
from plotly import tools
from plotly.offline import plot


def plot_bar(heroes_stat, species_chart, classes_chart):

    bar_1 = go.Bar(
         x=[key for key in heroes_stat.keys()],
         y=[heroes_stat[key] for key in heroes_stat.keys()]
    )

    bar_2 = go.Bar(
         x=[key for key in species_chart.keys()],
         y=[species_chart[key] for key in species_chart.keys()]
    )

    bar_3 = go.Bar(
         x=[key for key in classes_chart.keys()],
         y=[classes_chart[key] for key in classes_chart.keys()]
    )

    fig = tools.make_subplots(rows=3, cols=1, subplot_titles=('Heroes', 'Species', 'Classes'))
    fig.append_trace(bar_1, 1, 1)
    fig.append_trace(bar_2, 2, 1)
    fig.append_trace(bar_3, 3, 1)

    plot(fig, filename='heroes.html', auto_open=False)
