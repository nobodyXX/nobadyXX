from selenium import webdriver
from time import sleep


def print1(s, i):
    print(s)
    for n in range(i):
        print()


'''大物实验有具体成绩'''
'''窗口最大化，有的电脑不是1808*1920的'''
print("          平均成绩计算器")
print1("程序提示输入密码是为了登录教务处查询成绩，任何人不会获得你的密码。", 1)
print1("源代码已上传至Github，卑微求赞", 1)
print1("在这个程序写到一半的时候发现上线了绩点分析功能，但是程序完成的时候教务处又下架了这个功能。如果教务处的绩点分析功能一直没恢复，本程序会添加每学期的绩点分析、图形界面和其他功能", 1)
print1("后续会在Github发布选课小助手和自动评教的程序，为各位同学节省宝贵的时间", 1)
print1("菜鸡小高，在线求赞:", 1)
name = input("请输入学号/手机号/NetID:")
password = input("请输入密码:")
ch = input("是否统计通识类选修/核心课(y/n):")
print1("", 3)

browser = webdriver.Chrome(executable_path='chromedriver.exe')
browser.set_window_size(1920, 1080)
browser.get("http://ehall.xjtu.edu.cn")
print1("浏览器已启动", 2)
sleep(2)
browser.find_element_by_xpath('//*[@id="ampLoginBtn"]').click()  # 选择账号密码登录
browser.implicitly_wait(2)
browser.find_element_by_name("username").send_keys(name)  # 输入账户密码
browser.find_element_by_name("pwd").send_keys(password)
browser.find_element_by_xpath('//*[@id="account_login"]').click()  # 登录按钮
sleep(8)
print1("登录成功", 2)
browser.find_element_by_xpath('//*[@amp-id="allCanUseApps"]').click()  # 全部应用
sleep(2)
browser.find_element_by_xpath('//*[@amp-appid="4768574631264620"]').click()  # 成绩查询
browser.implicitly_wait(5)
browser.find_element_by_xpath('//*[@id="ampDetailEnter"]').click()  # 进入服务
current_window = browser.current_window_handle  # 当前窗口句柄
all_handles = browser.window_handles  # 获所有窗口句柄
for handle in all_handles:
    if handle != current_window:
        browser.switch_to.window(handle)
        print1("窗口已切换", 2)
try:
    browser.find_element_by_xpath('//*["学生组"]').click()
except:
    print()
browser.implicitly_wait(30)
browser.find_element_by_xpath('/html/body/main/article/section/div[3]/div/div[1] /ul/li[2]').click()  # 全部成绩
# 人傻了，上面这条id是动态的

browser.implicitly_wait(10)
table = browser.find_element_by_xpath('//*[@id="tabledqxq-index-table"]')
table1 = browser.find_element_by_xpath('//*[@id="tableqb-index-table"]')
# tr = table.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
# td = tr[1].find_elements_by_tag_name('td')
# a = td[0].find_element_by_tag_name('a')
# print("a",a.get_attribute("data-kcm"))
# print(len(tr))
element = browser.find_element_by_xpath('//*[@id="row0dqxq-index-table"]/td[1]/a')
# 完整路径，用chrome-检查-copy-copy full xpath
# /html/body/main/article/section/div[3]/div/div[2]/div[1]/section/div/div[2]/div/div[4]/div[2]/div/table[2]/tbody/tr[2]/td[1]/a
td_content = element.get_attribute("data-kcm")
# 快写哭了，看了官方文档以后终于试出来了，网上就没个能用的教程，还有教务处的网页也够奇葩
grades = []


def get_ls(table):
    ls, grade = [], []
    for tr in table.find_elements_by_tag_name('tr'):
        td_a = tr.find_elements_by_tag_name('td')[0].find_element_by_tag_name('a')  # 二条及以上记录
        for s in ["data-kcm", "data-xf", "data-zcj", "data-xfjd", "data-jxbid"]:
            ls.append(td_a.get_attribute(s))
        grade.append(ls)
        ls = []
    return grade


pre_page_ls = table.find_elements_by_tag_name('tr')[0].find_elements_by_tag_name('td')[0].find_element_by_tag_name(
    'a').get_attribute("data-kcm")
grades = grades + get_ls(table)
grades = grades + get_ls(table1)
print1("已查询到成绩!", 2)

while grades[len(grades) - 20][0] != pre_page_ls[0] and len(table.find_elements_by_tag_name('tr')) == 10:
    browser.implicitly_wait(10)
    browser.find_element_by_xpath('//*[@id="pagerqb-index-table"]/div/div/div[1]/a[2]').click()  # 翻页
    sleep(2)
    table = browser.find_element_by_xpath('//*[@id="pinnedtableqb-index-table"]')  # 爬取当前页表格
    next_page_ls = table.find_elements_by_tag_name('tr')[0].find_elements_by_tag_name('td')[0].find_element_by_tag_name(
        'a').get_attribute("data-kcm")
    grades = grades + get_ls(table)
    table1 = browser.find_element_by_xpath('//*[@id="pinnedtabledqxq-index-table"]')  # 爬取隐藏表格，我是sb，这么多天才发现教务处少显示了几十门课的成绩
    grades = grades + get_ls(table1)

table = browser.find_element_by_xpath('//*[@id="pinnedtableqb-index-table"]')  # 爬取当前页表格
grades = grades + get_ls(table)
table1 = browser.find_element_by_xpath('//*[@id="pinnedtabledqxq-index-table"]')  # 爬取隐藏表格，我是sb，这么多天才发现教务处少显示了几十门课的成绩
grades = grades + get_ls(table1)

courses, grades1 = [], []
for i in grades:  # 去重
    if i[0] not in courses:
        courses.append(i[0])
        grades1.append(i)

# 成绩get，剩下的就简单了
# 人傻了，上条注释是两小时以前写的，现在成绩还是没get
# 距上条注释差不多一小时，翻页后表格的Xpath和第一页不一样

grades1.insert(0, ["课程名", "学分", "成绩", "绩点", "课程号"])

ave_score, gpa, discount_course, no_score, l, credit_ave, credit_gpa, discount_ave_score, discount_gpa= 0.0, 0.0, [], [], [], 0.0, 0.0, 0.0, 0.0

for i in range(1, len(grades1)):
    if ch in ["n", "no", "N", "No", "NO"]:
        if grades1[i][4][9:13] in ["GNED", "CORE"]:
            discount_course.append(grades1[i])
            l.append(i)
            discount_ave_score += float(grades1[i][1])*float(grades1[i][2])
            discount_gpa += float(grades1[i][1]) * float(grades1[i][3])
        else:
            credit_gpa += float(grades1[i][1])
    else:
        credit_gpa += float(grades1[i][1])

for i in range(1, len(grades1)):
    try:
        float(grades1[i][2])
        ave_score += float(grades1[i][2])*float(grades1[i][1])
        gpa += float(grades1[i][3])*float(grades1[i][1])
    except:
        gpa += float(grades1[i][3]) * float(grades1[i][1])
        no_score.append(grades1[i])

for i in range(len(no_score)):
    gpa += float(no_score[i][3])*float(no_score[i][1])

s = "0123456789 abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-"
for i in grades1:
    c = [0, 0]
    for ss in i[0]:  # 对齐,汉字与空格的宽度约为5:9
        if ss in s:
            c[0] += 1
        else:
            c[1] += 1
    i[0] = i[0] + " "*(30 - c[0] - c[1]*9//5)
    print("{}{: <6s}{: <6s}{: <6s}".format(i[0], i[1], i[2], i[3]))

for i in discount_course:
    c = [0, 0]
    for ss in i[0]:  # 对齐,汉字与空格的宽度约为5:9
        if ss in s:
            c[0] += 1
        else:
            c[1] += 1
    i[0] = i[0] + " "*(15 - c[0] - c[1]*9//5)

no_score_credit = 0.0
if no_score:  # no_score != []有错误，[]等价与false
    for i in no_score:
        no_score_credit += float(i[1])
        print("平均成绩未统计科目:")
        print(i[0:5])

ave_score -= discount_ave_score
gpa -= discount_gpa
ave_score /= (credit_gpa - no_score_credit)
gpa /= credit_gpa

print1("", 2)
print1("平均成绩：{:.3f}，平均绩点：{:.3f}".format(ave_score, gpa), 2)
if ch in ["n", "no", "N", "No", "NO"]:
    for i in discount_course:
        print("没统计选修/核心课: {},学分:{},成绩:{},绩点:{}".format(i[0], i[1], i[2], i[3]))


print("运行结束")
