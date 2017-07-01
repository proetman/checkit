# Stolen from here:
# https://github.com/slobdell/motion_detection/blob/master/basic_motion_detection.py

import sys
import cv2
# import numpy as np

IMAGE_WIDTH = 500


def resized_frame(frame):
    height, width = frame.shape[0: 2]
    desired_width = IMAGE_WIDTH
    desired_to_actual = float(desired_width) / width
    new_width = int(width * desired_to_actual)
    new_height = int(height * desired_to_actual)
    new_frame = cv2.resize(frame, (new_width, new_height))
    #### cv2.imshow('step2', new_frame)
    return frame



class BasicMotionDetector(object):
    def __init__(self, file_to_read):
        self.file_to_read = file_to_read
        self.capture = cv2.VideoCapture(self.file_to_read)

        self.video_writer = None
        self.frames_per_sec = 25
        self.codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        # self.codec = cv2.VideoWriter_fourcc(*'H264')
        self.frame_number = 0

    def _generate_working_frames(self):
        while True:
            success, frame_from_video = self.capture.read()
            if not success:
                break
            #### cv2.imshow('step1', frame_from_video2)
            # frame_from_video = resized_frame(frame_from_video2)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            yield frame_from_video

    def _generate_motion_detection_frames(self):
        previous_frame = None
        previous_previous_frame = None
        for frame in self._generate_working_frames():

            motion_detection_frame = None
            if previous_previous_frame is not None:
                motion_detection_frame = self._get_motion_detection_frame(previous_previous_frame, previous_frame, frame)
            previous_previous_frame = previous_frame
            previous_frame = frame
            if motion_detection_frame is not None:
                cv2.imshow('step2', motion_detection_frame)
                yield motion_detection_frame

    def _get_motion_detection_frame(self, previous_previous_frame, previous_frame, frame):
        d1 = cv2.absdiff(frame, previous_frame)
        d2 = cv2.absdiff(previous_frame, previous_previous_frame)
        motion_detection_frame = cv2.bitwise_xor(d1, d2)
        return motion_detection_frame

    def create(self, output_filename):
        for motion_detection_frame in self._generate_motion_detection_frames():
            height, width = motion_detection_frame.shape[0: 2]
            self.video_writer = self.video_writer or cv2.VideoWriter(output_filename, self.codec, self.frames_per_sec, (width, height))
            self.video_writer.write(motion_detection_frame)
            self.frame_number += 1
            print("Writing {}".format(self.frame_number))

        if self.video_writer is not None:
            self.video_writer.release()


if __name__ == "__main__":
    file_to_read = sys.argv[1]
    BasicMotionDetector(file_to_read).create("basic_motion.avi")
    print('the end')
