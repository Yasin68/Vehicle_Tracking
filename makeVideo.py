import cv2
import numpy as np
import os
import json
import shutil
from getLaneCoordinates import Data
from getDistance import get_midpoint_bbox, get_vehicle_name
from util import frame_to_video
import argparse


def save_cords():
    cords = get_midpoint_bbox()
    final = get_vehicle_name(cords)
    data = Data()
    data.load(args.name)
    # save cords to json
    total_frames = len(cords.keys())
    for ind in range(total_frames - 1):
        data_list = []
        for ind1, point in enumerate(cords["frame{}".format(ind)]["car"]):
            # convert point to int
            point = tuple(map(int, point))
            # write car name from final
            car_name = final["frame{}".format(ind)][ind1]
            data_list.append(
                {"label": car_name, "lane": data.check_lane(point), "mid-point": point}
            )
        final["frame{}".format(ind)] = data_list
    with open("data/tracking_vehicle.json", "w") as f:
        json.dump(final, f, indent=4)


def final_frames(args):
    data = Data()
    data.load(args.name)
    cords = get_midpoint_bbox()
    final = get_vehicle_name(cords)
    save_cords()
    total_frames = len(cords.keys())
    print("Saving frames to folder {}...".format(args.output_frame))
    for ind in range(total_frames - 1):
        frame = cv2.imread("data/frame/frame{}.jpg".format(ind))
        for ind1, point in enumerate(cords["frame{}".format(ind)]["car"]):
            # convert point to int
            point = tuple(map(int, point))
            cv2.circle(frame, point, 5, (0, 0, 255), -1)
            # write car name from final
            car_name = final["frame{}".format(ind)][ind1]
            cv2.putText(
                frame,
                "{}|{}".format(car_name, data.check_lane(point)),
                point,
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2,
                cv2.LINE_AA,
            )
        if ind % 1000 == 0:
            print("frame{}".format(ind))

        cv2.imwrite(os.path.join(args.output_frame, "frame{}.jpg".format(ind)), frame)


if __name__ == "__main__":
    # add argument of output folder of frames using argparse
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-o", "--output_frame", default="data/final", help="path to output frames"
    )
    ap.add_argument(
        "-v", "--video", default="data/final.mp4", help="path to output video"
    )
    ap.add_argument(
        "-r", "--remove", action="store_true", help="do not remove frames folder"
    )
    # add argument of slope_intercept.txt
    ap.add_argument(
        "-n",
        "--name",
        default="data/slope_intercept.txt",
        help="path to generated slope intercept file",
    )
    args = ap.parse_args()
    # check if output frames folder exists
    if not os.path.exists(args.output_frame):
        os.makedirs(args.output_frame)
    final_frames(args)
    print("Converting frames to video...")
    frame_to_video(args.output_frame, args.video, fps=60)
    if args.remove:
        print("Removing frames and {} folder...".format(args.output_frame))
        shutil.rmtree(args.output_frame)
        shutil.rmtree(os.path.join("data", "frame"))
