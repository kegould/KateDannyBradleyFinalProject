import json
import sqlite3
import os
import requests

#This file is responsible for our Sport Radar API and creating the table NBA_Stats
#Calling table() will get this function to work, and limits the data to 25 items each time it runs

def stats(year):
    player_names_1=[]
    player_stats=[]
    player_id=0
    url='https://api.sportradar.us/nba/trial/v7/en/seasons/{}/REG/leaders.json?api_key=jnxztd6mxbwm79hjxt6bm93q'.format(str(year))
    data=requests.get(url).text
    new_data=json.loads(data)
    y=new_data.get('categories')
    for val in range(44):
        data=y[val]['ranks']
        for x in data:
            player_name=x['player']['full_name']
            if player_name not in player_names_1:
                player_names_1.append(player_name)
                team=x['teams']
                for t in team:
                    team_name=t['name']
                avg_pts=x['average']['points']
                player_id+=1
                stat=(player_id,player_name,team_name,avg_pts) 
                player_stats.append(stat)    
    return player_stats      

def table():
    path = os.path.dirname(os.path.abspath(__file__))
    db = os.path.join(path, 'final.db')
    conn= sqlite3.connect(db)
    cur = conn.cursor() 
    cur.execute("CREATE TABLE IF NOT EXISTS NBA_Stats (Player_ID INTEGER, Player TEXT, Team TEXT, PPG INTEGER)")
    ppg=stats(2018)
    count=0
    cur.execute("SELECT Player_ID FROM NBA_Stats")
    player_id=cur.fetchall()
    new_id = [i[j] for i in player_id for j in range(len(i))]


    for x in ppg:
        if count<=24:
            if x[0] not in new_id:
                cur.execute("INSERT INTO NBA_Stats (Player_ID, Player, Team, PPG) VALUES (?, ?, ?, ?)",(x[0], x[1], x[2], x[3]))
                count+=1
            else:
                continue
    conn.commit()
table()

        
 