#!/usr/bin/env python

##### Public Domain via CC0
#
# Because we're all in this together, I have decided to dedicate this
# script to the public domain by way of CC0.  You are free to do what
# you will with this code - I will pass no judgement upon you.
#
# See http://creativecommons.org/publicdomain/zero/1.0/ for more info.
#
# Have a nice day!
#


##### Other notes
#
# This script is for converting between the LPC universal sprite sheet
# layout to the sprite sheet format used by some of Aeva's .gani files
# for m.grl and other projects.
#
# This script requires "Pillow" to be installed, for more information,
# see: https://pillow.readthedocs.org/en/latest/
#


##### Consumer Advisory Notice
#
# We wish you a pleasant journey.
#


import argparse
from PIL import Image
import os.path


sizes = {
    "idle"   : (1, 4),
    "walk"   : (8, 4),
    "swipe"  : (5, 4),
    "arrow"  : (12, 4),
    "magic"  : (6, 4),
    "thrust" : (7, 4),
    "fall_1" : (1, 1),
    "fall_2" : (1, 1),
    "fall_3" : (1, 1),
    "fall_4" : (1, 1),
    "fall_5" : (1, 1),
}


universal_offsets = {
    "magic"  : (1, 0),
    "thrust" : (1, 4),
    "idle"   : (0, 8),
    "walk"   : (1, 8),
    "swipe"  : (1, 12),
    "arrow"  : (1, 16),
    "fall_1" : (1, 20),
    "fall_2" : (2, 20),
    "fall_3" : (3, 20),                
    "fall_4" : (4, 20),
    "fall_5" : (5, 20),
}


body_offsets = {
    "idle"   : (0, 0),
    "walk"   : (1, 0),
    "swipe"  : (9, 0),
    "magic"  : (0, 4),
    "thrust" : (6, 4),
    "arrow"  : (0, 8),
    "fall_1" : (13, 4),
    "fall_2" : (13, 5),
    "fall_3" : (13, 6),
    "fall_4" : (13, 7),
    "fall_5" : (13, 8),
}

wiggle = {
    "fall_1" : -1,
    "fall_2" : -1,
    "fall_3" : -1,
    "fall_4" : -2,
    "fall_5" : -2,
}


def main(src_path, dest_path, underlay=False):
    source = Image.open(src_path)
    out = Image.new("RGBA", (896, 768), (0,0,0,0))

    for target in body_offsets.keys():
        size = [i*64 for i in sizes[target]]
        lpc_offset = [i*64 for i in universal_offsets[target]]
        body_offset = [i*64 for i in body_offsets[target]]

        if wiggle.has_key(target):
            x_mod = wiggle[target]
            body_offset[0] += x_mod

        copy_box = lpc_offset + [i+k for i,k in zip(size, lpc_offset)]
        paste_box = body_offset + [i+k for i,k in zip(size, body_offset)]
    
        region = source.crop(tuple(copy_box))
        out.paste(region, tuple(paste_box))

    if os.path.isfile(dest_path):
        old = Image.open(dest_path)
        args = [old, out]
        if underlay:
            args.reverse()
        combined = Image.alpha_composite(*args)
        combined.save(dest_path)
    else:
        out.save(dest_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
This script is for converting between the LPC universal sprite sheet
layout to the sprite sheet format used by some of Aeva's .gani files
for m.grl and other projects.""")
    
    #parser.add_argument(
    #    'mode', metavar="mode", type=str, nargs=1, default="body",
    #    help="One of: 'body', 'head', 'hair'.  Default is 'body'.")

    #parser.add_argument(
    #    '--underlay', action="store_true",
    #    help="""When using this command to paste sprites into an existing image,
    #paste beneath the image instead.""")
    
    parser.add_argument(
        'src', metavar="input", type=str, nargs=1,
        help="Input image map (universal style sheet format).")

    parser.add_argument(
        'dest', metavar="output", type=str, nargs=1,
        help="Output image map (custom format).")

    args = parser.parse_args()
    #mode = args.mode[0]
    mode = "body"
    src_path = args.src[0]
    out_path = args.dest[0]
    #underlay = args.underlay
    underlay = False
    if not mode in ["body", "head", "hair"]:
        print "Unknown output mode:", args.mode[0]
        exit()

    if not os.path.isfile(src_path):
        print "Bad path:", path
        exit()

    print mode, src_path, out_path
    main(src_path, out_path, underlay)
