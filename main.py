from srcs.config.Config import Config
from srcs.context.Contexts import Contexts


conf = Config("config.yaml")
cts = Contexts("context.yaml")
print(cts)
