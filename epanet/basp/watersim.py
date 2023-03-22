
#!/usr/bin/python
from __future__ import print_function
import json
from datetime import datetime
import datetime as dtm
import os
from basp.outbin import EpanetOutBin
import basp.readEpanetFile as d
import basp.epamodule as em
import basp.databaseTables as databaseTables
import basp.dbcommunication as dbcommunication
import itertools
import math
import random
from operator import itemgetter
import subprocess
import shutil
import wntr
from . import sensorsProfile


def readinputfile(initial_input_filename, epanet_keywords):
    initial_input_file = open(initial_input_filename)
    finalresult = []
    currentresult = []
    RecordingMode = False
    for line in initial_input_file:
        if line.strip() in epanet_keywords:
            if len(currentresult) != 0:
                finalresult.append(currentresult)
            currentresult = []
            currentresult.append(line.strip())
        else:
            if len(line.strip()) != 0:
                currentresult.append(line.strip())
    return finalresult


def addtodata(ids, uneditedmeasurements, placetosave, category):
    if len(uneditedmeasurements) > 1:
        if category == 'CURVES':
            for details in uneditedmeasurements:
                if details[0] != '[' and details[0] != ';':
                    result = [x.strip() for x in details.split('\t')]
                    result = list(filter(None, result))
                    data = {}
                    for x in range(0, len(ids)):
                        textid = ids[x]
                        try:
                            data[textid] = result[x]
                        except:
                            data[textid] = ''
                    placetosave.append(data)
        elif category == 'REACTIONS' or category == 'ENERGY' or category == 'TIMES' or category == 'REPORT' or category =='OPTIONS':
            for details in uneditedmeasurements:
                if details[0] != '[' and details[0] != ';':
                    result = [x.strip() for x in details.split('\t')]
                    data = {}
                    for x in range(0, len(ids)):
                        textid = ids[x]
                        try:
                            data[textid] = result[x]
                        except:
                            data[textid] = ''
                    placetosave.append(data)
        elif category == 'PATTERNS' or category == 'BACKDROP':
            for details in uneditedmeasurements:
                if details[0] != '[' and details[0] != ';':
                    details = details.replace('\t\t', '\t')
                    result = [x.strip() for x in details.split('\t')]
                    data = {}
                    try:
                        data[ids[0]] = result[0]
                    except:
                        pass
                    try:
                        data[ids[1]] = ','.join(result[1:])
                    except:
                        pass
                    placetosave.append(data)
        elif category == 'RULES':
            data = []
            placetosave1 = []
            for details in uneditedmeasurements:
                if details[0] != '[' and details[0] != ';':
                    if 'RULE' in details:
                        if data:
                            placetosave1.append(data)
                        data = []
                        data.append(details.strip())
                    else:
                        data.append(details.strip())
            if data:
                placetosave1.append(data)
            for value in placetosave1:
                data = {}
                try:
                    data[ids[0]] = value[0]
                except:
                    pass
                try:
                    data[ids[1]] = ' \n '.join(value[1:])
                except:
                    pass
                placetosave.append(data)
        else:
            for details in uneditedmeasurements:
                if details[0] != '[' and details[0] != ';':
                    result = [x.strip() for x in details.split('\t')]
                    result = list(filter(None, result))
                    data = {}
                    for x in range(0, len(ids)):
                        textid = ids[x]
                        try:
                            data[textid] = result[x]
                        except:
                            data[textid] = ''
                    placetosave.append(data)


def addinfotolists(finalresult, fields):
    fullinputs = {}
    inp_title = []
    inp_junctions = []
    inp_reservoirs = []
    inp_tanks = []
    inp_pipes = []
    inp_pumps = []
    inp_valves = []
    inp_tags = []
    inp_demands = []
    inp_status = []
    inp_patterns = []
    inp_curves = []
    inp_controls = []
    inp_rules = []
    inp_energy = []
    inp_emitters = []
    inp_quality = []
    inp_sources = []
    inp_reactions = []
    inp_mixing = []
    inp_times = []
    inp_report = []
    inp_options = []
    inp_coordinates = []
    inp_vertices = []
    inp_labels = []
    inp_backdrop = []

    for val in finalresult:
        if val[0] == '[TITLE]':
            data = {}
            data["title"] = val[1]
            inp_title.append(data)
            fullinputs['TITLE'] = val[1]
        elif val[0] == '[JUNCTIONS]':
            addtodata(fields['JUNCTIONS'], val, inp_junctions, 'JUNCTIONS')
            fullinputs['JUNCTIONS'] = inp_junctions
        elif val[0] == '[RESERVOIRS]':
            addtodata(fields['RESERVOIRS'], val, inp_reservoirs, 'RESERVOIRS')
            fullinputs['RESERVOIRS'] = inp_reservoirs
        elif val[0] == '[TANKS]':
            addtodata(fields['TANKS'], val, inp_tanks, 'TANKS')
            fullinputs['TANKS'] = inp_tanks
        elif val[0] == '[PIPES]':
            addtodata(fields['PIPES'], val, inp_pipes, 'PIPES')
            fullinputs['PIPES'] = inp_pipes
        elif val[0] == '[PUMPS]':
            addtodata(fields['PUMPS'], val, inp_pumps, 'PUMPS')
            fullinputs['PUMPS'] = inp_pumps
        elif val[0] == '[VALVES]':
            addtodata(fields['VALVES'], val, inp_valves, 'VALVES')
            fullinputs['VALVES'] = inp_valves
        elif val[0] == '[TAGS]':
            addtodata(fields['TAGS'], val, inp_tags, 'TAGS')
            fullinputs['TAGS'] = inp_tags
        elif val[0] == '[DEMANDS]':
            addtodata(fields['DEMANDS'], val, inp_demands, 'DEMANDS')
            fullinputs['DEMANDS'] = inp_demands
        elif val[0] == '[STATUS]':
            addtodata(fields['STATUS'], val, inp_status, 'STATUS')
            fullinputs['STATUS'] = inp_status
        elif val[0] == '[PATTERNS]':
            addtodata(fields['PATTERNS'], val, inp_patterns, 'PATTERNS')
            fullinputs['PATTERNS'] = inp_patterns
        elif val[0] == '[CURVES]':
            addtodata(fields['CURVES'], val, inp_curves, 'CURVES')
            fullinputs['CURVES'] = inp_curves
        elif val[0] == '[CONTROLS]':
            addtodata(fields['CONTROLS'], val, inp_controls, 'CONTROLS')
            fullinputs['CONTROLS'] = inp_controls
        elif val[0] == '[RULES]':
            addtodata(fields['RULES'], val, inp_rules, 'RULES')
            fullinputs['RULES'] = inp_rules
        elif val[0] == '[ENERGY]':
            addtodata(fields['ENERGY'], val, inp_energy, 'ENERGY')
            fullinputs['ENERGY'] = inp_energy
        elif val[0] == '[EMITTERS]':
            addtodata(fields['EMITTERS'], val, inp_emitters, 'EMITTERS')
            fullinputs['EMITTERS'] = inp_emitters
        elif val[0] == '[QUALITY]':
            addtodata(fields['QUALITY'], val, inp_quality, 'QUALITY')
            fullinputs['QUALITY'] = inp_quality
        elif val[0] == '[SOURCES]':
            addtodata(fields['SOURCES'], val, inp_sources, 'SOURCES')
            fullinputs['SOURCES'] = inp_sources
        elif val[0] == '[REACTIONS]':
            addtodata(fields['REACTIONS'], val, inp_reactions, 'REACTIONS')
            fullinputs['REACTIONS'] = inp_reactions
        elif val[0] == '[MIXING]':
            addtodata(fields['MIXING'], val, inp_mixing, 'MIXING')
            fullinputs['MIXING'] = inp_mixing
        elif val[0] == '[TIMES]':
            addtodata(fields['TIMES'], val, inp_times, 'TIMES')
            fullinputs['TIMES'] = inp_times
        elif val[0] == '[REPORT]':
            addtodata(fields['REPORT'], val, inp_report, 'REPORT')
            fullinputs['REPORT'] = inp_report
        elif val[0] == '[OPTIONS]':
            addtodata(fields['OPTIONS'], val, inp_options, 'OPTIONS')
            fullinputs['OPTIONS'] = inp_options
        elif val[0] == '[COORDINATES]':
            addtodata(fields['COORDINATES'], val, inp_coordinates, 'COORDINATES')
            fullinputs['COORDINATES'] = inp_coordinates
        elif val[0] == '[VERTICES]':
            addtodata(fields['VERTICES'], val, inp_vertices, 'VERTICES')
            fullinputs['VERTICES'] = inp_vertices
        elif val[0] == '[LABELS]':
            addtodata(fields['LABELS'], val, inp_labels, 'LABELS')
            fullinputs['LABELS'] = inp_labels
        elif val[0] == '[BACKDROP]':
            addtodata(fields['BACKDROP'], val, inp_backdrop, 'BACKDROP')
            fullinputs['BACKDROP'] = inp_backdrop

    return fullinputs


def adddbtolists():
    fullinputs = {}
    inp_title = []
    inp_junctions = []
    inp_reservoirs = []
    inp_tanks = []
    inp_pipes = []
    inp_pumps = []
    inp_valves = []
    inp_tags = []
    inp_demands = []
    inp_status = []
    inp_patterns = []
    inp_curves = []
    inp_controls = []
    inp_rules = []
    inp_energy = []
    inp_emitters = []
    inp_quality = []
    inp_sources = []
    inp_reactions = []
    inp_mixing = []
    inp_times = []
    inp_report = []
    inp_options = []
    inp_coordinates = []
    inp_vertices = []
    inp_labels = []
    inp_backdrop = []
    fullinputs['TITLE'] = 'KIOS BaSP EPANET Simulation'
    junctions = dbcommunication.read_db_values('SELECT * FROM water_junctions')
    for value in junctions:
        jun = {'ID': value[1], 'Elev': value[2], 'Demand': value[3], 'Pattern': value[4]}
        inp_junctions.append(jun)
    fullinputs['JUNCTIONS'] = inp_junctions
    reservoirs = dbcommunication.read_db_values('SELECT * FROM water_reservoirs')
    for value in reservoirs:
        res = {'ID': value[1], 'Head': value[2], 'Pattern': value[3]}
        inp_reservoirs.append(res)
    fullinputs['RESERVOIRS'] = inp_reservoirs
    tanks = dbcommunication.read_db_values('SELECT * FROM water_tanks')
    for value in tanks:
        tan = {'ID': value[1], 'Elevation': value[2], 'InitLevel': value[3], 'MinLevel': value[4], 'MaxLevel': value[5], 'Diameter': value[6], 'MinVol': value[7], 'VolCurve': value[8]}
        inp_tanks.append(tan)
    fullinputs['TANKS'] = inp_tanks
    pipes = dbcommunication.read_db_values('SELECT * FROM water_pipes')
    for value in pipes:
        pip = {'ID': value[1], 'Node1': value[2], 'Node2': value[3], 'Length': value[4], 'Diameter': value[5], 'Roughness': value[6], 'MinorLoss': value[7], 'Status': value[8]}
        inp_pipes.append(pip)
    fullinputs['PIPES'] = inp_pipes
    pumps = dbcommunication.read_db_values('SELECT * FROM water_pumps')
    for value in pumps:
        pum = {'ID': value[1], 'Node1': value[2], 'Node2': value[3], 'Parameters': value[4]}
        inp_pumps.append(pum)
    fullinputs['PUMPS'] = inp_pumps
    valves = dbcommunication.read_db_values('SELECT * FROM water_valves')
    for value in valves:
        val = {'ID': value[1], 'Node1': value[2], 'Node2': value[3], 'Diameter': value[4], 'Type': value[5], 'Setting': value[6], 'MinorLoss': value[7]}
        inp_valves.append(val)
    fullinputs['VALVES'] = inp_valves
    tags = dbcommunication.read_db_values('SELECT * FROM water_tags')
    for value in tags:
        tag = {'Object': value[1], 'ID': value[2], 'Tag': value[3]}
        inp_tags.append(tag)
    fullinputs['TAGS'] = inp_tags
    demands = dbcommunication.read_db_values('SELECT * FROM water_demands')
    for value in demands:
        demand = {'Junction': value[1], 'Demand': value[2], 'Pattern': value[3], 'Category': value[4]}
        inp_demands.append(demand)
    fullinputs['DEMANDS'] = inp_demands
    status = dbcommunication.read_db_values('SELECT * FROM water_status')
    for value in status:
        statu = {'ID': value[1], 'StatusSetting': value[2]}
        inp_status.append(statu)
    fullinputs['STATUS'] = inp_status
    patterns = dbcommunication.read_db_values('SELECT * FROM water_patterns')
    for value in patterns:
        pattern = {'ID': value[1], 'Multipliers': value[2]}
        inp_patterns.append(pattern)
    fullinputs['PATTERNS'] = inp_patterns
    curves = dbcommunication.read_db_values('SELECT * FROM water_curves')
    for value in curves:
        curve = {'ID': value[1], 'XValue': value[2], 'YValue': value[3]}
        inp_curves.append(curve)
    fullinputs['CURVES'] = inp_curves
    controls = dbcommunication.read_db_values('SELECT * FROM water_controls')
    for value in controls:
        control = {'----': value[1]}
        inp_controls.append(control)
    fullinputs['CONTROLS'] = inp_controls
    rules = dbcommunication.read_db_values('SELECT * FROM water_rules')
    for value in rules:
        rule = {'ruleID': value[1], 'Rule': value[2]}
        inp_rules.append(rule)
    fullinputs['RULES'] = inp_rules
    energy = dbcommunication.read_db_values('SELECT * FROM water_energy')
    for value in energy:
        ene = {'field': value[1], 'value': value[2]}
        inp_energy.append(ene)
    fullinputs['ENERGY'] = inp_energy
    emitters = dbcommunication.read_db_values('SELECT * FROM water_emitters')
    for value in emitters:
        emitter = {'Junction': value[1], 'Coefficient': value[2]}
        inp_emitters.append(emitter)
    fullinputs['EMITTERS'] = inp_emitters
    quality = dbcommunication.read_db_values('SELECT * FROM water_quality')
    for value in quality:
        quali = {'Node': value[1], 'InitQual': value[2]}
        inp_quality.append(quali)
    fullinputs['QUALITY'] = inp_quality
    sources = dbcommunication.read_db_values('SELECT * FROM water_sources')
    for value in sources:
        source = {'Node': value[1], 'Type': value[2], 'Quality': value[3], 'Pattern': value[4]}
        inp_sources.append(source)
    fullinputs['SOURCES'] = inp_sources
    reactions = dbcommunication.read_db_values('SELECT * FROM water_reactions')
    for value in reactions:
        reaction = {'Type': value[1], 'Coefficient': value[2]}
        inp_reactions.append(reaction)
    fullinputs['REACTIONS'] = inp_reactions
    mixing = dbcommunication.read_db_values('SELECT * FROM water_mixing')
    for value in mixing:
        mix = {'Tank': value[1], 'Model': value[2], 'Volume': value[2]}
        inp_mixing.append(mix)
    fullinputs['MIXING'] = inp_mixing
    times = dbcommunication.read_db_values('SELECT * FROM water_times')
    for value in times:
        time = {'field': value[1], 'value': value[2]}
        inp_times.append(time)
    fullinputs['TIMES'] = inp_times
    reports = dbcommunication.read_db_values('SELECT * FROM water_report')
    for value in reports:
        report = {'field': value[1], 'value': value[2]}
        inp_report.append(report)
    fullinputs['REPORT'] = inp_report
    options = dbcommunication.read_db_values('SELECT * FROM water_options')
    for value in options:
        option = {'field': value[1], 'value': value[2]}
        inp_options.append(option)
    fullinputs['OPTIONS'] = inp_options
    coordinates = dbcommunication.read_db_values('SELECT * FROM water_coordinates')
    for value in coordinates:
        coordinate = {'Node': value[1], 'XCoord': value[2], 'YCoord': value[3]}
        inp_coordinates.append(coordinate)
    fullinputs['COORDINATES'] = inp_coordinates
    vertices = dbcommunication.read_db_values('SELECT * FROM water_vertices')
    for value in vertices:
        vertice = {'Link': value[1], 'XCoord': value[2], 'YCoord': value[3]}
        inp_vertices.append(vertice)
    fullinputs['VERTICES'] = inp_vertices
    labels = dbcommunication.read_db_values('SELECT * FROM water_labels')
    for value in labels:
        label = {'XCoord': value[1], 'YCoord': value[2], 'Label': value[3], 'Anchor': value[4]}
        inp_labels.append(label)
    fullinputs['LABELS'] = inp_labels
    backdrops = dbcommunication.read_db_values('SELECT * FROM water_backdrop')
    for value in backdrops:
        backdro = {'field': value[1], 'value': value[2]}
        inp_backdrop.append(backdro)
    fullinputs['BACKDROP'] = inp_backdrop

    return fullinputs


def addDataToDatabase(allfields, fieldsdic):
    for val in allfields:
        alldata = []
        final_query = "INSERT INTO water_" + str(val) + "(" + ','.join(map(str, allfields[val])) + ") VALUES ("
        empty_fields = []
        for x in range(0, len(allfields[val])):
            empty_fields.append('%s')
        final_query = final_query + ','.join(map(str, empty_fields)) + ");"
        for value in fieldsdic[val]:
            data = tuple(value.values())
            alldata.append(data)
        dbcommunication.mod_db_values(final_query, alldata)


def writeTheTitles(file, title):
    file.write("\n")
    file.write(str(title)+"\n")
    file.write(";")


def writeTheValuesUnderTitles(file, infovariable, title):
    if title == '[PATTERNS]':
        writeTheTitles(file, title)
        try:
            for value in infovariable[0].keys():
                file.write(str(value) + "\t\t\t\t")
            file.write("\n")
        except:
            pass
        try:
            for entries in infovariable:
                for value in entries.values():
                    if ',' in value:
                        value = value.replace(",", "\t\t")
                    file.write(str(value) + "\t\t")
                file.write("\n")
        except:
            pass
    elif title == '[RULES]':
        writeTheTitles(file, title)
        try:
            file.write("\n")
            for entries in infovariable:
                for value in entries.values():
                    file.write(str(value) + "\n")
                file.write("\n")
        except:
            pass
    else:
        writeTheTitles(file, title)
        try:
            for value in infovariable[0].keys():
                file.write(str(value) + "\t\t\t\t")
            file.write("\n")
        except:
            pass
        try:
            for entries in infovariable:
                for value in entries.values():
                    file.write(str(value) + "\t\t\t\t")
                file.write("\n")
        except:
            pass


def writeTheValuesUnderTitlesNoFields(file, infovariable, title):
    writeTheTitles(file, title)
    if title == '[ENERGY]' or title == '[REACTIONS]' or title == '[TIMES]' or title == '[REPORT]' or title == '[OPTIONS]' or title == '[BACKDROP]':
        file.write('\n')
        if title == '[REACTIONS]':
            try:
                for entries in infovariable:
                    file.write(str(entries['Type']) + '\t' + str(entries['Coefficient']))
                    file.write("\n")
            except:
                pass
        else:
            try:
                for entries in infovariable:
                    for value in entries.values():
                        if title == '[BACKDROP]':
                            value = value.replace(",", "\t\t")
                        file.write(value + '\t')
                    file.write("\n")
            except:
                pass
    else:
        try:
            for it in infovariable:
                for k, v in it.items():
                    file.write(k + '\t' + v + '\n')
        except:
            pass


def newinputfilecreation(filename, datadic):
    f = open(filename, "w+")
    f.write("[TITLE]" + "\n")
    f.write(datadic['TITLE'] + "\n")
    writeTheValuesUnderTitles(f, datadic['JUNCTIONS'], "[JUNCTIONS]")
    writeTheValuesUnderTitles(f, datadic['RESERVOIRS'], "[RESERVOIRS]")
    writeTheValuesUnderTitles(f, datadic['TANKS'], "[TANKS]")
    writeTheValuesUnderTitles(f, datadic['PIPES'], "[PIPES]")
    writeTheValuesUnderTitles(f, datadic['PUMPS'], "[PUMPS]")
    writeTheValuesUnderTitles(f, datadic['VALVES'], "[VALVES]")
    writeTheValuesUnderTitles(f, datadic['TAGS'], "[TAGS]")
    writeTheValuesUnderTitles(f, datadic['DEMANDS'], "[DEMANDS]")
    writeTheValuesUnderTitles(f, datadic['STATUS'], "[STATUS]")
    writeTheValuesUnderTitles(f, datadic['PATTERNS'], "[PATTERNS]")
    writeTheValuesUnderTitles(f, datadic['CURVES'], "[CURVES]")
    writeTheValuesUnderTitles(f, datadic['CONTROLS'], "[CONTROLS]")
    writeTheValuesUnderTitles(f, datadic['RULES'], "[RULES]")
    writeTheValuesUnderTitlesNoFields(f, datadic['ENERGY'], "[ENERGY]")
    writeTheValuesUnderTitles(f, datadic['EMITTERS'], "[EMITTERS]")
    writeTheValuesUnderTitles(f, datadic['QUALITY'], "[QUALITY]")
    writeTheValuesUnderTitles(f, datadic['SOURCES'], "[SOURCES]")
    writeTheValuesUnderTitlesNoFields(f, datadic['REACTIONS'], "[REACTIONS]")
    writeTheValuesUnderTitles(f, datadic['MIXING'], "[MIXING]")
    writeTheValuesUnderTitlesNoFields(f, datadic['TIMES'], "[TIMES]")
    writeTheValuesUnderTitlesNoFields(f, datadic['REPORT'], "[REPORT]")
    writeTheValuesUnderTitlesNoFields(f, datadic['OPTIONS'], "[OPTIONS]")
    writeTheValuesUnderTitles(f, datadic['COORDINATES'], "[COORDINATES]")
    writeTheValuesUnderTitles(f, datadic['VERTICES'], "[VERTICES]")
    writeTheValuesUnderTitles(f, datadic['LABELS'], "[LABELS]")
    writeTheValuesUnderTitlesNoFields(f, datadic['BACKDROP'], "[BACKDROP]")
    f.write("\n")
    f.write("[END]" + "\n")
    f.close()


def runepanetsim(inputfilename, binaryfilename, reportfilename):
    print('Running Water Simulator')
    #commandtorun = 'cmd /c epanet2d '+str(inputfilename)+' '+str(reportfilename)+' '+str(binaryfilename)
    commandtorun = 'epanet2 ' + str(inputfilename) + ' ' + str(reportfilename) + ' ' + str(binaryfilename)
    print(commandtorun)
    os.system(commandtorun)


def bin2jsonfull(nomeinp, nomeout, nomebin, nomeresult, sim_dur, rep_step, qual_step, net):
    em.ENepanet(nomeinp, nomeout, nomebin)
    d.LoadFile(net + '.inp')
    d.BinUpdateClass()
    nodeNameIDs = d.getBinNodeNameID()
    linkNameIDs = d.getBinLinkNameID()

    with EpanetOutBin(net + ".bin") as a:
        data = {}
        data['NodeID'] = {}
        data['NodeType'] = {}
        data['NodeDemand'] = {}
        data['NodeHead'] = {}
        data['NodePressure'] = {}
        data['NodeQuality'] = {}
        for i, id in enumerate(nodeNameIDs):
            data['NodeID'][i] = a.nodes[id].ID
            data['NodeType'][i] = a.nodes[id]._type
            data['NodeDemand'][i] = a.nodes[id].demand
            data['NodeHead'][i] = a.nodes[id].head
            data['NodePressure'][i] = a.nodes[id].pressure
            data['NodeQuality'][i] = a.nodes[id].quality

        data['LinkID'] = {}
        data['LinkType'] = {}
        data['LinkFlow'] = {}
        data['LinkFriction'] = {}
        data['LinkHeadLoss'] = {}
        data['LinkQuality'] = {}
        data['LinkReactionRate'] = {}
        data['LinkSetting'] = {}
        data['LinkStatus'] = {}
        data['LinkVelocity'] = {}
        for i, id in enumerate(linkNameIDs):
            data['LinkID'][i] = a.links[id].ID
            data['LinkType'][i] = a.links[id].linktype
            data['LinkFlow'][i] = a.links[id].flow
            data['LinkFriction'][i] = a.links[id].friction
            data['LinkHeadLoss'][i] = a.links[id].headloss
            data['LinkQuality'][i] = a.links[id].quality
            data['LinkReactionRate'][i] = a.links[id].reactionrate
            data['LinkSetting'][i] = a.links[id].setting
            data['LinkStatus'][i] = a.links[id].status
            data['LinkVelocity'][i] = a.links[id].velocity

        data['CountLinks'] = a._Nlinks
        data['CountNodes'] = a._Nnodes
        data['CountTanks'] = a._Ntanks
        data['CountPumps'] = a._Npumps
        data['CountValves'] = a._Nvalves
        data['BulkRate'] = a.bulk_rrate
        data['ChemicalName'] = a.chemicalname
        data['Periods'] = a._Nperiods
        data['ChemicalUnits'] = a.chemicalunits
        data['DynamicStart'] = a.dynamic_start
        data['DynamicStep'] = a.dynamic_step
        data['Energy'] = a.energy
        data['EnergyStart'] = a.energy_start
        data['EpilogStart'] = a.epilog_start
        data['Filename'] = a.filename
        data['FlowUnits'] = a.flowunits
        data['InputFilename'] = a.inputfilename
        data['PressureUnits'] = a.pressureunits
        data['PrologStart'] = a.prolog_start
        data['Quality'] = a.quality
        data['SourceFlowRate'] = a.source_inflowrate
        data['TankRate'] = a.tank_rrate
        data['Title'] = a.title
        data['TraceNode'] = a.tracenode
        data['WallRate'] = a.wall_rrate
        data['SimDuration'] = sim_dur
        data['RepStep'] = rep_step
        data['QualStep'] = qual_step
        with open(nomeresult, "w") as write_file:
            json.dump(data, write_file)


def epanetandbin2jsonwntr(inp_file,out_json):
    wn = wntr.network.WaterNetworkModel(inp_file)
    simulation = wntr.sim.EpanetSimulator(wn, mode='PDD')
    results = simulation.run_sim(file_prefix='basp/Water/WaterResults')
    jsontoexport = {"NodeID": {}, "NodeType": {}, "NodeDemand": {}, "NodeHead": {}, "NodePressure": {},
                    "NodeQuality": {}, "LinkID": {}, "LinkType": {}, "LinkFlow": {}, "LinkFriction": {},
                    "LinkHeadLoss": {}, "LinkQuality": {}, "LinkReactionRate": {}, "LinkSetting": {}, "LinkStatus": {},
                    "LinkVelocity": {}}
    x = 0
    for value in results.node['demand'].keys():
        jsontoexport["NodeID"][str(x)] = value
        jsontoexport["NodeType"][str(x)] = wn.get_node(value).node_type
        dem = results.node['demand'][value]
        dem = [elem * 3600 for elem in dem]
        jsontoexport["NodeDemand"][str(x)] = dem
        #jsontoexport["NodeDemand"][str(x)] = list(results.node['demand'][value])
        jsontoexport["NodePressure"][str(x)] = list(results.node['pressure'][value])
        #jsontoexport["NodeHead"][str(x)] = list(results.node['head'][value])
        #jsontoexport["NodeQuality"][str(x)] = list(results.node['quality'][value])
        x += 1
    x = 0
    for value in results.link['linkquality'].keys():
        jsontoexport["LinkID"][str(x)] = value
        jsontoexport["LinkType"][str(x)] = wn.get_link(value).link_type
        flows = results.link['flowrate'][value]
        flows = [elem * 3600 for elem in flows]
        jsontoexport["LinkFlow"][str(x)] = flows
        #jsontoexport["LinkFlow"][str(x)] = list(results.link['flowrate'][value])
        #jsontoexport["LinkFriction"][str(x)] = list(results.link['frictionfact'][value])
        #jsontoexport["LinkHeadLoss"][str(x)] = list(results.link['headloss'][value])
        #jsontoexport["LinkQuality"][str(x)] = list(results.link['linkquality'][value])
        #jsontoexport["LinkReactionRate"][str(x)] = list(results.link['rxnrate'][value])
        #jsontoexport["LinkSetting"][str(x)] = list(results.link['setting'][value])
        #jsontoexport["LinkStatus"][str(x)] = list(results.link['status'][value])
        #jsontoexport["LinkVelocity"][str(x)] = list(results.link['velocity'][value])
        x += 1
    with open(out_json, 'w') as outfile:
        json.dump(jsontoexport, outfile)


def wntr2jsonwntr(wn,out_json):
    #wn = wntr.network.WaterNetworkModel(inp_file)
    sim = wntr.sim.WNTRSimulator(wn)
    results = sim.run_sim()
    jsontoexport = {"NodeID": {}, "NodeType": {}, "NodeDemand": {}, "NodeHead": {}, "NodePressure": {},
                    "NodeQuality": {}, "LinkID": {}, "LinkType": {}, "LinkFlow": {}, "LinkFriction": {},
                    "LinkHeadLoss": {}, "LinkQuality": {}, "LinkReactionRate": {}, "LinkSetting": {}, "LinkStatus": {},
                    "LinkVelocity": {}}
    x = 0
    for value in results.node['demand'].keys():
        jsontoexport["NodeID"][str(x)] = value
        jsontoexport["NodeType"][str(x)] = wn.get_node(value).node_type
        dem = results.node['demand'][value]
        dem = [elem * 3600 for elem in dem]
        jsontoexport["NodeDemand"][str(x)] = dem
        jsontoexport["NodePressure"][str(x)] = list(results.node['pressure'][value])
        x += 1
    x = 0
    for value in wn.link_name_list:
        jsontoexport["LinkID"][str(x)] = value
        jsontoexport["LinkType"][str(x)] = wn.get_link(value).link_type
        flows = results.link['flowrate'][value]
        flows = [elem * 3600 for elem in flows]
        jsontoexport["LinkFlow"][str(x)] = flows
        x += 1
    with open(out_json, 'w') as outfile:
        json.dump(jsontoexport, outfile)


def bin2json(nomeinp, nomeout, nomebin, nomeresult, sim_dur, rep_step, qual_step, net):
    em.ENepanet(nomeinp, nomeout, nomebin)
    d.LoadFile(net + '.inp')
    d.BinUpdateClass()
    nodeNameIDs = d.getBinNodeNameID()
    linkNameIDs = d.getBinLinkNameID()

    with EpanetOutBin(net + ".bin") as a:
        data = {}
        data['NodeID'] = {}
        data['NodeType'] = {}
        data['NodeDemand'] = {}
        data['NodeHead'] = {}
        data['NodePressure'] = {}
        data['NodeQuality'] = {}
        for i, id in enumerate(nodeNameIDs):
            data['NodeID'][i] = a.nodes[id].ID
            data['NodeDemand'][i] = a.nodes[id].demand
            data['NodePressure'][i] = a.nodes[id].pressure

        data['LinkID'] = {}
        data['LinkType'] = {}
        data['LinkFlow'] = {}
        data['LinkFriction'] = {}
        data['LinkHeadLoss'] = {}
        data['LinkQuality'] = {}
        data['LinkReactionRate'] = {}
        data['LinkSetting'] = {}
        data['LinkStatus'] = {}
        data['LinkVelocity'] = {}
        for i, id in enumerate(linkNameIDs):
            data['LinkID'][i] = a.links[id].ID
            data['LinkType'][i] = a.links[id].linktype
            data['LinkFlow'][i] = a.links[id].flow

        with open(nomeresult, "w") as write_file:
            json.dump(data, write_file)


def readjson(file, starttime, timeinterval):
    timeinterval = timeinterval.split(':')
    water_output_nodes = []
    water_output_nodes_values = []
    water_output_links = []
    water_output_links_values = []

    with open(file) as json_file:
        data = json.load(json_file)

        for p in data['NodeID']:
            outputnodes = (data['NodeID'][p], data['NodeType'][p])
            water_output_nodes.append(outputnodes)
            newstarttime = starttime
            for (v1, v2, v3, v4) in zip(data['NodeDemand'][p], data['NodeHead'][p], data['NodePressure'][p], data['NodeQuality'][p]):
                outputnodedetails = (data['NodeID'][p], newstarttime, v1, v2, v3, v4)
                water_output_nodes_values.append(outputnodedetails)
                newstarttime = newstarttime + dtm.timedelta(hours=int(timeinterval[0]), minutes=int(timeinterval[1]))

        for p in data['LinkID']:
            outputlinks = (data['LinkID'][p], data['LinkType'][p])
            water_output_links.append(outputlinks)
            newstarttime = starttime
            for (v1, v2, v3, v4, v5, v6, v7) in zip(data['LinkFriction'][p], data['LinkHeadLoss'][p], data['LinkQuality'][p], data['LinkReactionRate'][p], data['LinkSetting'][p], data['LinkStatus'][p], data['LinkVelocity'][p]):
                outputlinkdetails = (data['LinkID'][p], newstarttime, v1, v2, v3, v4, v5, v6, v7)
                water_output_links_values.append(outputlinkdetails)
                newstarttime = newstarttime + dtm.timedelta(hours=int(timeinterval[0]), minutes=int(timeinterval[1]))

    final_query = "INSERT INTO water_output_nodes(nodeid,nodetype) VALUES (%s,%s)"
    dbcommunication.mod_db_values(final_query, water_output_nodes)
    final_query = "INSERT INTO water_output_nodes_values(nodeid,readingtime,nodedemand,nodehead,nodepressure,nodequality) VALUES (%s,%s,%s,%s,%s,%s)"
    dbcommunication.mod_db_values(final_query, water_output_nodes_values)
    final_query = "INSERT INTO water_output_links(linkid,linktype) VALUES (%s,%s)"
    dbcommunication.mod_db_values(final_query, water_output_links)
    final_query = "INSERT INTO water_output_links_values(linkid,readingtime,linkfriction,linkheadloss,linkquality,linkreactionrate,linksetting,linkstatus,linkvelocity) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    dbcommunication.mod_db_values(final_query, water_output_links_values)


def readjsonwithfiles(file, starttime, timeinterval, sensors, experimentname):
    from datetime import datetime
    from influxdb import InfluxDBClient
    import time
    try:
        os.remove("/usr/src/app/grafana-provisioning/dashboards/WaterSensorsBaSP.json")
    except:
        noremove=True
    try:
        client = InfluxDBClient(host='influxdb', port=8086, username='kios',
                                password='kios1234!', database='virtual_city')
        print(client)
    except:
        client.close()
    #Copy Generated Data JSON File
    src_dir = "/usr/src/app/basp/Water/jsonoutput.json"
    dst_dir = "/usr/src/app/basp/uploads/"+str(experimentname)+"/simulationdata.json"
    shutil.copy2(src_dir, dst_dir)
    timeinterval = int(timeinterval/60)
    WaterOutputScadaSensorDetails = []
    WaterOutputScadaSensors = []
    WaterOutputScadaSensorsinflux = []
    # sensor types flow, pressure, demand
    flow = []
    pressure = []
    demand = []
    influxsensordata = []
    sumodata = []
    influxsensordatainfluxname = "water_output_"+str(experimentname)+"_sensors"
    for values in sensors['sensors']:
        if values['sensortype'] == "pressure":
            pressure.append({"sid": values['sensorid'], "nlid": values['id'], "sensortype":values['sensortype'], "sensorlat":values['lat'], "sensorlong":values['long']})
        elif values['sensortype'] == "flow":
            flow.append({"sid": values['sensorid'], "nlid": values['id'], "sensortype":values['sensortype'], "sensorlat":values['lat'], "sensorlong":values['long']})
        elif values['sensortype'] == "demand":
            demand.append({"sid": values['sensorid'], "nlid": values['id'], "sensortype":values['sensortype'], "sensorlat":values['lat'], "sensorlong":values['long']})
    for values in sensors['sensors']:
        sensordata = (values['sensorid'], values['id'], values['sensortype'], values['lat'], values['long'])
        WaterOutputScadaSensorDetails.append(sensordata)
        current_time = round(time.time() * 1000)
        influxsensordata.append(
            '{measurement},sensorid={sensorid},sensortype={sensortype},nodelink={nodelink},nodelinkid={nodelinkid},min={min},max={max},uncertainty={uncertainty},uncertaintydist={uncertaintydist},lat={lat},long={long} resolution={resolution} {currenttime}'
            .format(measurement=str(influxsensordatainfluxname),
                    sensorid=values['sensorid'],
                    sensortype=values['sensortype'],
                    nodelink=values['nodelink'],
                    nodelinkid=values['id'],
                    min=values['min'],
                    max=values['max'],
                    resolution=values['resolution'],
                    uncertainty=values['uncertainty'],
                    uncertaintydist=values['uncertaintydist'],
                    lat=values['lat'],
                    long=values['long'],
                    currenttime=current_time,
                    ))

    with open(file) as json_file:
        data = json.load(json_file)
        for ps in pressure:
            for key, value in data['NodeID'].items():
                if ps['nlid'] == value:
                    ps['realid'] = key
                    break
        for ps in demand:
            for key, value in data['NodeID'].items():
                if ps['nlid'] == value:
                    ps['realid'] = key
                    break
        for ps in flow:
            for key, value in data['LinkID'].items():
                if ps['nlid'] == value:
                    ps['realid'] = key
                    break
        scadaresultsname = "water_output_" + str(experimentname) + "_scada_sensors"
        for ps in pressure:
            newstarttime = starttime
            for p1 in data['NodePressure'][ps['realid']]:
                for values in sensors['sensors']:
                    if values['sensorid'] == ps['sid']:
                        #res=sensorsProfile.sensorsValue(values['sensorid'], p1)
                        res = "error"
                        if res=="error":
                            resolution = values['resolution']
                            uncertainty = values['uncertainty']
                            uncertaintydist = values['uncertaintydist']
                            minval = values['min']
                            maxval = values['max']
                            #Sensor Resolution
                            t001 = str(resolution).split('.')
                            flformat = "{:." + str(len(t001[1])) + "f}"
                            if (float(p1) / float(resolution)).is_integer():
                                resultwithrest = p1
                            else:
                                resultwithrest = float(p1) - math.fmod(float(p1), float(resolution))
                                resultwithrest = flformat.format(resultwithrest)
                            #Sensor Uncertainty
                            if uncertainty > 0:
                                unc_value = (float(resultwithrest) * float(uncertainty))/float(100)
                                randval = 0
                                #Sensor Uncertainty Distribution
                                if uncertaintydist == "uniform":
                                    randval = random.uniform(-unc_value, unc_value)
                                resultwithrest = float(resultwithrest) + float(randval)
                                resultwithrest = flformat.format(resultwithrest)
                            if float(resultwithrest) > float(maxval):
                                resultwithrest = maxval
                            #elif float(resultwithrest) < float(minval):
                            #    resultwithrest = minval
                        else:
                            resultwithrest=res
                        outputsensdetails = (newstarttime, ps['sid'], resultwithrest, ps['nlid'], ps['sensortype'], ps['sensorlat'],ps['sensorlong'])
                        #my_date_format = datetime.strptime(newstarttime, '%Y-%m-%d %H:%M:%S')
                        epoch_time = (newstarttime - datetime(1970, 1, 1)).total_seconds()
                        epoch_time = int(epoch_time * 1000)
                        WaterOutputScadaSensorsinflux.append('{measurement},sensorid={sensorid},sensortype={sensortype},sensorlat={sensorlat},sensorlong={sensorlong} sensor_value={sensor_value},sensorconnectionid="{sensorconnectionid}" {timestamp}'
                                                             .format(measurement=str(scadaresultsname),
                                                                     sensorid=ps['sid'],
                                                                     sensortype=ps['sensortype'],
                                                                     sensorlat=ps['sensorlat'],
                                                                     sensorlong=ps['sensorlong'],
                                                                     sensor_value=p1,
                                                                     sensorconnectionid=ps['nlid'],
                                                                     timestamp=epoch_time))
                        WaterOutputScadaSensors.append(outputsensdetails)
                        newstarttime = newstarttime + dtm.timedelta(minutes=int(timeinterval))
        for ps in demand:
            newstarttime = starttime
            for p1 in data['NodeDemand'][ps['realid']]:
                for values in sensors['sensors']:
                    if values['sensorid'] == ps['sid']:
                        '''
                        #res = sensorsProfile.sensorsValue(values['sensorid'], p1)
                        res = "error"
                        if res == "error":
                            resolution = values['resolution']
                            uncertainty = values['uncertainty']
                            uncertaintydist = values['uncertaintydist']
                            minval = values['min']
                            maxval = values['max']
                            #Change Resolution
                            t001 = str(resolution).split('.')
                            flformat = "{:." + str(len(t001[1])) + "f}"
                            if (float(p1) / float(resolution)).is_integer():
                                resultwithrest = p1
                            else:
                                resultwithrest = float(p1) - math.fmod(float(p1), float(resolution))
                                resultwithrest = flformat.format(resultwithrest)
                            
                            #Add Uncertainty
                            if uncertainty > 0:
                                unc_value = (float(resultwithrest) * float(uncertainty))/float(100)
                                randval = 0
                                if uncertaintydist == "uniform":
                                    randval = random.uniform(-unc_value, unc_value)
                                resultwithrest = float(resultwithrest) + float(randval)
                                resultwithrest = flformat.format(resultwithrest)
                            if float(resultwithrest) > float(maxval):
                                resultwithrest = maxval
                            elif float(resultwithrest) < float(minval):
                                resultwithrest = minval
                        else:
                            resultwithrest=res
                        '''
                        outputsensdetails = (newstarttime, ps['sid'], resultwithrest,ps['nlid'],ps['sensortype'],ps['sensorlat'],ps['sensorlong'])
                        #my_date_format = datetime.strptime(newstarttime, '%Y-%m-%d %H:%M:%S')
                        epoch_time = (newstarttime - datetime(1970, 1, 1)).total_seconds()
                        epoch_time = int(epoch_time * 1000)
                        WaterOutputScadaSensorsinflux.append(
                            '{measurement},sensorid={sensorid},sensortype={sensortype},sensorlat={sensorlat},sensorlong={sensorlong} sensor_value={sensor_value},sensorconnectionid="{sensorconnectionid}" {timestamp}'
                            .format(measurement=str(scadaresultsname),
                                    sensorid=ps['sid'],
                                    sensortype=ps['sensortype'],
                                    sensorlat=ps['sensorlat'],
                                    sensorlong=ps['sensorlong'],
                                    sensor_value=p1,
                                    sensorconnectionid=ps['nlid'],
                                    timestamp=epoch_time))
                        WaterOutputScadaSensors.append(outputsensdetails)
                        newstarttime = newstarttime + dtm.timedelta(minutes=int(timeinterval))
        for ps in flow:
            newstarttime = starttime
            for p1 in data['LinkFlow'][ps['realid']]:
                for values in sensors['sensors']:
                    if values['sensorid'] == ps['sid']:
                        #res = sensorsProfile.sensorsValue(values['sensorid'], p1)
                        res = "error"
                        if res == "error":
                            resolution = values['resolution']
                            uncertainty = values['uncertainty']
                            uncertaintydist = values['uncertaintydist']
                            minval = values['min']
                            maxval = values['max']
                            #Change Resolution
                            t001 = str(resolution).split('.')
                            flformat = "{:." + str(len(t001[1])) + "f}"
                            if (float(p1) / float(resolution)).is_integer():
                                resultwithrest = p1
                            else:
                                resultwithrest = float(p1) - math.fmod(float(p1), float(resolution))
                                resultwithrest = flformat.format(resultwithrest)
                            #Add Uncertainty
                            if uncertainty > 0:
                                unc_value = (float(resultwithrest) * float(uncertainty))/float(100)
                                randval = 0
                                if uncertaintydist == "uniform":
                                    randval = random.uniform(-unc_value, unc_value)
                                resultwithrest = float(resultwithrest) + float(randval)
                                resultwithrest = flformat.format(resultwithrest)
                            if float(resultwithrest) > float(maxval):
                                resultwithrest = maxval
                            #elif float(resultwithrest) < float(minval):
                            #    resultwithrest = minval
                        else:
                            resultwithrest=res
                        outputsensdetails = (newstarttime, ps['sid'], resultwithrest,ps['nlid'],ps['sensortype'],ps['sensorlat'],ps['sensorlong'])
                        epoch_time = (newstarttime - datetime(1970, 1, 1)).total_seconds()
                        epoch_time = int(epoch_time * 1000)
                        WaterOutputScadaSensorsinflux.append(
                            '{measurement},sensorid={sensorid},sensortype={sensortype},sensorlat={sensorlat},sensorlong={sensorlong} sensor_value={sensor_value},sensorconnectionid="{sensorconnectionid}" {timestamp}'
                            .format(measurement=str(scadaresultsname),
                                    sensorid=ps['sid'],
                                    sensortype=ps['sensortype'],
                                    sensorlat=ps['sensorlat'],
                                    sensorlong=ps['sensorlong'],
                                    sensor_value=p1,
                                    sensorconnectionid=ps['nlid'],
                                    timestamp=epoch_time))
                        WaterOutputScadaSensors.append(outputsensdetails)
                        newstarttime = newstarttime + dtm.timedelta(minutes=int(timeinterval))

    water_table_for_json = "water_output_"+str(experimentname)+"_scada_sensors"
    water_table_for_json_sensors = "water_output_" + str(experimentname) + "_sensors"

    if WaterOutputScadaSensors:
        import time
        try:
            client = InfluxDBClient(host='influxdb', port=8086, username='kios',
                                    password='kios1234!', database='virtual_city')
            print(client)
        except:
            client.close()
        client.write_points(WaterOutputScadaSensorsinflux, database='virtual_city', time_precision='ms', batch_size=10000, protocol='line')
        client.write_points(influxsensordata, database='virtual_city', time_precision='ms',batch_size=10000, protocol='line')
        #client.write_points(sumodata, database='virtual_city', time_precision='ms', batch_size=10000,protocol='line')


        client.close()

    '''
    try:
        with open('/usr/src/app/grafana-provisioning/dashboards/WaterSensorsBaSP.json') as f:
            datagrafana = json.load(f)

        versiongrafana = datagrafana['version']
    except:
        versiongrafana = 1
    '''

    '''
    try:
        os.remove("/usr/src/app/grafana-provisioning/dashboards/template/WaterSensorsBaSPedit.json")
    except:
        noremove=True

    shutil.copyfile("/usr/src/app/grafana-provisioning/dashboards/template/WaterSensorsBaSP.json",
             "/usr/src/app/grafana-provisioning/dashboards/template/WaterSensorsBaSPedit.json")
    '''
    with open('/usr/src/app/grafana-provisioning/template/WaterSensorsBaSP.json', 'r') as file:
        filedata = file.read()
    filedata = filedata.replace('water_output_test1_scada_sensors', str(water_table_for_json))
    filedata = filedata.replace('water_output_test1_sensors', str(water_table_for_json_sensors))
    with open('/usr/src/app/grafana-provisioning/dashboards/WaterSensorsBaSP.json', 'w') as file:
        file.write(filedata)
    '''
    if versiongrafana>1:
        datagrafana['version'] = versiongrafana+10
        with open("/usr/src/app/grafana-provisioning/dashboards/template/WaterSensorsBaSPedit.json", "w") as jsonFile:
            json.dump(datagrafana, jsonFile)
    shutil.copyfile("/usr/src/app/grafana-provisioning/dashboards/template/WaterSensorsBaSPedit.json","/usr/src/app/grafana-provisioning/dashboards/WaterSensorsBaSP.json")
    '''
    '''
    import fileinput
    from shutil import copyfile
    copyfile("/usr/src/app/grafana-provisioning/dashboards/template/WaterSensorsBaSP.json", "/usr/src/app/grafana-provisioning/dashboards/WaterSensorsBaSP.json")
    filename = "/usr/src/app/grafana-provisioning/dashboards/WaterSensorsBaSP.json"
    with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
        for line in file:
            if 'water_output_test1_scada_sensors' in line:
                print(line.replace('water_output_test1_scada_sensors', str(water_table_for_json)), end='')
            elif 'water_output_test1_sensors' in line:
                print(line.replace('water_output_test1_sensors', str(water_table_for_json_sensors)), end='')
            else:
                print(line)
    '''


def readjsonwithfilesstep(file, starttime, timeinterval, sensors, experimentname):
    from datetime import datetime
    from influxdb import InfluxDBClient
    import time
    try:
        client = InfluxDBClient(host='influxdb', port=8086, username='kios',
                                password='kios1234!', database='virtual_city')
        print(client)
    except:
        client.close()
    #Copy Generated Data JSON File
    src_dir = "/usr/src/app/basp/Water/jsonoutput.json"
    dst_dir = "/usr/src/app/basp/uploads/"+str(experimentname)+"/simulationdata.json"
    shutil.copy2(src_dir, dst_dir)
    timeinterval = int(timeinterval/60)
    WaterOutputScadaSensorDetails = []
    WaterOutputScadaSensors = []
    WaterOutputScadaSensorsinflux = []
    # sensor types flow, pressure, demand
    flow = []
    pressure = []
    demand = []
    influxsensordata = []
    influxsensordatainfluxname = "water_output_"+str(experimentname)+"_sensors"
    query = "SELECT * FROM " + influxsensordatainfluxname
    resultneedsensors = client.query(query)
    client.close()
    for values in sensors['sensors']:
        if values['sensortype'] == "pressure":
            pressure.append({"sid": values['sensorid'], "nlid": values['id'], "sensortype":values['sensortype'], "sensorlat":values['lat'], "sensorlong":values['long']})
        elif values['sensortype'] == "flow":
            flow.append({"sid": values['sensorid'], "nlid": values['id'], "sensortype":values['sensortype'], "sensorlat":values['lat'], "sensorlong":values['long']})
        elif values['sensortype'] == "demand":
            demand.append({"sid": values['sensorid'], "nlid": values['id'], "sensortype":values['sensortype'], "sensorlat":values['lat'], "sensorlong":values['long']})
    for values in sensors['sensors']:
        sensordata = (values['sensorid'], values['id'], values['sensortype'], values['lat'], values['long'])
        WaterOutputScadaSensorDetails.append(sensordata)
        current_time = round(time.time() * 1000)
        influxsensordata.append(
            '{measurement},sensorid={sensorid},sensortype={sensortype},nodelink={nodelink},nodelinkid={nodelinkid},min={min},max={max},uncertainty={uncertainty},uncertaintydist={uncertaintydist},lat={lat},long={long} resolution={resolution} {currenttime}'
            .format(measurement=str(influxsensordatainfluxname),
                    sensorid=values['sensorid'],
                    sensortype=values['sensortype'],
                    nodelink=values['nodelink'],
                    nodelinkid=values['id'],
                    min=values['min'],
                    max=values['max'],
                    resolution=values['resolution'],
                    uncertainty=values['uncertainty'],
                    uncertaintydist=values['uncertaintydist'],
                    lat=values['lat'],
                    long=values['long'],
                    currenttime=current_time,
                    ))
    with open(file) as json_file:
        data = json.load(json_file)
        for ps in pressure:
            for key, value in data['NodeID'].items():
                if ps['nlid'] == value:
                    ps['realid'] = key
                    break
        for ps in demand:
            for key, value in data['NodeID'].items():
                if ps['nlid'] == value:
                    ps['realid'] = key
                    break
        for ps in flow:
            for key, value in data['LinkID'].items():
                if ps['nlid'] == value:
                    ps['realid'] = key
                    break
        scadaresultsname = "water_output_" + str(experimentname) + "_scada_sensors"
        for ps in pressure:
            newstarttime = starttime
            for p1 in data['NodePressure'][ps['realid']]:
                for values in sensors['sensors']:
                    if values['sensorid'] == ps['sid']:
                        #res=sensorsProfile.sensorsValue(values['sensorid'], p1)
                        res = "error"
                        if res=="error":
                            resolution = values['resolution']
                            uncertainty = values['uncertainty']
                            uncertaintydist = values['uncertaintydist']
                            minval = values['min']
                            maxval = values['max']
                            #Sensor Resolution
                            t001 = str(resolution).split('.')
                            flformat = "{:." + str(len(t001[1])) + "f}"
                            if (float(p1) / float(resolution)).is_integer():
                                resultwithrest = p1
                            else:
                                resultwithrest = float(p1) - math.fmod(float(p1), float(resolution))
                                resultwithrest = flformat.format(resultwithrest)
                            #Sensor Uncertainty
                            if uncertainty > 0:
                                unc_value = (float(resultwithrest) * float(uncertainty))/float(100)
                                randval = 0
                                #Sensor Uncertainty Distribution
                                if uncertaintydist == "uniform":
                                    randval = random.uniform(-unc_value, unc_value)
                                resultwithrest = float(resultwithrest) + float(randval)
                                resultwithrest = flformat.format(resultwithrest)
                            if float(resultwithrest) > float(maxval):
                                resultwithrest = maxval
                            elif float(resultwithrest) < float(minval):
                                resultwithrest = minval
                        else:
                            resultwithrest=res
                        outputsensdetails = (newstarttime, ps['sid'], resultwithrest, ps['nlid'], ps['sensortype'], ps['sensorlat'],ps['sensorlong'])
                        #my_date_format = datetime.strptime(newstarttime, '%Y-%m-%d %H:%M:%S')
                        epoch_time = (newstarttime - datetime(1970, 1, 1)).total_seconds()
                        epoch_time = int(epoch_time * 1000)
                        WaterOutputScadaSensorsinflux.append('{measurement},sensorid={sensorid},sensortype={sensortype},sensorlat={sensorlat},sensorlong={sensorlong} sensor_value={sensor_value},sensorconnectionid="{sensorconnectionid}" {timestamp}'
                                                             .format(measurement=str(scadaresultsname),
                                                                     sensorid=ps['sid'],
                                                                     sensortype=ps['sensortype'],
                                                                     sensorlat=ps['sensorlat'],
                                                                     sensorlong=ps['sensorlong'],
                                                                     sensor_value=resultwithrest,
                                                                     sensorconnectionid=ps['nlid'],
                                                                     timestamp=epoch_time))
                        WaterOutputScadaSensors.append(outputsensdetails)
                        newstarttime = newstarttime + dtm.timedelta(minutes=int(timeinterval))
        for ps in demand:
            newstarttime = starttime
            for p1 in data['NodeDemand'][ps['realid']]:
                for values in sensors['sensors']:
                    if values['sensorid'] == ps['sid']:
                        #res = sensorsProfile.sensorsValue(values['sensorid'], p1)
                        res = "error"
                        if res == "error":
                            resolution = values['resolution']
                            uncertainty = values['uncertainty']
                            uncertaintydist = values['uncertaintydist']
                            minval = values['min']
                            maxval = values['max']
                            #Change Resolution
                            t001 = str(resolution).split('.')
                            flformat = "{:." + str(len(t001[1])) + "f}"
                            if (float(p1) / float(resolution)).is_integer():
                                resultwithrest = p1
                            else:
                                resultwithrest = float(p1) - math.fmod(float(p1), float(resolution))
                                resultwithrest = flformat.format(resultwithrest)
                            #Add Uncertainty
                            if uncertainty > 0:
                                unc_value = (float(resultwithrest) * float(uncertainty))/float(100)
                                randval = 0
                                if uncertaintydist == "uniform":
                                    randval = random.uniform(-unc_value, unc_value)
                                resultwithrest = float(resultwithrest) + float(randval)
                                resultwithrest = flformat.format(resultwithrest)
                            if float(resultwithrest) > float(maxval):
                                resultwithrest = maxval
                            elif float(resultwithrest) < float(minval):
                                resultwithrest = minval
                        else:
                            resultwithrest=res
                        outputsensdetails = (newstarttime, ps['sid'], resultwithrest,ps['nlid'],ps['sensortype'],ps['sensorlat'],ps['sensorlong'])
                        #my_date_format = datetime.strptime(newstarttime, '%Y-%m-%d %H:%M:%S')
                        epoch_time = (newstarttime - datetime(1970, 1, 1)).total_seconds()
                        epoch_time = int(epoch_time * 1000)
                        WaterOutputScadaSensorsinflux.append(
                            '{measurement},sensorid={sensorid},sensortype={sensortype},sensorlat={sensorlat},sensorlong={sensorlong} sensor_value={sensor_value},sensorconnectionid="{sensorconnectionid}" {timestamp}'
                            .format(measurement=str(scadaresultsname),
                                    sensorid=ps['sid'],
                                    sensortype=ps['sensortype'],
                                    sensorlat=ps['sensorlat'],
                                    sensorlong=ps['sensorlong'],
                                    sensor_value=resultwithrest,
                                    sensorconnectionid=ps['nlid'],
                                    timestamp=epoch_time))
                        WaterOutputScadaSensors.append(outputsensdetails)
                        newstarttime = newstarttime + dtm.timedelta(minutes=int(timeinterval))
        for ps in flow:
            newstarttime = starttime
            for p1 in data['LinkFlow'][ps['realid']]:
                for values in sensors['sensors']:
                    if values['sensorid'] == ps['sid']:
                        #res = sensorsProfile.sensorsValue(values['sensorid'], p1)
                        res = "error"
                        if res == "error":
                            resolution = values['resolution']
                            uncertainty = values['uncertainty']
                            uncertaintydist = values['uncertaintydist']
                            minval = values['min']
                            maxval = values['max']
                            #Change Resolution
                            t001 = str(resolution).split('.')
                            flformat = "{:." + str(len(t001[1])) + "f}"
                            if (float(p1) / float(resolution)).is_integer():
                                resultwithrest = p1
                            else:
                                resultwithrest = float(p1) - math.fmod(float(p1), float(resolution))
                                resultwithrest = flformat.format(resultwithrest)
                            #Add Uncertainty
                            if uncertainty > 0:
                                unc_value = (float(resultwithrest) * float(uncertainty))/float(100)
                                randval = 0
                                if uncertaintydist == "uniform":
                                    randval = random.uniform(-unc_value, unc_value)
                                resultwithrest = float(resultwithrest) + float(randval)
                                resultwithrest = flformat.format(resultwithrest)
                            if float(resultwithrest) > float(maxval):
                                resultwithrest = maxval
                            elif float(resultwithrest) < float(minval):
                                resultwithrest = minval
                        else:
                            resultwithrest=res
                        outputsensdetails = (newstarttime, ps['sid'], resultwithrest,ps['nlid'],ps['sensortype'],ps['sensorlat'],ps['sensorlong'])
                        epoch_time = (newstarttime - datetime(1970, 1, 1)).total_seconds()
                        epoch_time = int(epoch_time * 1000)
                        WaterOutputScadaSensorsinflux.append(
                            '{measurement},sensorid={sensorid},sensortype={sensortype},sensorlat={sensorlat},sensorlong={sensorlong} sensor_value={sensor_value},sensorconnectionid="{sensorconnectionid}" {timestamp}'
                            .format(measurement=str(scadaresultsname),
                                    sensorid=ps['sid'],
                                    sensortype=ps['sensortype'],
                                    sensorlat=ps['sensorlat'],
                                    sensorlong=ps['sensorlong'],
                                    sensor_value=resultwithrest,
                                    sensorconnectionid=ps['nlid'],
                                    timestamp=epoch_time))
                        WaterOutputScadaSensors.append(outputsensdetails)
                        newstarttime = newstarttime + dtm.timedelta(minutes=int(timeinterval))

    water_table_for_json = "water_output_"+str(experimentname)+"_scada_sensors"
    water_table_for_json_sensors = "water_output_" + str(experimentname) + "_sensors"

    if WaterOutputScadaSensors:
        import time
        try:
            client = InfluxDBClient(host='influxdb', port=8086, username='kios',
                                    password='kios1234!', database='virtual_city')
            print(client)
        except:
            client.close()
        client.write_points(WaterOutputScadaSensorsinflux, database='virtual_city', time_precision='ms', batch_size=10000, protocol='line')
        if len(resultneedsensors)==0:
            client.write_points(influxsensordata, database='virtual_city', time_precision='ms',batch_size=10000, protocol='line')
        client.close()

    shutil.copyfile("/usr/src/app/grafana-provisioning/dashboards/template/WaterSensorsBaSP.json",
             "/usr/src/app/grafana-provisioning/dashboards/WaterSensorsBaSP.json")
    with open('/usr/src/app/grafana-provisioning/dashboards/WaterSensorsBaSP.json', 'r') as file:
        filedata = file.read()
    filedata = filedata.replace('water_output_test1_scada_sensors', str(water_table_for_json))
    filedata = filedata.replace('water_output_test1_sensors', str(water_table_for_json_sensors))
    with open('/usr/src/app/grafana-provisioning/dashboards/WaterSensorsBaSP.json', 'w') as file:
        file.write(filedata)


if __name__ == "__main__":
    print('Create PostgreSQL database tables if they do not exist')
    dbcommunication.mod_db_tables(databaseTables.waterDBtables('add'))
    print('Delete any existing values from that tables')
    dbcommunication.mod_db_tables(databaseTables.waterDBtables('delete'))
    print('Read the EPANET Input (inp) file')
    finalresult = readinputfile('Water/Virtual_City_WaterNetwork.inp', databaseTables.epanetINPKeywords())
    print('Add EPANET Input (inp) file parameters into Python lists')
    fullinputs = addinfotolists(finalresult, databaseTables.epanetINPFields())
    print('Add EPANET parameters into the PostgreSQL database')
    addDataToDatabase(databaseTables.finalAllINPFields(), fullinputs)
    print('Create new EPANET Input (inp) file using the database values')
    newinputfilecreation('Water/Water.inp', fullinputs)
    runepanetsim('Water/Water.inp', 'Water/report.txt', 'Water/binary.bin')
    bin2json(b'Water/Water.inp', b'Water/Water.txt', b'Water/Water.bin', 'Water/jsonoutput.json', '24:00', '0:05', '0:05', 'Water')
    startdate = '2020-01-01'
    startdate_object = datetime.strptime(startdate, '%Y-%m-%d')
    interval = 30
    readjson('Water/jsonoutput.json', startdate_object, interval)
