# NHL Player Point Prediction: Project Overview

- Optimised a regression model which predicts how many points an NHL player can be expected to achieve next year (RMSE of ~6.7 and r<sup>2</sup> of 91%) which can hopefully help me (and others) find success in fantasy hockey.
- Used the official NHL API to create a custom function that collects data on every complete NHL season from 2008 through 2018.
- Visualised the data and engineered features from the scraped data that were used to improve model performance.
- Built transformation pipelines to take incoming data and convert it to a structure which could be easily ingested by my final model.
- Trained and tuned the following models: Linear, Lasso, Support Vector Machine, Decision Tree, Random Forest, Voting Regressor.

## Framing The Problem


### Data Collection

I created a custom function using the official NHL API to collect the data for this project. I chose to scrape the data for each season between 2008 and 2018, excluding the lockout year of 2012. This is due to the fact that since the game has changed so much even in the past 10 years, any data further back beyond that I was worried might skew some of our predictions. The features that I ended up extracting via the API were:
[season, team, name, birthday, age, nationality, height, weight, number, rookie, position_code, position_type, captain, alternate_capt, handedness, toi, pp_toi, sh_toi, ev_toi, assists, goals, pim, shots, shot_perc, games, hits, blocked, plusminus, shifts, points].

<img src="images/scraping-2.png" height=500 width=800/>
<img src="images/scraping-1.png" height=400 width=600/>


## Data Cleaning & Engineering

After scraping the data I needed to clean it up in various ways. The modifications I made to the data were:

- Calculated the players *age at the start of each season*. Since the *age* feature I scraped was the players current age (at time of scraping).
- Transformed the *height* variable from *FT'IN"* to just *Inches* which made it readily available to be passed into the machine learning model.
- Parsed all of the *time on ice (TOI)* features to represent *Seconds* on the ice, as opposed to *MM:SS*. 
- Combined the *captain* & *alternate_captain* features into one feature which represented whether or not the player had either of these letters on their sweater.
- Used a custom built dictionary to map each team to their respective *division* and *conference*.
- Parsed each players *birthday* and created a feature for their *birth_month* as well as *birth_season*


## Data Visualisation

I explored the distrubutions of various features in our data, and tried to uncover some relationships between any independent variables and our target variable, *points*.

Some interesting things I found during this step were:
- Players born in the Summer and Fall months tended to have more points per season on average compared to players born in the Spring or Winter months.
- Players size in the NHL is very normally distributed; meaning most players are roughly around the same size.
- The strongest correlations with our target variable were *shots* and *powerplay time on ice* which both make a lot of sense.
- Players with a letter (C or A) on their jersey tend to perform better than players without.
- Right handed players have more points on average than their left handed counterparts.

<img src="images/eda-2.png" height=400 width=600/>
<img src="images/eda-1.png" height=400 width=600/>
<img src="images/eda-6.png" height=400 width=600/>
<img src="images/eda-3.png" height=400 width=600/>
<img src="images/eda-4.png" height=400 width=600/>
<img src="images/eda-5.png" height=400 width=600/>


### Code & Resources Used
**Python Version:** 3.7

**Python Libraries:** Requests, NumPy, pandas, Matplotlib, Seaborn, Scikit-learn

**Resources:** [Using the NHL API](https://hackernoon.com/retrieving-hockey-stats-from-the-nhls-undocumented-api-zz3003wrw)


Framing the problem:
- objective: Predict the number of total points (goals + assists) a given player is expected to achieve in a particular NHL season (82 games).
- how used? This prediction will eventually be used to fill out a fantasy NHL team given some constraints (12 forwards, 6 defence, for example)

- The data I will be using is labelled and has previous years stats for each player along with their point output.

- For the purposes of this project I will just predict a players output based on similar stats from previous years, however a potential enhancement idea will be to incorporate season-to-date data, which will provide an up to date prediction part way through the season (eventually employ online learning with a high learning rate so that we learn from new information quicker).

- Therefore I have a supervised multiple regression problem, where I can apply batch learning.


Getting the data:
- For this project I found an NHL API which can be used to obtain previous years data. The API is not very well documented however using a source (https://hackernoon.com/retrieving-hockey-stats-from-the-nhls-undocumented-api-zz3003wrw) I was able to piece together how it works. I will need to use multiple API calls to first obtain every teams active roster for a particular season. Once I have the rosters I then make API calls to get player specific information for every player on each roster.
*NOTE* that this API only contains data on currently active players. Therefore players who have retired will not be included in any years data. 


Cleaning the data:

