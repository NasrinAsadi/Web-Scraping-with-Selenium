import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

Driver_Path= r"C:\\Program Files (x86)\\chromedriver.exe"
Patent_list=["3D printing", "WiFi", "Smart phone"]


# scroll through page results
def extractPages(folder):
    #extract title of patents and navigate to corressponding pages
        # number of pattents found
        number =(int)( driver.find_element_by_xpath("/html/body/i/strong[3]").text)
        # number of pages
        pageNumber = 2

        #number of pattents shown in each page of search result
        onePageItems = (int)(driver.find_element_by_xpath("/html/body/i/strong[2]").text)
        j = 0
        while j < number:
            row = (j % onePageItems) + 2
            title = driver.find_element_by_xpath("/html/body/table/tbody/tr[{}]/td[4]/a".format(row))
            title_text = title.text

            current_url = driver.current_url
            title.click()
            WebDriverWait(driver, 15).until(EC.url_changes(current_url))
            #extract abstract and full text (include Claims and Descriptions section) of each page
            findDetail(driver,folder, "abstract_{}.txt".format(j), "fullText_{}.txt".format(j),title_text)
            current_url = driver.current_url
            driver.back()
            WebDriverWait(driver, 15).until(EC.url_changes(current_url))
            #time.sleep(5)
            j = j + 50
            if j % onePageItems == 0 and j < number:
                # jump to next page results ("next 50 Hits" button )
                current_url = driver.current_url
                driver.find_element_by_name("NextList{}".format(pageNumber)).click()
                WebDriverWait(driver, 15).until(EC.url_changes(current_url))
                pageNumber = pageNumber + 1


#find abstract and full text of a patent .......
def findDetail(driver,folder, abstarctFile , fullTextFile, title):
    abstract = driver.find_element_by_xpath("/html/body/p[1]").text
    full_text=driver.find_element_by_xpath("/html/body").text

    start =str(full_text).index("Claims")
    end = str(full_text).index("* * * * *")
    if start>0:
        full_text=full_text[start:end]

    with open(str(folder+"\\"+abstarctFile), 'w') as filehandle:
        filehandle.writelines(title)
        filehandle.writelines("\n")
        filehandle.writelines(abstract)
    with open(str(folder+"\\"+fullTextFile), 'w') as filehandle2:
        filehandle2.writelines(title)
        filehandle2.writelines("\n")
        filehandle2.writelines(full_text)



options= webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver= webdriver.Chrome(Driver_Path, chrome_options=options)
driver.maximize_window()
driver.get("https://patft.uspto.gov/netahtml/PTO/search-bool.html")

# Extract all pages related to the patents list.
for patent in Patent_list:
    # fill search form with patent and "Title" as zone of search
    inFieldBox= driver.find_element_by_id("fld1")
    inFieldBox.send_keys("Title")

    keywordSearchBox= driver.find_element_by_id("trm1")
    keywordSearchBox.send_keys(patent)

    keywordSearchBox.send_keys(Keys.ENTER)

    if not os.path.exists(patent):
        os.mkdir(patent)

    extractPages(patent)
    #Back to search page
    driver.find_element_by_xpath("/html/body/center[1]/a[1]/table/tbody/tr/td/a[2]").click()

driver.quit()