"""SLIC Superpixel segmentation script
"""

from __future__ import print_function

import argparse
import time
import imutils
import cv2
import numpy as np

from superpixel import image_to_slic


# possible arguments (look up each help parameter for additional information)
SEGMENTS = 100
COMPACTNESS = 10.0
MAX_ITERATIONS = 10
SIGMA = 0.0


def get_arguments():
    """Parses the arguments from the terminal and overrides their corresponding
    default values. Returns all arguments in a dictionary."""

    parser = argparse.ArgumentParser(description='SLIC Superpixel '
                                     'segmentation script')

    parser.add_argument('-i', '--image', required=True, type=str,
                        help='Path to the image')
    parser.add_argument('--segments', type=int, default=SEGMENTS,
                        help='Number of segments')
    parser.add_argument('--compactness', type=float, default=COMPACTNESS,
                        help='Balances color proximity and space proximity. '
                        'A higher value gives more weight to space proximity '
                        'making superpixel shapes more square/cubic.')
    parser.add_argument('--max-iterations', type=int, default=MAX_ITERATIONS,
                        help='Maximum number of iterations of k-means')
    parser.add_argument('--sigma', type=float, default=SIGMA,
                        help='Width of gaussian smoothing kernel for pre-'
                        'processing')
    parser.add_argument('-o', '--output', type=str,
                        help='Path and name to the superpixel segmented image')

    args = parser.parse_args()

    # give output default value dependent on input if none was passed
    if not args.output:
        path = args.image.split('/')
        name = path[-1].split('.')
        name = '{}-super.{}'.format('.'.join(name[:-1]), name[-1])
        args.output = '{}/{}'.format('/'.join(path[:-1]), name)

    return args


def main():
    """Runs the SLIC superpixel segmentation."""

    args = get_arguments()

    # load the image from file
    image = cv2.imread(args.image)

    # apply SLIC and extract the supplied segments
    start_time = time.time()
    segments = image_to_slic(image, segments=args.segments,
                             compactness=args.compactness,
                             max_iterations=args.max_iterations,
                             sigma=args.sigma)
    print('Runtime: {0:.4f}s'.format(time.time() - start_time))

    # iterate over all segment values
    segment_values = np.unique(segments)
    for segment_value in segment_values:
        # build a mask for each segment
        mask = np.zeros(image.shape[:2], dtype="uint8")
        mask[segments == segment_value] = 255

        mean_c = cv2.mean(image, mask)

        # find the contour of the mask
        contours = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)

        # grab the tuples based on whether we are using OpenCV 2.4 or OpenCV 3
        contours = contours[0] if imutils.is_cv2() else contours[1]

        cv2.drawContours(image, contours, -1, mean_c, -1)
        # cv2.drawContours(image, contours, -1, (0, 0, 255), 1)

        for contour in contours:
            # compute the center of the contour
            M = cv2.moments(contour)
            if M['m00'] > 0.0:
                c_x = int(M['m10'] / M['m00'])
                c_y = int(M['m01'] / M['m00'])

                cv2.circle(image, (c_x, c_y), 4, mean_c, -1)

    # write the image to the specified output path
    cv2.imwrite(args.output, image)

    print('Number of segments generated: {}'.format(len(segment_values)))
    print('Output: {}'.format(args.output))


# only run if the script is executed directly
if __name__ == '__main__':
    main()
