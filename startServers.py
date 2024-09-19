import subprocess

def start_servers():
    servers = [
        "python -m database_prod.api.app",
        "python -m pricer.api.app",
        "python -m arm.api.app",
        "python -m imm.api.app"
    ]

    processes = []

    for server in servers:
        process = subprocess.Popen(server, shell=True)
        processes.append(process)

    for process in processes:
        process.wait()

if __name__ == "__main__":
    start_servers()