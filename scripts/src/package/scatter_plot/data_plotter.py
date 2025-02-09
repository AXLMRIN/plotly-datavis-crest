# Third Parties
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Native
# NOTE might be worth finding a cleaner way to do that
import sys
sys.path.append(("/Users/axelmorin/Library/Mobile Documents/com~apple~CloudDocs"
                 "/Axel_tout/Professionnel/Stages/TFE/CREST/workdirectory/Genre"
                 "/dataVis/plotly-datavis-crest/scripts/src"))
sys.path.append(("/Users/axelmorin/Library/Mobile Documents/com~apple~CloudDocs"
                 "/Axel_tout/Professionnel/Stages/TFE/CREST/workdirectory/Genre"
                 "/dataVis/plotly-datavis-crest/scripts"))

# Custom 

# Classes
from plotlyThemes.general_theme import TracesColours
# Functions

# Settings =====================================================================

def is_grey(colour : str) : 
    # Assume this is HEX
    r,g,b = colour[1:3], colour[3:5], colour[5:7]
    return (r == g) & (g == b)

def is_legendonly(colour : str):
    if is_grey(colour) : return "legendonly"
    return True

def add_dots(x : np.ndarray, y : np.ndarray, size : np.ndarray,
             text : np.ndarray, name : str, colour : str,
             visible : bool | str = True) -> go.Scatter :
    return go.Scatter(
        x = x, y = y,
        mode = "markers", name = name, 
        marker = {
            "size" : size,
            "color" : colour,
            "sizemin" : 0, "sizemode" : "area", 'sizeref' : 1/4,
            "line" : {"width" : 0.3}
            },
        opacity = 0.8, 
        customdata= text,
        hovertemplate= "%{customdata}",
        # visible = visible
    )

def create_data(fig : go.Figure, df : pd.DataFrame,
                traces_color : TracesColours) -> None : 
    fig.update(data = [
            add_dots(discipline_df["proportion_classe"],
                     discipline_df["proportion_genre"],
                     discipline_df["n_articles"],
                     discipline_df["text"],
                     discipline, traces_color[discipline],
                     is_legendonly(traces_color[discipline])
                     )
            for discipline, discipline_df in df.groupby("discipline")
    ])

def create_frame(df : pd.DataFrame, annee : float, 
                 traces_color : TracesColours) -> go.Frame:
    return go.Frame(data = [
            add_dots(discipline_df["proportion_classe"],
                     discipline_df["proportion_genre"],
                     discipline_df["n_articles"],
                     discipline_df["text"],
                     discipline, traces_color[discipline]
                     )
            for discipline, discipline_df in df.groupby("discipline")
        ], name = annee
    )



def create_control_buttons(fig : go.Figure) : 
    fig.update_layout(updatemenus =  [
        {
            "type": "buttons",
            "buttons": [{
                "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}],
                "label": "Pause",
                "method": "animate"
            },
            {
                "label": "Play",
                "method": "animate",
                "args": [None]
            }]
        }
    ])
