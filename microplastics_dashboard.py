import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html

file_url = 'https://drive.google.com/file/d/1HEf5grekNcE8b1FzMmjoZ8faonWg361A/view?usp=sharing'
df = pd.read_csv(file_url)
df["date_label"] = pd.to_datetime(df["date"]).dt.strftime("%b %d\n%Y")  # e.g., Feb 20\n2019

# Custom color scale
custom_scale = [
    [0.0, "#a2cbe8"],   # low (same as ocean color, blends in)
    [0.3, "#a2cbe8"],   # 
    [0.5, "#ffd92f"],   # yellow (mid)
    [0.75, "#d73027"],  # orange (high)
    [1.0, "#d73027"],   # red (very high)
]


vmin = df["mp_concentration_mean"].min()
vmax = df["mp_concentration_mean"].max()

# Create animated scatter_geo plot
fig = px.scatter_geo(
    df,
    lat="lat_bin",
    lon="lon_bin",
    color="mp_concentration_mean",
    #size="Microplastic_Concentration",
    animation_frame="date_label",
    title="Microplastic Concentration in Oceans Over Time Using NASA Satellite Data (2019)",
    #color_continuous_scale="RdBu_r",
    #color_continuous_scale="Blackbody_r",
    #color_continuous_scale="Turbo",
    color_continuous_scale=custom_scale,
    projection="natural earth",
    height=600,
    range_color=[vmin, vmax],  # FIXES the scale across frames
    hover_data={"lat_bin" : False,
                "lon_bin" : False,
                "ocean_name" : True,
        "mp_concentration_mean": True})


fig.update_geos(
    showland=True,
    landcolor="#f2f2f2",        # Clean light land
    showocean=True,
    oceancolor="#a2cbe8",       # Muted medium-dark blue (great for contrast)
    showcoastlines=True,
    coastlinecolor="#222a2a",   # White coastlines add visual edges
    showcountries=False,
    showlakes=False
)

# Clean layout, consistent font and background
fig.update_layout(
    coloraxis_colorbar=dict(
        title="Microplastics Concentration",
        tickvals=[
            vmin,
            vmax
        ],
        ticktext=["Lower", "Higher"],
        len=0.7
    ),
    margin=dict(l=0, r=0, t=40, b=0),
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(size=14)
)

# DASH app layout
app = dash.Dash(__name__)
app.title = "Microplastic Dashboard"

app.layout = html.Div([
    html.H1("Microplastic Movement in Oceans – 2019", style={'textAlign': 'center'}),
    html.P("Explore seasonal accumulation patterns using the animation below.", style={'textAlign': 'center'}),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port=8080)
