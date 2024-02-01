from ast import arg
import enum
import numpy as np
import cv2
import json
import pandas as pd
import os


def func(x, next_frame):
    temp = np.linalg.norm(x - next_frame, axis=1)
    # print(temp.min())
    if temp.min() < 10:
        return temp.argmin()
    return -1


def frame_to_video(folder, output, fps=30):
    img = cv2.imread(os.path.join("data", folder, "frame0.jpg"))
    total_frames = len(os.listdir(folder))
    height, width, layers = img.shape
    size = (width, height)
    out = cv2.VideoWriter(output, cv2.VideoWriter_fourcc(*"MP4V"), fps, size)
    for x in range(total_frames):
        img = cv2.imread(os.path.join(folder, "frame{}.jpg".format(x)))
        out.write(img)
    out.release()


def get_midpoint_bbox(
    bbox_file_per_frame="data/object_cordinates.json",
):
    with open(bbox_file_per_frame, "r") as f:
        cords = json.load(f)
    new_cord = {}
    # new_cord = {}
    for frame in cords.keys():
        # new_cord[frame] = {}
        new_cord[frame] = {}
        for vehicle in cords[frame].keys():
            # new_cord[frame][vehicle] = {}
            new_cord[frame][vehicle] = {}
            cord = []
            for (x1, y1, x2, y2, _) in cords[frame][vehicle]:
                cord.append(((x1 + x2) / 2, (y1 + y2) / 2))
            # sort cord by y
            cord.sort(key=lambda x: x[1], reverse=True)
            new_cord[frame][vehicle] = cord
            # new_cord[frame][vehicle] = np.array(cord)

    return new_cord


def get_vehicle_name(new_cord):
    def get_name(x):
        global max
        if x == -1:
            to_return = "car{}".format(max)
            max = max + 1
            return to_return
        return prev[x]

    frame_list = {}
    global max
    max = len(new_cord["frame0"]["car"]) + 1
    frame_list["frame0"] = [
        "car{}".format(x + 1) for x in range(len(new_cord["frame0"]["car"]))
    ]

    for ind1 in range(len(new_cord.keys()) - 1):
        s = pd.Series(new_cord["frame{}".format(ind1 + 1)]["car"])
        temp = s.apply(
            func, args=(np.array(new_cord["frame{}".format(ind1)]["car"]),)
        ).tolist()
        prev = frame_list["frame{}".format(ind1)]
        temp = list(map(get_name, temp))
        frame_list["frame{}".format(ind1 + 1)] = temp
    return frame_list


if __name__ == "__main__":
    new_cord = get_midpoint_bbox()
    frame_list = get_vehicle_name(new_cord)
    with open("data/car_names_for_each_frame.json", "w") as f:
        json.dump(frame_list, f, indent=4)
