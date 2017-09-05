from lxml.etree import tostring, fromstring, XMLParser

def getMachineInfo(pRoot):
    for program in pRoot.iter("Program"):
        name = program.attrib["Name"].split("_")
        if len(name[1]) == 3:
            return name[1], "_".join(name[2:])

def desReplace(project, template, machineNumber):
    pDes = project.find("Controller/Description")
    tDes = template.find("Controller/Description")

    pDes.text = tDes.text.replace("XXX", machineNumber)

def tskReplace(project, template):
    for task in project.iter("Task"):
        if task.attrib["Name"] == "T01_Main":
            pTask = task

    for task in template.iter("Task"):
        if task.attrib["Name"] == "T01_Main":
            tTask = task

    pTask.attrib["Watchdog"] = tTask.attrib["Watchdog"]
    pTask.attrib["Priority"] = tTask.attrib["Priority"]

def aoiReplace(project, template):
    pAois = project.find("Controller/AddOnInstructionDefinitions")
    tAois = template.find("Controller/AddOnInstructionDefinitions")

    pAois.getparent().replace(pAois, tAois)

def udtReplace(project, template):
    save = []
    for udt in project.iter("DataType"):
        if "StationData" in udt.attrib['Name']:
            save.append(udt)
        elif "StationResults" in udt.attrib['Name']:
            save.append(udt)

    pUdts = project.find("Controller/DataTypes")
    tUdts = template.find("Controller/DataTypes")
    
    for udt in save:
        tUdts.append(udt)

    pUdts.getparent().replace(pUdts, tUdts)

def findRoutine(program, routineName):
    for routine in program.iter("Routine"):
        if routineName in routine.attrib['Name']:
            return routine

def findRung(routine, rungNumber):
    for rung in routine.iter("Rung"):
        if rung.attrib["Number"] == rungNumber:
            return rung

def getTemplateProgram(template, find, machineNumber, machineName):
    for templateProgram in template.iter("Program"):
        if find in templateProgram.attrib["Name"]:
            program = templateProgram

    string = tostring(program)

    string = string.replace(b"XXX", bytes(machineNumber, encoding="utf-8"))
    string = string.replace(b"MACHINE_NAME", bytes(machineName, encoding="utf-8"))

    program = fromstring(string, parser = XMLParser(strip_cdata=False))

    return program

def replaceRoutines(program, replacementProgram, routineNamesAndRungs):
    for routine in program.iter("Routine"):
        skip = False
        for routineNameAndRungs in routineNamesAndRungs:
            if routineNameAndRungs["Name"] in routine.attrib["Name"]:
                skip = True
        if not skip:
            for replacementRoutine in replacementProgram.iter("Routine"):
                if routine.attrib["Name"] == replacementRoutine.attrib["Name"]:
                    routine.getparent().replace(routine, replacementRoutine)

    for routineNameAndRungs in routineNamesAndRungs:
        routine = findRoutine(program, routineNameAndRungs["Name"])
        replacementRoutine = findRoutine(replacementProgram, routineNameAndRungs["Name"])

        if routine is not None and replacementRoutine is not None:
            if routineNameAndRungs['Type'] == "Keep":
                replaceAllButSpecificRungs(routine, replacementRoutine, routineNameAndRungs["Rungs"])
            elif routineNameAndRungs['Type'] == "Replace":
                replaceSpecificRungs(routine, replacementRoutine, routineNameAndRungs["Rungs"])
            elif routineNameAndRungs['Type'] == "KeepWhole":
                continue

def replaceSpecificRungs(routine, replacementRoutine, rungNumbers):
    for rungNumber in rungNumbers:
        rung = findRung(routine, rungNumber)
        replacementRung = findRung(replacementRoutine, rungNumber)
        if rung is not None and replacementRung is not None:
            rung.getparent().replace(rung, replacementRung)

def replaceAllButSpecificRungs(routine, replacementRoutine, rungNumbers):
    for rung in routine.iter("Rung"):
        skip = False
        if rung.attrib["Number"] in rungNumbers:
            skip = True
        if not skip:
            replacementRung = findRung(replacementRoutine, rung.attrib["Number"])
            if replacementRung is not None:
                rung.getparent().replace(rung, replacementRung)
