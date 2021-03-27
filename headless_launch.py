import wmi
import hashlib
import requests
import urllib
import xml.etree.ElementTree as ET
import base64
import os
import subprocess

def base64_encode(s: str) -> str:
    return base64.b64encode(s.encode()).decode('utf-8')


def get_device_token():
    c = wmi.WMI()

    base_board_serial = c.Win32_BaseBoard()[0].SerialNumber
    bios_serial = c.Win32_BIOS()[0].SerialNumber
    os_serial = c.Win32_OperatingSystem()[0].SerialNumber

    concat = base_board_serial + bios_serial + os_serial

    m = hashlib.sha1()
    m.update(concat.encode())
    device_token = m.hexdigest()
    return device_token


def send_login_request(email, password, device_token):
    url = "https://www.realmofthemadgod.com/account/verify"
    payload = f'guid={urllib.parse.quote(email)}&' + \
                f'password={urllib.parse.quote(password)}&' +\
                f'clientToken={device_token}&' + \
                '&game_net=Unity&play_platform=Unity&game_net_user_id='

    headers = {
      'Host': 'www.realmofthemadgod.com',
      'User-Agent': 'UnityPlayer/2019.3.14f1 (UnityWebRequest/1.0, libcurl/7.52.0-DEV)',
      'Accept': '/',
      'Accept-Encoding': 'identity',
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-Unity-Version': '2019.3.14f1'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


def parse_response(response_xml):
    root = ET.fromstring(response_xml)
    encoded_token = base64_encode(root.find('AccessToken').text)
    encoded_timestamp = base64_encode(root.find('AccessTokenTimestamp').text)

    return encoded_token, encoded_timestamp

default_exe = f'C:\\Users\\{os.getlogin()}\\Documents\\RealmOfTheMadGod\\Production\\RotMG Exalt.exe'
email = os.getenv("ROTMG_EMAIL")
password = os.getenv("ROTMG_PASSWORD")
clientToken = get_device_token()

response = send_login_request(email, password, clientToken)
encoded_token, encoded_timestamp = parse_response(response)
encoded_email = base64_encode(email)

exe_path = os.getenv('ROTMG_PATH', default_exe)
data = f'data:{{platform:Deca,guid:{encoded_email},token:{encoded_token},tokenTimestamp:{encoded_timestamp},tokenExpiration:MTMwMDAwMA==,env:4}}'
subprocess.Popen([exe_path, data])
