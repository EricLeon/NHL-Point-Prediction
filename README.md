# NHL Player Point Prediction: Project Overview

- Optimised a regression model which predicts how many points an NHL player can be expected to achieve next year (RMSE of ~6.7 and r<sup>2</sup> of 91%) which can hopefully help me (and others) find success in fantasy hockey.
- Used the official NHL API to create a custom function that collects data on every complete NHL season from 2008 through 2018.
- Visualised the data and engineered features from the scraped data that were used to improve model performance.
- Built transformation pipelines to take incoming data and convert it to a structure which could be easily ingested by my final model.
- Trained and tuned the following models: Linear, Lasso, Support Vector Machine, Decision Tree, Random Forest, Voting Regressor.

## Framing The Problem

- Objective: Predict the number of total points (goals + assists) a given player is expected to produce in an upcoming NHL season.
- Why: This prediction will eventually be used to fill out a fantasy NHL in which I participate on an annual basis.
- This is framed as a supervised multiple regression problem where I can apply batch learning.
- Some potential enhancement ideas are:
  - Incorporate some sort of salary data which could act as a proxy for how their GM's expect them to perform.
  - Use partial season data to forecast performance for the rest of the season so that I can make adjustments to my predictions after any given number of games.


### Data Collection

I created a custom function using the official NHL API to collect the data for this project. I chose to scrape the data for each season between 2008 and 2018, excluding the lockout year of 2012. This is due to the fact that since the game has changed so much even in the past 10 years, any data further back beyond that I was worried might skew some of our predictions. The features that I ended up extracting via the API were:
[season, team, name, birthday, age, nationality, height, weight, number, rookie, position_code, position_type, captain, alternate_capt, handedness, toi, pp_toi, sh_toi, ev_toi, assists, goals, pim, shots, shot_perc, games, hits, blocked, plusminus, shifts, points].

![](images/scraping-2.png)
<img src="images/scraping-1.png" height=600 width=750/>


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


<img src="images/eda-2.png" height=600 width=700/>
<img src="images/eda-1.png" height=600 width=500/>
<img src="images/eda-6.png" height=700 width=500/>
<img src="images/eda-3.png" height=400 width=500/>
<img src="images/eda-4.png" height=400 width=600/>
<img src="images/eda-5.png" height=400 width=600/>



## Model Building

I first split the data into a train set and a test set. For this project I decided to test my models on the last full season of data I had (2018-2019 season) and see if I could use all the seasons prior to that to predict the top performers for that most recent season. So for that reason I held out the 2018/19 data as my testing set, and used all other seasons as the training data. 

I created a transformation pipeline using Scikit-learn transformers to encode my categorical variables, as well as added in some of my own custom transformers to take care of some of the feature engineering that I did. This made predicting new data easier as it ensured every piece of new data that came in was processed and transformed the exact same way.

The models I used were:
- **Multiple Linear Regression** as a baseline for model performance.
- **Lasso Regression** as since some of the features were a bit skewed, I thought a normalised model would perform well.
- **Support Vector, Decision Tree & Random Forest** models for the same reason as the Lasso. Also generally these are more powerful models and tend to perform well.
- **Voting Regressor** which used soft voting based on all of the previously listed models to arrive at a final prediction.


## Model Performance

The final performance on each of my tuned models was:
- Linear Regression: RMSE of 6.59
- Lasso Regression: RMSE of 6.58
- Support Vector Machine: RMSE of 5.56
- Random Forest: RMSE of 5.92
- Voting Regressor: RMSE of 5.7

<img src="images/results-1.png" height=300 width=750/>

Another test I did for my final model was to predict the top 20 performers for the 2018/19 season and compare my list to the actual top 20 performers for the same season. The results are below, and I was able to predict 15 players who were actually among the leagues top 20.

**Actual Top 20 Performers in 2018/19 Season**            |  **Predicted Top 20 Performers in 2018/19 Season**
:--------------------------------------------------------:|:--------------------------------------------------:
<img src="images/actual-1.png" height=650 width=200/>     |  <img src="images/predicted-1.png" height=650 width=200/> 


## In Action

My idea of the business use for this system would be to run it at the start of each draft round during draft day for my fantasy hockey league. All I would need to make it work would be a list of all of the players that are still available to be drafted. The function I have written would take this list, as well as my finalised regression model and would output a DataFrame sorted in descending order of what players (top 10 out of those who are still available) would be expected to produce the most points; and I would simply select the player at the top of the list. I took a list of random players names to represent a list of those who are still available and passed it to my model, the output would look like:

<img src="images/results-3.png" height=650 width=200/>


## Code & Resources Used
- **Python Version:** 3.7
- **Python Libraries:** Requests, NumPy, pandas, Matplotlib, Seaborn, Scikit-learn
- **Resources:** [Using the NHL API](https://hackernoon.com/retrieving-hockey-stats-from-the-nhls-undocumented-api-zz3003wrw)
