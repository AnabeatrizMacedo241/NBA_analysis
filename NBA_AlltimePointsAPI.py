from selenium import webdriver
import pandas as pd
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll

def get_table(driver, n_pages):
    
    def prox_pag(): #Next page function
        p= driver.find_element_by_xpath('/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[1]/div/div/a[2]')
        p.click()
    
    def clean_df(df):
        df = df.reset_index(drop=True)
        df = df.replace('-', 0)
        df = df.rename(columns={'#':'Ranking'})
        colunas = list(df.columns)
        colunas.remove('Player')
        df[colunas] = df[colunas].apply(pd.to_numeric,axis=1)
        return df
        
        
    url = 'https://www.nba.com/stats/alltime-leaders/?SeasonType=Regular%20Season'
    driver.get(url)
    df = pd.DataFrame()
    for c in range(n_pages):
        web_element=driver.find_element_by_xpath("""/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table""")
        #print(web_element.text)
        df2 = pd.read_html(web_element.get_attribute('outerHTML'))
        df = df.append(df2)
        prox_pag()
    driver.quit()
    return clean_df(df)

def get_player(df, player_name):
    player = df.loc[(df['Player']==player_name)]
    if len(player)==0:
        raise  ExceptionPlayerName('No results for this player, check if you wrote his name correctly.')
    return(player)

def top3(df): #Top 3 points leader function
     print('First, {}: {} points'.format(df['Player'][0], df['PTS'][0]))
     print('Second, {}: {} points'.format(df['Player'][1], df['PTS'][1]))
     print('Third, {}: {} points'.format(df['Player'][2], df['PTS'][2]))

def isLebronLeader(df): #LeBron all-time leader function
    df_lebron = df.copy()
    df_lebron.set_index('Player',inplace=True)
    pts_lebron = df_lebron.loc['LeBron James', 'PTS']
    pts_first =  df_lebron['PTS'][0]
    pts_second = df_lebron['PTS'][1]
    lebron_games = playergamelog.PlayerGameLog(player_id='2544', season=SeasonAll.all)
    lebron_games_df = lebron_games.get_data_frames()[0]
    mean = lebron_games_df['PTS'].mean()
    difference_first= pts_first-pts_lebron
    difference_second =  pts_second-pts_lebron
    games_first = difference_first/mean
    games_second = difference_second/mean
    if pts_lebron>38387:
        print('Lebron is the all-time NBA points leader!')
    elif pts_lebron>36928:
        print('Lebron is the second all-time NBA points leader!')
        print('Lebron needs to score {} points in {} to surprass {}'.format(difference_first,round(games_first), df['Player'][0]))
    else:
        print('Lebron is still the third all-time NBA points leader')
        print('Lebron needs {} points in {} games to surprass {}'.format(difference_first,round(games_first),df_lebron.index[0]))
        print('Lebron needs {} points in {} games to surprass {}'.format(difference_second,round(games_second),df_lebron.index[1]))

def bestTS(df):
    ts = df['TS%'].max()
    player = df.loc[df['TS%']==ts]
    name = player.loc[player.index[0], 'Player']
    position = player.loc[player.index[0], 'Ranking']
    print(f'Best FG% is {ts}% from {name} in the {position}th place on the all-time points list.')

def bestFG(df):
    fg = df['FG%'].max()
    player = df.loc[df['FG%']==fg]
    name = player.loc[player.index[0], 'Player']
    position = player.loc[player.index[0], 'Ranking']
    print(f'Best FG% is {fg}% from {name} in the {position}th place on the all-time points list.')

def best3P(df, minimumAttempts=100):
    df_3A = df.loc[df['3PA']>minimumAttempts]
    df_3Percent = df_3A['3P%'].max()
    player = df.loc[df['3P%']==df_3Percent]
    name = player.loc[player.index[0], 'Player']
    position = player.loc[player.index[0], 'Ranking']
    print(f'Best 3P% with, at least, {minimumAttempts} attempts is {name} with a {df_3Percent}% and he is at the {position}th place on the all-time points list.')

def bestFT(df):
    ft = df['FT%'].max()
    player = df.loc[df['FT%']==ft]
    name = player.loc[player.index[0], 'Player']
    position = player.loc[player.index[0], 'Ranking']
    print(f'Best FT% is {ft}% from {name} in the {position}th place from the all-time points list.')
    
def overallStats(df, player_name): #Still a series
    player = df.loc[(df['Player']==player_name)]
    name = player.loc[player.index[0], 'Player']
    mpg = player['MIN']/player['GP']
    ppg = player['PTS']/player['GP']
    rpg = player['REB']/player['GP']
    apg = player['AST']/player['GP']
    spg = player['STL']/player['GP']
    topg = player['TOV']/player['GP']
    if len(player)==0:
        raise  ExceptionPlayerName('No results for this player, check if you wrote his name correctly.')
    print(f'{name} stats:\nMPG:{mpg}\nPPG:{ppg}\nRPG:{rpg}\nAPG:{apg}\nSPG:{spg}\nTOPG:{topg}')
  
def overallRebounds(df, player_name): #Still a series
    player = df.loc[(df['Player']==player_name)]
    name = player.loc[player.index[0], 'Player']
    df_ovr = (player['OREB'])+(player['DREB'])
    oreb = (player['OREB']/df_ovr)*100
    dreb = (player['DREB']/df_ovr)*100
    if len(player)==0:
        raise  ExceptionPlayerName('No results for this player, check if you wrote his name correctly.')
    print(f'The overall reobunds of {name}:\n{round(oreb)}% offensive\n{round(dreb)}% defensive.')
    
def tovPercent(df, player_name): #Turnover percentage is an estimate of turnovers per 100 plays(Still a series)
    player = df.loc[(df['Player']==player_name)]
    name = player.loc[player.index[0], 'Player']
    tov = 100*(player['TOV']/(player['FGA']+0.44*(player['FTA']+player['TOV'])))
    if len(player)==0:
        raise  ExceptionPlayerName('No results for this player, check if you wrote his name correctly.')
    print(f'The TOV% of {name} is {tov}%.')
    
def mostRebounds(df):
    mostREB = df['REB'].max()
    player = df.loc[df['REB']==mostREB]
    name = player.loc[player.index[0], 'Player']
    position = player.loc[player.index[0], 'Ranking']
    print(f'The player with mosts rebounds is {name} with {mostREB} rebounds at the {position}th in the all-time points list')

def mostAssists(df):
    mostAST = df['AST'].max()
    player = df.loc[df['AST']==mostAST]
    name = player.loc[player.index[0], 'Player']
    position = player.loc[player.index[0], 'Ranking']
    print(f'The player with mosts assists is {name} with {mostAST} assists at the {position}th in the all-time points list')

def mostSteals(df):
    mostSTL = df['STL'].max()
    player = df.loc[df['STL']==mostSTL]
    name = player.loc[player.index[0], 'Player']
    position = player.loc[player.index[0], 'Ranking']
    print(f'The player with most steals is {name} with {mostSTL} steals at the {position}th in the all-time points list')

def mostTurnovers(df):
    mostTOV = df['TOV'].max()
    player = df.loc[df['TOV']==mostTOV]
    name = player.loc[player.index[0], 'Player']
    position = player.loc[player.index[0], 'Ranking']
    print(f'The player with most turnovers is {name} with {mostTOV} turnovers at the {position}th in the all-time points list')
     
def bestOffensivePlayer(df):
    df['OFE'] = ((df['PTS']+df['AST']+df['BLK']+df['REB']-(df['FGA']-df['FGM'])-(df['FTA']-df['FTM'])-df['TOV'])/df['GP'])
    higherOFE = df['OFE'].max()
    player = df.loc[df['OFE']==higherOFE]
    name = player.loc[player.index[0], 'Player']
    position = player.loc[player.index[0], 'Ranking']
    print(f'Best offensive player efficiency is {name} with a {higherOFE} and he is at the {position}th place on the all-time points list.')
    
def bestDefensivePlayer(df): #40 is an outstanding performance, 10 is an average performanc
    df['DFE'] = ((df['STL']+df['BLK']+df['REB'])/df['GP'])
    higherDFE = df['DFE'].max()
    player = df.loc[df['DFE']==higherDFE]
    name = player.loc[player.index[0], 'Player']
    position = player.loc[player.index[0], 'Ranking']
    print(f'Best defense player efficiency is {name} with a {higherDFE} and he is at the {position}th place on the all-time points list.')
    
class ExceptionPlayerName(Exception):
    pass

tabela = get_table(webdriver.Chrome(),1)
#best_3P(tabela, 100)
