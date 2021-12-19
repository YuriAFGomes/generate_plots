import json

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import norm

def prepare_data(filename):
    data=pd.read_csv(
    filename,
    low_memory=False,
    on_bad_lines = "skip"
    )

    data.dropna(subset=['Target_Date'],inplace=True)
    data.dropna(subset=['Disposal_Date'],inplace=True)
    data.dropna(subset=['Target_Date'],inplace=True)
    data.drop(data.index[data['Samadhan_One'] == 'Y'],inplace=True)

    data['EP_Trans_Date'] = pd.to_datetime(data['EP_Trans_Date'])
    data['Target_Date'] = pd.to_datetime(data['Target_Date'])
    data['DtOfAppCompletion'] = pd.to_datetime(data['DtOfAppCompletion'])
    data['Lsk_Fwd_Date'] = pd.to_datetime(data['Lsk_Fwd_Date'])
    data['Reg Date'] = pd.to_datetime(data['Reg Date'])
    data['Disposal_Date']=pd.to_datetime(data['Disposal_Date'], errors = 'coerce')
    data['appprocesstime'] = data['Disposal_Date'] - data['Reg Date']
    data['appprocesstime']=data['appprocesstime']/np.timedelta64(1,'D')
    data['dvt'] = data['Disposal_Date'] - data['Target_Date']
    data['dvt']=data['dvt']/np.timedelta64(1,'D')

    data.reset_index(inplace = True, drop = True)

    Q1 = np.percentile(data['dvt'], 25)
    Q3 = np.percentile(data['dvt'], 75)
    IQR = Q3 - Q1

    upper = np.where(data['dvt'] >= (Q3+8*IQR))
    lower = np.where(data['dvt'] <= (Q1-8*IQR))

    data.drop(upper[0], inplace = True)
    data.drop(lower[0], inplace = True)
    return data

def get_districts_and_services(data):
    districts = ['all'] +[value for value in list(data['District_Name_E'].unique())]
    services = ['all'] + [value for value in list(data['Service_Name_E'].unique())]
    return {'districts':districts,'services':services}

def plotit(data,district,service,save_path):
    d_pl = "s"
    s_pl = "s"
    if district== 'all' and service == 'all':
        rslt_df=data
    elif district== 'all' and service == service:
        rslt_df = data.loc[data["Service_Name_E"] == service]
        s_pl = ''
    elif district== district and service == 'all':
        rslt_df = data.loc[data["District_Name_E"] == district]
        d_pl = ''
    else:
        rslt_df = data.loc[(data["District_Name_E"] == district) & (data["Service_Name_E"] == service)]
        d_pl = ''
        s_pl = ''

    fig, ax = plt.subplots()

    sns.distplot(rslt_df['dvt'], hist=True, rug=True,kde=True,ax=ax)
    ax.set(
    xlabel='Disposal days',
    ylabel='Probability function value',
    title=f'Distribution curve for: {service} service{s_pl} in {district} district{d_pl}'
    )
    ax.set_xlim(-10,5)
    ax.set_xticks(range(-10,5))
    mean=rslt_df['dvt'].mean()
    std=rslt_df['dvt'].std()
    p=norm.cdf(1, mean, std)
    p1=int((1-p)*100)
    a1=int(rslt_df['dvt'].count())
    m1=int(min(rslt_df['dvt'],default = "EMPTY"))
    m2=int(rslt_df['dvt'].max())
    m3=int(rslt_df['dvt'].mean())
    text = [
        f"Total Applications : {a1}",
        f"Minimum Disposal time : {m1} days",
        f"Maximum Disposal time : {m2} days",
        f"Mean Disposal time : {m3} days",
        f"%  of applications Exceeding timeline : {p1} %"
    ]
    ax.plot([2], [1], 'o')

    filename = f"{district}-{service}"
    plt.savefig(f"{save_path}/{filename}.png",format='png',bbox_inches="tight",dpi=150)

    with open(f"{save_path}/{filename}.txt",'w') as f:
        for line in text:
            f.write(line+'\n')

def generate_plots(file,save_dir):
    combinations = set()
    data = prepare_data(file)

    districts_and_services = get_districts_and_services(data)

    with open(f"{save_dir}/districts_and_services.json",'w',encoding='utf-8') as f:
        json.dump(districts_and_services,f)

    for district in districts_and_services['districts']:
        for service in districts_and_services['services']:
            combination = (district,service)
            combinations.add(combination)

    i=0
    total = len(combinations)
    for combination in combinations:
        try:
            plotit(data,combination[0],combination[1],save_dir)
        except ValueError:
            continue
        i+=1
        print(f"{i}/{total}")
