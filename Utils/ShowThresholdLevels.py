""" The script will open all FF files in the given folder and plot color-coded images where the color
    represents the threshold needed to detect individual feacutres on the image.
"""

from __future__ import print_function, division, absolute_import

import os
import argparse

import numpy as np
import matplotlib.pyplot as plt

from RMS.Formats.FFfile import validFFName
from RMS.Formats.FFfile import read as readFF


if __name__ == "__main__":

    import RMS.ConfigReader as cr

    ### PARSE INPUT ARGUMENTS ###

    # Init the command line arguments parser
    arg_parser = argparse.ArgumentParser(description=""" Starting capture and compression.
        """)

    arg_parser.add_argument('dir_path', type=str, help="Path to the folder with FF files.")

    arg_parser.add_argument('-f', '--fireball', action="store_true", help="""Estimate threshold for fireball
        detection, not meteor detection. """)

    #############################

    # Parse the command line arguments
    cml_args = arg_parser.parse_args()

    if cml_args.fireball:
        print('FireballDetection')

    else:
        print('MeteorDetection')

    
    # Load the configuration file
    config = cr.parse(".config")


    if not os.path.exists(cml_args.dir_path):
        print('{:s} directory does not exist!'.format(cml_args.dir_path))

    # Load all FF files in the given directory
    for file_name in os.listdir(cml_args.dir_path):

        # Check if the file is an FF file
        if validFFName(file_name):

            # Read the FF file
            ff = readFF(cml_args.dir_path, file_name)

            # Use the fireball thresholding
            if cml_args.fireball:
                k1 = config.k1
                j1 = config.j1

            # Meteor detection
            else:
                k1 = config.k1_det
                j1 = config.j1_det

            # Compute the threshold value
            k1_vals = (ff.maxpixel.astype(np.float64) - ff.avepixel.astype(np.float64) \
                - j1)/ff.stdpixel.astype(np.float64)


            fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)

            # Plot the threshold map
            k1map = ax1.imshow(k1_vals, cmap='inferno', vmin=1, vmax=6,  aspect='auto')

            cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
            if cml_args.fireball:
                plt.colorbar(k1map, cax=cbar_ax, label='Top plot: k1')

            else:
                plt.colorbar(k1map, cax=cbar_ax, label='Top plot: k1_det')


            # Plot thresholded image
            threshld = ff.maxpixel > ff.avepixel + k1*ff.stdpixel + j1
            ax2.imshow(threshld, cmap='gray', aspect='auto')
            ax2.text(0, 0, "k1 = {:.2f}, j1 = {:.2f}".format(k1, j1), color='red', verticalalignment='top',
                weight='bold')

            fig.subplots_adjust(right=0.8, hspace=0)

            plt.show()
















