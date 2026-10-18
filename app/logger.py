
import logging


class Logger:
    """Configure application logging."""

    def __init__(self, log_file_path):
        self.logger = logging.getLogger("calculator")
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
            handler.close()

        log_file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        handler = logging.FileHandler(
            log_file_path,
            encoding="utf-8",
        )

        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
        )

        self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger
