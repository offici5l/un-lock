#!/usr/bin/python

version = "test"

import os

for lib in ['Cryptodome', 'urllib3', 'requests', 'colorama']:
    try:
        __import__(lib)
    except ImportError:
        prefix = os.getenv("PREFIX", "")
        if lib == 'Cryptodome':
            if "com.termux" in prefix:
                cmd = 'pkg install python-pycryptodomex'
            else:
                cmd = 'pip install pycryptodomex'
        else:
            cmd = f'pip install {lib}'
        os.system(cmd)

import re, requests, json, hmac, random, binascii, urllib, hashlib, io, urllib.parse, time, sys, urllib.request, zipfile, webbrowser, platform, subprocess, shutil, stat, datetime, threading
from urllib3.util.url import Url
from base64 import b64encode, b64decode
from Cryptodome.Cipher import AES
from urllib.parse import urlparse, parse_qs, urlencode
from colorama import init, Fore, Style

init(autoreset=True)

cg = Style.BRIGHT + Fore.GREEN
cgg = Style.DIM
cr = Fore.RED
crr = Style.BRIGHT + Fore.RED
cres = Style.RESET_ALL
cy = Style.BRIGHT + Fore.YELLOW
p_ = cg + "\n" + "_"*56 +"\n"
session = requests.Session()
headers = {"User-Agent": "XiaomiPCSuite"}

if '1' in sys.argv:
    pass
else:
    print(cgg + f"\n[V{version}] For issues or feedback:\n- GitHub: github.com/offici5l/MiUnlockTool/issues\n- Telegram: t.me/Offici5l_Group\n" + cres)

print(p_)

s = platform.system()
if s == "Linux" and os.path.exists("/data/data/com.termux"):
    up = os.path.join(os.getenv("PREFIX", ""), "bin", "miunlock")
    try:
        if "fastboot version" not in os.popen("fastboot --version").read():
            raise Exception
    except:
        os.system("curl https://raw.githubusercontent.com/offici5l/MiUnlockTool/main/.install | bash")
        exit()
    if not os.path.exists(up):
        shutil.copy(__file__, up)
        os.system(f"chmod +x {up}")
        print(f"\nuse command: {cg}miunlock{cres}\n")
        exit()
    if not os.path.exists("/data/data/com.termux.api"):
        print("\ncom.termux.api app is not installed\nPlease install it first\n")
        exit()
    cmd = "fastboot"
else:
    dir = os.path.dirname(__file__)
    fp = os.path.join(dir, "platform-tools")
    if not os.path.exists(fp):
        print("\ndownload platform-tools...\n")
        url = f"https://dl.google.com/android/repository/platform-tools-latest-{s}.zip"
        cd = os.path.join(os.path.dirname(__file__))
        fp = os.path.join(cd, os.path.basename(url))    
        urllib.request.urlretrieve(url, fp)    
        with zipfile.ZipFile(fp, 'r') as zip_ref:
            zip_ref.extractall(cd)
        os.remove(fp)
    cmd = os.path.join(fp, "fastboot")
    if s == "Linux" or s == "Darwin":
        st = os.stat(cmd)
        os.chmod(cmd, st.st_mode | stat.S_IEXEC)

datafile = os.path.join(os.path.dirname(__file__), "miunlockdata.json")

while os.path.isfile(datafile):
    try:
        with open(datafile, "r") as file:
            data = json.load(file)
        if '1' in sys.argv:
            break
        elif data and data.get("login") == "ok":
            choice = input(f"\nYou are already logged in with account uid: {data['uid']}\n{cg}Press Enter to continue\n{cgg}(to log out, type 2 and press Enter){cres}\n").strip().lower()
            if choice == "2":
                os.remove(datafile)
            else:
                break
        else:
            os.remove(datafile)
    except PermissionError:
        os.remove(datafile)
    except json.JSONDecodeError:
        os.remove(datafile)

def remove(*keys):
    print(f"\n{cr}invalid {keys[0] if len(keys) == 1 else ' or '.join(keys)}{cres}\n")
    with open(datafile, "r+") as file:
        data = json.load(file)
        for key in keys:
            data.pop(key, None)
        file.seek(0)
        json.dump(data, file, indent=2)
        file.truncate()
    os.execv(sys.executable, [sys.executable] + sys.argv + ['1'])

try:
    with open(datafile, "r+") as file:
        data = json.load(file)
except FileNotFoundError:
    data = {}
    with open(datafile, 'w') as file:
        json.dump(data, file)

def save(data, path):
    with open(path, "w") as file:
        json.dump(data, file, indent=2)

if "user" not in data:
    data["user"] = input("Xiaomi Account\nId or Email or Phone(in international format)\n : ")
    sys.stdout.write("\033[F\033[K\033[F\033[K\033[F\033[K")
    sys.stdout.flush()
    save(data, datafile)

if "pwd" not in data:
    data["pwd"] = input("Enter password: ")
    sys.stdout.write("\033[F\033[K")
    sys.stdout.flush()
    save(data, datafile)

if "wb_id" not in data:
    input(f"\n{Fore.CYAN}Notice:\nIf logged in with any account in your default browser,\nplease log out before pressing Enter.\n\n{cres}{cg}Press Enter{cres} to open confirmation page, \n copy link after seeing {Fore.CYAN}{Style.BRIGHT}\"R\":\"\",\"S\":\"OK\"{Style.RESET_ALL}, \n  and return here\n\n")
    conl = 'https://account.xiaomi.com/pass/serviceLogin?sid=unlockApi&checkSafeAddress=true&passive=false&hidden=false'
    if s == "Linux":
        os.system("xdg-open '" + conl + "'")
    else:
        webbrowser.open(conl)
    time.sleep(2)
    wb_id = parse_qs(urlparse(input("Enter Link: ")).query).get('d', [None])[0]
    if wb_id is None:
        print("\n\nInvalid link\n")
        os.execv(sys.executable, [sys.executable] + sys.argv + ['1'])
    data["wb_id"] = wb_id
    save(data, datafile)

user, pwd, wb_id = (data.get(key, "") for key in ["user", "pwd", "wb_id"])

datav = data

def add_email(SetEmail):
    input(f"\n{cr}Failed to get passToken !{cres}\n\nThe account is not linked to an email.\n{cg}Press Enter{cres} to open the email adding page.\nAfter successfully adding your email, return here")
    if s == "Linux":
        os.system("xdg-open '" + SetEmail + "'")
    else:
        webbrowser.open(SetEmail)
    time.sleep(2)
    input(f"\nIf email added successfully, {cg}press Enter{cres} to continue\n")
    os.execv(sys.executable, [sys.executable] + sys.argv + ['1'])

def postv(sid):
    return json.loads(session.post(f"https://account.xiaomi.com/pass/serviceLoginAuth2?sid={sid}&_json=true&passive=true&hidden=true", data={"user": user, "hash": hashlib.md5(pwd.encode()).hexdigest().upper()}, headers=headers, cookies={"deviceId": str(wb_id)}).text.replace("&&&START&&&", ""))

data = postv("unlockApi")

if data["code"] == 70016:
    remove("user", "pwd")

if data["securityStatus"] == 4 and "notificationUrl" in data and "bizType=SetEmail" in data["notificationUrl"]:
    add_email(data["notificationUrl"])

if data["securityStatus"] == 16:
    p = postv("passport")
    if p["securityStatus"] == 4 and "notificationUrl" in p and "bizType=SetEmail" in p["notificationUrl"]:
        add_email(p["notificationUrl"])
    elif "passToken" not in p:
         print(f"\n{cr}Failed to get passToken !{cres}\n")
         exit()
    data = json.loads(requests.get("https://account.xiaomi.com/pass/serviceLogin?sid=unlockApi&_json=true&passive=true&hidden=true", headers=headers, cookies={'passToken': p['passToken'], 'userId': str(p['userId']), 'deviceId': parse_qs(urlparse(p['location']).query)['d'][0]}).text.replace("&&&START&&&", ""))

ssecurity, nonce, location = data["ssecurity"], data["nonce"], data["location"]

cookies = {cookie.name: cookie.value for cookie in session.get(location + "&clientSign=" + urllib.parse.quote_plus(b64encode(hashlib.sha1(f"nonce={nonce}".encode("utf-8") + b"&" + ssecurity.encode("utf-8")).digest())), headers=headers).cookies}

if 'serviceToken' not in cookies:
    print(f"\n{cr}Failed to get serviceToken.{cres}")
    remove("wb_id")

if "login" not in datav:
    datav["login"] = "ok"
    if "uid" not in datav:
        datav["uid"] = data['userId']
    save(datav, datafile)
    print(f"\n\n{cg}Login successful! Login saved.{cres}")

region = json.loads(requests.get("https://account.xiaomi.com/pass/user/login/region?", headers=headers, cookies={'passToken': data['passToken'], 'userId': str(data['userId']), 'deviceId': parse_qs(urlparse(data['location']).query)['d'][0]}).text.replace("&&&START&&&", ""))['data']['region']

print(f"\n{cg}AccountInfo:{cres}\nid: {data['userId']}\nregion: {region}")

region_config = json.loads(requests.get("https://account.xiaomi.com/pass2/config?key=register").text.replace("&&&START&&&", ""))['regionConfig']

for key, value in region_config.items():
    if 'region.codes' in value and region in value['region.codes']:
        region = value['name'].lower()
        break

for arg in sys.argv:
    if arg.lower() in ['global', 'india', 'russia', 'china', 'europe']:
        region = arg
        break

g = "unlock.update.intl.miui.com"

if region == "china":
    url = g.replace("intl.", "")
elif region == "india":
    url = f"in-{g}"
elif region == "russia":
    url = f"ru-{g}"
elif region == "europe":
    url = f"eu-{g}"
else:
    url = g

def read_stream(stream, output_list, process, restart_flag):
    try:
        for line in iter(stream.readline, ''):
            line = line.strip()
            output_list.append(line)
            if "No permission" in line or "< waiting for any device >" in line:
                process.terminate()
                print(f'\r< waiting for any device >', end='', flush=True)
                restart_flag[0] = True
                return
    finally:
        stream.close()

def CheckB(cmd, var_name, *fastboot_args):
    while True:
        process = subprocess.Popen([cmd] + list(fastboot_args), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
        stdout_lines, stderr_lines, restart_flag = [], [], [False]

        threading.Thread(target=read_stream, args=(process.stdout, stdout_lines, process, restart_flag)).start()
        threading.Thread(target=read_stream, args=(process.stderr, stderr_lines, process, restart_flag)).start()

        try:
            process.wait()
        except subprocess.SubprocessError as e:
            print(f"Error while executing process: {e}")
            return None

        if restart_flag[0]:
            time.sleep(2)
            sys.stdout.write('\r\033[K')
            continue

        print(f"\rFetching '{var_name}' — please wait...", end='', flush=True)

        lines = [line.split(f"{var_name}:")[1].strip() for line in stderr_lines + stdout_lines if f"{var_name}:" in line]
        if len(lines) > 1:
            return "".join(lines)
        return lines[0] if lines else None

[print(char, end='', flush=True) or time.sleep(0.01) for char in "\nEnsure you're in Bootloader mode (fastboot mode)\n\n"]

unlocked = None
product = None
SoC = None
token = None

while unlocked is None or product is None or SoC is None or token is None:
    if unlocked is None:
        unlocked = CheckB(cmd, "unlocked", "getvar", "unlocked")
    if product is None:
        product = CheckB(cmd, "product", "getvar", "product")
    if token is None:
        token = CheckB(cmd, "token", "oem", "get_token")
        if token:
            SoC = "Mediatek"
        else:
            token = CheckB(cmd, "token", "getvar", "token")
            if token:
                SoC = "Qualcomm"

sys.stdout.write('\r\033[K')

print(f"\n{cg}DeviceInfo:{cres}\nunlocked: {unlocked}\nSoC: {SoC}\nproduct: {product}\ntoken: {token}\n")

class RetrieveEncryptData:
    def add_nonce(self):
        r = RetrieveEncryptData("/api/v2/nonce", {"r":''.join(random.choices(list("abcdefghijklmnopqrstuvwxyz"), k=16)), "sid":"miui_unlocktool_client"}).run()
        self.params[b"nonce"] = r["nonce"].encode("utf-8")
        self.params[b"sid"] = b"miui_unlocktool_client"
        return self
    def __init__(self, path, params):
        self.path = path
        self.params = {k.encode("utf-8"): v.encode("utf-8") if isinstance(v, str) else b64encode(json.dumps(v).encode("utf-8")) if not isinstance(v, bytes) else v for k, v in params.items()}
    def getp(self, sep):
        return b'POST'+sep+self.path.encode("utf-8")+sep+b"&".join([k+b"="+v for k,v in self.params.items()])
    def run(self):
        self.params[b"sign"] = binascii.hexlify(hmac.digest(b'2tBeoEyJTunmWUGq7bQH2Abn0k2NhhurOaqBfyxCuLVgn4AVj7swcawe53uDUno', self.getp(b"\n"), "sha1"))
        for k, v in self.params.items():
            self.params[k] = b64encode(AES.new(b64decode(ssecurity), AES.MODE_CBC, b"0102030405060708").encrypt(v + (16 - len(v) % 16) * bytes([16 - len(v) % 16])))
        self.params[b"signature"] = b64encode(hashlib.sha1(self.getp(b"&")+b"&"+ssecurity.encode("utf-8")).digest())
        try:
            response_text = session.post(Url(scheme="https", host=url, path=self.path).url, data=self.params, headers=headers, cookies=cookies).text
            decoded_data = b64decode(response_text)
            decrypted_data = AES.new(b64decode(ssecurity), AES.MODE_CBC, b"0102030405060708").decrypt(decoded_data)
            unpadded_data = (lambda s: s[:-s[-1]] if s and s[-1] > 0 else s)(decrypted_data)
            decoded_unpadded_data = b64decode(unpadded_data)
            json_data = json.loads(decoded_unpadded_data)
            return json_data
        except Exception as e:
            print("\n\nData sent:\n")
            print(f"URL: {Url(scheme='https', host=url, path=self.path).url}")
            print(f"Params: {self.params}")
            print(f"Headers: {headers}")
            print(f"Cookies: {cookies}")
            print("\n\nError:", e)
            if 'response_text' in locals():
                print(f"\n\nresponse_text:\n\n{response_text}\n\n")
            if 'decoded_data' in locals():
                print(f"\n\ndecoded_data:\n\n{decoded_data}\n\n")
            if 'decrypted_data' in locals():
                print(f"\n\ndecrypted_data:\n\n{decrypted_data}\n\n")
            if 'unpadded_data' in locals():
                print(f"\n\nunpadded_data:\n\n{unpadded_data}\n\n")
            if 'decoded_unpadded_data' in locals():
                print(f"\n\ndecoded_unpadded_data:\n\n{decoded_unpadded_data}\n\n")
            if 'json_data' in locals():
                print(f"\n\njson_data:\n\n{json_data}\n\n")
           
            exit()

print(p_)

c = RetrieveEncryptData("/api/v2/unlock/device/clear", {"data":{"product":product}}).add_nonce().run()
cleanOrNot = c['cleanOrNot']

if cleanOrNot == 1:
    print(f"\n{crr}This device clears user data when it is unlocked{cres}\n")
elif cleanOrNot == -1:
    print(f"\n{cg}Unlocking the device does not clear user data{cres}\n") 

print(Style.BRIGHT + Fore.CYAN + c['notice'] + cres)

choice = input(f"\n{cg}Press Enter to Unlock\n{cgg}( or type q and press Enter to quit){cres}")
if choice.lower() == 'q':
    print("\nExiting...\n")
    exit() 

print(p_)

r = RetrieveEncryptData("/api/v3/ahaUnlock", {"appId":"1", "data":{"clientId":"2", "clientVersion":"7.6.727.43", "language":"en", "operate":"unlock", "pcId":hashlib.md5(wb_id.encode("utf-8")).hexdigest(), "product":product, "region":"","deviceInfo":{"boardVersion":"","product":product, "socId":"","deviceName":""}, "deviceToken":token}}).add_nonce().run()

if "code" in r and r["code"] == 0:
    ed = io.BytesIO(bytes.fromhex(r["encryptData"]))
    with open("encryptData", "wb") as edfile:
        edfile.write(ed.getvalue())
    CheckB(cmd, "serialno", "getvar", "serialno")
    sys.stdout.write('\r\033[K')
    try:
        result_stage = subprocess.run([cmd, "stage", "encryptData"], check=True, capture_output=True, text=True)
        result_unlock = subprocess.run([cmd, "oem", "unlock"], check=True, capture_output=True, text=True)
        print(f"\n{cg}Unlock successful{cgg}\n")
        os.remove("encryptData")
    except subprocess.CalledProcessError as e:
        print("Error message:", e.stderr)
elif "descEN" in r:
    print(f"\ncode {r['code']}\n\n{r['descEN']}")
    if r["code"] == 20036:
        print("\nYou can unlock on:", (datetime.datetime.now().replace(minute=0, second=0, microsecond=0) + datetime.timedelta(hours=r["data"]["waitHour"])).strftime("%Y-%m-%d %H:%M"))
    else:
        print(f"{cgg}\noffici5l.github.io/code\n{cres}")
else:
    for key, value in r.items():
        print(f"\n{key}: {value}")

print(p_)

if not os.path.exists("/data/data/com.termux"):
    input("\nPress Enter to exit ...")