from srcs.config.Config import Config
from srcs.context.Contexts import Contexts
from srcs.bot.Bot import Bot
from srcs.docker.Docker import Docker

conf = Config("config.yaml")
cts = Contexts("context.yaml")
# bot = Bot(conf, cts)
docker = Docker("python", "python main.py", volumes={"srcs/bot":"/home"}, remove=True, env={
	"DB_PASSWORD" : "ADMIN",
	"DB_USER" : "TOTO"
})
docker.run()