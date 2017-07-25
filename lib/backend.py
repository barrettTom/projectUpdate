from lxml.etree import tostring, fromstring, XMLParser

def getMachineInfo(pRoot):
    for program in pRoot.iter("Program"):
        name = program.attrib["Name"].split("_")
        if len(name[1]) == 3:
            return name[1], "_".join(name[2:])

def aoiReplace(project, template):
    save = []
    for aoi in project.iter("AddOnInstructionDefinition"):
        if aoi.attrib['Name'].find("Pinning")           != -1:
            save.append(aoi)

    pAois = project.find("Controller/AddOnInstructionDefinitions")
    tAois = template.find("Controller/AddOnInstructionDefinitions")

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

    pUdts = project.find("Controller/DataTypes")
    tUdts = template.find("Controller/DataTypes")
    
    for udt in save:
        tUdts.append(udt)

    return pUdts, tUdts

def replaceWholeProgram(template, find, machineNumber, machineName):
    for templateProgram in template.iter("Program"):
        if templateProgram.attrib["Name"].find(find) != -1:
            program = templateProgram

    parser = XMLParser(strip_cdata=False, resolve_entities=False)

    string = tostring(program)

    string = string.replace(b"XXX", bytes(machineNumber, encoding="utf-8"))
    string = string.replace(b"MACHINE_NAME", bytes(machineName, encoding="utf-8"))

    program = fromstring(string, parser = parser)

    return program

def replaceSpecificRoutineRungs(program, replacementProgram, routineNamesAndRungs):
    for routine in program.iter("Routine"):
        skip = False
        for routineNameAndRungs in routineNamesAndRungs:
            if routine.attrib["Name"].find(routineNameAndRungs["Name"]) != -1:
                skip = True
        if not skip:
            for replacementRoutine in replacementProgram.iter("Routine"):
                if routine.attrib["Name"] == replacementRoutine.attrib["Name"]:
                    parent = routine.getparent()
                    parent.replace(routine, replacementRoutine)

    for routineNameAndRungs in routineNamesAndRungs:
        if routineNameAndRungs['Type'] == "Keep":
            program = replaceAllButSpecificRungs(program, replacementProgram, routineNameAndRungs)
        elif routineNameAndRungs['Type'] == "Replace":
            program = replaceSpecificRungs(program, replacementProgram, routineNameAndRungs)
        elif routineNameAndRungs['Type'] == "KeepWhole":
            continue
    
    return program

def negativeFix(number, routine):
    if int(number) >= 0:
        return number
    else:
        return len(routine.findall("*/Rung")) - 1 + int(number)

def findRoutine(program, routineName):
    for routine in program.iter("Routine"):
        if routine.attrib['Name'].find(routineName) != -1:
            return routine

def findRung(routine, rungNumber):
    for rung in routine.iter("Rung"):
        if rung.attrib["Number"] == rungNumber:
            return rung

def replaceSpecificRungs(program, replacementProgram, routineNameAndRungs):
    routine = findRoutine(program, routineNameAndRungs["Name"])
    replacementRoutine = findRoutine(replacementProgram, routineNameAndRungs["Name"])

    if routine is not None and replacementRoutine is not None:
        for rungNumber in routineNameAndRungs["Rungs"]:
            fixedNumber = negativeFix(rungNumber, routine)
            rung = findRung(routine, fixedNumber)
            replacementRung = findRung(replacementRoutine, fixedNumber)
            if rung is not None and replacementRung is not None:
                parent = rung.getparent()
                parent.replace(rung, replacementRung)

    return program

def replaceAllButSpecificRungs(program, replacementProgram, routineNameAndRungs):
    routine = findRoutine(program, routineNameAndRungs["Name"])
    replacementRoutine = findRoutine(replacementProgram, routineNameAndRungs["Name"])

    if routine is not None and replacementRoutine is not None:
        for rung in routine.iter("Rung"):
            skip = False
            numbers = [negativeFix(rungNumber, routine) for rungNumber in routineNameAndRungs["Rungs"]]
            if rung.attrib["Number"] in numbers:
                skip = True
            if not skip:
                for replacementRung in replacementRoutine.iter("Rung"):
                    if rung.attrib["Number"] == replacementRung.attrib["Number"]:
                        parent = rung.getparent()
                        parent.replace(rung, replacementRung)

    return program
