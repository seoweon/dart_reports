# [전자공시시스템](http://dart.fss.or.kr/)에서 한 회사의 역대 사업보고서 한 번에 다운받기
전자공시시스템에서 한 회사의 역대 사업보고서를 한 번에 다운받는 간단한 script입니다. 

## Directions: 

1. 다음 repository를 클론합니다
2. (아직 없다면) [DART API Key 발급페이지](http://dart.fss.or.kr/dsap001/apikeyManagement.do;jsessionid=Bs7AWiSzD8YmbBx0Zg3WoEixviKFJ7tL2OmeavY5lXpuYNh4MBmNjvvrgldaazhx.dart2_servlet_engine2)에 접속해 API key를 발급받습니다 (쉬워요)
3. 동 폴더에 ```api_key.txt```라는 텍스트파일을 만들어 발급받은 KEY를 저장합니다
4. [dart_crawling.ipynb](https://github.com/seoweon/dart_reports/blob/master/dart_crawling.ipynb)를 Jupyter Notebook에서 열어 실행시킵니다
5. 회사명 등의 입력사항을 넣으면 파일이 다운로드 됩니다. 

### 참고한 블로그
* http://quantkim.blogspot.kr/2018/01/dart-api-with.html
* http://tariat.tistory.com/31
* https://woosa7.github.io/fss_dart/

### 추신: 
* Regular Expressions를 사용하면 ```dm_no```같은 변수를 찾거나 폴더명을 정렬하는 게 좀 더 간편할 것 같아요.
* 사업보고서는 코드가 A001인데, 이것 외에도 다운받을 수 있는 공식 문서들이 굉장히 많습니다 (홈페이지의 [API 개발가이드](http://dart.fss.or.kr/dsap001/guide.do) 중 "상세 유형" 보면 이것저것 많이 나와있어요). 근데 어떤 방식으로 다운 받는 게 목적에 부합할 지 확신이 안 서서 우선은 사업보고서만 다운받는 형식으로 구성했습니다
* 다음 단계는 다운받은 사업보고서 pdf를 크롤링해서 재무제표 같은 자료를 한 눈에 정리하거나, 아니면 어떤 analytics를 적용하는 건데, 생각을 좀 해봐야겠습니다
