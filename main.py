import requests
from bs4 import BeautifulSoup
import re
import json

# Making a GET request
url='https://www.ign.com/news/'

r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')

names=soup.find_all("span", class_="interface jsx-1469951667 item-title bold")
for count in range(0,len(names)):
    names[count]=str(names[count])

article_name = [s.replace('<span class="interface jsx-1469951667 item-title bold">', "").replace("</span>", "") for s in names]

pages=[]
for page in soup.find_all('a', class_="item-body"):
    pagedic = {}
    pagedic["href"] ="https://www.ign.com"+page.get('href') 
    pagedic["author"]=""
    pagedic["publish_date"]=""
    pagedic["update_date"]=""
    pagedic["content"]=""
    pages.append(pagedic)

for page in pages:
    try:
        article=requests.get(page["href"], headers={'User-Agent': 'Mozilla/5.0'})
        article=BeautifulSoup(article.content, 'html.parser')
        
        temp_array=article.find_all("div", class_="caption jsx-1541923331")


        if(len(temp_array)>0):
            page["author"]=temp_array[0].text.replace("By\xa0", "")        
        if(len(temp_array)>1):
            page["update_date"]=temp_array[1].text
        if(len(temp_array)>2):
            page["publish_date"] = temp_array[2].text
        
        temp_array=article.find_all("div", class_="jsx-3517015813 article-content page-0")
        if(len(temp_array)>0):
            page["content"] = temp_array[0].text
    except:
        print(f"Error: {page["href"]}")


file_path = "data.json"

# Convert the JSON data to a string
json_string = json.dumps(pages, indent=4)

# Save the JSON string to the file
with open(file_path, "w") as f:
    f.write(json_string)

print("JSON array saved to:", file_path)