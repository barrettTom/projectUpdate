#!/usr/bin/python3

from lxml.etree import tostring, fromstring, XMLParser

def aoiReplace(project, template):
    save = []
    for aoi in project.iter("AddOnInstructionDefinition"):
        if aoi.attrib['Name'].find("Pinning")           != -1:
            save.append(aoi)

    pAois = project.findall("Controller/AddOnInstructionDefinitions")[0]
    tAois = template.findall("Controller/AddOnInstructionDefinitions")[0]

    for aoi in save:
        tAois.append(aoi)

    return pAois, tAois

def udtReplace(project, template):
    save = []
    for udt in project.iter("DataType"):
        if udt.attrib['Name'].find("StationData")       != -1:
            save.append(udt)
        elif udt.attrib['Name'].find("StationResults")  != -1:
            save.append(udt)

    pUdts = project.findall("Controller/DataTypes")[0]
    tUdts = template.findall("Controller/DataTypes")[0]
    
    for udt in save:
        tUdts.append(udt)

    return pUdts, tUdts

def replaceWholeProgram(template, find, machineNumber):
    for templateProgram in template.iter("Program"):
        if templateProgram.attrib["Name"].find(find) != -1:
            program = templateProgram

    parser = XMLParser(strip_cdata=False, resolve_entities=False)

    string = tostring(program)

    string = string.replace(b"XXX", bytes(machineNumber, encoding="utf-8"))

    program = fromstring(string, parser = parser)

    return program

def replaceSpecificRoutines(program, replacementProgram, routineNamesToSkip):
    changes = []

    for routine in program.iter("Routine"):
        for replacementRoutine in replacementProgram.iter("Routine"):
            skip = False
            for routineNameToSkip in routineNamesToSkip:
                if routine.attrib['Name'] == routineNameToSkip:
                    skip = True

            if routine.attrib['Name'] == replacementRoutine.attrib['Name'] and not skip:
                changes.append({'original'      : routine,
                                'replacement'   : replacementRoutine})

    for change in changes:
        parent = change['original'].getparent()
        parent.replace(change['original'], change['replacement'])

    return program
