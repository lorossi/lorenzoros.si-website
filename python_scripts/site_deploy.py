import logging
import os
import re
from glob import glob

import pysftp
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

    for file in glob(s.local_path + "/**/*", recursive=True):
        remote_path = s.remote_path + re.sub(r".*" + s.local_path, "", file)
        logging.info(f"Uploading {file} ...")

        if os.path.isdir(file):
            try:
                sftp.mkdir(remote_path)
            except IOError:
                pass
        else:
            # get remote file mtime
            try:
                remote_mtime = sftp.stat(remote_path).st_mtime
            except IOError:
                remote_mtime = None

            # get local file mtime
            local_mtime = int(os.path.getmtime(file))
            if remote_mtime is None or local_mtime > remote_mtime:
                sftp.put(file, remote_path, preserve_mtime=True)
                logging.info("Uploaded.")
            else:
                time_diff = remote_mtime - local_mtime
                logging.info(f"Skipped (remote file is {time_diff} seconds newer).")

    logging.info("All files uploaded. Closing connection ...")
    sftp.close()
    logging.info("Connection closed.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    main()
