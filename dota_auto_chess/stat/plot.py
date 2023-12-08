import plotly.graph_objs as go
from plotly import tools
from plotly.offline import plot


def plot_bar(filename, heroes_stat, species_stat, classes_stat):
    bar_1 = go.Bar(
        x=[key for key in heroes_stat.keys()],
        y=[heroes_stat[key] for key in heroes_stat.keys()]
    )

    bar_2 = go.Bar(
        x=[key for key in species_stat.keys()],
        y=[species_stat[key] for key in species_stat.keys()]
    )

    bar_3 = go.Bar(
        x=[key for key in classes_stat.keys()],
        y=[classes_stat[key] for key in classes_stat.keys()]
    )

    fig = tools.make_subplots(rows=3, cols=1, subplot_titles=('Heroes', 'Species', 'Classes'))
    fig.append_trace(bar_1, 1, 1)
    fig.append_trace(bar_2, 2, 1)
    fig.append_trace(bar_3, 3, 1)

    plot(fig, filename=filename, auto_open=False)
