from __future__ import print_function
import time
import cfbd
from cfbd.rest import ApiException
from pprint import pprint
import numpy as np
from numpy import average, polyfit
import sportsdataverse
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.pyplot as plt
big10 = ["Indiana", "Maryland", "Michigan", "Michigan State", "Ohio State", "Penn State", "Rutgers",
         "Illinois", "Iowa", "Minnesota", "Nebraska", "Northwestern", "Purdue", "Wisconsin"]
def getImage(path, zoom=0.05):
    return OffsetImage(plt.imread(path), zoom=zoom)


# Configure API key authorization: ApiKeyAuth
configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = 'lw4qHxaSUI5PDRn77it/f/9yGXTML+qLbT57LmRbzpYcAHvnAEOVZooboY/VfVPi'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = cfbd.RatingsApi(cfbd.ApiClient(configuration))
year = 2021 # int | Season filter (required if team not specified) (optional)
team = 'Ohio State' # str | Team filter (required if year not specified) (optional)
df = sportsdataverse.cfb.get_cfb_teams()
#print(df.columns)
ap2 = cfbd.RecruitingApi(cfbd.ApiClient(configuration))
team_sprec = {}
team_spsum = {}
team_rec = {}
team_recsum = {}
# Historical SP+ ratings
for i in range(2012, 2022):
    if (i != 2025):
        response = api_instance.get_sp_ratings(year=i)
        for j in range(len(response)):
            api_response = response[j]
            #print(dir(api_response))
            sp_rank = api_response._ranking
            team = api_response.team
            if(not team in team_sprec):
                team_sprec[team] = []
            team_sprec[team].append(sp_rank)

for i in range(2012, 2022):
    response = ap2.get_recruiting_teams(year=i)
    for j in range(len(response)):
        api_response = response[j]
        #print(dir(api_response))
        rec_rank = api_response._rank
        team = api_response.team
        if(not team in team_rec):
            team_rec[team] = []
        team_rec[team].append(rec_rank)
for key in team_rec:
    value = team_rec[key]
    if len(value)>9:
        if(not key in team_recsum):
            team_recsum[key] = round(average(value), 1)
#print(f"Recruiting: {team_recsum}")
#print("--------------------------------")


for key in team_sprec:
    value = team_sprec[key]
    if len(value)>9:
        if(not key in team_spsum and key!="nationalAverages"):
            team_spsum[key] = round(average(value), 1)
#print(f"SP+: {team_spsum}")
xdata=[]
ydata=[]
img_paths = []
team_both = {}
for key in team_recsum:
    if key in team_spsum:

        team_both[key] = (team_recsum[key], team_spsum[key])
        path = df[df['school']==key]['logo'].values[0]
        xdata.append(team_recsum[key])
        ydata.append(team_spsum[key])
        img_paths.append(path)
#print(team_both)


fig, ax = plt.subplots()
b, m = polyfit(xdata, ydata, 1)
ll = []
print(b, m)
for x in xdata:
    ll.append(b+x*m)
print(ll)
ll = np.linspace(0, 130, 101)
ax.plot(ll, ll, '--k')
ax.scatter(xdata, ydata) 


for x0, y0, path in zip(xdata, ydata,img_paths):
    ab = AnnotationBbox(getImage(path), (x0, y0), frameon=False)
    ax.add_artist(ab)
ax.set_xlabel("Recruiting Rankings")
ax.set_ylabel("SP+ Ranking")
plt.title(f"CFB Average Recruiting Ranking vs SP+ Ranking since 2012")
ax.invert_xaxis()
ax.invert_yaxis()
plt.show()
    