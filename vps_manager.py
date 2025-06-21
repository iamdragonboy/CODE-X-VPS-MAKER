import docker, random, json, os

client = docker.from_env()
DATA_FILE = 'users.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def deploy_ipv4(userid):
    port = random.randint(20000, 65000)
    container = client.containers.run(
        "ubuntu_vps_ssh", detach=True,
        ports={'22/tcp': port},
        tty=True
    )
    ip = os.popen("curl -s ifconfig.me").read().strip()
    vps_info = {
        'container_id': container.short_id,
        'ip': ip,
        'port': port,
        'user': 'root',
        'password': 'dragoncloud'
    }
    data = load_data()
    data.setdefault(userid, []).append(vps_info)
    save_data(data)
    return vps_info

def list_vps(userid):
    data = load_data()
    return data.get(userid, [])

def list_all():
    return load_data()

def delete_vps(userid):
    data = load_data()
    if userid in data:
        for vps in data[userid]:
            try:
                container = client.containers.get(vps['container_id'])
                container.remove(force=True)
            except:
                pass
        del data[userid]
        save_data(data)
        return True
    return False
