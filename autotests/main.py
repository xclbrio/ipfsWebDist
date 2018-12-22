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
        options.binary_location = '/usr/local/bin/chromedriver'
        options.add_extension('metamask.crx')
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        # options.add_argument("--start-maximized")
        # options.add_extension('touchvpn.crx')
        if self.debug:
            options.add_extension('chroPath.crx')

        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.implicitly_wait(self.IMPLICITLY_WAIT)
        self.verificationErrors = []
        self.accept_next_alert = True

        # # enable VPN)
        # self.driver.get('chrome-extension://ijkgnecnaddmgefgaommnokpfadikbdj/panel/index.html')
        # self.driver.find_element_by_id('ConnectionButton').click()

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

        # СДЕЛАТЬ ПРОВЕРКУ НА ПОЯВЛЕНИЕ ОРДЕРА В СПИСКЕ
    def test_2_order_create_sell(self):
        driver = self.driver

        # переход во вкладку SELL, ввод числа токенов и кнопки PLACE SELL ORDER
        driver.find_element_by_xpath("//li[@id='t-SELL']").click()
        driver.find_element_by_xpath(
            "//form[@class='forms__box form__sell']//input[@placeholder='amount_']").send_keys("0.001")
        driver.find_element_by_xpath(
            "//button[@class='button sell']").click()

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

        # СДЕЛАТЬ ПРОВЕРКУ НА ПОЯВЛЕНИЕ ОРДЕРА В СПИСКЕ

    def test_3_order_execution(self):
        driver = self.driver

        # переход в ORDER BOOK
        driver.find_element_by_xpath("//li[@id='t-ORDERBOOK']").click()

        # выбор первого ордера в списке и нажатие кнопки исполнения ордера
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='spread'])[1]/following::div[6]").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='BNB'])[1]/following::button[1]").click()

        # ожидание окна Metamask'a и подтверждение транзакции
        while len(driver.window_handles) < 2:
            time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element_by_class_name('btn-green').click()
        driver.switch_to.window(driver.window_handles[0])

        # проверка, не высветилась ли ошибка
        try:
            self.assertFalse(driver.find_element_by_xpath(
                "(.//*[normalize-space(text()) and normalize-space(.)='SEND'])[2]/following::h3[1]").is_displayed())
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        self.assertFalse(driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='SEND'])[2]/following::div[1]").is_displayed())

        # проверка, высветилось ли сообщение об успешной сделке
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

        # переход в PERSONAL ORDER BOOK
        driver.find_element_by_xpath("//li[@id='t-PERSONAL OB']").click()

        # выбор первого ордера в списке и нажатие кнопки отмены ордера
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='FIAT'])[2]/following::div[6]").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='ADDRESS'])[1]/following::button[1]").click()

        # ожидание окна Metamask'a и подтверждение транзакции
        while len(driver.window_handles) < 2:
            time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element_by_class_name('btn-green').click()
        driver.switch_to.window(driver.window_handles[0])

        # проверка, не высветилась ли ошибка
        try:
            self.assertFalse(driver.find_element_by_xpath(
                "(.//*[normalize-space(text()) and normalize-space(.)='SEND'])[2]/following::h3[1]").is_displayed())
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        self.assertFalse(driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='SEND'])[2]/following::div[1]").is_displayed())

        # проверка, высветилось ли сообщение об успешной сделке
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

        # нажатие на кнопку авторизации
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Signup'])[1]/following::button[1]").click()

        # ожидание окна Metamask'a и осуществление подписи
        while len(driver.window_handles) < 2:
            time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        driver.find_elements_by_tag_name('BUTTON')[1].click()
        driver.switch_to.window(driver.window_handles[0])

        # ожидание появления панели ввода чата
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

        # нажатие кнопки регистрации, ввод будущего именя пользователя
        driver.find_element_by_xpath("//button[contains(text(),'Signup')]").click()
        driver.find_element_by_id("input").send_keys("name")
        driver.find_element_by_xpath("//button[@class='send-btn']").click()

        # ожидание окна Metamask'a и осуществление подписи
        while len(driver.window_handles) < 2:
            time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        driver.find_elements_by_tag_name('BUTTON')[1].click()
        driver.switch_to.window(driver.window_handles[0])

        # ожидание появления панели ввода чата
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

        # ожидание окна Metamask'a и осуществление подписи
        while len(driver.window_handles) < 2:
            time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        driver.find_elements_by_tag_name('BUTTON')[1].click()
        driver.switch_to.window(driver.window_handles[0])

        # ожидание появления панели ввода чата
        for i in range(self.IMPLICITLY_WAIT):
            try:
                if driver.find_element_by_id("input").is_displayed(): break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")

        # пользователь авторизирован, отправка сообщения
        driver.find_element_by_id("input").clear()
        test_Msg = 'test_Msg' + str(random.randint(0, 100))
        driver.find_element_by_id("input").send_keys(test_Msg)
        driver.find_element_by_xpath("//button[@class='send-btn']").click()
        time.sleep(1)

        # проверка сообщения
        last_Message = driver.find_elements_by_class_name("message")[
            len(driver.find_elements_by_class_name("message")) - 1].text
        if last_Message.find(test_Msg) == -1:
            self.fail("msg not found")

    def test_8_select_pair(self):
        driver = self.driver

        # выбор текущей пары из выпадающего списка
        driver.find_element_by_xpath("//div[@class='cur-pair']").click()
        time.sleep(0.5)
        driver.find_element_by_xpath("//a[contains(text(),'omg/eth')]").click()

        # проверка правильности отображения выбранной пары
        self.assertEqual("OMG,", driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='balances:'])[1]/following::span[2]").text)
        self.assertEqual("ETH", driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='omg,'])[1]/following::span[2]").text)

    def test_9_make_withdraw(self):
        driver = self.driver
        withdraw_money = 0.001

        # выбор пары и считывание текущего значения эфиров
        driver.find_element_by_xpath("//div[@class='cur-pair']").click()
        time.sleep(0.5)
        driver.find_element_by_xpath("//a[contains(text(),'bnb/eth')]").click()
        check_number_old = float(driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='bnb,'])[1]/following::span[1]").text)

        # переход к разделу MANAGE и выбор токена ETH
        driver.find_element_by_xpath("//li[@id='t-MANAGE']").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='bnb'])[4]/following::label[1]").click()

        # ввод значения и нажатие кнопки SEND, подтверждение всплывающего подтверждени я
        driver.find_element_by_xpath("//div[@class='form__sell__withdraw']//input[@placeholder='amount_']").send_keys(
            str(withdraw_money))
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='eth'])[5]/following::button[1]").click()
        driver.find_element_by_xpath("//button[@class='btn accept']").click()

        # ожидание окна Metamask'a и подтверждение транзакции
        while len(driver.window_handles) < 2:
            time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element_by_class_name('btn-green').click()
        driver.switch_to.window(driver.window_handles[0])

        check_number_new = check_number_old - withdraw_money

        # ожидание сообщения об корректности транзакции и ожидание изменения текущего счёта
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

        # выбор пары и считывание текущего значения эфиров
        driver.find_element_by_xpath("//div[@class='cur-pair']").click()
        time.sleep(0.5)
        driver.find_element_by_xpath("//a[contains(text(),'bnb/eth')]").click()
        check_number_old = float(driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='bnb,'])[1]/following::span[1]").text)

        # переход к разделу MANAGE и выбор токена ETH
        driver.find_element_by_xpath("//li[@id='t-MANAGE']").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='bnb'])[3]/following::label[1]").click()

        # ввод значения и нажатие кнопки SEND
        driver.find_element_by_xpath("//div[@class='form__sell__deposit']//input[@placeholder='amount_']").send_keys(
            str(deposit_money))
        driver.find_element_by_xpath(
            "//div[@class='form__sell__deposit']//button[@class='btn btn_deposit'][contains(text(),'SEND')]").click()

        # ожидание окна Metamask'a и подтверждение транзакции
        while len(driver.window_handles) < 2:
            time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element_by_class_name('btn-green').click()
        driver.switch_to.window(driver.window_handles[0])

        check_number_new = check_number_old + deposit_money

        # ожидание сообщения об корректности транзакции и ожидание изменения текущего счёта
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
    unittest.main()
