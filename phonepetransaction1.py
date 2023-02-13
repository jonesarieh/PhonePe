import pandas as pd
import mysql.connector

#Read data as a json file
df =pd.read_json('1.json',orient='records')

#DATA CLEANING:

#Create a Empty DataFrame
empty = empty = pd.DataFrame(columns=['name','metric'])

#Append the list of Dict Keys and Values into the empty DataFrame to handle
x = df['data'][0]
y = empty.append(x)

#Store the values to be handled in a new variable 
z = y['metric']

#Create a DataFrame and append the values into the DataFrame
df2 = pd.DataFrame()
for i in range(len(z)):
   df2= pd.concat([df2.append(z[i])],ignore_index=True)

#Concatenate into pandas DataFrame
#df2= pd.concat([df11,df22,df33,df44,df55],ignore_index=True)

#Add name column and join into the DataFrame
df3 = y[['name']]
final=df3.join(df2)
print(final)

#DATA STORING:
#Store the DataFrame into MySQL Database

conn = mysql.connector.connect(host="localhost",
                               port="3306",
                               user="root",
                               password="***********",
                               database="transaction2022")
mycursor = conn.cursor()

mycursor.execute("CREATE TABLE 4thquarter (name VARCHAR(255), type VARCHAR(255), count int, amount decimal(20,2))")

#creating column list for insertion
cols = "`,`".join([str(i) for i in final.columns.tolist()])

# Insert DataFrame records one by one.
for i,row in final.iterrows():
    sql = "INSERT INTO `4thquarter` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
    mycursor.execute(sql, tuple(row))
    conn.commit()


