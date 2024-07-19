import spatialdata
import spatialdata_plot
import napari
import napari_spatialdata

import sopa.segmentation
import sopa.io

import argparse
from loguru import logger
import os
import ast

def get_args():

    description="""Segment with many parameters"""

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)

    inputs = parser.add_argument_group(title="Required Input", description="Path to required input file")
    inputs.add_argument("-i", "--image",    dest="image",       action="store", required=True, help="File path to input image or folder with images")
    inputs.add_argument("-o", "--output",   dest="output",      action="store", required=True, help="Path to output file or folder")

    inputs.add_argument("-pw", "--patch-width",     dest="patch_width", action="store", default=1000, help="Patch width")
    inputs.add_argument("-po", "--patch-overlap",   dest="patch_overlap", action="store", default=75, help="Patch overlap")

    inputs.add_argument("-c", "--channels",         dest="channels",    action="store", required=True, default=None, help="Channels to segment")
    inputs.add_argument("-m", "--model",            dest="model",       action="store", required=True, default=None, help="Model to use for segmentation")
    inputs.add_argument("-ft", "--flow-threshold",  dest="flow_threshold", action="store", default=0.4, help="Flow threshold for cellpose")
    inputs.add_argument("-cpt", "--cellprobability-threshold",  dest="cellprob_threshold", action="store", default=-4, help="Cell probability threshold for cellpose")
    inputs.add_argument("-d", "--diameter",         dest="diameter",   action="store", default=0, help="Cell size for cellpose")

    inputs.add_argument("-ll", "--log-level",   dest="loglevel", default='INFO', choices=["DEBUG", "INFO"], help='Set the log level (default: INFO)')

    arg = parser.parse_args()
    arg.image   = os.path.abspath(arg.image)
    arg.output  = os.path.abspath(arg.output)
    arg.channels = ast.literal_eval(arg.channels)
    return arg

def check_inputs(args):
    assert os.path.exists(args.image), f"Input image cannot be found : {args.image}"
    assert isinstance(args.patch_width, int), "Patch width must be an integer"
    assert args.patch_width > 0, "Patch width must be greater than 0"
    assert isinstance(args.patch_overlap, int), "Patch overlap must be an integer"
    assert args.patch_overlap > 0, "Patch overlap must be greater to 0"
    assert isinstance(args.channels, list), "Channels must be a string"
    assert isinstance(args.model, str), "Model must be a string"
    assert isinstance(args.flow_threshold, float), "Flow threshold must be a float"
    assert isinstance(args.cellprob_threshold, int), "Cell probability threshold must be an integer"
    assert isinstance(args.diameter, int), "Diameter must be an integer"

def create_sdata_object(args):
    sdata = sopa.io.ome_tif(args.image, as_image=False)
    logger.info(f"Loaded image into spatialdata object")
    return sdata

def create_patches(sdata, args):
    patches = sopa.segmentation.Patches2D(sdata, element_name="991_subset", patch_width=args.patch_width, patch_overlap=args.patch_overlap)
