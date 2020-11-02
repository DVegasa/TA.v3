import queue

import src.log as log

tag = "FileManager"

append_queue = queue.Queue()


def grab_and_write():
    while True:
        if not append_queue.empty():
            path, content = append_queue.get()
            log.n(tag, "Writing to " + path)
            with open(path, "ab") as f:
                f.write(content)
