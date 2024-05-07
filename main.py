"""Script to query the real-time NREL ASI-16 image"""
import datetime
import glob
import hashlib
import os
import pytz
import requests
import time

image_url = "https://midcdmz.nrel.gov/data/rt/srrlasi.jpg"
no_picture_md5_hash = "604c77fd179dd033f129c4397a8095eb"

# image is generally taken at 33 seconds but not updated until about 30 seconds later.
# eg. 12:00:33 -> ~12:01:30

def wait_until_next_minute(seconds=0):
    current_time = datetime.datetime.now()
    next_minute = current_time + datetime.timedelta(minutes=1)
    next_minute = next_minute.replace(second=seconds, microsecond=0)
    time.sleep((next_minute - current_time).total_seconds())

def get_and_save_image(out_dir):
    previous_hash = None
    while True:
        response = requests.get(image_url)
        current_hash = hashlib.md5(response.content).hexdigest()

        if current_hash != no_picture_md5_hash:
            # current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            current_time_mst = datetime.datetime.now(pytz.timezone('US/Mountain'))
            current_time_mst = current_time_mst - datetime.timedelta(minutes=1)
            current_time_mst = current_time_mst.replace(second=33, microsecond=0)
            filepath = os.path.join(
                out_dir, current_time_mst.strftime("%Y"), current_time_mst.strftime("%m"), current_time_mst.strftime("%d"), current_time_mst.strftime("%Y%m%d-%H%M%S.jpg")
            )
            
            # previous_time_mst = current_time_mst - datetime.timedelta(minutes=1)
            # previous_filepath = os.path.join(
            #     out_dir, previous_time_mst.strftime("%Y"), previous_time_mst.strftime("%m"), previous_time_mst.strftime("%d"), previous_time_mst.strftime("%Y%m%d-%H%M**.jpg")
            # )
            # if os.path.exists(previous_filepath):
            #     with open(previous_filepath, "rb") as file:
            #         previous_hash = hashlib.md5(file.read()).hexdigest()
            # else:
            #     previous_hash = None
            
            if previous_hash != current_hash:
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, "wb") as file:
                    file.write(response.content)
                previous_hash = current_hash
                
                wait_until_next_minute(seconds=10)
                
            else:
                time.sleep(10)
            
        else:
            time.sleep(10)
            

if __name__ == "__main__":
    get_and_save_image("/data/")
    