import sys
import os
odbmodel_version = "[% version %]"
odbmodel_date = "[% date %]"

# 0.01    Erste Version bei BMW
# 0.02    09.02.2012    kleinere Aenderungen an Hilfetext
# 0.1     04.02.2013    Zusaetzlicher Parameter 'postfunction' implementiert

external_lib = os.path.realpath(os.path.dirname(sys.argv[0])) + "/../lib"
sys.path.append(external_lib)
#print sys.path
import argparse
from model import *

# Definieren der Kommandozeilenparameter
parser = argparse.ArgumentParser(description='a tool for extracting model data from an abaqus output database file.',
                                 epilog='author: alexander.vogel@caegroup.de | version: '+odbmodel_version+' | date: '+odbmodel_date)
parser.add_argument('--odb', metavar='ODBFILE', type=str, required=True,
                   help='abaqus output database file')
parser.add_argument('--instance', metavar='INSTANCE', action='store', default='PART-1-1',
                   help='part of the model e.g. PART-1-1')
parser.add_argument('--output', metavar='OUTPUT', action='store',
                   help='name of output variable. e.G. coordinates, label')
parser.add_argument('--postfunction', metavar='POSTFUNCTION', action='store',
                   help='name of function to manipulate retrieved values.')
parser.add_argument('--interactive', "-i", action='store_true', default=False,
                   help='interactive mode.')

# Exklusivgruppen der Parameter
group_2 = parser.add_mutually_exclusive_group()
group_2.add_argument('--elset', metavar='ELSETNAME', action='store',
                   help='name of element set')
group_2.add_argument('--nset', metavar='NSETNAME', action='store',
                   help='name of node set')
group_2.add_argument('--nid', metavar='NID', action='store',
                   help='node id')
group_2.add_argument('--eid', metavar='EID', action='store',
                   help='element id')

args = parser.parse_args()

ergebniswert = model(args)
