from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
# from main import DataHouse

url='https://www.aljazeera.com/news/'


options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
#driver = webdriver.Chrome(options=options, executable_path= r"C:\webdrivers\chromedriver.exe")
driver = webdriver.Chrome(options=options)



driver.get(url)
page_content = driver.page_source
page1 =BeautifulSoup(page_content,'lxml')
# /html/body/div[1]/div/div[2]/div[2]/div/div/div/div[1]/a[1]
print("page1")
link = page1.select('div.breaking-ticker__items a')[0]['href']
LINK="https://www.aljazeera.com"+link
print(LINK)

driver.get(LINK)
page_content2 = driver.page_source
page2 =BeautifulSoup(page_content2,'lxml')

news = page2.select('div.wysiwyg.wysiwyg--all-content.css-1ck9wyi ul')[0].select('li')
neww=[]
for e in news:
    neww.append(e.text)
print(neww)


# links=[]
# for e in tex :
#     link= e.select('a')[1]['href']
#     links.append('http://www.tunisie-annonce.com/'+link)
#
# print(links)
#
# #extraction le DATA de chaque house
#
# for lien in links:
#     driver = webdriver.Chrome(options=options)
#     driver.get(lien)
#     page_content = driver.page_source
#
#     print(DataHouse(page_content))
#
# ---------------------------------------------------------




# tex = page1.select('tr.Tableau1')[0].select('a')[1]['href']
# print('http://www.tunisie-annonce.com/'+tex)


#/html/body/table[1]/tbody/tr/td[2]/table[2]/tbody/tr/td[4]/table/tbody/tr[3]/td/table[1]/tbody/tr[7]/td[6]/a
# .select('tr td')[3].select('table tr')[2].select('td table')[0].select('tr')[6].select('td')[6].select('a')
# DetailsAnnonceImmobilier.asp








# title1=driver.find_element_by_xpath('/html/body/div/table/tbody/tr/td[1]/form/table/tbody/tr/td/table/tbody/tr[{i}]/th'.format(i=i+1))
# title2=driver.find_element_by_xpath('/html/body/div/table/tbody/tr/td[1]/form/table/tbody/tr/td/table/tbody/tr[{i}]/td'.format(i=i+1))
# print("*******************************************************************************************************")
# print(title1.text)
# print("----------------")
# print(title2.text)

#
# def finder ():
#     for i in range (17):
#         title1=driver.find_element_by_xpath('/html/body/div/table/tbody/tr/td[1]/form/table/tbody/tr/td/table/tbody/tr[{i}]/th'.format(i=i+1))
#         title2=driver.find_element_by_xpath('/html/body/div/table/tbody/tr/td[1]/form/table/tbody/tr/td/table/tbody/tr[{i}]/td'.format(i=i+1))
#         print("*******************************************************************************************************")
#         print(title1.text)
#         print("----------------")
#         print(title2.text)
#
# finder()
