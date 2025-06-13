import multiprocessing
import os

port = int(os.getenv('PORT', 10000))
bind = f"0.0.0.0:{port}"
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 120
keepalive = 5
errorlog = "-"
accesslog = "-"
loglevel = "info" 
