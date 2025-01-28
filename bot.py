from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientTimeout
)
from colorama import *
from datetime import datetime
from fake_useragent import FakeUserAgent
import asyncio, json, os, pytz

wib = pytz.timezone('Asia/Jakarta')

class EtherDrops:
    def __init__(self) -> None:
        self.headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'App-Version': '1.0.0',
            'Origin': 'https://mdkefjwsfepf.dropstab.com',
            'Pragma': 'no-cache',
            'Referer': 'https://mdkefjwsfepf.dropstab.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': FakeUserAgent().random
        }
        self.API = "https://api.miniapp.dropstab.com/api"

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
    
    async def auth_login(self, query: str, retries=5):
        url = f'{self.API}/auth/login'
        data = json.dumps({'webAppData':query})
        headers = {
            **self.headers,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json',
            'X-Tg-Data': query
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        result = await response.json()
                        return result['jwt']['access']['token']
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
                
    async def user_data(self, token: str, query: str, retries=5):
        url = f'{self.API}/user/current'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'X-Tg-Data': query
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
                
    async def apply_reff(self, token: str, query: str, retries=5):
        url = f'{self.API}/user/applyRefLink'
        data = json.dumps({'code':'LAAIT'})
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json',
            'X-Tg-Data': query
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.put(url=url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
    async def welcome_bonus(self, token: str, query: str, retries=5):
        url = f'{self.API}/bonus/welcomeBonus'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Length': '0',
            'Content-Type': 'application/json',
            'X-Tg-Data': query
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
                
    async def daily_bonus(self, token: str, query: str, retries=5):
        url = f'{self.API}/bonus/dailyBonus'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Length': '0',
            'Content-Type': 'application/json',
            'X-Tg-Data': query
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
                
    async def reff_link(self, token: str, query: str, retries=5):
        url = f'{self.API}/refLink'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'X-Tg-Data': query
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
                
    async def claim_reff(self, token: str, query: str, retries=5):
        url = f'{self.API}/refLink/claim'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Length': '0',
            'Content-Type': 'application/json',
            'X-Tg-Data': query
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
                
    async def my_order(self, token: str, query: str, retries=5):
        url = f'{self.API}/order'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'X-Tg-Data': query
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None

    async def btc_stats(self, token: str, query: str, retries=5):
        url = f'{self.API}/order/coinStats/1'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'X-Tg-Data': query
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
                
    async def create_order(self, token: str, query: str, period_id: int, trade: bool, retries=5):
        url = f'{self.API}/order'
        data = json.dumps({'coinId':1, 'periodId':period_id, 'short':trade})
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json',
            'X-Tg-Data': query
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        if response.status == 400:
                            return None
                        
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
                
    async def claim_order(self, token: str, query: str, order_id: int, type: str, retries=5):
        url = f'{self.API}/order/{order_id}/{type}'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Length': '0',
            'Content-Type': 'application/json',
            'X-Tg-Data': query
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.put(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
                
    async def quest_lists(self, token: str, query: str, retries=5):
        url = f'{self.API}/quest'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'X-Tg-Data': query
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
                
    async def verify_quests(self, token: str, query: str, sub_quest_id: int, retries=5):
        url = f'{self.API}/quest/{sub_quest_id}/verify'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Length': '0',
            'Content-Type': 'application/json',
            'X-Tg-Data': query
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.put(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
                
    async def claim_quests(self, token: str, query: str, sub_quest_id: int, retries=5):
        url = f'{self.API}/quest/{sub_quest_id}/claim'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Length': '0',
            'Content-Type': 'application/json',
            'X-Tg-Data': query
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.put(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying.... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
                
    async def process_query(self, query: str):
        token = await self.auth_login(query)
        if not token:
            self.log(
                f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.RED + Style.BRIGHT} Query ID Isn't Valid {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
            )
            return
        
        if token:
            user = await self.user_data(token, query)
            if not user:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                )
                return
            
            if user:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {user['tgUsername']} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}] [ Balance{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {user['balance']} $DPS {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                )
                await asyncio.sleep(1)

                used_reff = user['usedRefLinkCode']
                if used_reff is None:
                    await self.apply_reff(token, query)
                    await asyncio.sleep(1)

                welcome_bonus = user['welcomeBonusReceived']
                if not welcome_bonus:
                    receive = await self.welcome_bonus(token, query)
                    if receive:
                        claimed = receive['result']
                        if claimed:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Welcome Bonus{Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT} Is Received {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {receive['bonus']} $DPS {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Welcome Bonus{Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT} Isn't Received {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                    else:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Welcome Bonus{Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                    await asyncio.sleep(1)

                daily_bonus = await self.daily_bonus(token, query)
                if daily_bonus:
                    claimed = daily_bonus['result']
                    if claimed:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Daily Bonus{Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {daily_bonus['bonus']} $DPS {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                    else:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Daily Bonus{Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT} Is Already Claimed {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Daily Bonus{Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                await asyncio.sleep(1)

                reff = await self.reff_link(token, query)
                if reff:
                    available = reff['availableToClaim']
                    if available > 0:
                        claim = await self.claim_reff(token, query)
                        if claim:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Friends{Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {available} $DPS {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Friends{Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT} Isn't Claimed {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                    else:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Friends{Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT} No Available $DPS to Claim {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Friends{Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                await asyncio.sleep(1)

                my_order = await self.my_order(token, query)
                if my_order:
                    result = my_order['results']
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Orders{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Total {result['orders']} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Win {result['wins']}x {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Win Rate {result['winRate']}% {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Win Streak {result['streak']['count']}x {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                    await asyncio.sleep(1)

                    order_periodes = my_order['periods']
                    for period in order_periodes:
                        period_id = period['period']['id']
                        order_data = period.get('order', None)

                        if period and order_data is None:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Orders{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {period_id} {Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT}Is Prepared{Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                            )
                            await asyncio.sleep(1)

                            btc_stats = await self.btc_stats(token, query)
                            if btc_stats:
                                one_hours_stats = btc_stats['coin']['change']['1H']
                                stats_color = Fore.RED if one_hours_stats < 0 else Fore.GREEN
                                stats = f"{one_hours_stats:.2f}"  if one_hours_stats < 0 else f"+{one_hours_stats:.2f}"
                                trade = True if one_hours_stats < 0 else False
                                trade_type = 'Short' if trade else 'Long'

                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Orders{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} BTC {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} 1H Stats is {Style.RESET_ALL}"
                                    f"{stats_color + Style.BRIGHT}{stats}%{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                )
                                await asyncio.sleep(1)

                                create = await self.create_order(token, query, period_id, trade)
                                if create:
                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}[ Orders{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {period_id} {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {trade_type} BTC {Style.RESET_ALL}"
                                        f"{Fore.GREEN + Style.BRIGHT}Is Created{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )
                                else:
                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}[ Orders{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {period_id} {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {trade_type} BTC {Style.RESET_ALL}"
                                        f"{Fore.YELLOW + Style.BRIGHT}Not Eligible to Create{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )

                            else:
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Orders{Style.RESET_ALL}"
                                    f"{Fore.RED + Style.BRIGHT} Failed to Get 1H BTC Stats {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            await asyncio.sleep(1)

                        else:
                            order_id = str(order_data['id'])
                            status = order_data['status']
                            if status in ['CLAIM_AVAILABLE', 'NOT_WIN']:
                                type = 'claim' if status == 'CLAIM_AVAILABLE' else 'markUserChecked'
                                reward = order_data['reward'] if status == 'CLAIM_AVAILABLE' else 0
                                claim = await self.claim_order(token, query, order_id, type)
                                if claim:
                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}[ Orders{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {period_id} {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} ID {order_id} BTC {Style.RESET_ALL}"
                                        f"{Fore.GREEN + Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {reward} $DPS {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                    )
                                    await asyncio.sleep(1)

                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}[ Orders{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {period_id} {Style.RESET_ALL}"
                                        f"{Fore.GREEN + Style.BRIGHT}Is Prepared{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )
                                    await asyncio.sleep(1)

                                    btc_stats = await self.btc_stats(token, query)
                                    if btc_stats:
                                        one_hours_stats = btc_stats['coin']['change']['1H']
                                        stats_color = Fore.RED if one_hours_stats < 0 else Fore.GREEN
                                        stats = f"{one_hours_stats:.2f}"  if one_hours_stats < 0 else f"+{one_hours_stats:.2f}"
                                        trade = True if one_hours_stats < 0 else False
                                        trade_type = 'Short' if trade else 'Long'

                                        self.log(
                                            f"{Fore.MAGENTA + Style.BRIGHT}[ Orders{Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT} BTC {Style.RESET_ALL}"
                                            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT} 1H Stats is {Style.RESET_ALL}"
                                            f"{stats_color + Style.BRIGHT}{stats}%{Style.RESET_ALL}"
                                            f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                        )
                                        await asyncio.sleep(1)

                                        create = await self.create_order(token, query, period_id, trade)
                                        if create:
                                            self.log(
                                                f"{Fore.MAGENTA + Style.BRIGHT}[ Orders{Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT} {period_id} {Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT} {trade_type} BTC {Style.RESET_ALL}"
                                                f"{Fore.GREEN + Style.BRIGHT}Is Created{Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                            )
                                        else:
                                            self.log(
                                                f"{Fore.MAGENTA + Style.BRIGHT}[ Orders{Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT} {period_id} {Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT} {trade_type} BTC {Style.RESET_ALL}"
                                                f"{Fore.YELLOW + Style.BRIGHT}Not Eligible to Create{Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                            )

                                    else:
                                        self.log(
                                            f"{Fore.MAGENTA + Style.BRIGHT}[ Orders{Style.RESET_ALL}"
                                            f"{Fore.RED + Style.BRIGHT} Failed to Get 1H BTC Stats {Style.RESET_ALL}"
                                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                        )
                                    await asyncio.sleep(1)

                                else:
                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}[ Orders{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {period_id} {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} ID {order_id} BTC {Style.RESET_ALL}"
                                        f"{Fore.RED + Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )
                                await asyncio.sleep(1)

                            else:
                                now = int(datetime.now(pytz.utc).timestamp())
                                finish_time_utc = datetime.fromtimestamp(now + order_data['secondsToFinish'], pytz.utc)
                                finish_time_wib = finish_time_utc.astimezone(wib).strftime('%x %X %Z')
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Orders{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {period_id} {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} ID {order_id} BTC {Style.RESET_ALL}"
                                    f"{Fore.YELLOW + Style.BRIGHT}Not Time to Claim{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ] [ Claim at{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {finish_time_wib} {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            await asyncio.sleep(1)

                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Orders{Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                await asyncio.sleep(1)

                quests = await self.quest_lists(token, query)
                if quests:
                    completed = False
                    for quest in quests:
                        type = quest['name']
                        sub_quests = quest['quests']

                        if quest:
                            sub_completed = False
                            for sub_quest in sub_quests:
                                sub_quest_id = str(sub_quest['id'])
                                status = sub_quest['status']

                                if sub_quest and status == 'NEW':
                                    can_claim = sub_quest['claimAllowed']
                                    if not can_claim:
                                        verify = await self.verify_quests(token, query, sub_quest_id)
                                        if verify and verify['status'] == 'OK':
                                            self.log(
                                                f"{Fore.MAGENTA + Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT} {type} {Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT} {sub_quest['name']} {Style.RESET_ALL}"
                                                f"{Fore.GREEN + Style.BRIGHT}Is Verified{Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                            )
                                        else:
                                            self.log(
                                                f"{Fore.MAGENTA + Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT} {type} {Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT} {sub_quest['name']} {Style.RESET_ALL}"
                                                f"{Fore.RED + Style.BRIGHT}Isn't Verified{Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                            )
                                        await asyncio.sleep(1)

                                    else:
                                        claim = await self.claim_quests(token, query, sub_quest_id)
                                        if claim and claim['status'] == 'OK':
                                            self.log(
                                                f"{Fore.MAGENTA + Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT} {type} {Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT} {sub_quest['name']} {Style.RESET_ALL}"
                                                f"{Fore.GREEN + Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT} {sub_quest['reward']} $DPS {Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                            )
                                        else:
                                            self.log(
                                                f"{Fore.MAGENTA + Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT} {type} {Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                                f"{Fore.WHITE + Style.BRIGHT} {sub_quest['name']} {Style.RESET_ALL}"
                                                f"{Fore.RED + Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                            )
                                        await asyncio.sleep(1)

                                elif sub_quest and status == 'VERIFICATION':
                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {type} {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {sub_quest['name']} {Style.RESET_ALL}"
                                        f"{Fore.YELLOW + Style.BRIGHT}In Verification{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )

                                else:
                                    sub_completed = True

                            if sub_completed:
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {type} {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}Is Completed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                )
                        else:
                            completed = True

                    if completed:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT} Is Completed {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )

    async def main(self):
        try:
            with open('query.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)

                for query in queries:
                    query = query.strip()
                    if query:
                        await self.process_query(query)
                        self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)
                        await asyncio.sleep(3)

                seconds = 1800
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}",
                        end="\r"
                    )
                    await asyncio.sleep(1)
                    seconds -= 1

        except FileNotFoundError:
            self.log(f"{Fore.RED}File 'query.txt' tidak ditemukan.{Style.RESET_ALL}")
            return
        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        bot = EtherDrops()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] EtherDrops - BOT{Style.RESET_ALL}",                                       
        )