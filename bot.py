from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientTimeout
)
from aiohttp_socks import ProxyConnector
from fake_useragent import FakeUserAgent
from urllib.parse import unquote, parse_qs
from datetime import datetime
from colorama import *
import asyncio, json, time, os, pytz

wib = pytz.timezone('Asia/Jakarta')

class EtherDrops:
    def __init__(self) -> None:
        self.headers = {
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "App-Version": "1.0.0",
            "Origin": "https://miniapp.dropstab.com",
            "Referer": "https://miniapp.dropstab.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": FakeUserAgent().random
        }
        self.BASE_API = "https://api.miniapp.dropstab.com/api"
        self.ref_code = "XKFWG" # U can change it with yours.
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.query_ids = {}
        self.access_tokens = {}

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Claim {Fore.BLUE + Style.BRIGHT}EtherDrops - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    async def load_proxies(self, use_proxy_choice: int):
        filename = "proxy.txt"
        try:
            if use_proxy_choice == 1:
                async with ClientSession(timeout=ClientTimeout(total=30)) as session:
                    async with session.get("https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt") as response:
                        response.raise_for_status()
                        content = await response.text()
                        with open(filename, 'w') as f:
                            f.write(content)
                        self.proxies = content.splitlines()
            else:
                if not os.path.exists(filename):
                    self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                    return
                with open(filename, 'r') as f:
                    self.proxies = f.read().splitlines()
            
            if not self.proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}No Proxies Found.{Style.RESET_ALL}")
                return

            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Proxies Total  : {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(self.proxies)}{Style.RESET_ALL}"
            )
        
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Proxies: {e}{Style.RESET_ALL}")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        return f"http://{proxies}"

    def get_next_proxy_for_account(self, token):
        if token not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[token] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[token]

    def rotate_proxy_for_account(self, token):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[token] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
    
    def load_query_data(self, query_id: str):
        try:
            query_data = parse_qs(query_id).get("user", [None])[0]
            user_data = json.loads(unquote(query_data))
            user_id = user_data.get("id", None)
            username = user_data.get("username", "unknown")

            return user_id, username
        except Exception as e:
            raise Exception("Invalid Query Id Format")
        
    def print_question(self):
        while True:
            try:
                print(f"{Fore.WHITE + Style.BRIGHT}1. Run With Monosans Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Run With Private Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}3. Run Without Proxy{Style.RESET_ALL}")
                choose = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2/3] -> {Style.RESET_ALL}").strip())

                if choose in [1, 2, 3]:
                    proxy_type = (
                        "Run With Monosans Proxy" if choose == 1 else 
                        "Run With Private Proxy" if choose == 2 else 
                        "Run Without Proxy"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}{proxy_type} Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2 or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2 or 3).{Style.RESET_ALL}")

        rotate = False
        if choose in [1, 2]:
            while True:
                rotate = input(f"{Fore.BLUE + Style.BRIGHT}Rotate Invalid Proxy? [y/n] -> {Style.RESET_ALL}").strip()

                if rotate in ["y", "n"]:
                    rotate = rotate == "y"
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter 'y' or 'n'.{Style.RESET_ALL}")

        return choose, rotate
            
    async def auth_login(self, user_id: int, proxy=None, retries=5):
        url = f"{self.BASE_API}/auth/login"
        data = json.dumps({"webAppData":self.query_ids[user_id]})
        headers = {
            **self.headers,
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
            "X-Tg-Data": self.query_ids[user_id]
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        if response.status == 403:
                            self.log(
                                f"{Fore.CYAN+Style.BRIGHT}Status  :{Style.RESET_ALL}"
                                f"{Fore.RED+Style.BRIGHT} Retrieving Token Failed {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                f"{Fore.YELLOW+Style.BRIGHT} Query Id Expired {Style.RESET_ALL}"
                            )
                            return None
                        response.raise_for_status()
                        result = await response.json()
                        return result["jwt"]
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
            
    async def user_current(self, user_id: int, proxy=None, retries=5):
        url = f"{self.BASE_API}/user/current"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.access_tokens[user_id]}",
            "Content-Type": "application/json",
            "X-Tg-Data": self.query_ids[user_id]
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
            
    async def apply_reflink(self, user_id: int, proxy=None, retries=5):
        url = f"{self.BASE_API}/user/applyRefLink"
        data = json.dumps({"code":self.ref_code})
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.access_tokens[user_id]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
            "X-Tg-Data": self.query_ids[user_id]
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.put(url=url, headers=headers, data=data) as response:
                        if response.status == 400:
                            return None
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
            
    async def welcome_bonus(self, user_id: int, proxy=None, retries=5):
        url = f"{self.BASE_API}/bonus/welcomeBonus"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.access_tokens[user_id]}",
            "Content-Length": "0",
            "Content-Type": "application/json",
            "X-Tg-Data": self.query_ids[user_id]
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
            
    async def daily_bonus(self, user_id: int, proxy=None, retries=5):
        url = f"{self.BASE_API}/bonus/dailyBonus"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.access_tokens[user_id]}",
            "Content-Length": "0",
            "Content-Type": "application/json",
            "X-Tg-Data": self.query_ids[user_id]
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
            
    async def user_reflink(self, user_id: int, proxy=None, retries=5):
        url = f"{self.BASE_API}/refLink"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.access_tokens[user_id]}",
            "Content-Type": "application/json",
            "X-Tg-Data": self.query_ids[user_id]
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
            
    async def claim_reflink(self, user_id: int, proxy=None, retries=5):
        url = f"{self.BASE_API}/refLink/claim"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.access_tokens[user_id]}",
            "Content-Length": "0",
            "Content-Type": "application/json",
            "X-Tg-Data": self.query_ids[user_id]
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
                
    async def user_order(self, user_id: int, proxy=None, retries=5):
        url = f"{self.BASE_API}/order"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.access_tokens[user_id]}",
            "Content-Type": "application/json",
            "X-Tg-Data": self.query_ids[user_id]
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
            
    async def create_order(self, user_id: int, period_id: int, proxy=None, retries=5):
        url = f"{self.BASE_API}/order"
        data = json.dumps({"coinId":1, "periodId":period_id, "short":False})
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.access_tokens[user_id]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
            "X-Tg-Data": self.query_ids[user_id]
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
                
    async def check_order(self, user_id: int, order_id: int, type: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/order/{str(order_id)}/{type}"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.access_tokens[user_id]}",
            "Content-Length": "0",
            "Content-Type": "application/json",
            "X-Tg-Data": self.query_ids[user_id]
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.put(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
                
    async def task_lists(self, user_id: int, proxy=None, retries=5):
        url = f"{self.BASE_API}/quest"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.access_tokens[user_id]}",
            "Content-Type": "application/json",
            "X-Tg-Data": self.query_ids[user_id]
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
                
    async def verify_task(self, user_id: int, task_id: int, proxy=None, retries=5):
        url = f"{self.BASE_API}/quest/{str(task_id)}/verify"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.access_tokens[user_id]}",
            "Content-Length": "0",
            "Content-Type": "application/json",
            "X-Tg-Data": self.query_ids[user_id]
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.put(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
                
    async def claim_task(self, user_id: int, task_id: int, proxy=None, retries=5):
        url = f"{self.BASE_API}/quest/{str(task_id)}/claim"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.access_tokens[user_id]}",
            "Content-Length": "0",
            "Content-Type": "application/json",
            "X-Tg-Data": self.query_ids[user_id]
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.put(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
            
    async def process_auth_login(self, user_id: int, use_proxy: bool, rotate_proxy: bool):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.YELLOW + Style.BRIGHT}Retrieving Token...{Style.RESET_ALL}",
            end="\r",
            flush=True
        )

        proxy = self.get_next_proxy_for_account(user_id) if use_proxy else None
        if rotate_proxy:
            token = None
            while token is None:
                token = await self.auth_login(user_id, proxy)
                if not token:
                    self.log(
                        f"{Fore.CYAN+Style.BRIGHT}Status    :{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Retrieving Token Failed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Rotating Proxy... {Style.RESET_ALL}"
                    )
                    proxy = self.rotate_proxy_for_account(user_id) if use_proxy else None
                    await asyncio.sleep(5)
                    continue

                self.access_tokens[user_id] = token["access"]["token"]

                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Status    :{Style.RESET_ALL}"
                    f"{Fore.GREEN+Style.BRIGHT} Retrieving Token Success {Style.RESET_ALL}"
                )
                return True

        token = await self.auth_login(user_id, proxy)
        if not token:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Status    :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Retrieving Token Failed {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.YELLOW+Style.BRIGHT} Skipping This Account {Style.RESET_ALL}"
            )
            return False
        
        self.access_tokens[user_id] = token["access"]["token"]
        
        self.log(
            f"{Fore.CYAN+Style.BRIGHT}Status    :{Style.RESET_ALL}"
            f"{Fore.GREEN+Style.BRIGHT} Retrieving Token Success {Style.RESET_ALL}"
        )
        return True
        
    async def process_accounts(self, user_id: int, username: str, use_proxy: bool, rotate_proxy: bool):
        self.log(
            f"{Fore.CYAN+Style.BRIGHT}Username  :{Style.RESET_ALL}"
            f"{Fore.WHITE+Style.BRIGHT} {username} {Style.RESET_ALL}"
        )

        is_logined = await self.process_auth_login(user_id, use_proxy, rotate_proxy)
        if is_logined:
            proxy = self.get_next_proxy_for_account(user_id) if use_proxy else None

            await self.apply_reflink(user_id, proxy)

            balance = "N/A"
            user = await self.user_current(user_id, proxy)
            if user:
                balance = user.get("balance", 0)
                bonus = user.get("welcomeBonusReceived", False)

                if not bonus:
                    await self.welcome_bonus(user_id, proxy)

            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Balance   :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {balance} DPS {Style.RESET_ALL}"
            )

            checkin = await self.daily_bonus(user_id, proxy)
            if checkin:
                is_claimed = checkin.get("result", False)

                if is_claimed:
                    reward = checkin.get("bonus", 0)
                    streak = checkin.get("streak", 0)
                    self.log(
                        f"{Fore.CYAN+Style.BRIGHT}Check-In  :{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} Day {streak} {Style.RESET_ALL}"
                        f"{Fore.GREEN+Style.BRIGHT}Claimed Successfully{Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT} - {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}Reward:{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {reward} DPS {Style.RESET_ALL}"
                    )
                else:
                    self.log(
                        f"{Fore.CYAN+Style.BRIGHT}Check-In  :{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Already Claimed {Style.RESET_ALL}"
                    )
            else:
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Check-In  :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Not Claimed {Style.RESET_ALL}"
                )

            reflink = await self.user_reflink(user_id, proxy)
            if reflink:
                available_reward = reflink.get("availableToClaim", 0)

                if available_reward > 0:
                    claim = await self.claim_reflink(user_id, proxy)
                    if claim:
                        self.log(
                            f"{Fore.CYAN+Style.BRIGHT}Refferal  :{Style.RESET_ALL}"
                            f"{Fore.GREEN+Style.BRIGHT} Claimed Successfully {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                            f"{Fore.CYAN+Style.BRIGHT} Reward: {Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT}{available_reward} DPS{Style.RESET_ALL}"
                        )
                    else:
                        self.log(
                            f"{Fore.CYAN+Style.BRIGHT}Refferal  :{Style.RESET_ALL}"
                            f"{Fore.RED+Style.BRIGHT} Not Claimed {Style.RESET_ALL}"
                        )
                else:
                    self.log(
                        f"{Fore.CYAN+Style.BRIGHT}Refferal  :{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} No Available Reward {Style.RESET_ALL}"
                    )
            else:
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Refferal  :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} GET Data Failed {Style.RESET_ALL}"
                )

            order = await self.user_order(user_id, proxy)
            if order:
                self.log(f"{Fore.CYAN+Style.BRIGHT}Your Order:{Style.RESET_ALL}")

                total_order = order.get("results", {}).get("orders", 0)
                total_win = order.get("results", {}).get("wins", 0)
                winrate = order.get("results", {}).get("winRate", 0)
                winstreak = order.get("results", {}).get("streak", {}).get("count", 0)
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}  ● {Style.RESET_ALL}"
                    f"{Fore.BLUE+Style.BRIGHT}Total  :{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {total_order} {Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}  ● {Style.RESET_ALL}"
                    f"{Fore.BLUE+Style.BRIGHT}Win    :{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {total_win}x {Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}  ● {Style.RESET_ALL}"
                    f"{Fore.BLUE+Style.BRIGHT}Winrate:{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {winrate}% {Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}  ● {Style.RESET_ALL}"
                    f"{Fore.BLUE+Style.BRIGHT}Streak :{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {winstreak}x {Style.RESET_ALL}"
                )

                periodes = order.get("periods", [])
                if periodes:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}  ● {Style.RESET_ALL}"
                        f"{Fore.BLUE+Style.BRIGHT}Order Lists{Style.RESET_ALL}"
                    )

                    for idx, period in enumerate(periodes):
                        if period:
                            display_order = (
                                "1H - Order" if idx == 0 else
                                "4H - Order" if idx == 1 else
                                "24H - Order"
                            )

                            period_id = period.get("period", {}).get("id")
                            order_data = period.get("order")
                            if order_data:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}    # {Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT}{display_order}{Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT} [FILLED] {Style.RESET_ALL}"
                                )

                                order_id = order_data.get("id")
                                order_status = order_data.get("status")

                                if order_status == "CLAIM_AVAILABLE":
                                    order_reward = order_data.get("reward", 0)

                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}      ● {Style.RESET_ALL}"
                                        f"{Fore.CYAN+Style.BRIGHT}Check Status :{Style.RESET_ALL}"
                                        f"{Fore.GREEN+Style.BRIGHT} WIN {Style.RESET_ALL}"
                                    )

                                    claim = await self.check_order(user_id, order_id, "claim")
                                    if claim:
                                        self.log(
                                            f"{Fore.MAGENTA+Style.BRIGHT}      ● {Style.RESET_ALL}"
                                            f"{Fore.CYAN+Style.BRIGHT}Claim Status :{Style.RESET_ALL}"
                                            f"{Fore.GREEN+Style.BRIGHT} Success {Style.RESET_ALL}"
                                            f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                            f"{Fore.CYAN+Style.BRIGHT} Reward: {Style.RESET_ALL}"
                                            f"{Fore.WHITE+Style.BRIGHT}{order_reward} DPS{Style.RESET_ALL}"
                                        )

                                        create = await self.create_order(user_id, period_id, proxy)
                                        if create:
                                            self.log(
                                                f"{Fore.MAGENTA+Style.BRIGHT}      ● {Style.RESET_ALL}"
                                                f"{Fore.CYAN+Style.BRIGHT}Create Status:{Style.RESET_ALL}"
                                                f"{Fore.GREEN+Style.BRIGHT} Success {Style.RESET_ALL}"
                                                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                                f"{Fore.CYAN+Style.BRIGHT} Coin Type: {Style.RESET_ALL}"
                                                f"{Fore.WHITE+Style.BRIGHT}BTC{Style.RESET_ALL}"
                                                f"{Fore.MAGENTA+Style.BRIGHT} - {Style.RESET_ALL}"
                                                f"{Fore.WHITE+Style.BRIGHT}Long{Style.RESET_ALL}"
                                            )
                                        else:
                                            self.log(
                                                f"{Fore.MAGENTA+Style.BRIGHT}      ● {Style.RESET_ALL}"
                                                f"{Fore.CYAN+Style.BRIGHT}Create Status:{Style.RESET_ALL}"
                                                f"{Fore.RED+Style.BRIGHT} Failed {Style.RESET_ALL}"
                                                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                                f"{Fore.CYAN+Style.BRIGHT} Coin Type: {Style.RESET_ALL}"
                                                f"{Fore.WHITE+Style.BRIGHT}BTC{Style.RESET_ALL}"
                                                f"{Fore.MAGENTA+Style.BRIGHT} - {Style.RESET_ALL}"
                                                f"{Fore.WHITE+Style.BRIGHT}Long{Style.RESET_ALL}"
                                            )
                                    else:
                                        self.log(
                                            f"{Fore.MAGENTA+Style.BRIGHT}      ● {Style.RESET_ALL}"
                                            f"{Fore.CYAN+Style.BRIGHT}Claim Status :{Style.RESET_ALL}"
                                            f"{Fore.RED+Style.BRIGHT} Failed {Style.RESET_ALL}"
                                        )
                                
                                elif order_status == "NOT_WIN":
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}      ● {Style.RESET_ALL}"
                                        f"{Fore.CYAN+Style.BRIGHT}Check Status :{Style.RESET_ALL}"
                                        f"{Fore.RED+Style.BRIGHT} Lose {Style.RESET_ALL}"
                                    )

                                    mark = await self.check_order(user_id, order_id, "markUserChecked")
                                    if mark:
                                        self.log(
                                            f"{Fore.MAGENTA+Style.BRIGHT}      ● {Style.RESET_ALL}"
                                            f"{Fore.CYAN+Style.BRIGHT}Mark Status  :{Style.RESET_ALL}"
                                            f"{Fore.GREEN+Style.BRIGHT} Success {Style.RESET_ALL}"
                                        )

                                        create = await self.create_order(user_id, period_id, proxy)
                                        if create:
                                            self.log(
                                                f"{Fore.MAGENTA+Style.BRIGHT}      ● {Style.RESET_ALL}"
                                                f"{Fore.CYAN+Style.BRIGHT}Create Status:{Style.RESET_ALL}"
                                                f"{Fore.GREEN+Style.BRIGHT} Success {Style.RESET_ALL}"
                                                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                                f"{Fore.CYAN+Style.BRIGHT} Coin Type: {Style.RESET_ALL}"
                                                f"{Fore.WHITE+Style.BRIGHT}BTC{Style.RESET_ALL}"
                                                f"{Fore.MAGENTA+Style.BRIGHT} - {Style.RESET_ALL}"
                                                f"{Fore.WHITE+Style.BRIGHT}Long{Style.RESET_ALL}"
                                            )
                                        else:
                                            self.log(
                                                f"{Fore.MAGENTA+Style.BRIGHT}      ● {Style.RESET_ALL}"
                                                f"{Fore.CYAN+Style.BRIGHT}Create Status:{Style.RESET_ALL}"
                                                f"{Fore.RED+Style.BRIGHT} Failed {Style.RESET_ALL}"
                                                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                                f"{Fore.CYAN+Style.BRIGHT} Coin Type: {Style.RESET_ALL}"
                                                f"{Fore.WHITE+Style.BRIGHT}BTC{Style.RESET_ALL}"
                                                f"{Fore.MAGENTA+Style.BRIGHT} - {Style.RESET_ALL}"
                                                f"{Fore.WHITE+Style.BRIGHT}Long{Style.RESET_ALL}"
                                            )
                                    else:
                                        self.log(
                                            f"{Fore.MAGENTA+Style.BRIGHT}      ● {Style.RESET_ALL}"
                                            f"{Fore.CYAN+Style.BRIGHT}Mark Status  :{Style.RESET_ALL}"
                                            f"{Fore.RED+Style.BRIGHT} Failed {Style.RESET_ALL}"
                                        )

                                else:
                                    seconds_to_finish = order_data.get("secondsToFinish")
                                    check_time_wib = datetime.fromtimestamp(int(time.time()) + seconds_to_finish).astimezone(wib).strftime('%x %X %Z')
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}      ● {Style.RESET_ALL}"
                                        f"{Fore.CYAN+Style.BRIGHT}Check Status :{Style.RESET_ALL}"
                                        f"{Fore.YELLOW+Style.BRIGHT} Not Time to Check {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                        f"{Fore.CYAN+Style.BRIGHT} Check at: {Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT}{check_time_wib}{Style.RESET_ALL}"
                                    )

                            else:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}    # {Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT}{display_order}{Style.RESET_ALL}"
                                    f"{Fore.YELLOW+Style.BRIGHT} [EMPTY] {Style.RESET_ALL}"
                                )

                                create = await self.create_order(user_id, period_id, proxy)
                                if create:
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}      ● {Style.RESET_ALL}"
                                        f"{Fore.CYAN+Style.BRIGHT}Create Status:{Style.RESET_ALL}"
                                        f"{Fore.GREEN+Style.BRIGHT} Success {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                        f"{Fore.CYAN+Style.BRIGHT} Coin Type: {Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT}BTC{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT} - {Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT}Long{Style.RESET_ALL}"
                                    )
                                else:
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}      ● {Style.RESET_ALL}"
                                        f"{Fore.CYAN+Style.BRIGHT}Create Status:{Style.RESET_ALL}"
                                        f"{Fore.RED+Style.BRIGHT} Failed {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                        f"{Fore.CYAN+Style.BRIGHT} Coin Type: {Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT}BTC{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT} - {Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT}Long{Style.RESET_ALL}"
                                    )
                
            else:
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Your Order:{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} GET Data Failed {Style.RESET_ALL}"
                ) 

            task_lists = await self.task_lists(user_id, proxy)
            if task_lists:
                self.log(f"{Fore.CYAN+Style.BRIGHT}Task Lists:{Style.RESET_ALL}")

                for tasks in task_lists:
                    if tasks:
                        group_name = tasks.get("name")
                        group_tasks = tasks.get("quests", [])

                        if group_tasks:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}  ● {Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT}{group_name}{Style.RESET_ALL}"
                            )

                            for task in group_tasks:
                                if task:
                                    task_id = task.get("id")
                                    title = task.get("name")
                                    reward = task.get("reward")
                                    status = task.get("status")
                                    allow_to_claim = task.get("claimAllowed")

                                    if status == "COMPLETED":
                                        self.log(
                                            f"{Fore.MAGENTA+Style.BRIGHT}    > {Style.RESET_ALL}"
                                            f"{Fore.WHITE+Style.BRIGHT}{title}{Style.RESET_ALL}"
                                            f"{Fore.GREEN+Style.BRIGHT} [Completed] {Style.RESET_ALL}"
                                        )
                                        continue

                                    if allow_to_claim:
                                        self.log(
                                            f"{Fore.MAGENTA+Style.BRIGHT}    > {Style.RESET_ALL}"
                                            f"{Fore.WHITE+Style.BRIGHT}{title}{Style.RESET_ALL}"
                                            f"{Fore.BLUE+Style.BRIGHT} [CLAIMABLE] {Style.RESET_ALL}"
                                        )

                                        claim = await self.claim_task(user_id, task_id, proxy)
                                        if claim and claim.get("status") == "Ok":
                                            self.log(
                                                f"{Fore.MAGENTA+Style.BRIGHT}      ● {Style.RESET_ALL}"
                                                f"{Fore.CYAN+Style.BRIGHT}Claim Status :{Style.RESET_ALL}"
                                                f"{Fore.GREEN+Style.BRIGHT} Success {Style.RESET_ALL}"
                                                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                                f"{Fore.CYAN+Style.BRIGHT} Reward: {Style.RESET_ALL}"
                                                f"{Fore.WHITE+Style.BRIGHT}{reward} DPS{Style.RESET_ALL}"
                                            )
                                        else:
                                            self.log(
                                                f"{Fore.MAGENTA+Style.BRIGHT}      ● {Style.RESET_ALL}"
                                                f"{Fore.CYAN+Style.BRIGHT}Claim Status :{Style.RESET_ALL}"
                                                f"{Fore.RED+Style.BRIGHT} Failed {Style.RESET_ALL}"
                                            )

                                    else:
                                        self.log(
                                            f"{Fore.MAGENTA+Style.BRIGHT}    > {Style.RESET_ALL}"
                                            f"{Fore.WHITE+Style.BRIGHT}{title}{Style.RESET_ALL}"
                                            f"{Fore.BLUE+Style.BRIGHT} [NEW] {Style.RESET_ALL}"
                                        )

                                        verify = await self.verify_task(user_id, task_id, proxy)
                                        if verify and verify.get("status") == "Ok":
                                            self.log(
                                                f"{Fore.MAGENTA+Style.BRIGHT}      ● {Style.RESET_ALL}"
                                                f"{Fore.CYAN+Style.BRIGHT}Verify Status:{Style.RESET_ALL}"
                                                f"{Fore.GREEN+Style.BRIGHT} Success {Style.RESET_ALL}"
                                            )

                                            claim = await self.claim_task(user_id, task_id, proxy)
                                            if claim and claim.get("status") == "Ok":
                                                self.log(
                                                    f"{Fore.MAGENTA+Style.BRIGHT}      ● {Style.RESET_ALL}"
                                                    f"{Fore.CYAN+Style.BRIGHT}Claim Status :{Style.RESET_ALL}"
                                                    f"{Fore.GREEN+Style.BRIGHT} Success {Style.RESET_ALL}"
                                                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                                    f"{Fore.CYAN+Style.BRIGHT} Reward: {Style.RESET_ALL}"
                                                    f"{Fore.WHITE+Style.BRIGHT}{reward} DPS{Style.RESET_ALL}"
                                                )
                                            else:
                                                self.log(
                                                    f"{Fore.MAGENTA+Style.BRIGHT}      ● {Style.RESET_ALL}"
                                                    f"{Fore.CYAN+Style.BRIGHT}Claim Status :{Style.RESET_ALL}"
                                                    f"{Fore.RED+Style.BRIGHT} Failed {Style.RESET_ALL}"
                                                )
                                        else:
                                            self.log(
                                                f"{Fore.MAGENTA+Style.BRIGHT}      ● {Style.RESET_ALL}"
                                                f"{Fore.CYAN+Style.BRIGHT}Verify Status:{Style.RESET_ALL}"
                                                f"{Fore.RED+Style.BRIGHT} Failed {Style.RESET_ALL}"
                                            )

                        else:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}  ● {Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT}{group_name}{Style.RESET_ALL}"
                                f"{Fore.YELLOW+Style.BRIGHT} No Available Tasks {Style.RESET_ALL}"
                            )
            else:
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Task Lists:{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} GET Lists Data Failed {Style.RESET_ALL}"
                )     
        
    async def main(self):
        try:
            with open('query.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]
            
            use_proxy_choice, rotate_proxy = self.print_question()

            while True:
                use_proxy = False
                if use_proxy_choice in [1, 2]:
                    use_proxy = True

                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )

                if use_proxy:
                    await self.load_proxies(use_proxy_choice)
                
                separator = "=" * 25
                for idx, query_id in enumerate(queries, start=1):
                    if query_id:
                        user_id, username = self.load_query_data(query_id)

                        if user_id and username:
                            self.query_ids[user_id] = query_id

                            self.log(
                                f"{Fore.CYAN + Style.BRIGHT}{separator}[{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {idx} {Style.RESET_ALL}"
                                f"{Fore.CYAN + Style.BRIGHT}Of{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {len(queries)} {Style.RESET_ALL}"
                                f"{Fore.CYAN + Style.BRIGHT}]{separator}{Style.RESET_ALL}"
                            )
                            await self.process_accounts(user_id, username, use_proxy, rotate_proxy)
                            await asyncio.sleep(3)

                self.log(f"{Fore.CYAN + Style.BRIGHT}={Style.RESET_ALL}"*60)
                seconds = 1 * 60 * 60
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.BLUE+Style.BRIGHT}All Accounts Have Been Processed.{Style.RESET_ALL}",
                        end="\r"
                    )
                    await asyncio.sleep(1)
                    seconds -= 1

        except FileNotFoundError:
            self.log(f"{Fore.RED}File 'query.txt' Not Found.{Style.RESET_ALL}")
            return
        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")
            raise e

if __name__ == "__main__":
    try:
        bot = EtherDrops()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] EtherDrops - BOT{Style.RESET_ALL}                                       "                              
        )