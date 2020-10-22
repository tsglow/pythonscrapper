
#first we need go indeed.com python limit 50
#indeed에서 python 잡을 페이지당 50개씩 
#then find how many pages exist

import requests
from bs4 import BeautifulSoup

#indeed에서 python 잡을 페이지당 50개씩 
LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"
JOB_URL = "https://www.indeed.com/viewjob?jk="

def get_last_pages():     
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, 'html.parser')

  pagination = soup.find("div", {"class" : "pagination"})
  links = pagination.find_all("a")
  pages = []
  for link in links[:-1]:
    pages.append(int(link.string)) #page.string해도 text는 동일해서 같은 결과
  max_page = pages[-1]
  return max_page

def extract_job(html):
  title = html.find("h2", {"class": "title"}).find("a")["title"] #강좌엔 div로 되어     있지만 사이트에서 h2로 바뀜
  company = html.find("span", {"class" : "company"})
  if company:
    company_a = company.find("a")
    if company_a is not None:  #값이 none일 때의 처리
      company = str(company_a.string) #company 가 soup인 상태에서 company_a  값을 만들고, company_a의 값을 이용해서 만든 결과를 다시 company에 덮어쓰기
    else:
      company = str(company.string)
  else:
    company = None
  company = company.strip()  
  location = html.find("div", {"class","recJobLoc"})["data-rc-loc"] #.attrs를 생략가능
  location = str(location)  
  j_id = html["data-jk"]
  j_link = f"{JOB_URL}{j_id}"  
  return {'title': title, 'company': company, 'location': location, 'url' : j_link}


def extract_jobs(last_page):  
  jobs = []  
  for page in range(last_page): # 0부터 last page -1만큼의 리스트가 만들어짐
    #print(f"scrapping page {page}")
    result = requests.get(f"{URL}&start={page*LIMIT}")  
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class" : "jobsearch-SerpJobCard"})
    print(f"now scrapping indeed page : {page}")
    for result in results:      
      job = extract_job(result) #soup로 만든 result는 현재 html
      jobs.append(job)
  return jobs #인덴트 위치 중요 

def get_jobs():
  #get_last_pages()함수로 last page 추출
  last_page = get_last_pages() 
  #last page 값을 extract_jobs에 넣어 반환된 jobs list를 jobs로 함 
  jobs = extract_jobs(last_page)
  return jobs

