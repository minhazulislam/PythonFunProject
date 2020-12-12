# importing libraries
import os
import requests
import pandas as pd

# setting working directory
# set the folder directory to save the files
os.chdir("/content/drive/My Drive/WebDataTableScrappingOutput/TRMM LIS Dataset")

# from year 1998 to 2015
year = list(range(1998,2016))

for j in year:
  # writing the url link
  url = 'https://lightning.nsstc.nasa.gov/nlisib/lisfound.exe?origin=ST&lat=23.5&lon=91&alat=7&alon=7&donob=both&'+str(j)+'.1=on&'+str(j)+'.2=on&'+str(j)+'.3=on&'+str(j)+'.4=on&'+str(j)+'.5=on&'+str(j)+'.6=on&'+str(j)+'.7=on&'+str(j)+'.8=on&'+str(j)+'.9=on&'+str(j)+'.10=on&'+str(j)+'.11=on&'+str(j)+'.12=on'
  html = requests.get(url).content
  # getting df list from the html object
  df_list = pd.read_html(html)
  day = [int(x.split('_')[-1].split('.')[1]) for x in list(df_list[3][0][1:])]
  orbit = [int(x.split('_')[-1].split('.')[2][:-1]) for x in list(df_list[3][0][1:])]
  k = 0
  for i in range(0,len(day)):
    new_url = 'https://lightning.nsstc.nasa.gov/nlisib/lis1orbit.exe?which=nqc&year='+str(j)+'&day='+str(day[i])+'&orbit='+str(orbit[i])
    html_new = requests.get(new_url).content
    try:
      df_list_new = pd.read_html(html_new)
      df_list_new[1].columns = list(df_list_new[1].loc[0])
      new = df_list_new[1].drop(0)
      new["Latitude"] = pd.to_numeric(new["Latitude"], downcast="float")
      new["Longitude"] = pd.to_numeric(new["Longitude"], downcast="float")
      new = new[new['Longitude'] > 87.5] # spelling mistake
      new = new[new['Longitude'] < 92.0] # spelling mistake
      new = new[new['Latitude'] > 20.5]
      new = new[new['Latitude'] < 27.0]
      if new.empty:
        print('No Data found for year = '+str(j)+'.day = '+str(day[i])+'.orbit = '+str(orbit[i]))
      elif k == 0:
        new1 = new
        k += 1
      else:
        new1 = pd.concat([new1,new],ignore_index=True)
    except:
      print('Error for '+str(j))
  new1.to_excel(str(j)+'.xlsx')