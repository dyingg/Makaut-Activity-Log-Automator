import pandas as d
import datetime
import requests

from procedure.init import prepare_session


# token = "agd0bwhakCxhWcEQwaGYIKiCyaPURGI65spX1rIm"
# student_code = "TS0148717"
sub_codes = {
    "PCC CS 401" : "SU00016086",
    "PCC CS401": "SU00016086",
    "PCC CS404": "SU00016089",
    "PCC CS 402": "SU00016087",
    "PCC CS-402": "SU00016087",
    "PCC CS-403": "SU00016088",
    "MC-401" : "SU00016091",
    "MC401" : "SU00016091",
    "MC 401" : "SU00016091",
    "PCC CS 492": "SU00016092"
}

teachers = {
    "Shahana Sengupta": "182111",
    "Kamalesh Karmakar" : "176357",
    "Shikha Nayak": "177130",
    "Soumya Suvra Khan": "180911",
    "Dr.Debasish De": "181038",
    "Dr Subrata Kr Debnath": "178987",
    "Dr.Subrata Kr. Debnath": "178987",
    "Sayan Das" : "178677",
    "Mr.Sayan Das" : "178677",
    "Rianka Dalal":"181365"
}

def get_date(date):
    date_time_obj = ""
    if "2020" in date:
        date_time_obj = datetime.datetime.strptime(date, '%d/%m/%Y')
    else:
        date_time_obj = datetime.datetime.strptime(date, '%d/%m/%y')
    return str(date_time_obj).split(" ")[0]

def get_time(time):
    flag = False
    if 'p' in time or 'P' in time:
        flag = True

    hh = time.split(':')[0]
    if len(hh) > 2:
        hh = time.split('.')[0]
        mm = time.split('.')[1][:2]
    else:
        mm = time.split(':')[1][:2]
    
    if flag:
        hh = int(hh) + 12

    if hh >= 24:
        hh = 12
    hh = str(hh)
    return "%s:%s" % (hh, mm)


def gen_week(str):
    fields = str.split(" ")
    week_code = fields[1].split('\r\n')[0].zfill(2)
    return "1"+week_code

def gen_teacher_code(code): 
    if code in teachers:
        return teachers[code]
    
    return "NULL"

def gen_subject_code(code): 
    if code in sub_codes:
        return sub_codes[code]
    
    return "NULL"

def save_data(handle, index, data, student_code, token):
    url = "https://makaut1.ucanapply.com/smartexam/public/student/save-week-report-activity"
    week = gen_week(data[0])
    date = data[1]
    sem_code = "SM04"
    course_code = "C000024"
    subject_code = gen_subject_code(data[4])
    topic = data[5].strip()
    platform_used = data[6].strip()
    teacher = gen_teacher_code(data[7].strip())
    date = get_date(data[8].strip())
    time = get_time(data[9].strip())
    lecture_link = str(data[10]).strip() 
    duration = str(data[11]).strip() 
    post_class = str(data[12]).strip() 
    asgn_recv = str(data[13]).strip()
    asgn_sub = str(data[14]).strip()
    test = data[15].strip()


    if(subject_code == "NULL"):
        if(teacher == "176357"):
            subject_code = "SU00016093"


#     headers= {
# "Origin": "https://makaut1.ucanapply.com",
# "Content-Type": "application/x-www-form-urlencoded",
# "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36",
# "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
# "Sec-Fetch-Site": "same-origin",
# "Sec-Fetch-Mode": "navigate",
# "Sec-Fetch-User": "?1",
# "Sec-Fetch-Dest": "document",
# "Referer": "https://makaut1.ucanapply.com/smartexam/public/student/week-report-activity/create",
# "Accept-Encoding": "gzip, deflate, br",
# "Accept-Language": "en-US,en;q=0.9",
# "Cookie": "PHPSESSID=7cvgvkr6bjqa1kt9e55kqr1qr4; XSRF-TOKEN=eyJpdiI6IkMycVNsdXJVVE1SRTRLY29DaXUwd0E9PSIsInZhbHVlIjoiNlhOdUNJMXB1eHVOdjZyTW5GUHdtRHZGMGhoZGx0SDJNVXFQS3BDVFpEbjcrN3hLZW9MZ3ZHejZrMlJJQ245KyIsIm1hYyI6ImU1NmZhMGE5MmEwNDQ3ZDI4MmNkMWNhMmJmMTI4NGUwZjRhNTJjM2VjYzBmYzdkYjE2ZDYwMGU1NzA0NDQ4ZTYifQ%3D%3D; maulana_abul_kalam_azad_university_of_technology_session=eyJpdiI6ImpZczdudDlSS1RHd0pBNEJheWZGVlE9PSIsInZhbHVlIjoiY28yTCt1SmZNYUFURXRjckFMUE9XMHBLVGZEYUVmemRMNjBvZGswbUE1T0FcL1RuSHhcLzgxN2FnYjlXd1JXemtXIiwibWFjIjoiNWJhOGI3ZDY3MzVkZTQ4MGU1Y2Y3Yzc1ODQ1ODlhNWUwNTE0OTI5NWI2NjVjOGQ5ZDM1OGRmNGFiZGM5MWE3NyJ9"
#     }


    data =  {
        "_token": token,
        "week":week,
        "SEMCODE": sem_code,
        "COURSECD": course_code,
        "SUBJECTCODE": subject_code,
        "topic_covered": topic,
        "platform_used": platform_used,
        "class_taken_by": teacher,
        "date_tme": "%s %s" % (date, time),
        "record_lecture_upload_link": lecture_link,
        "duration_in_min": duration,
        "post_class_interraction_note": post_class,
        "assignment_received": asgn_recv,
        "assignment_submitted": asgn_sub,
        "test_attended_if_any": test,
        "daily_self_acitvity": "/",
        "remark": "/",
        "id": "",
        "subject_id": "",
        "studentcode": student_code,
        "session": "SE10"
    }
    
    print(data)
    for k in data.keys():
        if(data[k] == "nan"):
            data[k] = "N/A"

    
    # x = handle.post(url,
    # data= data
    # # headers = headers
    # )
    print("Attendance logged for %s on %s" %  (topic, date))
   
username = "YOUR USERNAME"
password = "YOUR PASSWORD"
name = "YOUR NAME"

df = d.read_csv("data.csv")
try:
    att = list(df[name])
    data = df.to_numpy()
    s = requests.Session()
    [token, studentcode] = prepare_session(s, username, password)
    for index,w in enumerate(data):
        if(att[index] != 'A'):
            save_data(s, index, w[:16], studentcode, token)
except KeyError:
    print("[ERR] No student exists with that name in csv [ERR]")




