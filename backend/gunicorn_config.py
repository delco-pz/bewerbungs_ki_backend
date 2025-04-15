def post_fork(server, worker):
    server.log.info("Gunicorn worker spawned (pid: %s)", worker.pid)

bind = "0.0.0.0:8000"
workers = 1
timeout = 120

