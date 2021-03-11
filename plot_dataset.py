from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import curdoc
import pandas as pd 
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import row

data = pd.read_csv("data/cmu/overall-state-smoothed.csv") 

group = data.groupby(['date']).mean()
group = group.reset_index()
group['date'] = pd.to_datetime(group['date'])


source = ColumnDataSource(data={
    'x' : group['date'],
    'y' : group['smoothed_pct_cli']
})
 
plot = figure()
plot.circle('x', 'y', source=source)
 
# Define a callback function: update_plot
def update_plot(attr, old, new):
        source.data = {
            'x' : group['date'],
            'y' : group[new]
        }
        
# Create a dropdown Select widget: select    
select = Select(title="distribution", options=list(group.columns), value='')
select.on_change('value', update_plot)
 
# Create layout and add to current document
layout = row(select, plot)
curdoc().add_root(layout)

output_file("plot_cmu.html")
show(layout)