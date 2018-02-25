
# coding: utf-8

# # DART.fss.or.kr에서 역대 사업보고서 다운로드하기

# In[ ]:

#json을 읽기 위해서 우선 requests가 필요하고...
import requests
import pandas as pd
#나중에 등장하는 dcm_no의 xpath을 구하기 위한 lxml 
from lxml import html
#RegEx를 나중에 쓰게 된다면 필요한 re
import re

get_ipython().magic('load_ext autoreload')
get_ipython().magic('autoreload 2')

from utils import *

#위에 있는 download_file util 대신 curl을 이용할까 했으나 한국말을 못알아들어서 포기...
from subprocess import call


# API Key를 넣어주세요. [인증키 신청](http://dart.fss.or.kr/dsap001/apikeyManagement.do;jsessionid=Bs7AWiSzD8YmbBx0Zg3WoEixviKFJ7tL2OmeavY5lXpuYNh4MBmNjvvrgldaazhx.dart2_servlet_engine2)은 DART 계정을 만든 후 간단하게 할 수 있습니다

# In[ ]:

with open('api_key.txt','r') as f:
    API_KEY = f.read()


# ## 1. 원하는 회사의 사업보고서 링크 목록을 가져와봅시다. 

# #### 1) 회사의 종목코드를 가져오세요. (엑셀 출처: [한국거래소 전자공시 홈페이지](http://kind.krx.co.kr/corpgeneral/corpList.do?method=loadInitPage))

# In[ ]:

#회사 정보가 들어있는 엑셀을 읽어오되, 종목코드는 int가 아닌 str로 가져와야 합니다 (안 그러면 앞의 0이 지워져서 나오게 돼요)
#엑셀 source: http://kind.krx.co.kr/corpgeneral/corpList.do?method=loadInitPage
company_codes = pd.read_excel('company_codes.xlsx',converters={'종목코드':str})


# In[ ]:

#회사명 입력란을 만들어요
name_input = input('회사명을 입력해주세요: ')


# In[ ]:

#입력된 회사명이 없으면 진행이 안돼요
#CAVEAT: CJ같이 단독으로도 회사명이 존재하지만 CJ오쇼핑 같이 이게 포함된 회사명이 있는 경우, 찾아주지는 못합니다
while len(company_codes[company_codes.회사명 ==  name_input]) == 0:
    print('해당 이름의 회사명이 존재하지 않습니다. \n아래 회사명 중 하나를 찾으시나요? 다시 입력해주세요.\n')
    for row in company_codes.회사명:
        if row.find(name_input) != -1:
            print(row)
    name_input = input()
code = company_codes[company_codes.회사명 == name_input].종목코드.iloc[0]
print(name_input+" 종목코드: "+code)


# #### 2) 보고서 목록 URL을 생성하세요

# In[ ]:

#t시작날짜는 최초의 기업이 상장한 날짜인 1956년 3월보다 이전으로 잡았습니다
start_date = '19560101'
#Document type: 사업보고서
bsn_tp = 'A001'


# In[ ]:

url = "http://dart.fss.or.kr/api/search.json?auth="+API_KEY+"&crp_cd="+code+"&start_dt="+start_date+"&bsn_tp="+bsn_tp+"&fin_rpt=Y&page_set=100"


# #### 3) 개별 보고서 URL을 생성하세요

# In[ ]:

#json 값을 추출합시다
a = requests.get(url).json()


# In[ ]:

#각 사업보고서 당 리스트가 제대로 생성되는 지 봅시다. 하나도 없으면 코드 돌려봤자 아무것도 다운 안 됨
urldict = {}
for row in a['list']:
    url2 = "http://dart.fss.or.kr/dsaf001/main.do?rcpNo="
    name = row['rpt_nm']
    #[기재정정] [첨부추가] [첨부정정] 등 앞에 붙은 것을 제거해봅시다
    if name.find('[') != -1:
        name = name.split(']')[1]
    urldict[name] = url2+row['rcp_no']
    print(name+": "+url2+row['rcp_no'])


# ## 2. 각 사업보고서의 첨부파일 리스트를 확인하고 다운로드합시다

# In[ ]:

#카운터 선정
n=1

for key, value in urldict.items(): 
    #dcm_no 값을 알아야 다운로드 링크에 접근할 수 있는데, 알 방법이 링크에서 바로 가져오는 방법밖에 없으므로 xpath을 활용해서 알아봅시다
    test = requests.get(value)
    tree = html.fromstring(test.content)
    testpath = tree.xpath('//*[@id="north"]/div[2]/ul/li[1]/a/@onclick')[0]
    dcm_no = dcm_no = testpath.split(", '")[1].split("')")[0]
    
    #다운로드를 위한 url은 보고서 url과 차이점이 몇 가지 있는데, replace를 통해 추가할 수 있어요
    download_url = value.replace('dsaf001','pdf/download').replace('rcpNo','rcp_no')+"&dcm_no="+dcm_no
    print(key+" "+download_url+" 다운 중... "+str(n)+" out of "+str(len(urldict)))
    
    #dcm_no를 구했던 것과 같은 방법으로 첨부파일 다운로드 url을 추출합니다
    dtest = requests.get(download_url)
    dtree = html.fromstring(dtest.text)
    
    #각 보고서 당 복수의 첨부파일이 존재하는데, 첨부파일 이름과 함께 저장하기 위해 downloadpath라는 dict를 사용했습니다
    downloadpath={}
    keys = dtree.xpath('/html/body/div/div/table/tr/td[1]/text()')
    key_links = dtree.xpath('/html/body/div/div/table/tr/td/a/@href')
    for key2, link in zip(keys, key_links):
        l = "http://dart.fss.or.kr"+link
        k = key2.replace(")","")
        downloadpath[k] = l
    #print(downloadpath)
        
    #utils에 있는 download_file을 이요해 디렉토리를 만들고 그 안에다가 파일을 집어넣습니다
    for key2, link in downloadpath.items():
        download_file(link,filename=key2,directory="dart_"+name_input+"/"+key)
        #try:
            #os.mkdir(key)
        #except:
            #pass
        #call(['curl',link,'-o',key+'/'+key2])
    n+=1


# #### 마지막으로 파일 탐색기를 열어 다운로드받은 파일을 확인합니다. 

# In[ ]:

yesno = input('파일 다운로드가 완료되었습니다. 파일 탐색기를 열어 확인하시겠습니까? (y/n)  ')

if yesno.startswith('y'):
    call(['explorer','dart_'+name_input])


# In[ ]:



