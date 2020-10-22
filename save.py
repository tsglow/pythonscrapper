import csv
def save_to_file(so_jobs):
  file = open("jobs.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["title","company","location","url"])  
  for job in so_jobs:
    writer.writerow(job.values()) #값만을 가져와라
  return
  

