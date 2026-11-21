import streamlit as st
import altair as alt
import pandas as pd

st.title("IS445 HW6 ")

st.text("UFO Sightings: When are sightings the most common and what is being spotted?")
# read in dataset
dataset = "https://raw.githubusercontent.com/UIUC-iSchool-DataViz/is445_data/main/ufo-scrubbed-geocoded-time-standardized-00.csv"
column_names = ['datetime', 'city', 'state', 'country', 'shape', 'duration_seconds',
                'duration_text', 'comments', 'date_posted', 'latitude', 'longitude']
ufo = pd.read_csv(dataset, header=None, names=column_names)

# convert to datetime
ufo["datetime"] = pd.to_datetime(ufo["datetime"], errors="coerce")

# Viz 1 line chart of sightings by hour of day
ufo_1 = ufo.dropna(subset=['datetime']).copy() 
ufo_1["Hour"] = ufo_1["datetime"].dt.hour 
hour_counts = ufo_1.groupby("Hour").size().reset_index(name="Count")

line_chart = alt.Chart(hour_counts).mark_line(point=True).encode(
    x=alt.X("Hour:O", title="Hour of Day (24 Hour Time)"),
    y=alt.Y("Count:Q", title="Number of Sightings"),
    tooltip=["Hour", "Count"]
).properties(
    title="Number of UFO Sightings by Hour of Day"
)
st.altair_chart(line_chart, use_container_width=True)

st.subheader("Visualization #1 Write-up")
st.write("""
My first visualization shows the number of UFO sightings that were reported at each hour of the day. I chose a line chart
to display this as it makes it easy to see how sighting rise and fall throughout the day. I encoded hour as ordinal since 
there is a natural hour and the number of sightings as quantitative. I added a points so that each metric can be read when
hovered over. The sightings are lowest around the morning, hitting the lowest at hour 8 with 803 and starting to climn
sharply at hour 16 and peaking at hour 21 at 11,445 sightings, likely because the night sky makes lights more apparent
when it is dark. If I had more time, I think that I would make it so that the time could be adjusted to take the light level
into account, as different seasons and times of the year will influence when it is light or dark even at the same time
of day. 
         """)

# Viz 2 scatter plot of sighting durations
ufo_2 = ufo.dropna(subset=['datetime', 'shape', 'country']).copy()
ufo_2 = ufo_2[(ufo_2['duration_seconds'] > 0) & (ufo_2['duration_seconds'] <= 86400)]
ufo_2["Year"] = ufo_2["datetime"].dt.year
ufo_2 = ufo_2[(ufo_2['Year'] >= 1990) & (ufo_2['Year'] <= 2013)] # most sightings are after between 1990 and 2013

shape_options = ['All'] + sorted(ufo_2['shape'].unique()) 
shape_dropdown = st.selectbox("Select UFO Shape: ", options=shape_options)
if shape_dropdown == 'All':
    filtered = ufo_2.copy()
else:
    filtered = ufo_2[ufo_2["shape"] == shape_dropdown].copy()
filtered = filtered[['duration_seconds', 'Year', 'country', 'shape']]

scatter_plot = alt.Chart(filtered).mark_circle(size=30).encode(
    x = alt.X("duration_seconds:Q", title='Sighting Duration (Seconds, log scale)'),
    y = alt.Y("Year:O", title='Year of Sighting'),
    color = alt.Color("country:N", title='Country'),
    tooltip = ["duration_seconds", "Year", "country", "shape"],
).properties(
    title = ("UFO Sighting Duration by Year")
)

st.altair_chart(scatter_plot, use_container_width=True)

st.subheader("Visualization #2 Write-up")
st.write("""
My second visualization shows how long each UFO sighting lasted for each reported UFO shape(light, cigar,
 disk, etc) from 1990 to 2013. I chose a scatter plot as it shows every individual sighting and duration in seconds on 
 the x axis and year on the y axis. I originally plotted the durations as is but found the plot difficult to read due 
 to the variance in sighting duration so I changed it to a log scale to accommodate. I excluded data points with durations
 of 0 and also those over one day since they were likely data entry errors. Coloring by country was another element
 that I thought added a layer of depth to the chart, thought most are from the US. I added a dropdown menu to sort
  by UFP shape for interactivity, allowing viewers to compare the durations for different shapes. If I had more 
  time, I would make the points more easily distinguishable from each other when they overlap.
         """)

st.subheader("Overlap with Homework #5")
st.write("""
There is no overlap with my Homework 5 submission. I used a dataset about the Illinois buildings
 but used the UFO dataset provided for this homework. I used a bar charts for both of my visualizations in HW 5 
 but used a line chart and scatter plot for HW 6.
         """)