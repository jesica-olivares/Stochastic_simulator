import pandas as pd
import numpy as np

from scipy.interpolate import CubicSpline
from scipy.stats import norm
import random
import math

import streamlit as st
import altair as alt

import matplotlib.pyplot as plt
import seaborn as sns

from streamlit_metrics import metric, metric_row
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder

from PIL import Image

st.set_page_config(layout="wide")

# with st.form(key='my_form'):
#     with st.sidebar:
#         average_p80 =st.number_input("Average P80",min_value=35,max_value=300)
#         std_p80 =st.number_input("Standard Deviation P80",min_value=1)
#         simul_number =st.number_input("Number of Simulations",min_value=1)
#         node_number =int(st.selectbox("Number of Nodes",
#             ("3", "4", "5","6","7","8")))
#         #node_number_int=int(node_number)
#         submit_button = st.form_submit_button(label='Submit')    

with st.sidebar:
    average_p80 =st.number_input("Average P80",min_value=35,max_value=300,value=200)
    std_p80 =st.number_input("Standard Deviation P80",min_value=1,value=15)
    simul_number =st.number_input("Number of Simulations",min_value=1,value=1000,)
    node_number =int(st.selectbox("Number of Nodes",
            ("3", "4", "5","6","7","8")))
        #node_number_int=int(node_number)


#df=pd.read_csv('datos_modelo_estocastico.csv',sep=";")
d={'p80':[1,50,110,200,250,300],'Recovery':[30,70,90,90,78,39]}
df=pd.DataFrame(d)

x=df["p80"]
y=df["Recovery"]    

p80_min=df['p80'].min()
p80_max=df['p80'].max()

max_graph=round(p80_max*1.1)

f = CubicSpline(x, y, bc_type='natural')
x_new = np.linspace(0, max_graph, 100)
y_new = f(x_new)




prob=random.random()
norm.ppf(prob,loc=average_p80,scale=std_p80)
df_rand= pd.DataFrame(np.random.random(size=(simul_number, 1)), columns=['random'])
df_rand['Simulated_p80']=norm.ppf(df_rand['random'],loc=average_p80,scale=std_p80)

def check(row):
    if row['Simulated_p80']<35: 
        val=np.nan
    elif row['Simulated_p80']>300: 
        val=np.nan
    else: 
        val=row['Simulated_p80']
    return val


df_rand['Simulated_p80_check']=df_rand.apply(check, axis=1) 
df_rand["recovery"]=df_rand['Simulated_p80_check'].apply(f)

simul_recovery=df_rand[df_rand["recovery"]>0]["recovery"].mean()
simul_recovery=round(simul_recovery,2)


#add_slider =st.sidebar.slider("Fecha",value=[datetime.date(2021,1,1),datetime.date(2021,7,1)])
#age = st.slider('How old are you?', 0, 130, 25)



col11, col12, col13 = st.beta_columns((1,8  ,1))

with col12:
    st.write('')  
    st.title("Stochastic Simulator to evaluate Control Strategies in Flotation")
    st.write('')  
    st.write('')  
    st.write('')    

with col13:
    image = Image.open('FLS1.jpg')
    st.image(image, caption='FLSmidth')
    st.write('')  

node_max=node_number-1
middle_node_f=math.floor(node_max/2)
middle_node_c=math.ceil(node_max/2)
for i in range(node_number):
    j=i+1
    if i<middle_node_f:
        globals()['val_rec_%s' % j]=round(85*(1-(middle_node_f-i)/node_max))
    elif (i==middle_node_f or i==middle_node_c):
        globals()['val_rec_%s' % j]=85
    else:
        globals()['val_rec_%s' % j]=round(85*(1+(middle_node_f-i)/node_max))


for i in range(node_number):
    j=i+1
    if i<middle_node_c:
        globals()['val_p80_%s' % j]=round(120*(1-(node_max-j)/node_max))
    elif (i==middle_node_f):
        globals()['val_p80_%s' % j]=120
    else:
        globals()['val_p80_%s' % j]=round(120*(0.8*(j)/middle_node_c))


#generamos 3 columnas
col21, col22, col23, col24 = st.beta_columns((3,1,1,1))

with col23:
    i=0
    st.write('')
    for i in range(node_number):
        j=i+1
        globals()['p80%s' % j] =st.number_input(f"P80 {j}",max_value=300,value=globals()['val_p80_%s' % j])

with col24:
    
    st.write('')
    i=0
    for i in range(node_number):
        j=i+1
        globals()['rec%s' % j]  =st.number_input(f"Recovery {j}",min_value=0,max_value=100,value=globals()['val_rec_%s' % j])

data=[]
for i in range(node_number):
    j=i+1
    data.append([globals()['p80%s' % j],globals()['rec%s' % j ]])

df_test = pd.DataFrame(data,columns=("p80","Recovery"))
x=df_test["p80"]
y=df_test["Recovery"]    

p80_min=df_test['p80'].min()
p80_max=df_test['p80'].max()

max_graph=round(p80_max*1.1)

f = CubicSpline(x, y, bc_type='natural')
x_new = np.linspace(0, max_graph, 100)
y_new = f(x_new)

with col21:
    st.write('')  
    # fig1, ax = plt.subplots(figsize=(12,8))
    # plt.grid(True, axis='y',linewidth=0.2, color='gray', linestyle='-')
    # plt.plot(x_new, y_new,linewidth =0.4, color='midnightblue')
    # plt.plot(x, y, 'ro')
    # #plt.axhline(y = thr_mean, color = 'r', linestyle = '--',linewidth =0.4)
    # #fig1.text(0.7,0.4,'Average: '+str(round(thr_mean)),color='red',size=4)
    # plt.ylabel("", fontsize=3)
    # ax.tick_params(axis='both', which='major', labelsize=10,width=0.2)
    # ax.spines['top'].set_linewidth('0.3') 
    # ax.spines['right'].set_linewidth('0.3') 
    # ax.spines['bottom'].set_linewidth('0.3') 
    # ax.spines['left'].set_linewidth('0.3') 
    # st.pyplot(fig1)
    color1='#002A54'
    color2='#C94F7E'
    plt.rcParams.update({'font.size': 16})
    fig1, ax = plt.subplots(figsize=(12,8))
    ax2=ax.twinx()
    plt.grid(True, axis='y',linewidth=0.2, color='gray', linestyle='-')
    ax.fill_between(x_new, y_new,alpha=0.1,color=color1,linewidth=2)
    ax.plot(x_new, y_new,linewidth =2, color=color1, alpha=.8)
    ax.plot(x, y, 'o', color=color1)
    ax.set_ylabel("Recovery", color = color1)
    ax.set_xlabel("P80")
    #plt.axhline(y = thr_mean, color = 'r', linestyle = '--',linewidth =0.4)
    #fig1.text(0.7,0.4,'Average: '+str(round(thr_mean)),color='red',size=4)
    plt.ylabel("", fontsize=16)
    plt.xlabel("", fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize=16,width=0.2)
    ax.spines['top'].set_linewidth('0.3') 
    ax.spines['right'].set_linewidth('0.3') 
    ax.spines['bottom'].set_linewidth('0.3') 
    ax.spines['left'].set_linewidth('0.3') 
    ax.set_ylim([0,100])
    ax2=sns.histplot(df_rand,x='Simulated_p80_check', bins=20, color=color2)
    ax2.set_ylabel("Count", color = color2)
    st.pyplot(fig1)

    metric("Simulated Recovery", simul_recovery,)

    #st.write(df)
    #st.table(df,)


    # st.header("Output data")
    # if 'data' in response:
    #     st.dataframe(response['data'])
    

col31, col32, col33,col34,col35 = st.beta_columns((1,3,3,1,1))

#with col32:
#    st.table(df_test)  

#with col32:
    #st.write('')
    #st.subheader('Simulated Recovery:')
    #st.header(f'    |   {simul_recovery}    |  ')
    #metric("Simulated Recovery", simul_recovery,)



    #node_number2 =st.selectbox("Number of Nodes2",("3", "4", "5","6"))
    #n1=st.number_input("11")



# input_dataframe = pd.DataFrame(
#     np.array([[18,30],[50,70],[110,90],[140,90],[190,78],[230,39]]),
#     #index=range(node_number),
#     columns=[
#         'p80',
#         'Recovery'
#     ])

# response = AgGrid(
#     input_dataframe, 
#     editable=True,
#     sortable=False,
#     filter=False,
#     resizable=True,
#     defaultWidth=10,
#     fit_columns_on_grid_load=True,
#     key='input_frame')

#col41, col42 = st.beta_columns((1,1))

