import pysftp
from glob import glob
import re
import logging

from modules.settings import Settings


def main():
    s = Settings.from_toml("settings.toml", "Deploy")

    logging.info(f"Connecting to {s.url} ...")
    sftp = pysftp.Connection(
        s.url,
        username=s.username,
        private_key=s.key_path,
        private_key_pass=s.private_key_pass,
    )
    logging.info("Connected.")

    for file in glob(s.local_path + "/**/*"):
        remote_path = s.remote_path + re.sub(r".*" + s.local_path, "", file)
        logging.info(f"Uploading {file} ...")
        sftp.put(file, remote_path, preserve_mtime=True)
        logging.info("Uploaded.")

    logging.info("All files uploaded. Closing connection ...")
    sftp.close()
    logging.info("Connection closed.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    main()
