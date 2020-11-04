import concurrent.futures

import src.camcatalog as cams
import src.file_manager as files
import src.detection_queue

tag = "main"


def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(files.grab_and_write)
        executor.submit(src.detection_queue.tracking)
        executor.submit(cams.powernet[7].start)


if __name__ == '__main__':
    main()
