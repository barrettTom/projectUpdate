#!/usr/bin/python3

from lxml.etree import tostring, fromstring

def getReplacementProgram(template, find):
    for templateProgram in template.iter("Program"):
        if templateProgram.attrib["Name"].find(find) != -1:
            replacementProgram = templateProgram

    return replacementProgram

def aoiReplace(project, template):
    pAois = project.findall("Controller/AddOnInstructionDefinitions")[0]
    tAois = template.findall("Controller/AddOnInstructionDefinitions")[0]
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

def checkSA(program, template, find, parser):
    replacementProgram = getReplacementProgram(template, find)

    machineNumber = program.attrib["Name"].split("_")[1][:3]

    replacementString = tostring(replacementProgram)
    replacementString = replacementString.replace(b"XXX", bytes(machineNumber, encoding="utf-8"))
    replacementProgram = fromstring(replacementString, parser = parser)

    return replacementProgram

def powerSupply(program, template, find):
    replacementProgram = getReplacementProgram(template, find)

    for routine in program.iter("Routine"):
        for replacementRoutine in replacementProgram.iter("Routine"):
            if routine.attrib['Name'] == "R20_Conditions":
                continue
            elif routine.attrib['Name'] == replacementRoutine.attrib['Name']:
                routine = replacementRoutine

def replaceAllRoutines(program, template, find):
    replacementProgram = getReplacementProgram(template, find)

    for routine in program.iter("Routine"):
        for replacementRoutine in replacementProgram.iter("Routine"):
            if routine.attrib['Name'] == replacementRoutine.attrib['Name']:
                routine = replacementRoutine
    
def plc(program, template, find):
    print("plc")

def busStructures(program, template, find):
    print("busStructures")

def safetyUnits(program, template, find):
    print("safetyUnits")
