#!/usr/bin/python3

from lxml.etree import tostring, fromstring, XMLParser

def getReplacementProgram(template, find, machineNumber):
    for templateProgram in template.iter("Program"):
        if templateProgram.attrib["Name"].find(find) != -1:
            program = templateProgram

    program = XXXreplace(program, machineNumber)

    return program

def XXXreplace(program, machineNumber):
    parser = XMLParser(strip_cdata=False, resolve_entities=False)

    string = tostring(program)

    string = string.replace(b"XXX", bytes(machineNumber, encoding="utf-8"))

    program = fromstring(string, parser = parser)

    return program

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

def replaceAllRoutines(template, find, machineNumber):
    return getReplacementProgram(template, find, machineNumber)

def powerSupply(program, template, find, machineNumber):
    replacementProgram = getReplacementProgram(template, find, machineNumber)

    changes = []

    for routine in program.iter("Routine"):
        for replacementRoutine in replacementProgram.iter("Routine"):
            if routine.attrib['Name'] == "R20_Conditions":
                continue
            elif routine.attrib['Name'] == replacementRoutine.attrib['Name']:
                changes.append({'original'      : routine,
                                'replacement'   : replacementRoutine})

    for change in changes:
        parent = change['original'].getparent()
        parent.replace(change['original'], change['replacement'])

    return program

def plc(program, template, find, machineNumber):
    replacementProgram = getReplacementProgram(template, find, machineNumber)

    changes = []

    for routine in program.iter("Routine"):
        for replacementRoutine in replacementProgram.iter("Routine"):
            if routine.attrib['Name'] == "R10_BootCycle":
                continue
            elif routine.attrib['Name'] == "R11_MotionGroup":
                continue
            elif routine.attrib['Name'] == replacementRoutine.attrib['Name']:
                changes.append({'original'      : routine,
                                'replacement'   : replacementRoutine})

    for change in changes:
        parent = change['original'].getparent()
        parent.replace(change['original'], change['replacement'])

    return program

def busStructures(program, template, find, machineNumber):
    replacementProgram = getReplacementProgram(template, find, machineNumber)

    changes = []

    for routine in program.iter("Routine"):
        for replacementRoutine in replacementProgram.iter("Routine"):
            if routine.attrib['Name'] == "R00_S01_Init":
                continue
            elif routine.attrib['Name'] == "R22_PIO_Diagnostics":
                continue
            elif routine.attrib['Name'] == replacementRoutine.attrib['Name']:
                changes.append({'original'      : routine,
                                'replacement'   : replacementRoutine})

    for change in changes:
        parent = change['original'].getparent()
        parent.replace(change['original'], change['replacement'])

    return program

def safetyUnits(program, template, find):
    print("safetyUnits")

def controlCircuit(program, template, find):
    print("controlCircuit")

def scada(program, template, find):
    print("scada")
    return program

def station(program, template):
    print(program.attrib['Name'])

def machine(program, template):
    print(program.attrib['Name'])
