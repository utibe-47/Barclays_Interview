# User Guide



I have included 3 simple dashboards in the folders:
- population dashboard

The population dashboard is created using flask and plotly and can be activated directly from python by running 
the location_stats_app.py module. You can then access it via the http style url in your browser either by clicking
on the url or copying and pasting it to a browser.

- stocks dashboard

The stocks dashboard was created using bokeh. It needs to be activated from the command promp
by opening a new command prompt, navigating your way to the stocks_dashboard folder where the code 
sits and typing the following into the command window: bokeh serve --show stock_dashboard.py

Please note that it may not work if you copy and paste the command into the command window

- returns dashboard

Like the stocks dashboard, this also runs using boke. To activate the dashboard, open a command prompt 
and make your way to the returns_dashboard folder and type the following into the command prompt:
bokeh serve --show returns_dashboard.py

- Four dashboard

I also left in an unfinished enterprise solution in flask which includes, a gui to
run different models, a dashboard and a job queue. This is part of a personal project 
I have been working but it requires more time to complete.


## Please see requirements.txt file for dependencies