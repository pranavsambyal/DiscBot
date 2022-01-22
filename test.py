import pickle


COMMANDWORD='?'
greet=['Hello','Hola','Namaste']

df={}
df['COMMANDWORD']=COMMANDWORD
df['greet']=greet

print(df)
temp=open('config.pkl','wb')
pickle.dump(df,temp)
temp.close()