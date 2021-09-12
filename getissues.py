from guietta import _, Gui, Quit
from requests.api import get
import requests
import json
import codecs
import pandas as pd
from requests.models import to_native_string
from os import environ

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

suppress_qt_warnings()

gui = Gui(
  [  'Gname：'     , '__n__'   ],
  [  'user ID：'   , '__a__'   ],
  [  'token: '     , '__b__'   ],
  [  ['Go']        ,   Quit    ]
)

def recalc(gui):
    json_list=[]
    index=1
    repository='{}/{}'.format(gui.a,gui.n)#输入用户名和代码库 格式：'xxxxx/xxxx'
    token=gui.b#输入token 格式：'xxxxxxxxxxx'
    inf = requests.get(url="https://api.github.com/repos/{}".format(repository))
    inf_json=inf.json()
    totnum=inf_json['open_issues']
    totpages=totnum/100+1
    while index <=totpages:
            response = requests.get(url="https://api.github.com/repos/{}/issues?state=all&per_page=100&page={}&sort=created".format(repository,index), headers={'Authorization': 'token {}'.format(token)})
            response.raise_for_status()
            if response.status_code == requests.codes.ok:
                response_json_list=response.json()
                if len(response.json())>0:
                    json_list=json_list+response_json_list
                    print("Got {} issues from page {}".format(len(response_json_list),index))
                    index=index+1
                else:
                    print("Get all issues successfully") 
                    break
            else:
                print("Stop to get issues due to {}".format(response.text))
                break
    with codecs.open('./issues.json','w','utf-8') as fp:
                print("Total number of issues:{}".format(len(json_list)))
                json.dump(json_list,fp=fp,indent=4)#输出文件issues.json
    json_data = pd.read_json('issues.json')
    json_data.head()
    json_data.to_csv('issues.csv',encoding="utf-8-sig",index=False)#输出文件issues.csv


gui.events(
    [       _        ,     _     ],
    [       _        ,     _     ],
    [       _        ,     _     ],
    [       recalc        ,     _     ] 
    ) 

gui.run() 