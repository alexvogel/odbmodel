#!/usr/bin/python

import sys

if len(sys.argv)!=2:
    print "call: abaqus python $scriptname $odbfile"
    sys.exit()

from odbAccess import *
from textRepr import *

odbfile = sys.argv[1]
if isUpgradeRequiredForOdb(odbfile):
    print "The database is from a previous release of Abaqus."
    print "Run abaqus -upgrade -job <newFileName> -odb <oldOdbFileName> to upgrade it."
    sys.exit()

odb=openOdb(odbfile)

###############################
#
# Metadaten listen
#
###############################
print "======="
print "These metadata are available in " + odb.name
print "-------"

#print odb.materials
sectionassignmentNr = 0
print odb.rootAssembly.instances['PART-1-1'].elementSets['X7239205_FRONTKLAPPE_AUSSENHAUT_M1A_FRGMOD_0P7MM']

sys.exit()

###############################
#
# Materialdaten listen
#
###############################
print "======="
print "These materials are available in " + odb.name
print "-------"

#print odb.materials
matNr = 0
mats = odb.materials.keys()

for mat in mats:
    print "(" + str(matNr) + ") " + mat
    matNr+=1
print "-------"

desired_mat_nr = input("Please specify the material of desire: ")

while (((len(mats)-1) < desired_mat_nr ) or (desired_mat_nr < 0)):
    desired_mat_nr = input("unknown choice - please use a index mentioned above: ")

mat = mats[desired_mat_nr]
print "You've chosen mat '" + mat + "'"

###############################
#
# Koordinatensysteme listen
#
###############################
print "======="
print "These coordinate systems are available in " + odb.name
print "-------"

orientationNr = 0
orientations = odb.rootAssembly.connectorOrientations
#print orientations

for orientation in orientations:
    if orientation.localCsys1:
        print "(" + str(orientationNr) + ") " + orientation.localCsys1.name
    else:
        print "(" + str(orientationNr) + ") " + "None"
    orientationNr+=1

print "-------"

desired_orientation_nr = input("Please specify the orientation of desire: ")

while (((len(orientations)-1) < desired_orientation_nr ) or (desired_orientation_nr < 0)):
    desired_orientation_nr = input("unknown choice - please use a index mentioned above: ")

if orientations[desired_orientation_nr].localCsys1:
    orientation = orientations[desired_orientation_nr].localCsys1.name
    print "You've chosen orientation '" + orientation + "'"
else:
    print "You've chosen orientation 'None'"

###############################
#
# Partabfrage
#
###############################
print "======="
print "These parts are available in " + odb.name
print "-------"

partNr = 0
#parts = odb.parts.keys()
parts = odb.rootAssembly.instances.keys()

for part in parts:
    print "(" + str(partNr) + ") " + part
    partNr+=1
print "-------"

desired_part_nr = input("Please specify the part of desire: ")

while (((len(parts)-1) < desired_part_nr ) or (desired_part_nr < 0)):
    desired_part_nr = input("unknown choice - please use a index mentioned above: ")

part = parts[desired_part_nr]
print "You've chosen part '" + part + "'"


###############################
#
# elset Abfrage
#
###############################
print "======="
print "These elementsets are available in " + part
print "-------"

elsetNr = 0
#parts = odb.parts.keys()
elsets = odb.rootAssembly.instances[part].elementSets.keys()

for elset in elsets:
    print "(" + str(elsetNr) + ") " + elset
    elsetNr+=1
print "-------"

desired_elset_nr = input("Please specify the elementset of desire: ")

while (((len(elsets)-1) < desired_elset_nr ) or (desired_elset_nr < 0)):
    desired_elset_nr = input("unknown choice - please use a index mentioned above: ")

elset = elsets[desired_elset_nr]
print "You've chosen elset '" + elset + "'"


elsetinhalt = odb.rootAssembly.instances[part].elementSets[elset]
print elsetinhalt

###############################
#
# nodeset Abfrage
#
###############################
print "======="
print "These nodesets are available in " + part
print "-------"

setNr = 0
#parts = odb.parts.keys()
nodesets = odb.rootAssembly.instances[part].nodeSets.keys()

for nodeset in nodesets:
    print "(" + str(setNr) + ") " + nodeset
    setNr+=1
print "-------"

desired_nodeset_nr = input("Please specify the nodeset of desire: ")

while (((len(nodesets)-1) < desired_nodeset_nr ) or (desired_nodeset_nr < 0)):
    desired_nodeset_nr = input("unknown choice - please use a index mentioned above: ")

nodeset = nodesets[desired_nodeset_nr]
print "You've chosen elset '" + nodeset + "'"


nodesetinhalt = odb.rootAssembly.instances[part].nodeSets[nodeset]
print nodesetinhalt


###############################
#
# nodes of nodeset Abfrage
#
###############################
print "======="
print "These nodesets are defined in " + nodeset
print "-------"

setNr = 0
#parts = odb.parts.keys()
nodes = odb.rootAssembly.instances[part].nodeSets[nodeset].nodes

nodeobj = nodes[1].coordinates
nodeobj2 = nodes[1].label
print nodeobj
print nodeobj2

exit(0)

