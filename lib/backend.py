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

def replaceAllButSpecificRoutines(program, replacementProgram, routineNamesToSkip):
    changes = []

    for routine in program.iter("Routine"):
        skip = False
        for routineNameToSkip in routineNamesToSkip:
            if routine.attrib['Name'] == routineNameToSkip:
                skip = True
        
        if not skip:
            for replacementRoutine in replacementProgram.iter("Routine"):
                if routine.attrib['Name'] == replacementRoutine.attrib['Name']:
                    changes.append({'original'      : routine,
                                    'replacement'   : replacementRoutine})

    for change in changes:
        parent = change['original'].getparent()
        parent.replace(change['original'], change['replacement'])

    return program

def replaceSpecificRoutineRungs(program, replacementProgram, routineNamesAndRungs):
    changes = []
    for routine in program.iter("Routine"):
        skip = False
        for routineNameAndRungs in routineNamesAndRungs:
            if routine.attrib["Name"] == routineNameAndRungs["Name"]:
                skip = True

        if not skip:
            for replacementRoutine in replacementProgram.iter("Routine"):
                if routine.attrib["Name"] == replacementRoutine.attrib["Name"]:
                        changes.append({'original'      :   routine,
                                        'replacement'   :   replacementRoutine})
    for change in changes:
        parent = change['original'].getparent()
        parent.replace(change['original'], change['replacement'])

    for routineNameAndRungs in routineNamesAndRungs:
        if routineNameAndRungs['Type'] == "Keep":
            program = replaceAllButSpecificRungs(program, replacementProgram, routineNameAndRungs)
        elif routineNameAndRungs['Type'] == "Replace":
            program = replaceSpecificRungs(program, replacementProgram, routineNameAndRungs)
    
    return program

def replaceSpecificRungs(program, replacementProgram, routineNameAndRungs):
    changes = []

    for routine in program.iter("Routine"):
        for replacementRoutine in replacementProgram.iter("Routine"):
            if routine.attrib['Name'] == replacementRoutine.attrib["Name"] == routineNameAndRungs["Name"]:
                for rung in routine.iter("Rung"):
                    for replacementRung in replacementRoutine.iter("Rung"):
                        for rungNumber in routineNameAndRungs["Rungs"]:
                            if rung.attrib["Number"] == replacementRung.attrib["Number"] == rungNumber:
                                changes.append({'original'      :   rung,
                                                'replacement'   :   replacementRung})

    for change in changes:
        parent = change['original'].getparent()
        parent.replace(change['original'], change['replacement'])

    return program


def replaceAllButSpecificRungs(program, replacementProgram, routineNameAndRungs):
    changes = []

    for routine in program.iter("Routine"):
        for replacementRoutine in replacementProgram.iter("Routine"):
            if routine.attrib['Name'] == replacementRoutine.attrib["Name"] == routineNameAndRungs["Name"]:
                for rung in routine.iter("Rung"):
                    skip = False
                    for rungNumber in routineNameAndRungs["Rungs"]:
                        if rung.attrib["Number"] == rungNumber:
                            skip = True
                    if not skip:
                        for replacementRung in replacementRoutine.iter("Rung"):
                            if rung.attrib["Number"] == replacementRung.attrib["Number"]:
                                changes.append({'original'      :   rung,
                                                'replacement'   :   replacementRung})

    for change in changes:
        parent = change['original'].getparent()
        parent.replace(change['original'], change['replacement'])

    return program
