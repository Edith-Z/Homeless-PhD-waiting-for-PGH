# EdithZ
# This is for luckless guy on the CUHK PGH waiting list.
# It will check the PGH waiting list every day and send you a email if there is any update.
# I only wrote the female version.
# It is easy to modify to male version (delete 2 lines).

import time
import datetime
import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# Information of sender address
# If you use gmail, you should set "Less secure app access" first
# CUHK email address is not recommended as sender address
# for other email, refer to google or baidu, I'm not your mom
send_smtp = 'smtp.gmail.com'
send_port = 465
send_address = '12345678@gmail.com'
send_password = '******'
# Receiver address
receive_address = '1155000000@link.cuhk.edu.hk'
# CUHK SID
sid = 1155000000
N = 0
# N=1 if you want to see how many person left on the original waiting list
# save the original waiting list as "source.txt"

check_time = '18:00'    # It will check the waiting list this time every day
rest_t = 5  # loop gap

pgh_link = 'http://www.pgh.cuhk.edu.hk/announcements/2020/Pending.php'
start_line = '<tr><th bgcolor="blue"><font face="Arial, Helvetica, sans-serif" ' \
             'color="yellow">Student ID</font></th></tr>'
end_line = '</table>'
separate_line = '</font></td></tr>\n'


def Spider():
    pgh_page = requests.get(pgh_link).text
    start_place = pgh_page.find(start_line)
    pgh_page = pgh_page[start_place + len(start_line):]
    start_place = pgh_page.find(start_line, 3)  # Delete these 2 lines if you are male
    pgh_page = pgh_page[start_place + len(start_line):]  # Delete these 2 lines if you are male
    end_place = pgh_page.find(end_line)
    pgh_page = pgh_page[:end_place]
    pgh_list = pgh_page.split(separate_line)
    pgh_list = pgh_list[:-1]
    sid_list = []
    for i in pgh_list:
        sid_list.append(int(i[-10:]))
    return sid_list


def ListCompare(list1, list2):
    result1 = list(set(list1).difference(set(list2)))
    result2 = list(set(list2).difference(set(list1)))
    return [len(result1), result1, len(result2), result2]


def Send(info, n):
    str1 = [str(i) for i in info[1]]
    str2 = [str(i) for i in info[3]]
    str1 = '\n'.join(str1)
    str2 = '\n'.join(str2)
    smtp_obj = smtplib.SMTP_SSL(send_smtp, send_port)
    smtp_obj.login(send_address, send_password)
    msg_content = f'{info[0]} person(s) removed:\n{str1}\n\n{info[2]} person(s) added:\n{str2}\n'
    if N == 1:
        msg_content += f'\n{n} student(s) has(have) been removed from the original waiting list ' \
                       f'of {len(original_list)} students.\n'
    if sid in current_list:
        msg_content += f'\nYou are still on the waiting list.\n'
    else:
        msg_content += f'\nCongratulations!'
    msg = MIMEText(msg_content, 'plain', 'utf-8')
    msg['Subject'] = Header('Updates on waiting list', 'utf-8')
    msg['From'] = Header('Reminder of PGH', 'utf-8')
    smtp_obj.sendmail(send_address, receive_address, msg.as_string())


def Monitor():
    time_now = str(datetime.datetime.now())
    time_now = ''.join(time_now[11:16])
    if time_now == check_time:
        global current_list
        global former_list
        current_list = Spider()
        compare_info = ListCompare(former_list, current_list)
        if (compare_info[0] != 0) or (compare_info[2] != 0):
            remove_num = 0
            if N == 1:
                global original_list
                remove_num = ListCompare(original_list, current_list)
                remove_num = remove_num[0]
            Send(compare_info, remove_num)
            former_list = current_list
        time.sleep(90)


def LoopMonitor():
    while True:
        Monitor()
        time.sleep(rest_t)


original_list = []
if N == 1:
    f = open("source.txt")
    for line in f.readlines():
        if line.strip():
            original_list.append(int(line))

current_list = []
former_list = Spider()
LoopMonitor()
