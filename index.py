import pickle
import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('https://images.unsplash.com/photo-1474487548417-781cb71495f3?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8M3x8dHJhaW58ZW58MHx8MHx8&auto=format&fit=crop&w=500&q=60');
    background-size: cover;
}
[data-testid="stSidebar"] {
    background-color: rgba(0,0,0,0.0);
}
h1{
    color: indianred;
}
table{
    background-color: #00425A;
    text-align: center;
}

</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)
st.title("Railway Route Optimization System")
with open('nodes.pkl', 'rb') as c:
    nod = pickle.load(c)
with open('nearstation.pkl', 'rb') as c:
    nearstation = pickle.load(c)
# print no of station and trains
st.header("Number Of Stations: ")
st.write(nod.number_of_nodes())
st.header("Number Of Trains: ")
st.write(nod.number_of_edges())

# listing busiest train
st.header("Busiest Railway Stations ")
stations = st.slider('Enter The No Of Stations Required', 0, 130, 25)
if st.button('Find Stations'):
    l = list(nod.degree(list(nod.nodes())))
    l.sort(key=lambda x: x[1], reverse=True)
    # top 10 nodes with highest degree (stations with most number of trains)
    busy=l[:stations]
    bstation = pd.DataFrame(busy, columns=['Station', 'No Of Trains'])
    st.table(bstation)

# Centrality Measure Calculation
G2 = nx.Graph(nod)
st.header("Centrality Measure Calculation")
centrality = st.selectbox('Select Source Station', ('Degree Centrality',
                          'Closeness Centrality', 'Betweenness Centrality', 'Eigenvector Centrality'))
if st.button('Calculate'):
    if centrality == 'Degree Centrality':
        st.write("Degree Centrality: ", nx.degree_centrality(nod))
    elif centrality == 'Closeness Centrality':
        st.write("Closeness Centrality: ", nx.closeness_centrality(nod))
    elif centrality == 'Betweenness Centrality':
        st.write("Betweenness Centrality: ", nx.betweenness_centrality(nod))
    elif centrality == 'Eigenvector Centrality':
        st.write("Eigenvector Centrality: ", nx.eigenvector_centrality(G2))

# Shortest Path Calculation
st.header("Shortest Path Calculation For Train Route")
with open('station.pkl', 'rb') as f:
    mynewlist = pickle.load(f)
import pickle
with open('station_name.pkl', 'rb') as f:
    stationname = pickle.load(f)
option1 = st.selectbox('Select Source Station', stationname.values())
option2 = st.selectbox('Select Destination Station', stationname.values())

if st.button('Find Route'):
    # route()
    st.write("Route Found")
    st.write("Route is:")
    p = nx.shortest_path(nod, source=[i for i in stationname if stationname[i]==option1][0],
                         target=[i for i in stationname if stationname[i]==option2][0], weight="distance")
    q = nx.shortest_path_length(
        nod, source=[i for i in stationname if stationname[i]==option1][0],target=[i for i in stationname if stationname[i]==option2][0], weight="distance")
    #Convert List To Table And Display
    temp=[]
    for z in p:
        temp.append(stationname[z])
    shrt_path = pd.DataFrame(temp)
    st.table(shrt_path)
    st.write('Distance travel is: ', q, 'km')

# df = pd.DataFrame([22.5958, 88.2636],
#     columns=['lat', 'lon'])

# # st.map(df,3)
# st.map()

# Clustering Coefficient Calculation
G2 = nx.Graph(nod)
st.header("Clustering Coefficient Calculation")
if st.button('Calculate Clustering Coefficient'):
    st.write("Clustering Coefficient: ", nx.average_clustering(G2))

# Bridges Calculation
st.header("Bridges Calculation")
if st.button('Calculate Bridges'):
    st.write("Bridges: ", list(nx.bridges(G2, root='MAS')))
    st.write("Number of Bridges: ", len(list(nx.bridges(G2, root='MAS'))))

# Articulation Points Calculation
st.header("Articulation Points Calculation")
if st.button('Calculate Articulation Points'):
    st.write("Articulation Points: ", list(nx.articulation_points(G2)))
    st.write("Number of Articulation Points: ",
             len(list(nx.articulation_points(G2))))


# Clustering
st.header("Clustering")
zoneselect = st.selectbox('Select Zone', ('North', 'South', 'East', 'West'))
if zoneselect == 'North':
    a="NDLS"
elif zoneselect == 'South':
    a="MAS"
elif zoneselect == 'East':
    a="HWH"
elif zoneselect == 'West':
    a="BCT"
st.write("Zone Main Station Is: ", a)
distance_possible = st.slider('Choose Max Distance:', 40, 600, 120)
if st.button('Calculate Clustering'):
    P = []
    for s in nod.edges(a):
        # print(s[1])
        if ((nx.shortest_path_length(nod, source=s[0], target=s[1], weight="distance")) < distance_possible) and (s[1] not in P):
            P.append(s[1])
    # P.sort
    x = list(nod.degree(list(P)))
    x.sort(key=lambda x: x[1], reverse=True)
    # print(x)
    dict2 = {}
    for i in x:
        dict2[i[0]] = nx.shortest_path_length(nod, source='HWH', target=i[0], weight="distance")
    st.write("Stations in Zone With Most No Of Train Stoppage: ")
    #Convert List To Table And Display
    df = pd.DataFrame(x, columns=['Station', 'No Of Train Stoppage'])
    st.table(df)
    dict3 = sorted(dict2.items(), key=lambda x:x[1])
    st.write("Stations in Zone With Shortest Distance From Main Station: ")
    #Convvert Dictionary To Table And Display
    df = pd.DataFrame(dict3, columns=['Station', 'Distance From Main Station'])
    st.table(df)


#Efficiency Calculation
st.header("Efficiency Calculation")
if st.button('Calculate Global Efficiency'):
    st.write("Efficiency: ", nx.global_efficiency(G2))

G0 = nx.Graph(nod)
su1 = st.selectbox('Select Source Airport:', nod.nodes)
des1 = st.selectbox('Select Destination1 Airport:', nod.nodes)
des2 = st.selectbox('Select Destination2 Airport:', nod.nodes)
if st.button('Calculate Efficiency'):
    st.write("Efficiency: ", nx.efficiency(G0, su1, des1))
    st.write("Efficiency: ", nx.efficiency(G0, su1, des2))
# efficiency = nx.efficiency(G0, "ATL", "YUM")

#Station withing a distance from a particular airport
st.header("Find Stations Nearer From A Particular Station")
option8 = st.selectbox('Select Station',stationname.values())
dist = st.slider('Enter The No Of Stations', 0, 20, 5)
op=st.radio("By distance or time", ("distance","time"))
if st.button('Find Stations Nearer:'):
    # route()
    st.write("Stations Found")
    st.write("Stations are:")
    n=nearstation[[i for i in stationname if stationname[i]==option8][0]]
    l=[]
    for idx, x in enumerate(nearstation):
        try:
            l.append((x, int(n[idx][0 if op=="distance" else 1])))
        except:
            pass
    l.sort(key=lambda x: x[1], reverse=False)
    o=l[0:dist]
    d={}
    for i in o:
        d[i[0]]=i[1]
    state_station = pd.DataFrame.from_dict(d, orient='index', columns=['Distance' if op=="distance" else "Time"])
    st.table(state_station)
    #convert n to dictionary
    # n=n.to_dict()
    # blank={}
    # for i in n:
    #     blank[i]=int(n[i][0])

