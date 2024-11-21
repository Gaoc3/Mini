import requests
from bs4 import BeautifulSoup
import json
import re

# بيانات الدخول
def extract_quality(textes):
  los = []
  for text in textes:
    match = re.search(r'(\d{3,4})p', text['resolution'])
    if match:
      los.append(int(match.group(1)))
  return sorted(los)
# الرؤوس

def get_res(video_id):
    
    headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ar,en-GB;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6,en-US;q=0.5',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://yt1d.com',
    'priority': 'u=1, i',
    'referer': 'https://yt1d.com/en11/',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    }  
      
    # البيانات
    data = {
        'url': f'https://youtu.be/watch?v={video_id}',
        'ajax': '1',
        'lang': 'en',
    }

    # الطلب

    response = requests.post('https://yt1d.com/mates/en/analyze/ajax', headers=headers, data=data)

    # تحليل الرد JSON
    response_json = response.json()
    html_content = response_json.get('result', '')
    # print(html_content)

    # استخدام BeautifulSoup لتحليل الكود HTML المستخرج
    soup = BeautifulSoup(html_content, 'html.parser')

    # البحث عن الأزرار باستخدام الصنف المحدد
    tables = soup.find('table', class_='table table-bordered table-hover table-responsive-sm')
    # print(tables.td)

    # استخراج قيم onclick وتحويلها إلى قاموس باستخدام التعبيرات العادية
    downloads = []
    
    resolutions = set()  # استخدام مجموعة للتأكد من الفريدات
    
    if tables:
        td_elements = tables.find_all('td')
        for td in td_elements:
            text = td.get_text(strip=True)
            if 'p60' in text or '360p' in text or '(.mp4)' in text:
                resolutions.add(text)
    
    # تحويل المجموعة إلى قائمة مع عرض النتائج
    data = [{'resolution': res} for res in resolutions]
    
    return data

def send_request(video_id,res):
    
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'ar,en-GB;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6,en-US;q=0.5',
        'origin': 'https://loader.to',
        'priority': 'u=1, i',
        'referer': 'https://loader.to/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

    params = {
        'start': '1',
        'end': '1',
        'format': res,
        'url': f'https://www.youtube.com/watch?v={video_id}',
    }

    response = requests.get('https://ab.cococococ.com/ajax/download.php', params=params, headers=headers)
    return response.json()

def get_progress(id):

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'ar,en-GB;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6,en-US;q=0.5',
        'origin': 'https://loader.to',
        'priority': 'u=1, i',
        'referer': 'https://loader.to/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

    params = {
        'id': id,
    }

    response = requests.get('https://p.oceansaver.in/ajax/progress.php', params=params, headers=headers)
    return response.json()
def get_bytes(url):
    bytees = requests.get(url).content
    return bytees


'''
    #send_request
        {
            "success": true,
            "id": "5mGEI5q1EktK5ueqtm76xiH",
            "content": "CiAgICAgICAgPGRpdiBpZD0iY2FyZC01bUdFSTVxMUVrdEs1dWVxdG03NnhpSCIgY2xhc3M9ImRvd25sb2FkLWNhcmQgbXgtYXV0byBiZy13aGl0ZSByb3VuZGVkLXhsIHNoYWRvdy1tZCBvdmVyZmxvdy1oaWRkZW4gZmxleCI+CiAgICAgICAgICAgIDxkaXYgY2xhc3M9Im1kOmZsZXggZmxleCI+CiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPSJtZDpmbGV4LXNocmluay0wIj4KICAgICAgICAgICAgICAgICAgICA8aW1nIGNsYXNzPSJoLTQ4IG9iamVjdC1jb3ZlciBtZDp3LTQ4IiBzcmM9Imh0dHBzOi8vaS55dGltZy5jb20vdmkvV1NPMDBJZy1STmMvaHFkZWZhdWx0LmpwZyI+CiAgICAgICAgICAgICAgICA8L2Rpdj4KICAgICAgICAgICAgICAgIDxkaXYgY2xhc3M9InAtOCBmbGV4Ij4KICAgICAgICAgICAgICAgIDxkaXYgY2xhc3M9InVwcGVyY2FzZSBwYi0xIG92ZXJmbG93IHRyYWNraW5nLXdpZGUgdGV4dC1zbSB0ZXh0LWluZGlnby01MDAgZm9udC1zZW1pYm9sZCI+2YXYrdmF2K8g2KfZhNmB2YTYp9it2YogLSDZhNit2LjYqSDZhtiv2YUgMjAyNCBNb2hhbWVkIEFsZmxhaGkgLSBMYWhkdCBOYWRtIHwgPHNtYWxsPjxhIGhyZWY9Imh0dHBzOi8vd3d3LnlvdXR1YmUuY29tL3dhdGNoP3Y9V1NPMDBJZy1STmMiIHRhcmdldD0iX2JsYW5rIiByZWw9Im5vb3BlbmVyIG5vcmVmZXJyZXIgbm9mb2xsb3ciPjxzdHJvbmc+VmlkZW88L3N0cm9uZz48L2E+IC0gTVA0IDcyMHAgLSAxIHRvIDEgfCA8YSBocmVmPSJodHRwczovL3d3dy5ieWNsaWNrZG93bmxvYWRlci5jb20vSG93LXRvLWRvd25sb2FkLXlvdXR1YmUtcGxheWxpc3RzLnBocD9zb3VyY2U9bG9hZGVyMiZpbm5lcnBhZ2U9cGxheWxpc3QiIG9uY2xpY2s9Imd0YWcoJ2V2ZW50JywgJ2FkX2J5Y2xpY2tfcGxheWxpc3QnLCB7J2V2ZW50X2NhdGVnb3J5JyA6ICdhZCcsJ2V2ZW50X2xhYmVsJyA6ICdieWNsaWNrX3BsYXlsaXN0J30pOyIgdGFyZ2V0PSJfYmxhbmsiIHJlbD0ibm9vcGVuZXIgbm9yZWZlcnJlciBub2ZvbGxvdyI+PHN0cm9uZz5Eb3dubG9hZCBiaWcgcGxheWxpc3Qgd2l0aCBtb3JlIHRoYW4gMjAgdmlkZW9zPC9zdHJvbmc+PC9hPjwvc21hbGw+PC9kaXY+CiAgICAgICAgICAgICAgICAgICAgPGRpdiBjbGFzcz0icHJvZ3Jlc3MiPgogICAgICAgICAgICAgICAgICAgICAgICA8ZGl2IHN0eWxlPSJ3aWR0aDoxMDAlIiBjbGFzcz0icHJvZ3Jlc3MtYmFyIiBpZD0iNW1HRUk1cTFFa3RLNXVlcXRtNzZ4aUhfcHJvZ3Jlc3MiPjEwMCU8L2Rpdj4KICAgICAgICAgICAgICAgICAgICA8L2Rpdj4KICAgICAgICAgICAgICAgICAgICA8YSBvbmNsaWNrPSJ3aW5kb3cub3BlbignaHR0cHM6Ly9jb252ZXJ0ci5vcmcnLCAnX2JsYW5rJyk7Z3RhZygnZXZlbnQnLCAnYWRfY29udmVydHInLCB7J2V2ZW50X2NhdGVnb3J5JyA6ICdhZCcsJ2V2ZW50X2xhYmVsJyA6ICdhZF9jb252ZXJ0cid9KTsiIGhyZWY9IiMiIGRpc2FibGVkIGlkPSI1bUdFSTVxMUVrdEs1dWVxdG03NnhpSF9kb3dubG9hZExpbmsiIGRvd25sb2FkPgogICAgICAgICAgICAgICAgICAgICAgICA8YnV0dG9uIGRpc2FibGVkIGlkPSI1bUdFSTVxMUVrdEs1dWVxdG03NnhpSF9kb3dubG9hZEJ1dHRvbiIgY2xhc3M9InN0cm9uZyI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8ZGl2IGlkPSI1bUdFSTVxMUVrdEs1dWVxdG03NnhpSF9sb2FkaW5nSWNvbiIgY2xhc3M9ImxvYWRlciI+PC9kaXY+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8c3ZnIGlkPSI1bUdFSTVxMUVrdEs1dWVxdG03NnhpSF9kb3dubG9hZEljb24iIHN0eWxlPSJkaXNwbGF5Om5vbmU7IiB3aWR0aD0iMWVtIiBoZWlnaHQ9IjFlbSIgdmlld0JveD0iMCAwIDE2IDE2IiBjbGFzcz0iYmkgYmktZG93bmxvYWQiIGZpbGw9ImN1cnJlbnRDb2xvciIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik0uNSA5LjlhLjUuNSAwIDAgMSAuNS41djIuNWExIDEgMCAwIDAgMSAxaDEyYTEgMSAwIDAgMCAxLTF2LTIuNWEuNS41IDAgMCAxIDEgMHYyLjVhMiAyIDAgMCAxLTIgMkgyYTIgMiAwIDAgMS0yLTJ2LTIuNWEuNS41IDAgMCAxIC41LS41eiIvPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxwYXRoIGZpbGwtcnVsZT0iZXZlbm9kZCIgZD0iTTcuNjQ2IDExLjg1NGEuNS41IDAgMCAwIC43MDggMGwzLTNhLjUuNSAwIDAgMC0uNzA4LS43MDhMOC41IDEwLjI5M1YxLjVhLjUuNSAwIDAgMC0xIDB2OC43OTNMNS4zNTQgOC4xNDZhLjUuNSAwIDEgMC0uNzA4LjcwOGwzIDN6Ii8+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3N2Zz4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIERvd25sb2FkCiAgICAgICAgICAgICAgICAgICAgICAgIDwvYnV0dG9uPgogICAgICAgICAgICAgICAgICAgIDwvYT4KICAgICAgICAgICAgICAgICAgICA8YSBpZD0idmVlZC01bUdFSTVxMUVrdEs1dWVxdG03NnhpSCIgaHJlZj0iaHR0cHM6Ly9jb252ZXJ0ci5vcmciIG9uY2xpY2s9Imd0YWcoJ2V2ZW50JywgJ2FkX3ZlZWRfaW8nLCB7J2V2ZW50X2NhdGVnb3J5JyA6ICdhZCcsJ2V2ZW50X2xhYmVsJyA6ICd2ZWVkX2lvJ30pOyIgdGFyZ2V0PSJfYmxhbmsiIHJlbD0ibm9vcGVuZXIgbm9yZWZlcnJlciBub2ZvbGxvdyI+PHN0cm9uZyBzdHlsZT0ibWF4LXdpZHRoOiA4MCU7ZGlzcGxheTogYmxvY2s7bWFyZ2luLWxlZnQ6IGF1dG87bWFyZ2luLXJpZ2h0OiBhdXRvO3RleHQtYWxpZ246IGNlbnRlcjsiPlRoYW5rcyBmb3IgZG93bmxvYWRpbmcgeW91ciB2aWRlby4gWW91IGNhbiBub3cgY29udmVydCB5b3VyIHZpZGVvIGZvciBmcmVlIG9ubGluZSBoZXJlPC9zdHJvbmc+PC9hPgogICAgICAgICAgICAgICAgPC9kaXY+CiAgICAgICAgICAgIDwvZGl2PgogICAgICAgIDwvZGl2PgogICAgICAgIDxkaXY+PHNjcmlwdCBkYXRhLWNmYXN5bmM9ImZhbHNlIiBhc3luYyB0eXBlPSJ0ZXh0L2phdmFzY3JpcHQiIHNyYz0iLy9ob29mc2R1a2UuY29tL3RRUThGQ0tYSFR4cDQvODA2NjIiPjwvc2NyaXB0PjwvZGl2PiAKICAgIA==",
            "title": "\u0645\u062d\u0645\u062f \u0627\u0644\u0641\u0644\u0627\u062d\u064a - \u0644\u062d\u0638\u0629 \u0646\u062f\u0645 2024 Mohamed Alflahi - Lahdt Nadm",
            "info": {
                "image": "https:\/\/i.ytimg.com\/vi\/WSO00Ig-RNc\/hqdefault.jpg",
                "title": "\u0645\u062d\u0645\u062f \u0627\u0644\u0641\u0644\u0627\u062d\u064a - \u0644\u062d\u0638\u0629 \u0646\u062f\u0645 2024 Mohamed Alflahi - Lahdt Nadm"
            },
            "repeat_download": true,
            "message": "If you want your application to use our API contact us: sp_golubev@protonmail.com or visit https:\/\/video-download-api.com\/"
        }
'''
'''
    #progress
        {
            "success": 0,
            "progress": 10,
            "download_url": null,
            "text": "Initialising",
            "message": "If you want your application to use our API contact us: sp_golubev@protonmail.com or visit https:\/\/video-download-api.com\/"
        }

'''

'''
    #get_bytes
        {
            "success": 1,
            "progress": 1000,
            "download_url": "https:\/\/jill46.oceansaver.in\/pacific\/?5mGEI5q1EktK5ueqtm76xiH",
            "text": "Finished",
            "message": "If you want your application to use our API contact us: sp_golubev@protonmail.com or visit https:\/\/video-download-api.com\/"
        }
'''

vid_id = '9LNv_mFERwI'

id = (send_request(vid_id,360))
url = get_progress(id)['download_url']
print(id)
# print(get_bytes(url))