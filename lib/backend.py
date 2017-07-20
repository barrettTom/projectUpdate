#!/usr/bin/python3

from lxml.etree import tostring, fromstring

def aoiReplace(template, project):
    pAois = project.findall("Controller/AddOnInstructionDefinitions")[0]
    tAois = template.findall("Controller/AddOnInstructionDefinitions")[0]
    tAois = pAois

def udtReplace(template, project):
    save = []
    for udt in project.iter("DataType"):
        if udt.attrib['Name'].find("StationData")       != -1:
            save.append(udt)
        elif udt.attrib['Name'].find("StationResults")  != -1:
            save.append(udt)

    pUdts = project.findall("Controller/DataTypes")[0]
    tUdts = template.findall("Controller/DataTypes")[0]
    
    for udt in save:
        pUdts.append(udt)

    tUdts = pUdts

def checkSA(program, template, parser):
    for templateProgram in template.iter("Program"):
        if templateProgram.attrib["Name"].find("CHECK_SA") != -1:
            replacementProgram = templateProgram

    machineNumber = program.attrib["Name"].split("_")[1][:3]

    replacementString = tostring(replacementProgram)
    replacementString = replacementString.replace(b"XXX", bytes(machineNumber, encoding="utf-8"))
    replacementProgram = fromstring(replacementString, parser = parser)

    program = replacementProgram

def powerSupply(program, template):
    for templateProgram in template.iter("Program"):
        if templateProgram.attrib["Name"].find("POWER_SUPPLY") != -1:
            replacementProgram = templateProgram

def devicesGeneral(program):
    print("devicesGeneral")

def plc(program):
    print("plc")

def operatorInterface(program):
    print("operatorInterface")

def busStructures(program):
    print("busStructures")

def safetyUnits(program):
    print("safetyUnits")

