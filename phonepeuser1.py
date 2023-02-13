import pandas as pd
import mysql.connector

#Read data as a json file
df =pd.read_json('1.json',orient='records')

#DATA CLEANING
x = df['data'][0]
df1 = pd.DataFrame(x.keys(),columns=['name'])
y = x.values()
df2 = pd.DataFrame(y)

#Join the DataFrame
final=df1.join(df2)
print(final)

#DATA STORING
#Store the DataFrame into MySQL Database

conn = mysql.connector.connect(host="localhost",
                               port="3306",
                               user="root",
                               password="**********",
                               database="user2022")
mycursor = conn.cursor()
mycursor.execute("CREATE TABLE 4thquarter (name VARCHAR(255), registeredUsers int, appOpens bigint)")

#creating column list for insertion
cols = "`,`".join([str(i) for i in final.columns.tolist()])

# Insert DataFrame records one by one.
for i,row in final.iterrows():
    sql = "INSERT INTO `4thquarter` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
    mycursor.execute(sql, tuple(row))
    conn.commit()


