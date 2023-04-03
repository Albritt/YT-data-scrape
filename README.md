# YT Data Scraper
Python script created to use the Youtube Data API to grab channel statistics. Additional analysis follows in SQL to make insights out of the data available from the API.

Libraries Used
--------

Used pandas, googleapiclient, and isodate.

Objective
--------
Using the public Youtube Data API to pull all available public video statistics from [Genshin Impact official channel](https://www.youtube.com/@GenshinImpact). From there I wanted to do some data exploration in SQL to give me an idea of what I wanted to visualize and then create the visualizations in Powe BI. I did some slight data cleaning in Python but not much as I wanted to mostly use this as a learning opportunity for PowerBI's features. 

About the dataset
--------
The data is somewhat limited as the information from Youtube's data API is limited if you are not the channel owner. 

Visualization
--------

Since the youtube channel has not been around for long (started in 2019) I mostly focused on averages in the visualizations as the only years with a full set of information are 2020-2022.

![2023-04-03_01-57-40](https://user-images.githubusercontent.com/61941068/229425686-eb3b486c-c519-44d8-b379-1b42f1ef0ffc.png)
