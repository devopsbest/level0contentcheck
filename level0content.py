import re

import requests

# session = None
# token = None

media_url = []
fail_media_url_list = []


def login():
    url = "http://staging.englishtown.cn/services/api/mobile/service/login"
    data = {
        "serviceRequest": {
            "appVersion": "2.0.2",
            "password": "1",
            "platform": "Android",
            "productId": 4,
            "unifiedLogin": True,
            "userName": "stestc637"
        }
    }

    result = requests.post(url=url, json=data)

    session = result.json()["serviceResponse"]["sessionId"]
    token = result.json()["serviceResponse"]["token"]
    return session, token


def get_course(session, token, id):
    url = "http://staging.englishtown.cn/services/api/mobile/service/activitycontent"
    data = {
        "serviceRequest": {
            "activities": [id],
            "countrycode": "cn",
            "partnercode": "Cool",
            "siteVersion": "development",
            "appVersion": "2.0.2",
            "culturecode": "zh-CN",
            "platform": "Android",
            "productId": 4,
            "sessionId": session,
            "token": token,
            "unifiedLogin": True
        }
    }

    result = requests.post(url=url, json=data)
    if result.status_code == 200:
        match_path = re.compile("('|\")\w+Path('|\"):\s('|\")((http|https):\/\/.*?)('|\")", re.IGNORECASE)
        url_list = match_path.findall(str(result.json()))
        # print(str(result.json()))

        urls = [y for x in url_list for y in x if y.endswith((".mp3", ".mp4", ".jpg"))]

        media_url.append(urls)


def check_resource(url):
    pattern = re.compile(r'http:\/\/+(.*).[(mp3)|(mp4)|(jpg)]$', re.IGNORECASE)

    url_status = 0
    # print(url)

    if re.search(pattern, url):
        try:
            status = requests.head(url, allow_redirects=False).status_code
            if status != 200:
                fail_media_url_list.append(url)
                url_status += 1

        except:

            fail_media_url_list.append(url)
            url_status += 1

    else:
        fail_media_url_list.append(url)
        url_status += 1

    return url_status


activity_ids = []


# def get_activity_id():
#     with open("/Users/anderson/Downloads/lzero1.json", 'r') as f:
#         lines = f.readlines()
#
#     for line in lines:
#         searchObj = re.search("\"activityId\": (\d+)", line, re.M | re.I)
#
#         if searchObj:
#             activity_ids.append(searchObj.group(1))

def get_activity_id(session, token):
    url = "http://staging.englishtown.cn/services/api/mobile/service/coursestructure"
    data = {
        "serviceRequest": {
            "level": 20001126,
            "countrycode": "cn",
            "partnercode": "Socn",
            "siteVersion": "1-1",
            "appVersion": "2.0.2",
            "culturecode": "zh-CN",
            "platform": "Android",
            "productId": 4,
            "sessionId": session,
            "token": token,
            "unifiedLogin": True
        }
    }
    result = requests.post(url=url, json=data)

    print(result.text)


    seo = re.compile("\"activityId\":(\d+)")

    searchObj = seo.findall(result.text)

    if searchObj:
        activity_ids.append(searchObj)


#
# if __name__ == "__main__":
#
#     get_activity_id()
#     if activity_ids != []:
#
#         session, token = login()
#         for id in activity_ids:
#             get_course(session, token, int(id))
#
#         # print(media_url)
#
#         urls = [y for x in media_url for y in x]
#
#         # print(urls)
#         print(len(urls))
#
#         if urls != []:
#             for url in urls:
#                 check_resource(url)
#
#         else:
#             print("please check your activity")
#
#         from collections import Counter
#
#         print(Counter(urls).most_common(20))
#
#         if len(fail_media_url_list)>0:
#             print(len(fail_media_url_list))
#             print(fail_media_url_list)


if __name__ == "__main__":

    session, token = login()

    get_activity_id(session, token)

    print(activity_ids)
    if activity_ids != []:
        print("success")
        for id in activity_ids[0]:
            get_course(session, token, int(id))

        urls = [y for x in media_url for y in x]

        print(len(urls))

        if urls != []:
            for url in urls:
                check_resource(url)

        else:
            print("please check your activity")

        from collections import Counter

        print(Counter(urls).most_common(20))

        if len(fail_media_url_list) > 0:
            print(len(fail_media_url_list))
            print(fail_media_url_list)
