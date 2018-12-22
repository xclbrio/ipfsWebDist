# -*- coding: utf-8 -*-
from selenium import webdriver
import unittest, time
import random


class ExcaliburIPSFTestSuite(unittest.TestCase):
    debug = True
    IMPLICITLY_WAIT = 30

    def setUp(self):

        # launch browser with metamask and touchvpn
        options = webdriver.ChromeOptions()
        # options.binary_location = '/usr/local/bin/chromedriver'
        options.add_extension('metamask.crx')
        #options.add_argument("--headless")
       # options.add_argument("--disable-gpu")
        options.add_argument("--start-maximized")
        # options.add_extension('touchvpn.crx')
        if self.debug:
            options.add_extension('chroPath.crx')
           
        
        self.driver = webdriver.Chrome(options=options)
        print("!!")
        self.driver.implicitly_wait(self.IMPLICITLY_WAIT)
        self.verificationErrors = []
        self.accept_next_alert = True

        # # enable VPN)
        # self.driver.get('chrome-extension://ijkgnecnaddmgefgaommnokpfadikbdj/panel/index.html')
        # self.driver.find_element_by_id('ConnectionButton').click()
        
        driver.get("https://translate.google.ru/")
        driver.find_element_by_id("source").click()
        driver.find_element_by_id("source").clear()
        driver.find_element_by_id("source").send_keys("csdfdsffsd")
        self.assertEqual("csdfdsffsd", driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='Подробнее…'])[1]/following::span[2]").text)
        exit()
        # enable MetaMask test account
        self.driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')

        self.driver.find_element_by_class_name("negative").click()
        markdown = self.driver.find_element_by_link_text('Terms of Use')
        self.driver.execute_script("arguments[0].scrollIntoView(90);", markdown)

        self.driver.find_element_by_tag_name("BUTTON").click()
        self.driver.find_element_by_tag_name("BUTTON").click()
        self.driver.find_element_by_tag_name("BUTTON").click()
        self.driver.find_element_by_tag_name("P").click()
        self.driver.find_element_by_id('password-box').send_keys("Metamask88mel!")
        self.driver.find_element_by_id('password-box-confirm').send_keys("Metamask88mel!")
        self.driver.find_element_by_tag_name('TEXTAREA').send_keys(
            "affair float asthma arrange sentence machine transfer leg fury napkin obvious process")
        self.driver.find_elements_by_tag_name('BUTTON')[1].click()
        self.driver.find_element_by_class_name('network-indicator').click()
        time.sleep(0.5)
        self.driver.find_elements_by_class_name('dropdown-menu-item')[2].click()

        # заходим на сайт
        self.driver.get('http://localhost:8081')  # https://kovan.xclbr.io/?token=kRzaWWPtEwHY81Zn#/zrx_eth
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.find_element_by_class_name('btn-green').click()
        self.driver.switch_to.window(self.driver.window_handles[0])

        # ожидание исчезновения pre-loader'а
        self.driver.implicitly_wait(1)
        while len(self.driver.find_elements_by_xpath("//div[@class='pre-loader__container']")) > 0:
            time.sleep(1)
        self.driver.implicitly_wait(self.IMPLICITLY_WAIT)

    def test_1_order_create_buy_(self):
        driver = self.driver

        # переход во вкладку BUY, ввод числа токенов и кнопки PLACE BUY ORDER
        driver.find_element_by_xpath("//li[@id='t-BUY']").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='MANAGE'])[1]/following::input[1]").send_keys("0.001")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='eth'])[2]/following::span[5]").click()

        # ожидание окна Metamask'a и подтверждение транзакции
        while len(driver.window_handles) < 2:
            time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        driver.find_elements_by_tag_name('BUTTON')[1].click()
        driver.switch_to.window(driver.window_handles[0])

        # проверка, не высветилась ли ошибка
        try:
            self.assertFalse(driver.find_element_by_xpath(
                "(.//*[normalize-space(text()) and normalize-space(.)='SEND'])[2]/following::h3[1]").is_displayed())
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        self.assertFalse(driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='SEND'])[2]/following::div[1]").is_displayed())

  
    def tearDown(self):
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
