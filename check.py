import pandas as pd

data = pd.read_csv("test.csv")
datas = sorted(data['url_from'])
print(len(datas))
print (len(set(datas)))
