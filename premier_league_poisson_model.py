from turtle import color
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

#load and filter data
data = pd.read_csv("G:\\DataSc\\results.csv",encoding="windows-1252")
compressed_dat = data[10044:10875]
compressed_dat = compressed_dat[["HomeTeam","AwayTeam","FTHG","FTAG"]]

#Home and Away total Goals
home_total_goals = compressed_dat[["FTHG"]].sum()
home_average_goals = compressed_dat[["FTHG"]].mean()
Away_total_goals= compressed_dat[["FTAG"]].sum()
Away_average_goals = compressed_dat[["FTAG"]].mean()

#LIVERPOOL AND LEICESTER DATA
liverpool_df = compressed_dat[compressed_dat["HomeTeam"] == "Liverpool"]
liverpool_total_home_goals = liverpool_df[["FTHG"]].sum()
liverpool_home_goals_avg = liverpool_df[["FTHG"]].mean()
liverpool_total_conceded = liverpool_df[["FTAG"]].sum()
liverpool_conceded_avg = liverpool_df[["FTAG"]].mean()

Leicester_df = compressed_dat[compressed_dat["AwayTeam"] == "Leicester"]
leicester_total_away_goals = Leicester_df[["FTAG"]].sum()
leicester_away_goals_avg= Leicester_df[["FTAG"]].mean()
leicester_total_conceded = Leicester_df[["FTHG"]].sum()
leicester_conceded_avg = Leicester_df[["FTHG"]].mean()

#PUT THE DATA TO A DATAFRAME
compiled_data = {"Total Home goals by all":[int(home_total_goals),len(compressed_dat),round(float(home_average_goals),3)],
    "Total Away goals by all":[int(Away_total_goals),len(compressed_dat),round(float(Away_average_goals),3)],
    "Home Goals scored by Liverpool":[int(liverpool_total_home_goals),len(liverpool_df),round(float(liverpool_home_goals_avg),3)],
    "Home Goals conceded by Liverpool":[int(liverpool_total_conceded),len(liverpool_df),round(float(liverpool_conceded_avg),3)],
    "Away Goals scored by Leicester": [int(leicester_total_away_goals),len(Leicester_df),float(leicester_away_goals_avg)],
    "Away Goals coceded by Leicester":[int(leicester_total_conceded),len(Leicester_df),round(float(leicester_conceded_avg),3)]}

dataframe = pd.DataFrame(compiled_data,index=["Total","Matches","Average"])

#CALCULATE TEAM RELATIVE STRENGTHS
liverpool_attack_strength = liverpool_home_goals_avg / home_average_goals
liverpool_defense_strength = liverpool_conceded_avg / Away_average_goals

leicester_attack_strength = leicester_away_goals_avg / Away_average_goals
leicester_defense_stregth = leicester_conceded_avg/home_average_goals

#CALCULATE EXPECTED GOALS
liverpool_xG = float(liverpool_attack_strength) * float(liverpool_defense_strength) * float(home_average_goals)
leicester_xG = float(leicester_attack_strength )*float(leicester_defense_stregth )* float(Away_average_goals)


#DEFINE FUNCTIONS TO CALCULATE GOAL PROBABILITIES
def factorial(num):
    tmp = 1
    for i in range (num+1):
        if i !=0:
            tmp *= i
    return tmp

def poisson(lambda_):
    result =[]
    for i in range (6):
        temp = pow(lambda_,i)/ factorial(i) * math.exp(-lambda_)
        result.append(temp * 100 )
    return np.array(result)

liverpool_goal_probabilities_= np.round(poisson(liverpool_xG),3)
leicester_goal_probabilities = np.round(poisson(leicester_xG),3)


#PLOT GOAL PROBABILITIES
X= [0,1,2,3,4,5]
fig,ax = plt.subplots(1,1,figsize=(8,6) )
ax.plot(X,liverpool_goal_probabilities_,'bo',ms =7)
plt.xlabel("Liverpool goals",fontsize =16)
plt.ylabel("Probabilities",fontsize =16)
plt.title("goal probability Vs goals",fontsize =18)
ax.vlines(X,0,liverpool_goal_probabilities_,colors="g",lw = 5,alpha =0.5)

for x,y in enumerate (liverpool_goal_probabilities_):
    ax.text(x,y,str(float(y)),color = "red",fontweight = "bold")
plt.show()


X = [0,1,2,3,4,5]
fig,ax = plt.subplots(1,1,figsize=(8,6) )
ax.plot(X,leicester_goal_probabilities,'bo',ms =7)
plt.xlabel("Leicester goals",fontsize =16)
plt.ylabel("Probabilities",fontsize =16)
plt.title("goal probability Vs goals",fontsize =18)
ax.vlines(X,0,leicester_goal_probabilities,colors="g",lw = 5,alpha =0.5)

for x,y in enumerate (leicester_goal_probabilities):
    ax.text(x,y,str(y),color = "red",fontweight = "bold")
plt.show()

