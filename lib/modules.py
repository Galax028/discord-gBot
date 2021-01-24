def read_token():
    with open('Python/discord-gBot/important/config.txt', 'r') as f:
        lines = f.readlines()
        return lines[2].strip()
def read_version():
    with open('Python/discord-gBot/important/config.txt', 'r') as f:
        lines = f.readlines()
        return lines[11].strip()
def check_build():
    with open('Python/discord-gBot/important/config.txt', 'r') as f:
        lines = f.readlines()
        return lines[8].strip()

token = read_token()
prebuild = check_build()

if token == prebuild:
    def pre_version():
        with open('Python/discord-gBot/important/config.txt', 'r') as f:
            lines = f.readlines()
            return lines[14].strip()
    global version
    version = pre_version()
elif token != prebuild:
    version = read_version()