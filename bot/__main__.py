import config as cfg

from .util.models import LavaBot


# make sure the main py file is being run as a file and not imported
def main():
    bot = LavaBot()
    bot.run(cfg.bot.token, log_formatter=bot.log_handler.formatter)


if __name__ == "__main__":
    main()
