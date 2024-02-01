# importing the module
import cv2
import argparse
import os


class Data:
    def __init__(self):
        self.points = []
        self.flag = False
        self.line_point = []
        self.slope_and_intercept = []

    def change_flag(self):
        self.flag = not self.flag

    def add_point(self, point):
        self.points.append(point)

    def get_line_point(self):
        points = self.line_point
        self.line_point = []
        return points

    def get_slope_and_intercept(self, point):
        p1, p2 = point
        x1, y1 = p1
        x2, y2 = p2
        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1
        return slope, intercept

    def map_points(self):
        self.slope_and_intercept = list(map(self.get_slope_and_intercept, self.points))

    def check_lane(self, p):
        x, y = p
        for point in range(len(self.slope_and_intercept) - 1):
            (m1, c1), (m2, c2) = (
                self.slope_and_intercept[point],
                self.slope_and_intercept[point + 1],
            )
            x1 = (y - c1) / m1
            x2 = (y - c2) / m2
            if x1 < x < x2:
                return "Lane {}".format(point + 1)
        return "Outside Lane"

    def load(self, file):
        with open(file, "r") as f:
            self.slope_and_intercept = eval(f.read())

    def save(self, file):
        if file is not None:
            print("Saving file {}...".format(file))
            with open(file, "w") as f:
                f.write(str(self.slope_and_intercept))


# function to display the coordinates of
# of the points on mouse click and mouse drag
def click_event_lane(event, x, y, flags, params):
    data, img = params
    if event == cv2.EVENT_LBUTTONDOWN:
        data.line_point.append((x, y))
        if len(data.line_point) == 2:
            data.add_point(data.get_line_point())
            p1, p2 = data.points[-1]
            # draw a line from the last point to the current point
            cv2.line(img, p1, p2, (0, 255, 0), 5)
            cv2.imshow("image", img)


def get_lane_cord(args):
    path_to_frame = args.frame
    data = Data()
    # reading the image
    original = cv2.imread(path_to_frame, 1)
    img = original.copy()
    # add text to image 'Start labeling lanes from left to right'
    cv2.putText(
        img,
        'Start labeling lanes from left to right. Press "s" to save',
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2,
        cv2.LINE_AA,
    )
    # displaying the image
    cv2.imshow("image", img)
    cv2.setMouseCallback("image", click_event_lane, param=[data, img])

    # wait for a key to be pressed to exit
    key = cv2.waitKey(0)
    if key == ord("q") or key == ord("s"):
        data.map_points()
        data.save(args.name)
        cv2.destroyAllWindows()


def click_event_point(event, x, y, flags, params):
    img, data = params
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 3, (0, 255, 255), -1)
        lane = data.check_lane((x, y))
        # write lane to image
        cv2.putText(
            img,
            str(lane),
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
            cv2.LINE_AA,
        )
        cv2.imshow("image", img)


def get_point_position(args):
    # load the points
    data = Data()
    data.load(args.name)
    # read the image
    original = cv2.imread(args.frame, 1)
    img = original.copy()
    cv2.imshow("image", img)
    cv2.setMouseCallback("image", click_event_point, param=[img, data])

    # wait for a key to be pressed to exit
    key = cv2.waitKey(0)
    if key == ord("q"):
        cv2.destroyAllWindows()


# driver function
if __name__ == "__main__":
    # get flags from command line using argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--frame",
        type=str,
        default="data/frame/frame0.jpg",
        help="path to frame file",
    )
    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        help="to test lanes, add path to points file",
    )
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        default="data/slope_intercept.txt",
        help="filename to save and load points",
    )
    args = parser.parse_args()
    if args.test:
        get_point_position(args)
    else:
        get_lane_cord(args)
