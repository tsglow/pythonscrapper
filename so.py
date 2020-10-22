import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=python"

def get_extract_job(html):  
  jobid = html.attrs["data-jobid"]
  jobid = int(jobid)
  jobinfo = html.find("div", {"class" : "grid--cell fl1"})
  title = jobinfo.find("h2").find("a")["title"]
  title = title.strip()
  
  company, location = jobinfo.find("h3").find_all("span", recursive=False)
  if company:
    company_s = company.string
    if company_s is not None:
      company = str(company_s)
      company = company.strip()
      company = company.strip(f"\r")
      company = company.strip(f"\n")
    else:
      company = "none"
  location = location.string.strip()
  url = f"https://stackoverflow.com/jobs/{jobid}"

  return {"title": title, "company": company, "location": location, "url" : url}

def extract_jobs(last_page):  
  jobs = []  
  for page in range(last_page): 
    so_result = requests.get(f"{URL}&pg={page+1}")    
    soup = BeautifulSoup(so_result.text, "html.parser")    
    results = soup.find_all("div", {"data-jobid" : True})
    print(f"now scrapping stackoverflow page : {page+1}")    
    for result in results:
      job = get_extract_job(result)
      jobs.append(job)  
  return jobs #인덴트 위치 중요 

def get_last_pages():     
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, 'html.parser')      
  links = soup.find("div", {"class" : "s-pagination"}).find_all("span")
  last_page = links[-2].string.strip()
  last_page = int(last_page)
  return last_page

def get_jobs():
  last_page = get_last_pages()   
  so_jobs = extract_jobs(last_page)
  return so_jobs