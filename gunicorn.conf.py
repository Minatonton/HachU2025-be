import multiprocessing

accesslog = "-"
max_requests = 1000
max_requests_jitter = 200
threads = 1
worker_class = "gthread"
workers = multiprocessing.cpu_count() * 2 + 1
wsgi_app = "hack_u__2025_be.wsgi:application"
