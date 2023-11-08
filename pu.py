from bs4 import BeautifulSoup
from wxpusher import WxPusher
import requests
import re

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
'Connection': 'keep-alive',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Cookie': ''
}

# 爬取的页面数量
urllist = []
href_list = []
credit_list = []
credits_dic = {}
result_list = []

for i in range(1, 3):
    url = 'https://pocketuni.net/index.php?app=event&mod=School&act=board&sid=all&&p={page}'.format(page=i)
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    titles = [title.a.get_text() for title in soup.find_all('div', class_='hd_c_left_title b')]
    titles2 = soup.find_all('div', class_='hd_c_left_title b')
    credits = soup.find_all('div', class_='hd_c_left_school')

    for j in range(1): #对"标题：学时"进行格式化，并存储在字典中
        credit_list = []
        for credit in credits:
            match = re.search(r'学时：(\d+\.\d+)', credit.get_text())
            if match:
                credit = match.group(1)
                credit_list.append(credit)
        credits_dic_test = dict(zip(titles, credit_list))
        credits_dic.update(credits_dic_test)

    for j in range(len(titles2)): #获取所有活动页面链接
        href = titles2[j].a['href']
        text = titles2[j].a.text.strip()
        href_list.append(href)  # 将href保存到列表中

for href in href_list:
    information = requests.get(href, headers=headers)
    soup = BeautifulSoup(information.content, 'html.parser')
    title = soup.find('div', class_='content_hd_menu b').text.strip()

    organization_tag = soup.find('span', class_='b1', string='归属组织：')
    organization = organization_tag.next_sibling.strip() if organization_tag else ""

    category_tag = soup.find('span', class_='b1', string='活动分类：')
    category = category_tag.next_sibling.strip() if category_tag else ""

    location_tag = soup.find('span', class_='b1', string='活动地点：')
    location = location_tag.find_next('a').get('title') if location_tag else ""

    department_tag = soup.find('span', class_='b1 hh_attr_bor')
    department = department_tag.find_next('span').get('title') if department_tag else ""

    grade_tag = soup.find('span', class_='b1', string='活动年级：')
    grade = grade_tag.next_sibling.strip() if grade_tag else ""

    time_tag = soup.find('span', class_='b1', string='活动时间：')
    time = time_tag.next_sibling.strip() if time_tag else ""

    registration_tag = soup.find('span', class_='b1', string='报名起止：')
    registration = registration_tag.find_next('br').previous_sibling.strip() if registration_tag else ""

    outdoor_check_tag = soup.find('span', class_='b1', string='外勤打卡：')
    outdoor_check = outdoor_check_tag.next_sibling.strip() if outdoor_check_tag else ""

    participants_tag = soup.find('span', class_='b1', string='参加人数：')
    participants = participants_tag.next_sibling.strip() if participants_tag else ""

    remaining_slots_tag = soup.find('span', class_='b1', string='剩余名额：')
    remaining_slots = remaining_slots_tag.next_sibling.strip() if remaining_slots_tag else ""

    contact_tag = soup.find('span', class_='b1', string='联系方式：')
    contact = contact_tag.find_next('a').get('title') if contact_tag else ""

    if (department == '全部' or department == '电气信息工程学院') and credits_dic.get(title, 0) >= '6.00':
        """print(f"标题：{title}")
        print(f'学时数量：{credits_dic.get(title)}')
        print(f"活动院系：{department}")
        print(f"活动时间：{time}")
        print(f"报名起止：{registration}")
        print(f"活动分类：{category}")
        print(f"活动地点：{location}")
        print(f"外勤打卡：{outdoor_check}")
        print(f"参加人数：{participants}  剩余名额：{remaining_slots}\n\n")"""
        result = f'\n标题：{title}\n学时数量：{credits_dic.get(title)}\n活动院系：{department}\n活动时间：{time}\n' \
                 f'报名起止：{registration}\n活动地点：{location}\n外勤打卡：{outdoor_check}\n' \
                 f'参加人数：{participants}  剩余名额：{remaining_slots}\n------------------------------------------------------------------'
        result_list.append(result)

str1 = ''
for str2 in result_list:
    str1 = str1 + str2.strip()

WxPusher.send_message(str1,
              uids=[''],
              topic_ids=[''],
              token='')
