# -*- coding: utf-8 -*-

__author__ = 'hanbei'
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from Base_Page import BasePage
from selenium.webdriver.common.action_chains import ActionChains



class Create_Plan(BasePage):
    # 定位器
    test_plan_manage_loc = (By.LINK_TEXT,u"测试计划管理")
    MTBF_plan_loc = (By.XPATH, "//li[4]/ul/li[3]/a/span")
    Feature_plan_loc = (By.LINK_TEXT, u"Feature测试计划")
    add_plan_loc = (By.CSS_SELECTOR, "#addBtn>span.glyphicon.glyphicon-plus")
    MTBF_plan_name_loc = (By.NAME, "planName")
    SW_version_loc = (By.CSS_SELECTOR, "input.select2-search__field")
    perso_loc = (By.CSS_SELECTOR,"#persoDiv>div>span>span.selection>span>ul>li>input")
    tester_loc = (By.CSS_SELECTOR, "#editForm>div>div.box-body>div:nth-child(17)>div>input")
    tester_email_loc = (By.CSS_SELECTOR, "#editForm>div>div.box-body>div:nth-child(18)>div>input")
    report_loc = (By.NAME, "isSendreport")
    recipient_email_loc = (By.NAME, "recipientEmail")
    cc_email_loc = (By.NAME, "ccEmail")
    email_theme_loc = (By.NAME, "emailSubject")
    email_content_loc = (By.NAME, "emailContent")
    save_plan_loc= (By.CSS_SELECTOR, "#saveBtn>span.lang")
    comfirm_loc = (By.LINK_TEXT, u"确定")

    #点击测试计划管理
    def click_plan_manage(self):
        self.find_element(*self.test_plan_manage_loc).click()


    #点击MTBF测试计划
    def click_MTBF_plan(self):
        self.find_element(*self.MTBF_plan_loc).click()

    #点击Feature测试计划
    def click_Feature_plan(self):
        self.find_element(*self.Feature_plan_loc).click()

    #点击新增按钮
    def click_add_icon(self):
        self.find_element(*self.add_plan_loc).click()

    #输入测试计划名称
    def input_plan_name(self, MTBFPlanName):
        self.find_element(*self.MTBF_plan_name_loc).send_keys(MTBFPlanName)

    #输入软件版本
    def input_SW_version(self,software_version):
        self.find_element(*self.SW_version_loc).send_keys(software_version)
        self.find_element(*self.SW_version_loc).send_keys(Keys.ENTER)

    #输入perso号
    def input_perso_version(self, perso):
        self.find_element(*self.perso_loc).send_keys(perso)
        self.find_element(*self.perso_loc).send_keys(Keys.ENTER)

    #测试人员
    def tester(self,tester_name):
        self.find_element(*self.tester_loc).clear()
        self.find_element(*self.tester_loc).send_keys(tester_name)

    #测试人员邮箱
    def tester_email(self, tester_email):
        self.find_element(*self.tester_email_loc).clear()
        self.find_element(*self.tester_email_loc).send_keys(tester_email)

    #是否发送测试报告
    def test_report(self):
        var = Select(self.find_element(*self.report_loc))
        var.select_by_visible_text(u"是")

    #设置收件人
    def recipient_email(self,recipient):
        self.find_element(*self.recipient_email_loc).send_keys(recipient)

    #设置收件邮箱
    def cc_email(self,cc_email):
        self.find_element(*self.cc_email_loc).send_keys(cc_email)

    #邮件主题
    def email_subject(self,subject):
        self.find_element(*self.email_theme_loc).send_keys(subject)

    #邮件内容
    def email_content(self,content):
        self.find_element(*self.email_content_loc).send_keys(content)

    #点击保存
    def save_plan(self):
        self.find_element(*self.save_plan_loc).click()

    #新增成功，点击确定按钮
    def confirm(self):
        self.find_element(*self.comfirm_loc).click()

















