from .Config import CONFIG
import random
import time

class EMQX(CONFIG):
    broker = CONFIG.host
    port = 1883
    topic = "switch"
