# Stolen from here:
# https://github.com/slobdell/motion_detection/blob/master/shaky_motion_detection.py

import sys
import cv2
import numpy as np

IMAGE_WIDTH = 800


def resized_frame(frame):
    height, width = frame.shape[0: 2]
    desired_width = IMAGE_WIDTH
    desired_to_actual = float(desired_width) / width
    new_width = int(width * desired_to_actual)
    new_height = int(height * desired_to_actual)
    return cv2.resize(frame, (new_width, new_height))


class ShakyMotionDetector(object):

    X_PIXEL_RANGE = 4
    Y_PIXEL_RANGE = 2

    def __init__(self, file_to_read):
        self.file_to_read = file_to_read
        self.capture = cv2.VideoCapture(self.file_to_read)

        self.video_writer = None
        self.frames_per_sec = 25
        self.codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

        self.frame_number = 0
        video_filename = (file_to_read.split("/")[-1]).split(".")[0]
        self.output_filename = "output_%s.avi" % video_filename

    def _generate_working_frames(self):
        while True:
            success, frame_from_video = self.capture.read()
            if not success:
                break
            frame_from_video = resized_frame(frame_from_video)
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
                yield motion_detection_frame

    def _get_motion_detection_frame(self, previous_previous_frame, previous_frame, frame):
        d1 = cv2.absdiff(frame, previous_frame)
        d2 = cv2.absdiff(previous_frame, previous_previous_frame)
        motion_detection_frame = cv2.bitwise_xor(d1, d2)
        return motion_detection_frame

    def _remove_shakiness(self, frames):
        clean_frames = []
        min_previous_frame_count = 6
        max_previous_frame_count = 20
        for index, frame in enumerate(frames):
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            print("Processing {}".format(index))
            previous_frames = frames[:index - min_previous_frame_count]
            previous_frames = previous_frames[index - max_previous_frame_count:]
            missing_frame_count = (max_previous_frame_count - min_previous_frame_count) - len(previous_frames)
            if missing_frame_count > 0:
                previous_frames = previous_frames + frames[-missing_frame_count:]
            # cumulative_motion = np.sum(previous_frames, axis=0)
            cumulative_motion = self._get_max_array(previous_frames)
            final_frame = frame.astype(int) - cumulative_motion.astype(int)
            final_frame[final_frame < 0] = 0
            clean_frames.append(final_frame.astype(np.uint8))
            print("Final sum: {}".format(np.sum(final_frame)))
            cv2.imshow('step1', final_frame)
            # cv2.imshow('orig', frame)
        return clean_frames

    def _get_max_array(self, array_list):
        resultant_array = np.zeros(array_list[0].shape)
        for array in array_list:
            resultant_array = np.maximum(resultant_array, array)

        for y_offset in range(-self.Y_PIXEL_RANGE, self.Y_PIXEL_RANGE + 1):
            for x_offset in range(-self.X_PIXEL_RANGE, self.X_PIXEL_RANGE + 1):
                offset_array = np.roll(resultant_array, x_offset, axis=1)
                offset_array = np.roll(offset_array, y_offset, axis=0)
                resultant_array = np.maximum(resultant_array, offset_array)
        return resultant_array

    def create(self):


        all_frames = list(self._generate_motion_detection_frames())
        all_frames = self._remove_shakiness(all_frames)

        for motion_detection_frame in all_frames:
            height, width = motion_detection_frame.shape[0: 2]
            self.video_writer = self.video_writer or cv2.VideoWriter(self.output_filename, self.codec, self.frames_per_sec, (width, height))
            self.video_writer.write(motion_detection_frame)
            self.frame_number += 1
            print("Writing {}".format(self.frame_number))
        if self.video_writer is not None:
            self.video_writer.release()


if __name__ == "__main__":
    file_to_read = 'C:/Temp/x.mp4'       # sys.argv[1]
    ShakyMotionDetector(file_to_read)    # .create()   # no need to create output.
    print('the end')