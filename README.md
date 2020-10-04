# NHL Player Point Prediction: Project Overview

- Optimised a regression model which predicts how many points an NHL player can be expected to achieve next year (RMSE of ~6.7 and r<sup>2</sup> of 91%) which can hopefully help me (and others) find success in fantasy hockey.
- Used the official NHL API to create a custom function that collects data on every complete NHL season from 2008 through 2018.
- Visualised the data and engineered features from the scraped data that were used to improve model performance.
- Built transformation pipelines to take incoming data and convert it to a structure which could be easily ingested by my final model.
- Trained and tuned the following models: Linear, Lasso, Support Vector Machine, Decision Tree, Random Forest, Voting Regressor.

## Framing The Problem


### Data Collection

I created a custom function using the official NHL API to collect the data for this project. I chose to scrape the data for each season between 2008 and 2018, excluding the lockout year of 2012. This is due to the fact that since the game has changed so much even in the past 10 years, any data further back beyond that I was worried might skew some of our predictions. The features that I ended up extracting via the API were:

season, team, name, birthday, age, nationality, height, weight, number, rookie, position_code, position_type, captain, alternate_capt, handedness, toi, pp_toi, sh_toi, ev_toi, assists, goals, pim, shots, shot_perc, games, hits, blocked, plusminus, shifts, points.

<img src="images/scraping-2.png" height=500 width=800/>
<img src="images/scraping-1.png" height=400 width=500/>


## Data Exploration


## 

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

