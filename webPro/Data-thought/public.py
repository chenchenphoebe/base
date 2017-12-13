#-*- coding:utf-8 -*-
class Login():
    def user_login(self, driver, username, password):
        driver.switch_to.frame('x-URS-iframe')
        driver.find_element_by_name("email").clear()
        driver.find_element_by_name("email").send_keys("username")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("password")
        driver.find_element_by_id("dologin").click()