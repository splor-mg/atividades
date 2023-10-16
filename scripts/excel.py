import pandas as pd
import json

with open('atividades.json') as fs:
    data = json.load(fs)

df = pd.DataFrame(data['issues'])
df.to_excel('atividades.xlsx', index=False)