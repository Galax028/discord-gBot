from data.config import TOKEN, PREBUILD_TOKEN, BOT_VERSION, PREBUILD_BOT_VERSION


token = TOKEN
prebuild = PREBUILD_TOKEN

if TOKEN == PREBUILD_TOKEN:
    global version
    version = PREBUILD_BOT_VERSION
elif token != prebuild:
    version = BOT_VERSION