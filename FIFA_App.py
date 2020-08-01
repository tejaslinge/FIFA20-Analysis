
import string
import pandas as pd
import numpy as np
import streamlit as st 
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from PIL import Image

st.write('*By:\nTejas Linge & Saurav Himmatrao Chavan*')

###########################################################################################################
pd.set_option('display.max_columns', 150)
image = Image.open('fifa_cover.jpeg')

###########################################################################################################
st.title('Some Insights on FIFA-20 ⚽')
st.markdown('''## This application is a Streamlit dashboard which can be used to visualize some insights of FIFA-20 ⚽ ''')
st.image(image, caption = 'FIFA-20 Cover', use_column_width = True)

###########################################################################################################
@st.cache(persist = True)
def load_data():

    fifa = pd.read_csv(r'players_20.csv')
    fifa.set_index('short_name', inplace = True)
    
    defense_pos = np.array(['CB','LB','RB'])
    defenders = fifa[fifa['player_positions'].isin(i for i in defense_pos)]
    defense_attributes = defenders[['overall', 'potential', 'defending', 'physic', 'pace', 'passing', 'dribbling', 'attacking_heading_accuracy', 'attacking_short_passing', 'skill_long_passing', 'skill_ball_control', 'movement_sprint_speed', 'movement_acceleration', 'movement_reactions', 'power_shot_power', 'power_jumping', 'power_stamina', 'power_strength', 'power_long_shots', 'defending_marking', 'defending_standing_tackle', 'defending_sliding_tackle',]]
    defense_attributes= defense_attributes.dropna()
    defense_attributes = defense_attributes.corr()

    gk_attributes = fifa[['overall', 'potential', 'gk_diving', 'gk_handling', 'gk_speed', 'gk_reflexes', 'gk_kicking', 'gk_positioning', 'goalkeeping_diving', 'goalkeeping_handling', 'goalkeeping_kicking', 'goalkeeping_positioning', 'goalkeeping_reflexes']]
    gk_attributes = gk_attributes.dropna()    
    gk_attributes = gk_attributes.corr()
    
    attack_pos = np.array(['LS','RS','ST','CF','CAM','RM','LM','RW','LW','LAM','RAM'])
    attackers = fifa[fifa['player_positions'].isin(i for i in attack_pos)]
    attack = attackers[['overall', 'potential', 'skill_moves', 'pace','shooting', 'passing', 'dribbling', 'physic',
                   'attacking_crossing', 'attacking_finishing', 'attacking_heading_accuracy', 'attacking_short_passing',
                   'attacking_volleys', 'skill_dribbling', 'skill_curve', 'skill_fk_accuracy', 'skill_long_passing',
                   'skill_ball_control', 'movement_acceleration', 'movement_sprint_speed', 'movement_agility',
                   'movement_reactions', 'movement_balance', 'power_shot_power', 'power_jumping', 'power_stamina',
                   'power_strength', 'power_long_shots']]
    attack = attack.dropna()
    attack_corr = attack.corr()
    
    fifa = fifa[['long_name', 'age', 'club', 'nationality', 'overall', 'potential', 'value_eur',
                'wage_eur', 'player_positions', 'preferred_foot', 'international_reputation', 'weak_foot', 'skill_moves', 'work_rate', 'body_type',
                'release_clause_eur', 'team_position', 'team_jersey_number', 'nation_position', 'nation_jersey_number', 'pace', 'shooting', 'passing', 'dribbling', 'defending',
                'physic', 'attacking_crossing', 'attacking_finishing', 'attacking_heading_accuracy', 'attacking_short_passing',
                'attacking_volleys', 'skill_dribbling', 'skill_curve', 'skill_fk_accuracy', 'skill_long_passing', 'skill_ball_control',
                'movement_acceleration', 'movement_sprint_speed', 'movement_agility', 'movement_reactions', 'movement_balance', 'power_shot_power', 'power_jumping',
                'power_stamina', 'power_strength', 'power_long_shots', 'mentality_aggression', 'mentality_interceptions', 'mentality_positioning', 'mentality_vision', 'mentality_penalties',
                'mentality_composure', 'defending_marking', 'defending_standing_tackle', 'defending_sliding_tackle', 'goalkeeping_handling']]

    fifa.columns = ['Full_Name', 'Age', 'Club', 'Nationality', 'Overall', 'Potential', 'Value(Euro)', 'Wage(Euro)', 'Position(s)', 'Foot', 'International Reputation', 'Weak Foot', 'Skill Moves', 'Work Rate', 'Body Type', 'Release Clause', 'Team Pos', 'Jersey No.', 'National Pos', 'National Jersey No.',
                    'Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending', 'Physic'] + [str(i) for i in fifa.columns[26:]] 

    fifa.fillna('-', inplace = True)
    fifa['Club'].fillna('No Club', inplace = True)
    fifa['Position(s)'].fillna('unknown', inplace = True)
    fifa['Work Rate'].fillna('Medium/ Medium', inplace = True)
    fifa['Foot'].fillna('Right', inplace = True)
    fifa['International Reputation'].fillna('No Rep', inplace = True)

    return fifa, gk_attributes, defense_attributes, attack_corr

data = load_data()
data_all = data[0]
GK_ATT = data[1]
DEF_ATT = data[2]
ATT_ATT = data[3]

###########################################################################################################
st.markdown('## Scatter Plot of All Players in FIFA-20')
def all_players():
    fig = go.Figure(data=go.Scatter(
        x = data_all['Overall'],
        y = data_all['Value(Euro)'],
        mode='markers',
        marker=dict(
            size=16,
            color=data_all['Age'], #set color equal to a variable
            colorscale='Plasma', # one of plotly colorscales
            showscale=True
        ),
        text= data_all.index,
    ))

    fig.update_layout(title='Styled Scatter Plot (colored by Age) year 2020 - Overall Rating vs Value in Euros',
                    xaxis_title='Overall Rating',
                    yaxis_title='Value in Euros',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Cambria, monospace', size=12, color='#000000'))
    return fig

players = all_players()
st.plotly_chart(players, use_container_width=True)

st.write('This is a scatter plot of all the players in FIFA-20.')

if st.checkbox("Show Players' Data", False):
    st.latex("Players' Data")
    number0 = st.slider('How many Players do you want to display?', 1, 18278)
    st.write(data_all.iloc[0 : number0, :])

###########################################################################################################
#A list of all colors in Plotly Charts (to be used later)
plotly_colors = np.array(['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure',
                'beige', 'bisque', 'black', 'blanchedalmond', 'blue',
                'blueviolet', 'brown', 'burlywood', 'cadetblue',
                'chartreuse', 'chocolate', 'coral', 'cornflowerblue',
                'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan',
                'darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen',
                'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange',
                'darkorchid', 'darkred', 'darksalmon', 'darkseagreen',
                'darkslateblue', 'darkslategray', 'darkslategrey',
                'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue',
                'dimgray', 'dimgrey', 'dodgerblue', 'firebrick',
                'forestgreen', 'fuchsia', 'gainsboro',
                'gold', 'goldenrod', 'gray', 'grey', 'green',
                'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo',
                'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen',
                'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan',
                'lightgoldenrodyellow', 'lightgray', 'lightgrey',
                'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen',
                'lightskyblue', 'lightslategray', 'lightslategrey',
                'lightsteelblue', 'lightyellow', 'lime', 'limegreen',
                'linen', 'magenta', 'maroon', 'mediumaquamarine',
                'mediumblue', 'mediumorchid', 'mediumpurple',
                'mediumseagreen', 'mediumslateblue', 'mediumspringgreen',
                'mediumturquoise', 'mediumvioletred', 'midnightblue',
                'mintcream', 'mistyrose', 'moccasin', 'navy',
                'oldlace', 'olive', 'olivedrab', 'orange', 'orangered',
                'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise',
                'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink',
                'plum', 'powderblue', 'purple', 'red', 'rosybrown',
                'royalblue', 'saddlebrown', 'salmon', 'sandybrown',
                'seagreen', 'seashell', 'sienna', 'skyblue',
                'slateblue', 'slategray', 'springgreen',
                'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise',
                'violet', 'wheat', 'yellow',
                'yellowgreen'])
plot_colors_select = plotly_colors.shape[0]

###########################################################################################################
st.write(''' ## Player Comparison''')
st.write(''' To compare two players check the box below and select name of Clubs, data to be compared and name of the Players from the side bar ''')

@st.cache(persist = True)
@st.cache(suppress_st_warning=True)
@st.cache(allow_output_mutation=True)
def comparison_data():
    fifa_org = pd.read_csv('players_20.csv')

    to_drop = ['sofifa_id','player_url', 'long_name', 'body_type', 'real_face', 'player_tags', 'team_jersey_number', 'loaned_from', 'joined', 'contract_valid_until','nation_jersey_number']
    fifa_org.drop(columns = to_drop, inplace=True)

    def rena(a):                       # function to rename columns
        if a=='club':
            return 'Clubs'
        if a=='short_name':
            return 'Name'
        if len(a)==2 or len(a)==3 and a!='age':
            a = a.upper()
        else:
            a = a.replace('_',' ')
            a = string.capwords(a)
        return a
        
    fifa_org.rename(columns = lambda x: rena(x), inplace=True)
    fifa_org.rename(columns = {'Height Cm':'Height(cm)','Weight Kg':'Weight(kg)','Value Eur':'Value(Euro)', 'Wage Eur':'Wage(Euro)'}, inplace = True)
    
    fifa_org.index+=1
    return fifa_org

fifa_org = comparison_data()

attr = ["Age","Height(cm)","Weight(kg)","Overall","Potential","Value(Euro)","Wage(Euro)","International Reputation","Weak Foot",
  "Skill Moves","Release Clause Eur","Pace","Shooting","Passing","Dribbling","Defending","Physic","Gk Diving","Gk Handling","Gk Kicking",
  "Gk Reflexes","Gk Speed","Gk Positioning","Player Traits","Attacking Crossing","Attacking Finishing","Attacking Heading Accuracy",         "Attacking Short Passing","Attacking Volleys","Skill Dribbling","Skill Curve","Skill Fk Accuracy","Skill Long Passing",
  "Skill Ball Control","Movement Acceleration","Movement Sprint Speed","Movement Agility","Movement Reactions","Movement Balance",
  "Power Shot Power","Power Jumping","Power Stamina","Power Strength","Power Long Shots","Mentality Aggression","Mentality Interceptions",
  "Mentality Positioning","Mentality Vision","Mentality Penalties","Mentality Composure","Defending Marking","Defending Standing Tackle",
  "Defending Sliding Tackle","Goalkeeping Diving","Goalkeeping Handling","Goalkeeping Kicking","Goalkeeping Positioning",
  "Goalkeeping Reflexes","LS","ST","RS","LW","LF","CF","RF","RW","LAM","CAM","RAM","LM","LCM","CM","RCM","RM","LWB","LDM","CDM","RDM",
  "RWB","LB","LCB","CB","RCB","RB"]

if st.checkbox("Check the box to compare Players"):
    
    teams = np.array(st.sidebar.multiselect("Select the name of Club:", fifa_org['Clubs'].unique()))
    
    variables = np.array(st.sidebar.multiselect("Select data to compare:", attr))
    
    selected_clubs = fifa_org[fifa_org['Clubs'].isin(teams)][variables]#.set_index('Name', inplace = True)
    selected_clubs['Name'] = fifa_org['Name']
    selected_clubs.set_index('Name', inplace = True)    
    selected_players = st.sidebar.multiselect('Select the Players to be compared:', selected_clubs.index)#.Name.unique())#.loc[:, 'Name'])#..unique())#, two_clubs_data.Name.unique())
    
    is_check = st.checkbox("Check the box to display Players of selected Clubs")
    
    if is_check:
        a = [teams, variables, selected_clubs]
        
        if not a:
            st.write('''### Please select required fields!''')
        else:
            st.write(selected_clubs)

        if st.button("Click to see comparison Graphically"):
            if not a:
                st.write('''### Please select required fields!''')
            else:                
                graphToPlot = pd.DataFrame(selected_clubs.loc[selected_players, :])
                values = graphToPlot.values[:, :]
                #st.write(values)
                @st.cache(persist = True)
                def Comp(ALL, COLS, n):
                    SamePlot = make_subplots(subplot_titles = variables[n:])
                    SamePlot.add_trace(go.Bar(x = ALL.index, y = ALL.values[:, n]))                                    
                    return SamePlot
                for n in range(0, variables.shape[0]):
                    FIGURE = Comp(graphToPlot, values, n)
                    FIGURE.update_traces(marker_color=plotly_colors[np.random.randint(0, plot_colors_select)])
                    st.plotly_chart(FIGURE)

##################################################
def gk_attributes():
    plt.figure(figsize = (28,12))
    sns.set_context('poster',font_scale=1)
    sns.heatmap(GK_ATT , annot = True).set_title('Correlation between GK Attributes')

st.markdown('## Correlation between Different GK 🧤 Attributes')
GK_ATTR = gk_attributes()
st.pyplot()

if st.checkbox('Show GK Attributes Correlation Table', False):
    st.latex('GK  Attributes  Correlation  Table')
    st.write(GK_ATT)    

st.write('''Here we can see how different goal-keeping attributes may be related to each other and how they may contribute to the overall attributes of a GK.
            For example, correlation between GK Handling and Overall attributes is 0.93 and that of Speed and Overall attributes is 0.48.
            Thus, we can infer from this data that speed is not that of an important factor when it comes to judging the quality of a GK but handling is.
            \nNOTE : Correlation doesn't always imply causation i.e it is not always necessary that two attributes who have a correlation close to 1 are always related to each other nor that they are not related to each other if correlation is close to 0. There may be other factors 
                   involved for two properties to affect each other.''')

###########################################################################################################
def defense_attributes():
    plt.figure(figsize = (28,12))
    sns.set_context('poster',font_scale=1)
    sns.heatmap(DEF_ATT , annot = True).set_title('Correlation between Def Attributes')

st.markdown('## Correlation between Different Defense 🛡️ Attributes')
DEF_ATTR = defense_attributes()
st.pyplot()

if st.checkbox('Show Defender Attributes Correlation Table', False):
    st.latex('Defense Attributes Correlation Table')
    st.write(DEF_ATT)

st.write('''Here we can see how different defense attributes may be related to each other and how they may contribute to the overall attributes of a Defender.
            \nNOTE : It is not always necessary that 2 attributes who have a correlation close to 1 are always related to each other. There may be other factors 
                   involved for two properties to affect each other.''')

###########################################################################################################
def attack_attributes():
    fig = go.Figure(data=go.Heatmap(
                   z=ATT_ATT,
                   x=ATT_ATT.columns,
                   y=ATT_ATT.columns, colorscale='Blues',
                   hoverongaps = True))
    return fig
    
st.markdown('## Correlation between Different Attacking ⚽ Attributes')
ATT_ATT_Heatmap = attack_attributes()
st.plotly_chart(ATT_ATT_Heatmap, use_container_width=True)

if st.checkbox('Show Attack Attributes Correlation Table', False):
    st.latex('Attacking Attributes Correlation Table')
    st.write(ATT_ATT)
st.write('''Here we can see how different attacking attributes may be related to each other and how they may contribute to the overall attributes of a Attackers.''')
    
###########################################################################################################    
st.markdown('## Total Count of Left v/s Right Footed Players')
sns.set(style = 'darkgrid')
plt.figure(figsize = (35,15))
sns.set_context('poster',font_scale=1.5)
sns.countplot(x = 'Foot', data = data_all, palette = 'coolwarm').set_title('Left v/s Right')
st.pyplot()
st.write('From the above countplot, we can see the total number of Left and Right footed players.')
###########################################################################################################
st.markdown('## Top Clubs by Total Player Value (Euro 💶)')           
def top20_clubs():
    TopClubsInVal = data_all[['Club', 'Value(Euro)']]
    #TopClubsInVal = TopClubsInVal.set_index(n for n in range(TopClubsInVal.shape[0]))
    TopClubsInVal = pd.DataFrame(TopClubsInVal.groupby('Club')['Value(Euro)'].sum()).sort_values('Value(Euro)', ascending = False)
    Top20ClubsInVal = pd.DataFrame(TopClubsInVal.groupby('Club')['Value(Euro)'].sum()).sort_values('Value(Euro)', ascending = False).head(20)

    fig = go.Figure(
            data = [go.Bar(y = Top20ClubsInVal['Value(Euro)'],
                        x = Top20ClubsInVal.index)],
            layout_title_text = "Top 20 Clubs by Total Player Value(Euro 💶) of Fifa 20"
            
    )
    fig.update_traces(marker_color='green')
    return fig, TopClubsInVal

ClubsTop20_FIG = top20_clubs()[0]
ClubsTABLE = top20_clubs()[1]
 
st.plotly_chart(ClubsTop20_FIG, use_container_width=True)

if st.checkbox('Top Clubs by Value (Euro 💶) Table', False):
    st.latex('Table - Clubs by Value (Euro)')
    number1 = st.slider('How many Clubs do you want to display?', 1, 698)
    st.write(ClubsTABLE.iloc[0 : number1, :])

###########################################################################################################
def MVPs():
    most_valued = data_all[['Value(Euro)', 'Club', 'Nationality']]
    most_valued = most_valued.sort_values('Value(Euro)', ascending = False)
    most_valued30 = most_valued.sort_values('Value(Euro)', ascending = False).head(30)
    fig = go.Figure(
            data = [go.Bar(y = most_valued30['Value(Euro)'],
                        x = most_valued30.index)],
                        
            
            layout_title_text = '30 Highest Valued Players of Fifa 20'
    )
    return fig, most_valued

most_valued_playersFIG = MVPs()[0]
most_valued_playersALL = MVPs()[1]
st.markdown('## Highest Valued Players of FIFA-20 (Euro 💶)')
st.plotly_chart(most_valued_playersFIG)

if st.checkbox('Players by Value (Euro 💶)', False):
    st.latex('Table - Players by Value')
    number2 = st.slider('How many Players (by Value) do you want to display?', 1, most_valued_playersALL.shape[0])
    st.write(most_valued_playersALL.iloc[0 : number2, :])


###########################################################################################################
def top_ratings():
    top_ratings = data_all[['Club', 'Overall', 'Potential', 'Value(Euro)']]
    top_ratings = top_ratings.sort_values('Overall', ascending = False)
    top30_ratings = top_ratings.head(30)

    fig = go.Figure(
            data = [go.Bar(y = top30_ratings['Overall'],
                        x = top30_ratings.index)],
            layout_title_text = 'Top 30 Rated Players of Fifa 20'
    )
    fig.update_traces(marker_color='#00A')
    return fig, top_ratings
top_ratedFIG = top_ratings()[0]
top_ratedALL = top_ratings()[1]


st.markdown('## Highest Rated Players of FIFA-20')
st.plotly_chart(top_ratedFIG)
if st.checkbox('Players by Ratings', False):
    st.latex('Table - Players by Ratings')
    number3 = st.slider('How many Players (by Ratings) do you want to display?', 1, top_ratedALL.shape[0])
    st.write(top_ratedALL.iloc[0 : number3, :])

###########################################################################################################
st.markdown('## Top 30 Free-Kick Takers')
def fk():
    best_fk = data_all[['skill_fk_accuracy']].sort_values('skill_fk_accuracy', ascending = False).head(30)

    x = best_fk.skill_fk_accuracy
    plt.figure(figsize=(12,8))
    plt.style.use('seaborn-paper')
    sns.set_context('poster',font_scale=.5)

    ax = sns.barplot(x = x, y = best_fk.index, data = best_fk)
    ax.set_xlabel(xlabel = "Free-Kick Attributes", fontsize = 16)
    ax.set_ylabel(ylabel = 'Player Name(s)', fontsize = 16)
    ax.set_title(label = "Bar Plot of Best Free-Kick Takers", fontsize = 20)
    return ax

free_kick = fk()
st.pyplot()

###########################################################################################################
def bestgk():
    GK = data_all[data_all['Position(s)'] == 'GK']
    GK = GK[['Club', 'Nationality', 'Overall', 'Potential']]
    GK = GK.sort_values('Overall', ascending = False).head(20)

    fig = go.Figure(
            data = [go.Bar(y = GK['Overall'],
                        x = GK.index)],
            layout_title_text = "Top Rated GK's 🧤 of Fifa 20"
    )
    fig.update_traces(marker_color='goldenrod')
    return fig

BESTGK = bestgk()
st.markdown("## Top 20 GK's 🧤 of FIFA-20")
st.plotly_chart(BESTGK)

top_clubs = ['Real Madrid', 'Manchester City', 'Tottenham Hotspur', 'Napoli',
             'FC Barcelona', 'Juventus', 'Paris Saint-Germain', 'Liverpool',
             'Manchester United', 'Chelsea', 'Atlético Madrid', 'Arsenal',
             'Borussia Dortmund', 'FC Bayern MÃ¼nchen', 'West Ham United', 'FC Schalke 04',
             'Roma', 'Leicester City', 'Inter', 'Milan']
condition_top20 = ((data_all['Potential'] - data_all['Overall']) >= 15) & (data_all['Potential'] >= 80) & (data_all['Club'].isin(top_clubs))  & (data_all['Age'] <= 20) 
young_players_top20 = data_all[condition_top20].sort_values('Potential', ascending = False)

young_clubs_top20 = young_players_top20.Club
young_clubs_top20 = pd.DataFrame(young_clubs_top20.value_counts())

condition_all = ((data_all['Potential'] - data_all['Overall']) >= 15) & (data_all['Potential'] >= 80)   & (data_all['Age'] <= 20) 
young_players_all = data_all[condition_all].sort_values('Potential', ascending = False)

young_clubs_all = young_players_all.Club
young_clubs_all = pd.DataFrame(young_clubs_all.value_counts())

###########################################################################################################
def young():
    fig = make_subplots(1, 2, specs=[[{'type':'domain'}, {'type':'domain'}]],
                        subplot_titles=['From Top 20 Clubs', 'From All Clubs'])
    fig.add_trace(go.Pie(labels=young_clubs_top20.index, values= young_clubs_top20.Club, scalegroup='one',
                        name="From Top 20 Clubs"), 1, 1)
    fig.add_trace(go.Pie(labels=young_clubs_all.head(20).index, values=young_clubs_all.head(20).Club, scalegroup='one',
                        name="From All Clubs"), 1, 2)

    #fig.update_layout(title_text='Count of Promising Young Players')
    return fig
Young = young()


st.markdown('### Count of Most Promising Young Players From Top Clubs and All over the World')
st.plotly_chart(Young)
st.write('''AS Monaco (France) has the highest number of promising players (9) and FC Barcelona (Spain) has the highest number of promising players (8) among Top-20 Clubs.\
          There are 59 Players under 20 in the Top 20 Clubs and 321 total player among all clubs who have high room of improvement 
          and the potential to become some of the Top players in the World.''')

if st.checkbox('Show All Promising Players from Top 20 Clubs', False):
    st.latex('Promising Players From Top 20 Clubs')
    number5 = st.slider('How many Players (from TOP 20 Clubs) do you want to display?', 1, young_players_top20.shape[0])
    st.write(young_players_top20.iloc[0 : number5, :])

if st.checkbox('Show All Promising Players', False):
    st.latex('All Promising Players')
    number6 = st.slider('How many Players (ALL) do you want to display?', 1, young_players_all.shape[0])
    st.write(young_players_all.iloc[0 : number6, :])

###########################################################################################################
st.markdown('## Scatter Plot of all Promising Players')
def YPP(): #YoungPlayerPrice

    young_players_all_cheapest = young_players_all[['Age', 'Club', 'Nationality', 'Overall', 'Potential', 'Value(Euro)', 'Wage(Euro)', 'Position(s)']].sort_values('Value(Euro)', ascending = True) 
    #young_players_all_cheapest = young_players_all_cheapest[young_players_all_cheapest['Potential'] >= 85]

    fig = go.Figure()

    fig = go.Figure(data=go.Scatter(
        x = young_players_all_cheapest['Potential'],
        y = young_players_all_cheapest['Value(Euro)'],
        mode='markers',
        marker=dict(
            size=16,
            color=young_players_all_cheapest['Age'], #set color equal to a variable
            colorscale='Plasma', # one of plotly colorscales
            showscale=True
        ),
        text= young_players_all_cheapest.index,
    ))

    fig.update_layout(title='Potential of Promising Young Players vs Value in Euros',
                    xaxis_title='Potential',
                    yaxis_title='Value in Euros',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Cambria, monospace', size=12, color='#000000'))
    return fig, young_players_all_cheapest

YPPC = YPP()[0]
YPPC_Table = YPP()[1]

st.plotly_chart(YPPC)

if st.checkbox('Show All Promising Players by Value (Euro 💶)', False):
    st.latex('All Promising Players by Value')
    number7 = st.slider('How many Players (Cheapest first) do you want to display?', 1, YPPC_Table.shape[0])
    st.write(YPPC_Table.iloc[0 : number7, :])
    
###########################################################################################################
