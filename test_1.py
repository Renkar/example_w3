from time import sleep

from selenium import webdriver

CUSTOMERS_DB = '//*[@id="yourDB"]/table/tbody/tr[2]/td[1]'
URL = 'https://www.w3schools.com/sql/trysql.asp?filename=trysql_select_all'
RUN_SQL = "/html/body/div[2]/div/div[1]/div[1]/button"
PERSONS_TABLE = '//*[@id="divResultSQL"]/div/table'




def parse_table(elemet):
    all_columns = elemet.find_elements_by_tag_name("tr")
    count_result = len(all_columns)
    columns_name = str(all_columns[0].text)
    columns_name = columns_name.split(" ")
    data = []
    for i in range(1, count_result):
        elements = all_columns[i].find_elements_by_tag_name("td")
        row_data = []
        for i in elements:
            row_data.append(i.text)
        data.append(dict(zip(columns_name, row_data)))
    return data


def test_person_address():
    driver = webdriver.Chrome("./chromedriver")
    driver.get(URL)
    sleep(2)
    driver.find_element_by_xpath(RUN_SQL).click()
    sleep(2)
    table_element = driver.find_element_by_xpath(PERSONS_TABLE)
    all_columns = parse_table(table_element)
    for i in all_columns:
        if i["ContactName"] == "Giovanni Rovelli":
            assert i['Address'] == 'Via Ludovico il Moro 22'


def test_city_london_count():
    driver = webdriver.Chrome("./chromedriver")
    driver.get(URL)
    sleep(2)
    driver.find_element_by_xpath(RUN_SQL).click()
    sleep(2)
    table_element = driver.find_element_by_xpath(PERSONS_TABLE)
    all_columns = parse_table(table_element)
    count = []
    for i in all_columns:
        if i["City"] == "London":
            count.append(i)
    assert len(count) == 6


def test_add_new_row():
    driver = webdriver.Chrome("./chromedriver")
    driver.get(URL)
    sleep(2)
    driver.execute_script(
        """window.editor.setValue("INSERT INTO Customers (CustomerName,ContactName,Address,City,PostalCode,Country) VALUES ('test name', 'test contact name', 'test address', 'test city', 12323, 'test country');")""")
    driver.find_element_by_xpath(RUN_SQL).click()
    sleep(2)
    driver.find_element_by_xpath(CUSTOMERS_DB).click()
    sleep(2)
    table_element = driver.find_element_by_xpath(PERSONS_TABLE)
    all_columns = parse_table(table_element)
    driver.find_element_by_xpath(RUN_SQL).click()
    count = []
    for i in all_columns:
        if i["CustomerName"] == "test name":
            assert i["ContactName"] == 'test contact name'
            assert i["Address"] == 'test address'
            assert i["City"] == 'test city'
            assert int(i["PostalCode"]) == int(12323)
            assert i["Country"] == 'test country'
            count.append(i)
    assert len(count) == 1


def test_update_row():
    driver = webdriver.Chrome("./chromedriver")
    driver.get(URL)
    sleep(2)
    driver.find_element_by_xpath(RUN_SQL).click()
    sleep(2)
    table_element = driver.find_element_by_xpath(PERSONS_TABLE)
    all_columns = parse_table(table_element)
    person_before = []
    for i in all_columns:
        if int(i['CustomerID']) == int(1):
            person_before.append(i)

    driver.execute_script(
        """window.editor.setValue("UPDATE Customers SET CustomerName = 'Update customer name', ContactName = 'Update contact name' ,Address = 'Update adress',City = 'Update city',PostalCode = 2222,Country = 'Update country' WHERE CustomerID = 1;")""")
    driver.find_element_by_xpath(RUN_SQL).click()
    sleep(2)
    driver.find_element_by_xpath(CUSTOMERS_DB).click()
    table_element = driver.find_element_by_xpath(PERSONS_TABLE)
    all_columns = parse_table(table_element)
    for i in all_columns:
        if int(i['CustomerID']) == int(1):
            assert i["CustomerName"] == 'Update customer name'
            assert i["ContactName"] == 'Update contact name'
            assert i["Address"] == 'Update adress'
            assert i["City"] == 'Update city'
            assert int(i["PostalCode"]) == int(2222)
            assert i["Country"] == 'Update country'
            assert i != person_before[0]