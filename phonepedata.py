import json
import streamlit as st
import plotly.express as px
import pandas as pd
import mysql.connector

#SETUP PAGE IN STREAMLIT

st.set_page_config(page_title = 'Phonepepulse',layout ="wide")
st.markdown("<h1 style='text-align: center; color: Red;'>PhonePe Data Analysis</h1>", unsafe_allow_html=True)

#DATA RETRIEVAL:
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("Data input")
        option = st.selectbox(
        'Select the Year?',
        ('2018', '2019', '2020','2021','2022'))
        st.write('You selected:', option)
        option3 = st.selectbox(
        'Select the Year?',
        ('Transaction','User'))
        st.write('You selected:', option3) 
        db = option3.lower()+option 
        conn = mysql.connector.connect(host="localhost",
                                       port="3306",
                                       user="root",
                                       password="************",
                                       database=db)
        
    with right_column:
        st.subheader("India") 
        option1 = st.selectbox(
        'Select the Quarters?',
        ('1stquarter','2ndquarter','3rdquarter','4thquarter'))
        st.write('You selected:', option1)
        
        form = st.form(key='my-form')
        submit = form.form_submit_button('Search')

        if submit:
            st.write('Please wait, it may take few seconds')
        
        mycursor = conn.cursor()
        select = "SELECT * from  " + option1
        mycursor.execute(select)
        # Fetch the records
        result = mycursor.fetchall()
        df =pd.DataFrame(result)
        #st.dataframe(df)
        # Close the connection
        conn.close()

#PLOTTING INDIAN STATES GEO MAP
        
if option3 == 'User':
    if submit:
        st.markdown("<h1 style='text-align: center; color: Blue;'>PhonePe in India-Statewise Map</h1>", unsafe_allow_html=True)

        india_states = json.load(open("states_india.geojson", "r"))

        df =pd.DataFrame(result, columns= ['name','registeredUsers','appOpens'])
        #print(df)
    
        state_id_map = {}

        for feature in india_states["features"]:
            feature["id"] = feature["properties"]["state_code"]
            state_id_map[feature["properties"]["st_nm"]] = feature["id"]
    
        print(state_id_map)   
#df["Density"] = df["num"].apply(lambda x: int(x.split("/")[0].replace(",", "")))
#df2 = pd.DataFrame(state_id_map.values(), columns=['idcode'])

        x = {'Telangana': 0, 'Andaman & Nicobar Island': 35, 'Andhra Pradesh': 28, 'Arunanchal Pradesh': 12, 'Assam': 18, 'Bihar': 10, 'Chhattisgarh': 22, 'Daman & Diu': 25, 'Goa': 30, 'Gujarat': 24, 'Haryana': 6, 'Himachal Pradesh': 2, 'Jammu & Kashmir': 1, 'Jharkhand': 20, 'Karnataka': 29, 'Kerala': 32, 'Lakshadweep': 31, 'Madhya Pradesh': 23, 'Maharashtra': 27, 'Manipur': 14, 'Chandigarh': 4, 'Puducherry': 34, 'Punjab': 3, 'Rajasthan': 8, 'Sikkim': 11, 'Tamil Nadu': 33, 'Tripura': 16, 'Uttar Pradesh': 9, 'Uttarakhand': 5, 'West Bengal': 19, 'Odisha': 21, 'Dadara & Nagar Havelli': 26, 'Meghalaya': 17, 'Mizoram': 15, 'Nagaland': 13, 'NCT of Delhi': 7}
        x =  {k.lower(): v for k, v in x.items()}

        x['dadra & nagar haveli & daman & diu'] = x['dadara & nagar havelli']
        del x['dadara & nagar havelli']
        x['andaman & nicobar islands'] = x['andaman & nicobar island']
        del x['andaman & nicobar island']
        x['ladakh'] =1
        x['arunachal pradesh'] = x['arunanchal pradesh']
        del x['arunanchal pradesh']
        x['delhi'] = x['nct of delhi']
        del x['nct of delhi']

        g= df['name'].tolist()
        #print(g)
        h = []
        for i in g:
            # print(x[i])
            h.append(x[i])

        #print(h)
        df['id'] = h
    
        fig = px.choropleth(
                    df,
                    locations="id",
                    geojson=india_states,
                    color=df['registeredUsers'],
                    hover_name="name",
                    hover_data =['appOpens'],
                    
                                )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(width =850, height =550)
        st.write(fig)


        x=  df['registeredUsers'].max()
        y = df['registeredUsers'].min()
        x1 =df['appOpens'].max()
        y1 =df['appOpens'].min()

        for i in range(len(df['registeredUsers'])):
            if df['registeredUsers'][i] == x:
                high=df['name'][i] 
                high1=df['registeredUsers'][i]
                
            elif df['registeredUsers'][i] == y:
                low=df['name'][i] 
                low1=df['registeredUsers'][i]
        
                col1, col2= st.columns(2)    
        with col1:
            st.header('Highest RegisteredUsers-State')
            st.subheader(high)
            st.subheader(high1)
    
        with col2:
            st.header('Lowest RegisteredUsers-State')
            st.subheader(low)
            st.subheader(low1)
    
elif option3 == 'Transaction':
    if submit:
        st.markdown("<h1 style='text-align: center; color: Blue;'>PhonePe in India-Statewise Map</h1>", unsafe_allow_html=True)

        india_states = json.load(open("states_india.geojson", "r"))

        df =pd.DataFrame(result, columns= ['name','type', 'count','amount'])
        #print(df)

        state_id_map = {}

        for feature in india_states["features"]:
            feature["id"] = feature["properties"]["state_code"]
            state_id_map[feature["properties"]["st_nm"]] = feature["id"]
        
        print(state_id_map)   
    #df["Density"] = df["num"].apply(lambda x: int(x.split("/")[0].replace(",", "")))
    #df2 = pd.DataFrame(state_id_map.values(), columns=['idcode'])

        x = {'Telangana': 0, 'Andaman & Nicobar Island': 35, 'Andhra Pradesh': 28, 'Arunanchal Pradesh': 12, 'Assam': 18, 'Bihar': 10, 'Chhattisgarh': 22, 'Daman & Diu': 25, 'Goa': 30, 'Gujarat': 24, 'Haryana': 6, 'Himachal Pradesh': 2, 'Jammu & Kashmir': 1, 'Jharkhand': 20, 'Karnataka': 29, 'Kerala': 32, 'Lakshadweep': 31, 'Madhya Pradesh': 23, 'Maharashtra': 27, 'Manipur': 14, 'Chandigarh': 4, 'Puducherry': 34, 'Punjab': 3, 'Rajasthan': 8, 'Sikkim': 11, 'Tamil Nadu': 33, 'Tripura': 16, 'Uttar Pradesh': 9, 'Uttarakhand': 5, 'West Bengal': 19, 'Odisha': 21, 'Dadara & Nagar Havelli': 26, 'Meghalaya': 17, 'Mizoram': 15, 'Nagaland': 13, 'NCT of Delhi': 7}
        x =  {k.lower(): v for k, v in x.items()}

        x['dadra & nagar haveli & daman & diu'] = x['dadara & nagar havelli']
        del x['dadara & nagar havelli']
        x['andaman & nicobar islands'] = x['andaman & nicobar island']
        del x['andaman & nicobar island']
        x['ladakh'] =1
        x['arunachal pradesh'] = x['arunanchal pradesh']
        del x['arunanchal pradesh']
        x['delhi'] = x['nct of delhi']
        del x['nct of delhi']

        g= df['name'].tolist()
        #print(g)
        h = []
        for i in g:
            # print(x[i])
            h.append(x[i])

        #print(h)
        df['id'] = h
        
        fig = px.choropleth(
                df,
                locations="id",
                geojson=india_states,
                color=df['count'],
                hover_name="name",
                hover_data =['amount'],
        
                )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(width =850, height =550)
        st.write(fig)


        x=  df['count'].max()
        y = df['count'].min()
        x1 =df['amount'].max()
        y1 =df['amount'].min()

        for i in range(len(df['count'])):
            if df['count'][i] == x:
                high=df['name'][i] 
                high1=df['count'][i]
           
            elif df['count'][i] == y:
                low=df['name'][i] 
                low1=df['count'][i]
            
                col1, col2= st.columns(2)
     
        with col1:
            st.header('Highest Count-State')
            st.subheader(high)
            st.subheader(high1)
        
        with col2:
            st.header('Lowest Count-State')
            st.subheader(low)
            st.subheader(low1)
        
        for i in range(len(df['amount'])):
            if df['amount'][i] == x1:
                high=df['name'][i] 
                high1=df['amount'][i]
           
            elif df['amount'][i] == y1:
                low=df['name'][i] 
                low1=df['amount'][i]
                
                col1, col2= st.columns(2)
                
        with col1:
            st.header('Highest Amount-State')
            st.subheader(high)
            st.subheader(high1)
        
        with col2:
            st.header('Lowest Amount-State')
            st.subheader(low)
            st.subheader(low1)


       


