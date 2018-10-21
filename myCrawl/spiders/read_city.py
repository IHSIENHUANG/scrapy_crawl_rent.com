
# coding: utf-8

# In[1]:


import pandas as pd 


# In[5]:


df = pd.read_csv("../../state_city.csv")
datas = df['California']
urls = []
url = "https://www.rent.com/california/riverside/apartments_condos_houses_townhouses?page=2"
for data in datas:
    data = data.replace(" ","-")
    url = "https://www.rent.com/california/" + str(data) +"/apartments_condos_houses_townhouses?page=2"
    urls.append(url)
for url in urls:
    print (url)

