# SQLAlchemy Challenge: Module 10

## Objective

The goal for this challenge was to explore and analyze climate data using Python and SQLAlchemy. After connecting the database and running some analysis on the precipitation and the stations that recorded it, an app was created using SQLite and Flask to create static and dynamic routes to query this information. 

### Data Analysis and Exploration
Pandas, matplotlib, and SQLAlchemy ORM queries were used to explore some of the findings recorded by different stations in the Hawaii area. This exploration and analysis included data visualization of the precipitation over one full year of the dataset's most recent data, summary statistics of the same query, and a data visualization of the temperature observation frequency of the most active station in Hawaii.

### Climate App

Flask API was used to design an app that pulls two types of queries: Static and Dynamic. The static queries calls the previous data analysis findings of precipitation over the most recent full year, observations of the most-active station during the same time period, and a list of stations in the database. The dynamic routes are designed to call queries of the minimum, maximum, and average temperatures for the dates in question, using the date written directly into the URL (in YYYY-MM-DD format). Inserting one date automatically returns the start date until the most recent entry in the database. Inserting 2 dates (with a / between) queries the range of both dates.

## Attributions

All information sourced and generated in this code is from the course material.
