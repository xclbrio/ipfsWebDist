# -*- coding: utf-8 -*-

from selenium import webdriver
import unittest, time
import random


class ExcaliburIPSFTestSuite(unittest.TestCase):
    IMPLICITLY_WAIT = 30

    def setUp(self):

        # launch browser with metamask and touchvpn
        options = webdriver.ChromeOptions()
        options.add_extension('metamask.crx')

        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")

        # launch chrome
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(self.IMPLICITLY_WAIT)
        self.verificationErrors = []
        self.accept_next_alert = True

        # enable MetaMask test account
        self.driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')

        # select old design, agree terms
        self.driver.find_element_by_class_name("negative").click()
        markdown = self.driver.find_element_by_link_text('Terms of Use')
        self.driver.execute_script("arguments[0].scrollIntoView(90);", markdown)

        # scroll through other menus
        self.driver.find_element_by_tag_name("BUTTON").click()
        self.driver.find_element_by_tag_name("BUTTON").click()
        self.driver.find_element_by_tag_name("BUTTON").click()
        self.driver.find_element_by_tag_name("P").click()

        # reset account
        self.driver.find_element_by_id('password-box').send_keys("DSJ2K4dflg289gFfG3")
        self.driver.find_element_by_id('password-box-confirm').send_keys("DSJ2K4dflg289gFfG3")
        self.driver.find_element_by_tag_name('TEXTAREA').send_keys(
            "affair float asthma arrange sentence machine transfer leg fury napkin obvious process")
        self.driver.find_elements_by_tag_name('BUTTON')[1].click()

        # select kovan
        self.driver.find_element_by_class_name('network-indicator').click()
        time.sleep(0.5)
        self.driver.find_elements_by_class_name('dropdown-menu-item')[2].click()

        # go to the site (local)
        self.driver.get('http://localhost:8080')
        time.sleep(5)

        # to accept notification
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.find_elements_by_tag_name('BUTTON')[0].click()
        self.driver.switch_to.window(self.driver.window_handles[0])

        # waiting for pre-loader to disappear
        self.driver.implicitly_wait(1)
        while len(self.driver.find_elements_by_xpath("//div[@class='pre-loader__container']")) > 0:
            time.sleep(1)
        self.driver.implicitly_wait(self.IMPLICITLY_WAIT)

    def test_1_order_create_buy_(self):
        driver = self.driver

        # go to the BUY tab, enter the number of tokens and press PLACE BUY ORDER
        driver.find_element_by_xpath("//li[@id='t-BUY']").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='MANAGE'])[1]/following::input[1]").send_keys("0.001")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='eth'])[2]/following::span[5]").click()

        # waiting for the Metamask window and confirming the transaction
        while len(driver.window_handles) < 2:
            time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        driver.find_elements_by_tag_name('BUTTON')[1].click()
        driver.switch_to.window(driver.window_handles[0])

        # check for no error
        try:
            self.assertFalse(driver.find_element_by_xpath(
                "(.//*[normalize-space(text()) and normalize-space(.)='SEND'])[2]/following::h3[1]").is_displayed())
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        self.assertFalse(driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='SEND'])[2]/following::div[1]").is_displayed())


    def test_2_order_create_sell(self):
        driver = self.driver

        # go to the SELL tab, enter the number of tokens and press PLACE SELL ORDER
        driver.find_element_by_xpath("//li[@id='t-SELL']").click()
        driver.find_element_by_xpath(
            "//form[@class='forms__box form__sell']//input[@placeholder='amount_']").send_keys("0.001")
        driver.find_element_by_xpath(
            "//button[@class='button sell']").click()

        # waiting for the Metamask window and confirming the transaction
        while len(driver.window_handles) < 2:
            time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        driver.find_elements_by_tag_name('BUTTON')[1].click()
        driver.switch_to.window(driver.window_handles[0])

        # check for no error
        try:
            self.assertFalse(driver.find_element_by_xpath(
                "(.//*[normalize-space(text()) and normalize-space(.)='SEND'])[2]/following::h3[1]").is_displayed())
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        self.assertFalse(driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='SEND'])[2]/following::div[1]").is_displayed())

    def test_3_order_execution(self):
        driver = self.driver

        # go to ORDER BOOK
        driver.find_element_by_xpath("//li[@id='t-ORDERBOOK']").click()

        # selection of the first order in the list and pressing the order execution button
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='spread'])[1]/following::div[6]").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='BNB'])[1]/following::button[1]").click()

        # waiting for the Metamask window and confirming the transaction
        while len(driver.window_handles) < 2:
            time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)
        driver.find_elements_by_tag_name('INPUT')[2].click()
        driver.switch_to.window(driver.window_handles[0])

        # check for no error
        try:
            self.assertFalse(driver.find_element_by_xpath(
                "(.//*[normalize-space(text()) and normalize-space(.)='SEND'])[2]/following::h3[1]").is_displayed())
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        self.assertFalse(driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='SEND'])[2]/following::div[1]").is_displayed())

        # verification of a successful transaction notification
        for i in range(self.IMPLICITLY_WAIT):
            try:
                if driver.find_element_by_xpath(
                        "(.//*[normalize-space(text()) and normalize-space(.)='TRANSACTION'])[1]/following::div[2]").is_displayed(): break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")

    def test_4_order_cancel(self):
        driver = self.driver

        # go to PERSONAL ORDER BOOK
        driver.find_element_by_xpath("//li[@id='t-PERSONAL OB']").click()

        # selection of the first order in the list and pressing cancel button
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='FIAT'])[2]/following::div[6]").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='ADDRESS'])[1]/following::button[1]").click()

        # waiting for the Metamask window and confirming the transaction
        while len(driver.window_handles) < 2:
            time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)
        driver.find_elements_by_tag_name('INPUT')[2].click()
        driver.switch_to.window(driver.window_handles[0])

        # check for no error
        try:
            self.assertFalse(driver.find_element_by_xpath(
                "(.//*[normalize-space(text()) and normalize-space(.)='SEND'])[2]/following::h3[1]").is_displayed())
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        self.assertFalse(driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='SEND'])[2]/following::div[1]").is_displayed())

        # verification of a successful transaction notification
        for i in range(self.IMPLICITLY_WAIT):
            try:
                if driver.find_element_by_xpath(
                        "(.//*[normalize-space(text()) and normalize-space(.)='TRANSACTION'])[1]/following::div[2]").is_displayed(): break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")

    def test_5_chat_sign_in(self):
        driver = self.driver

        # authorization
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Signup'])[1]/following::button[1]").click()

        # waiting for the Metamask window and confirming the transaction
        while len(driver.window_handles) < 2:
            time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        driver.find_elements_by_tag_name('BUTTON')[1].click()
        driver.switch_to.window(driver.window_handles[0])

        # waiting for the chat panel to appear
        for i in range(self.IMPLICITLY_WAIT):
            try:
                if driver.find_element_by_id("input").is_displayed(): break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")

    def test_6_chat_sign_up(self):
        driver = self.driver

        # new user registration
        driver.find_element_by_xpath("//button[contains(text(),'Signup')]").click()
        driver.find_element_by_id("input").send_keys("name")
        driver.find_element_by_xpath("//button[@class='send-btn']").click()

        # waiting for the Metamask window and confirming sign
        while len(driver.window_handles) < 2:
            time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        driver.find_elements_by_tag_name('BUTTON')[1].click()
        driver.switch_to.window(driver.window_handles[0])

        # waiting for chat
        for i in range(60):
            try:
                if driver.find_element_by_id("input").is_displayed(): break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")

    def test_7_chat_send_msg(self):
        driver = self.driver
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Signup'])[1]/following::button[1]").click()

        # waiting for the Metamask window and confirming sign
        while len(driver.window_handles) < 2:
            time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        driver.find_elements_by_tag_name('BUTTON')[1].click()
        driver.switch_to.window(driver.window_handles[0])

        # waiting for the chat panel to appear
        for i in range(self.IMPLICITLY_WAIT):
            try:
                if driver.find_element_by_id("input").is_displayed(): break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")

        # waiting for chat
        driver.find_element_by_id("input").clear()
        test_Msg = 'test_Msg' + str(random.randint(0, 100))
        driver.find_element_by_id("input").send_keys(test_Msg)
        driver.find_element_by_xpath("//button[@class='send-btn']").click()
        time.sleep(1)

        # message verification
        last_Message = driver.find_elements_by_class_name("message")[
            len(driver.find_elements_by_class_name("message")) - 1].text
        if last_Message.find(test_Msg) == -1:
            self.fail("msg not found")

    def test_8_select_pair(self):
        driver = self.driver

        # selection of the current pair from the dropdown list
        driver.find_element_by_xpath("//div[@class='cur-pair']").click()
        time.sleep(0.5)
        driver.find_element_by_xpath("//a[contains(text(),'omg/eth')]").click()

        # validation of the display of the selected pair
        self.assertEqual("OMG,", driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='balances:'])[1]/following::span[2]").text)
        self.assertEqual("ETH", driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='omg,'])[1]/following::span[2]").text)

    def test_9_make_withdraw(self):
        driver = self.driver
        withdraw_money = 0.001

        # select pair and read current value of tokens (ETH)
        driver.find_element_by_xpath("//div[@class='cur-pair']").click()
        time.sleep(0.5)
        driver.find_element_by_xpath("//a[contains(text(),'bnb/eth')]").click()
        check_number_old = float(driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='bnb,'])[1]/following::span[1]").text)

        # go to the MANAGE section and select the ETH token
        driver.find_element_by_xpath("//li[@id='t-MANAGE']").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='bnb'])[4]/following::label[1]").click()

        # entering the value and pressing the SEND button, confirming the pop-up confirmation
        driver.find_element_by_xpath("//div[@class='form__sell__withdraw']//input[@placeholder='amount_']").send_keys(
            str(withdraw_money))
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='eth'])[5]/following::button[1]").click()
        driver.find_element_by_xpath("//button[@class='btn accept']").click()

        # waiting for the Metamask window and confirming the transaction
        while len(driver.window_handles) < 2:
            time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)
        driver.find_elements_by_tag_name('INPUT')[2].click()
        driver.switch_to.window(driver.window_handles[0])

        check_number_new = check_number_old - withdraw_money

        # waiting for a message on the correctness of the transaction and waiting for a change in the current account
        for i in range(60):
            try:
                if driver.find_element_by_xpath(
                    "//body/div[@id='app']/main/main[@class='workflow']/div[@class='window forms']/div[4]/div[1]").is_displayed() and float(
                    driver.find_element_by_xpath(
                        "(.//*[normalize-space(text()) and normalize-space(.)='bnb,'])[1]/following::span[1]").text) == check_number_new: break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")

    def test_10_make_deposit(self):
        driver = self.driver
        deposit_money = 0.001

        # select pair and read current value of tokens (ETH)
        driver.find_element_by_xpath("//div[@class='cur-pair']").click()
        time.sleep(0.5)
        driver.find_element_by_xpath("//a[contains(text(),'bnb/eth')]").click()
        check_number_old = float(driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='bnb,'])[1]/following::span[1]").text)

        # go to the MANAGE section and select the ETH token
        driver.find_element_by_xpath("//li[@id='t-MANAGE']").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='bnb'])[3]/following::label[1]").click()

        # entering the value and pressing the SEND button
        driver.find_element_by_xpath("//div[@class='form__sell__deposit']//input[@placeholder='amount_']").send_keys(
            str(deposit_money))
        driver.find_element_by_xpath(
            "//div[@class='form__sell__deposit']//button[@class='btn btn_deposit'][contains(text(),'SEND')]").click()

        # waiting for the Metamask window and confirming the transaction
        while len(driver.window_handles) < 2:
            time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)
        driver.find_elements_by_tag_name('INPUT')[2].click()
        driver.switch_to.window(driver.window_handles[0])

        check_number_new = check_number_old + deposit_money

        # waiting for a message on the correctness of the transaction and waiting for a change in the current account
        for i in range(60):
            try:
                if driver.find_element_by_xpath(
                    "//body/div[@id='app']/main/main[@class='workflow']/div[@class='window forms']/div[4]/div[1]").is_displayed() and float(
                    driver.find_element_by_xpath(
                        "(.//*[normalize-space(text()) and normalize-space(.)='bnb,'])[1]/following::span[1]").text) == check_number_new: break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")

  
    def tearDown(self):
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    print('Running functional tests:')
    unittest.main()
