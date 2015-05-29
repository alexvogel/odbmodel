from odbAccess import *
import sys
import re
class model(object):
    "all die auspraegungen"

    
    def __init__(self, argument):
#        self.batch    = argument.batch
        self.interactive = argument.interactive
        if (self.interactive):
            self.batch = False
        else:
            self.batch = True

        self.arg_odb  = str(argument.odb)
        self.odb      = self._getodb(self.arg_odb)

        
        self.arg_instance, self.instance = self._getinstance(str(argument.instance))

        self.arg_regiontype, self.regiontype = self._getregiontype(str(argument.nid), str(argument.eid), str(argument.nset), str(argument.elset))
        self.arg_region, self.region         = self._getregion(self.regiontype, str(argument.nid), str(argument.eid), str(argument.nset), str(argument.elset))

# self.field enthaelt nur die fields fuer die ermittelte region
        self.arg_output, self.output         = self._getoutput(str(argument.output))

        self.arg_postfunction, self.postfunction = self._getpostfunction(str(argument.postfunction))

        self.result = self._getresult()

#        if (self.batch is False):
#            self.gencall()
        
#        self.part     = argument.part
        
        if ((argument.elset is not "None") and (argument.nset is "None")):
            self.settype = "elset"
            self.elset    = argument.elset
        elif ((argument.elset is "None") and (argument.nset is not "None")):
            self.settype = "nset"
            self.nset     = argument.nset


    def gencall(self, batch, ):
        if (batch is False):
            print "to achieve the same information in batch mode call me:"
            print "abaqus python --odb sel"

    def print_args(self):
        for attribute, value in self.__dict__.iteritems():
            print attribute, value
            
    def check_odb_update_required(self):
        if isUpgradeRequiredForOdb(self.odbfile):
            print "The database is from a previous release of Abaqus."
            print "Run abaqus -upgrade -job <newFileName> -odb <oldOdbFileName> to upgrade it."
            sys.exit()
        else:
            print "no update is required for odb-File "+self.odbfile

# =============================
# Method: ermittlung des odb-objektes
# =============================
    def _getodb(self, odbfile):
        if isUpgradeRequiredForOdb(odbfile):
            print "The database is from a previous release of Abaqus."
            print "Run abaqus -upgrade -job <newFileName> -odb <oldOdbFileName> to upgrade it."
            sys.exit()
        else:
            if (self.batch == False):
                print "no update is required for odb-File "+odbfile
            
            odb=openOdb(odbfile)
            return(odb)

# =============================
# Method: ermittlung des output-objektes
# =============================
    def _getoutput(self, outputname):

        regiontype = self.regiontype

# eine einheitliche liste aus der region generieren
# falls ein nodeset oder elementset, so enthaelt die liste mehrere objekte, ansonsten nur 1
        region = self.region
        list_of_region = []

        if (regiontype == "nodeSets"):
            list_of_region = region.nodes       # hinzufuegen der nodeobjekte zur liste
        elif (regiontype == "elementSets"):
            list_of_region = region.elements    # hinzufuegen der elementobjekte zur liste
        else:
            list_of_region.append(region)       # hinzufuegen des node oder element objektes zur liste

## for debugging: drucken des listinhaltes
#        for region1 in list_of_region:
#                print region1
        
        try:
#            odb.steps[str(self.stepname)].frames
            output_array = []
            for region1 in list_of_region:
                output_array.append(getattr(region1, outputname))
#            odb.steps[self.stepname].frames
#            odb.steps[str(stepNames[desired_step_nr])].frames
#        except KeyError or TypeError:
        except:
            if (self.batch):
                print "modeldata '"+outputname+"' does not exist in region '"+regiontype+"'"
                sys.exit()
            else:
                print "======="
                print "These modeldata are available: "
                print "(example result) is from the first value of actual region: "
                print "-------"

                attrs = dir(list_of_region[0])
                selected_attrs = []                              #eine gefilterte liste erstellen (ohne __blabla__ etc)
                for attr in attrs:
                    if (re.match('[^_]', str(attr)) and str(attr) != "instance" and str(attr) != "dataDouble"):
                        selected_attrs.append(attr)
                
                outputNr = 0
                for selected_attr in selected_attrs:
                    try:
                        result = getattr(list_of_region[0], selected_attr)
                    except:
                        pass
#                        print "(" + str(outputNr) + ") " + selected_attr + " = "+str(result)
                    print "(" + str(outputNr) + ") " + selected_attr + " ("+str(result)+")"
                    outputNr+=1
                print "-------"

                # User Abfrage
                desired_output_nr = raw_input("Please specify output: ")
                while ((re.search('\D', str(desired_output_nr))) or ((len(selected_attrs)-1) < int(desired_output_nr)) or (int(desired_output_nr)) < 0):
#                    print desired_output_nr
                    desired_output_nr = raw_input("impermissible choice - please use an index mentioned above: ")

#                field = frame.fieldOutputs[fieldKeys[int(desired_output_nr)]].getSubset(region=self.region)
                outputname = str(selected_attrs[int(desired_output_nr)])
                print "You've chosen output '" +outputname+ "'"
                
                # bei nodeSets und elementSets gibt es mehrere Ergebnisdaten, deshalb ein array
                output_array = []
                for region1 in list_of_region:
                    output_array.append(getattr(region1, outputname))

        return (outputname, output_array)

        
# =============================
# Method: ermittlung der postfunction
# =============================
    def _getpostfunction(self, postfunction):

        postfunctions = ("none", "value_1", "value_2", "value_3", "vector")
        
        try: # feststellen, ob es die postfunction ueberhaupt gibt
            if (postfunction not in postfunctions):
                raise ('unknown postfunction '+ postfunction)
            else:
                return (postfunction, postfunction) 
            
        except:
            if (self.batch):
                print "error: unknown postfunction "+postfunction
                sys.exit()
            else:
                print "======="
                print "These postfunctions are available "
                print "If you don't know - try 'none' first"
                print "-------"

                postfunctionNr = 0
                
                for postfunction in postfunctions:
                    print "(" + str(postfunctionNr) + ") " + postfunction
                    postfunctionNr +=1
                print "-------"

                # User Abfrage
                desired_postfunction_nr = raw_input("Please specify postfunction: ")
                while ((re.search('\D', str(desired_postfunction_nr))) or ((len(postfunctions)-1) < int(desired_postfunction_nr)) or (int(desired_postfunction_nr)) < 0):
#                    print desired_coordsys_nr
                    desired_postfunction_nr = raw_input("impermissible choice - please use an index mentioned above: ")

                postfunction = postfunctions[int(desired_postfunction_nr)]
                print "You've chosen postfunction '" +postfunction+ "'"
                
                return (postfunction, postfunction)

# =============================
# Method: ermittlung des results
# =============================
    def _getresult(self):

        output_array = self.output
        
        ergebnis = self.output

        for output in output_array:

            if self.postfunction == "none":
                ergebnis = str(output)
            
            if self.postfunction == "value_1":
                search = re.search('([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?\s*)\s*,*\s*([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)\s*,*\s*([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)', str(output))
                if (search):
                    ergebnis = str(search.group(1))
                else:
                    ergebnis = "output '"+str(output)+"' doesn't match pattern used in postfunction 'value_1'"

            elif self.postfunction == "value_2":
                search = re.search('([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?\s*)\s*,*\s*([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)\s*,*\s*([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)', str(output))
                if (search):
                    ergebnis = str(search.group(3))
                else:
                    ergebnis = "output '"+str(output)+"' doesn't match pattern used in postfunction 'value_2'"

            elif self.postfunction == "value_3":
                search = re.search('([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?\s*)\s*,*\s*([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)\s*,*\s*([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)', str(output))
                if (search):
                    ergebnis = str(search.group(5))
                else:
                    ergebnis = "output '"+str(output)+"' doesn't match pattern used in postfunction 'value_3'"

            elif self.postfunction == "vector":
                search = re.search('([-+]?[0-9]*\.?[0-9]?+([eE][-+]?[0-9]+)?\s*)\s*,*\s*([-+]?[0-9]*\.?[0-9]?+([eE][-+]?[0-9]+)?)\s*,*\s*([-+]?[0-9]*\.?[0-9]?+([eE][-+]?[0-9]+)?)', str(output))
                if (search):
                    ergebnis = str(search.group())
                else:
                    ergebnis = "output '"+str(output)+"' doesn't match pattern used in postfunction 'vector'"

# ausgabe des ergebniswertes            
            print ergebnis

#        print self.output

        if (self.batch == False):
            print "To get the same information in batch mode, call:"
            command = "abaqus python "+sys.argv[0]+" --odb "+self.arg_odb+" --instance "+self.arg_instance+" --"+self.arg_regiontype+" "+str(self.arg_region)+" --output "+self.arg_output+" --postfunction "+self.arg_postfunction
            print command
        

# =============================
# Method: ermittlung der regiontypes
# =============================
    def _getregiontype(self, nid, eid, nset, elset):
        odb = self.odb
        arg_regiontype = ""
        
        if (nid != "None"):
            regiontype = "nodes"
            arg_regiontype = "nid"
        elif (eid != "None"):
            regiontype = "elements"
            arg_regiontype = "eid"
        elif (nset != "None"):
            regiontype = "nodeSets"
            arg_regiontype = "nset"
        elif (elset != "None"):
            regiontype = "elementSets"
            arg_regiontype = "elset"
        else:
            if (self.batch):
                print "no region (nid, eid, nset or elset) specified."
                sys.exit()
                

            print "======="
            print "This kind of output regions are available:"
            print "-------"
            
            regiontypeNr = 0
            regionTypes = ["nodes", "elements", "nodeSets", "elementSets"]
            arg_regionTypes = ["nid", "eid", "nset", "elset"]
            for regionType in regionTypes:
                print "(" + str(regiontypeNr) + ") " + regionType
                regiontypeNr+=1
            print "-------"
            
            # User Abfrage
            desired_regiontype_nr = raw_input("Please specify regionType: ")
            while ((re.search('\D', str(desired_regiontype_nr))) or ((len(regionTypes)-1) < int(desired_regiontype_nr)) or (int(desired_regiontype_nr)) < 0):
                print desired_regiontype_nr
                desired_regiontype_nr = raw_input("impermissible choice - please use an index mentioned above: ")

            regiontype = regionTypes[int(desired_regiontype_nr)]
            arg_regiontype = arg_regionTypes[int(desired_regiontype_nr)]
            print "You've chosen type '" +regiontype+ "'"
            
#        print "regiontype="+regiontype
#        print "RETURN: "+arg_regiontype+str(regiontype)
        return (arg_regiontype, regiontype)


# =============================
# Method: ermittlung der region
# =============================
    def _getregion(self, regiontype, nid, eid, nset, elset):
#        odb = self.odb
        instance = self.instance

# ermittlung der knotennummer, falls nicht bekannt
        if (regiontype == "nodes"):

            nodes = instance.nodes
            nid_existent = False
            for node in nodes:
                try:                # falls nid='None' ist, soll exception abgefangen werden
                    if (node.label == int(nid)):
                        nid_existent = True
                        return (node.label, node)
                except:
                    pass
            if ((nid_existent == False) and (self.batch)):
                print "nid '"+nid+"' does not exist in regiontype '"+regiontype+"'"
                sys.exit()
            
            else:
                nodes = instance.nodes
                amount_nodes = len(nodes)
                print "======="
                print str(amount_nodes)+" nodes are available in instance '"+instance.name+"'"
                print "-------"
            
            # User Abfrage
                desired_nid = input("Please specify nid: ")

                searching_nid = True;
            
                while(searching_nid):
                    for node in nodes:
                        try:
                            if (node.label == desired_nid):
#                            print "nid "+str(desired_nid)+" found"
                                print "You've chosen node '" +str(node.label)+ "'"
                                return (node.label, node)
                                searching_nid = False;
                        except:
                            pass
                    if (searching_nid):
                        desired_nid = input("node nid="+str(desired_nid)+" not found - please try again: ")

        elif (regiontype == "elements"):

            elements = instance.elements
            eid_existent = False
            for element in elements:
                try:                # falls eid='None' ist, soll exception abgefangen werden
                    if (element.label == int(eid)):
                        eid_existent = True
                        return (element.label, element)
                except:
                    pass
            if ((eid_existent == False) and (self.batch)):
                print "eid '"+eid+"' does not exist in regiontype '"+regiontype+"'"
                sys.exit()
            
            else:
                elements = instance.elements
                amount_elements = len(elements)
                print "======="
                print str(amount_elements)+" elements are available in instance '"+instance.name+"'"
                print "-------"
            
            # User Abfrage
                desired_eid = input("Please specify eid: ")

                searching_eid = True;
            
                while(searching_eid):
                    for element in elements:
                        try:
                            if (element.label == desired_eid):
#                            print "nid "+str(desired_nid)+" found"
                                print "You've chosen element '" +str(element.label)+ "'"
                                return (element.label, element)
                                searching_eid = False;
                        except:
                            pass
                    if (searching_eid):
                        desired_eid = input("element eid="+str(desired_eid)+" not found - please try again: ")

        elif (regiontype == "nodeSets"):

#            nset_existent = False
            nodeset = "unbekannt"
            
            try:                # falls eid='None' ist, soll exception abgefangen werden
                nodeset = instance.nodeSets[nset]
            except:
                if (self.batch):
                    print "nset '"+nset+"' does not exist in regiontype '"+regiontype+"'"
                    sys.exit()
            
                else:
                    print "======="
                    print "This nodeSets are available:"
                    print "-------"
            
                    nodesetKeys = instance.nodeSets.keys()
                    nodesetNr = 0
                    for nodesetKey in nodesetKeys:
                        print "(" + str(nodesetNr) + ") " + nodesetKey
                        nodesetNr+=1
                    print "-------"
            
            # User Abfrage
                    desired_nodeset_nr = raw_input("Please specify nodeSet: ")
                    while ((re.search('\D', str(desired_nodeset_nr))) or ((len(nodesetKeys)-1) < int(desired_nodeset_nr)) or (int(desired_nodeset_nr)) < 0):
                        print desired_nodeset_nr
                        desired_nodeset_nr = raw_input("impermissible choice - please use an index mentioned above: ")

                    nodeset = instance.nodeSets[nodesetKeys[int(desired_nodeset_nr)]]
                    print "You've chosen nodeSet '" +nodeset.name+ "'"
                    print "======="
                
            return (nodeset.name, nodeset)

        elif (regiontype == "elementSets"):

            elementset = "unbekannt"
            
            try:                # falls eid='None' ist, soll exception abgefangen werden
                elementset = instance.elementSets[elset]
            except:
                if (self.batch):
                    print "elset '"+elset+"' does not exist in regiontype '"+regiontype+"'"
                    sys.exit()
            
                else:
                    print "======="
                    print "This elementSets are available:"
                    print "-------"
            
                    elementsetKeys = instance.elementSets.keys()
                    elementsetNr = 0
                    for elementsetKey in elementsetKeys:
                        print "(" + str(elementsetNr) + ") " + elementsetKey
                        elementsetNr+=1
                    print "-------"
            
            # User Abfrage
                    desired_elementset_nr = raw_input("Please specify elementSet: ")
                    while ((re.search('\D', str(desired_elementset_nr))) or ((len(elementsetKeys)-1) < int(desired_elementset_nr)) or (int(desired_elementset_nr)) < 0):
                        print desired_elementset_nr
                        desired_elementset_nr = raw_input("impermissible choice - please use an index mentioned above: ")

                    elementset = instance.elementSets[elementsetKeys[int(desired_elementset_nr)]]
                    print "You've chosen elementSet '" +elementset.name+ "'"
                    print "======="
                
            return (elementset.name, elementset)

# =============================
# Method: ermittlung des instance-objektes
# =============================
    def _getinstance(self, instance_name):

        odb = self.odb
        try:
            instance = odb.rootAssembly.instances[instance_name]
#        except KeyError or TypeError:
        except:
            if (self.batch):
                print "instance '"+instance+"' not found in odb '"+odb.name+"'"
                sys.exit()
            else:
                print "======="
                print "These instances are available in " + odb.name# + str(odb.sectionCategories)
                print "-------"

                instanceNr = 0
                instanceKeys = odb.rootAssembly.instances.keys()
                for instanceKey in instanceKeys:
                    print "(" + str(instanceNr) + ") " + instanceKey
                    instanceNr+=1
                print "-------"

                # User Abfrage
                desired_instance_nr = raw_input("Please specify instance: ")
                while ((re.search('\D', str(desired_instance_nr))) or ((len(instanceKeys)-1) < int(desired_instance_nr)) or (int(desired_instance_nr)) < 0):
                    print desired_instance_nr
                    desired_instance_nr = raw_input("impermissible choice - please use an index mentioned above: ")

                instance = odb.rootAssembly.instances[instanceKeys[int(desired_instance_nr)]]
                print "You've chosen instance '" +instance.name+ "'"
                return (instance.name, instance)
        
        return (instance_name, instance)
