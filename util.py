import sys
import cv2
import argparse
import os


def frame_to_video(folder, output, fps=30):
    img = cv2.imread(os.path.join(folder, "frame0.jpg"))
    total_frames = len(os.listdir(folder))
    height, width, layers = img.shape
    size = (width, height)
    out = cv2.VideoWriter(output, cv2.VideoWriter_fourcc(*"mp4v"), fps, size)
    for x in range(total_frames):
        img = cv2.imread(os.path.join(folder, "frame{}.jpg".format(x)))
        out.write(img)
    out.release()


def video_to_frame(path_to_video, output_folder):
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    vidcap = cv2.VideoCapture(args.path)
    success, image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite(
            os.path.join(args.output, "frame{}.jpg".format(count)), image
        )  # save frame as JPEG file

        success, image = vidcap.read()
        if not count % 1000:
            print("frame{}".format(count))
        count += 1


if __name__ == "__main__":
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=True, help="path to input video")
    ap.add_argument(
        "-o", "--output", default="data/frame", help="path to output frames"
    )
    args = ap.parse_args()
    video_to_frame(args.path, args.output)
