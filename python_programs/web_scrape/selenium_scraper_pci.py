from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import random
import pandas as pd
import time
import math


# WebDriverWait(browser, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="results"]/tbody/tr[2]')))
# ignored_exceptions = (NoSuchElementException,StaleElementReferenceException,)

class PCIBrowser:

    def __init__(self,
                 starting_page=1,
                 url="https://www.pcilookup.com/?ven=&dev=&action=submit",
                 options=webdriver.ChromeOptions().add_argument('headless'),
                 executable_path='',
                 rows_xpath="//*[@id='results']/tbody/tr",
                 cols_xpath="//*[@id='results']/tbody/tr[2]/td",
                 pages_xpath="//*[@id='results_paginate']/span/a[6]",
                 table_base_xpath="//*[@id='results']/tbody/tr[",
                 end_num_cols=4,
                 next_page_xpath='//*[@id="results_next"]'):
        self.starting_page = starting_page
        self.url = url
        self.options = options
        self.executable_path = executable_path
        self.rows_xpath = rows_xpath
        self.cols_xpath = cols_xpath
        self.pages_xpath = pages_xpath
        self.table_base_xpath = table_base_xpath
        self.data = [[] for i in range(end_num_cols)]
        self.next_page_xpath = next_page_xpath

    def start_browser(self):
        print("\nStarting new session")
        browser = webdriver.Chrome(options=self.options, executable_path=self.executable_path)
        browser.get(self.url)
        WebDriverWait(browser, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="results"]/tbody/tr[2]')))
        self.browser = browser
        self.table_dims()

    def quit_browser(self):
        self.browser.quit()
        print("\nEnded session successfully")

    def table_dims(self):
        self.rows = len(self.browser.find_elements_by_xpath(self.rows_xpath))
        self.columns = len(self.browser.find_elements_by_xpath(self.cols_xpath))
        self.num_pages = int(self.browser.find_element_by_xpath(self.pages_xpath).text)
        print(f'{self.rows} rows by {self.columns} columns, on {self.num_pages} pages')

    def display_per_page(self, per_page=100, per_page_xpath='//*[@id="results_length"]/label/select'):
        sel = Select(self.browser.find_element_by_xpath(per_page_xpath))
        sel.select_by_visible_text(str(per_page))
        self.table_dims()

    def read_table(self, start_page=1, end_page=None):
        if end_page is None:
            end_page = self.num_pages + 1
        for page in range(start_page, end_page):
            if page == 131:
                next_page = self.browser.find_element_by_xpath(self.next_page_xpath)
                self.browser.execute_script("arguments[0].click();", next_page)
                page += 1
            for col in range(1, self.columns + 1):
                print(f"\nProcessing column: {col} on page: {page}")
                col_xpath = f"]/td[{col}]"
                time.sleep(random.randint(1, 10) / 100)
                for row in range(1, (self.rows + 1)):
                    final_xpath = self.table_base_xpath + str(row) + col_xpath
                    # cell_text = WebDriverWait(self.browser, 60).until(EC.visibility_of_element_located((By.XPATH, final_xpath)))
                    cell_text = self.browser.find_element_by_xpath(final_xpath)
                    self.data[col - 1].append(cell_text.text)
            # WebDriverWait(browser, 60,).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="results_next"]')))
            next_page = self.browser.find_element_by_xpath(self.next_page_xpath)
            self.browser.execute_script("arguments[0].click();", next_page)

    def scrape_table(self, batch=True, batch_size=100, results_text_xpath='//*[@id="results_info"]'):
        if batch:
            starting_pages = [(i * batch_size) + 1 for i in range(math.ceil(self.num_pages / batch_size))]
            for sp in starting_pages:
                ep = sp + batch_size
                if sp > 1:
                    self.quit_browser()
                    self.start_browser()
                    self.display_per_page()
                    while True:
                        next_page = self.browser.find_element_by_xpath(self.next_page_xpath)
                        page_results = self.browser.find_element_by_xpath(results_text_xpath).text
                        page_results = int(page_results.split()[3].replace(",", ""))
                        if (sp) * 100 == page_results:
                            print(f"Starting to read data from page {sp}")
                            break
                        else:
                            self.browser.execute_script("arguments[0].click();", next_page)
                if ep > self.num_pages + 1:
                    ep = self.num_pages + 1
                self.read_table(start_page=sp, end_page=ep)
        else:
            self.read_table()

    def table_as_df(self, columns=["vendor", "vendor_id", "desc", "device_id"]):
        self.df = pd.DataFrame(self.data)
        self.df = self.df.transpose()
        self.df.columns = columns
        for col in self.df.columns:
            self.df[col] = self.df[col].astype('str')

    def write_df(self, path="./", filename="pci_lookup.csv"):
        self.df.to_csv(path + filename, header=True)
