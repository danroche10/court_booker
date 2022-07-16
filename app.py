from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta

booking_date = (datetime.today() + timedelta(days=6)).strftime('%Y-%m-%d')
url = "https://bookings.better.org.uk/location/islington-tennis-centre/tennis-court-outdoor/2022-07-21/by-time/slot/13:00-14:00"

browser = webdriver.Chrome(executable_path='./chromedriver')
browser.get(url)
time.sleep(5)
WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(., 'Book now')]"))).click()

WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='username']"))).send_keys('danielroche10@gmail.com')
WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='password']"))).send_keys('Dr061091!')
showmore_link = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, ".//button[contains(@class,'Button__StyledButton-sc-5h7i9w-1 fBHwHD SharedLoginComponent__LoginButton-sc-hdtxi2-5 fQXEJi') and @type='submit']")))
showmore_link.click()
time.sleep(5)
showmore_link2 = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, ".//button[contains(@class,'Button__StyledButton-sc-5h7i9w-1 fBHwHD') and @type='button']")))
showmore_link2.click()

WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='billingFirstName']"))).send_keys('Daniel')
WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='billingLastName']"))).send_keys('Roche')
WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='billingAddressLineOne']"))).send_keys('28 Wells House')
WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='billingCity']"))).send_keys('London')
WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='billingPostcode']"))).send_keys('EC1R 4TR')
WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='cardholderName']"))).send_keys('Daniel Roche')
WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='cardNumber']"))).send_keys('5356664249552607')
WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='expiryDate']"))).send_keys('04/25')
WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='securityCode']"))).send_keys('877')
WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(., 'Continue')]"))).click()

ele = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='TermsModalComponent__Background-sc-1g34mtg-4 kARssu']")))
browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", ele)



WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(., 'I Agree')]"))).click()