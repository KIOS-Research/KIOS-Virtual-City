#Define Constants
#'water_output_nodes_demands', 'water_output_nodes_head', 'water_output_nodes_pressure', 'water_output_nodes_quality'
#'water_output_links_friction', 'water_output_links_headloss', 'water_output_links_quality', 'water_output_links_reactionrate', 'water_output_links_setting', 'water_output_links_status', 'water_output_links_velocity'
def epanetTableKeywords():
    epanet_Table_keywords = ['water_JUNCTIONS', 'water_RESERVOIRS', 'water_TANKS', 'water_PIPES', 'water_PUMPS', 'water_VALVES',
                       'water_EMITTERS',
                       'water_CURVES', 'water_PATTERNS', 'water_ENERGY', 'water_STATUS', 'water_DEMANDS',
                       'water_QUALITY', 'water_REACTIONS', 'water_SOURCES', 'water_MIXING',
                       'water_OPTIONS', 'water_TIMES', 'water_REPORT',
                       'water_COORDINATES', 'water_VERTICES', 'water_LABELS', 'water_CONTROLS', 'water_RULES', 'water_BACKDROP', 'water_TAGS', 'water_output_nodes', 'water_output_nodes_values', 'water_output_links', 'water_output_links_values']
    return epanet_Table_keywords


def epanetSimulationTableKeywords():
    epanet_Simulation_Table_keywords = ['water_output_nodes', 'water_output_nodes_values', 'water_output_links', 'water_output_links_values']
    return epanet_Simulation_Table_keywords


def epanetINPKeywords():
    epanet_INP_keywords = ['[TITLE]', '[JUNCTIONS]', '[RESERVOIRS]', '[TANKS]', '[PIPES]', '[PUMPS]', '[VALVES]',
                       '[EMITTERS]',
                       '[CURVES]', '[PATTERNS]', '[ENERGY]', '[STATUS]', '[CONTROLS]', '[RULES]', '[DEMANDS]',
                       '[QUALITY]', '[REACTIONS]', '[SOURCES]', '[MIXING]',
                       '[OPTIONS]', '[TIMES]', '[REPORT]',
                       '[COORDINATES]', '[VERTICES]', '[LABELS]', '[BACKDROP]', '[TAGS]',
                       '[END]']
    return epanet_INP_keywords


def epanetINPFields():
    INPfields = {'JUNCTIONS': ['ID', 'Elev', 'Demand', 'Pattern'],
              'RESERVOIRS': ['ID', 'Head', 'Pattern'],
              'TANKS': ['ID', 'Elevation', 'InitLevel', 'MinLevel', 'MaxLevel', 'Diameter', 'MinVol', 'VolCurve'],
              'PIPES': ['ID', 'Node1', 'Node2', 'Length', 'Diameter', 'Roughness', 'MinorLoss', 'Status'],
              'PUMPS': ['ID', 'Node1', 'Node2', 'Parameters'],
              'VALVES': ['ID', 'Node1', 'Node2', 'Diameter', 'Type', 'Setting', 'MinorLoss'],
              'TAGS': ['Object', 'ID', 'Tag'],
              'DEMANDS': ['Junction', 'Demand', 'Pattern', 'Category'],
              'STATUS': ['ID', 'StatusSetting'],
              'PATTERNS': ['ID', 'Multipliers'],
              'CURVES': ['ID', 'XValue', 'YValue'],
              'CONTROLS': ['----'],
              'RULES': ['ruleID', 'Rule'],
              'ENERGY': ['field', 'value'],
              'EMITTERS': ['Junction', 'Coefficient'],
              'QUALITY': ['Node', 'InitQual'],
              'SOURCES': ['Node', 'Type', 'Quality', 'Pattern'],
              'REACTIONS': ['Type', 'Coefficient'],
              'MIXING': ['Tank', 'Model', 'Volume'],
              'TIMES': ['field', 'value'],
              'REPORT': ['field', 'value'],
              'OPTIONS': ['field', 'value'],
              'COORDINATES': ['Node', 'XCoord', 'YCoord'],
              'VERTICES': ['Link', 'XCoord', 'YCoord'],
              'LABELS': ['XCoord', 'YCoord', 'Label', 'Anchor'],
              'BACKDROP': ['field', 'value']}
    return INPfields


def finalAllINPFields():
    allfields = {'JUNCTIONS': ["junctionid", "Elev", "Demand", "Pattern"],
                 "RESERVOIRS": ["reservoirid", "Head", "Pattern"],
                 "TANKS": ["tankid", "Elevation", "InitLevel", "MinLevel", "MaxLevel", "Diameter", "MinVol", "VolCurve"],
                 "PIPES": ["pipeid", "Node1", "Node2", "Length", "Diameter", "Roughness", "MinorLoss", "Status"],
                 "PUMPS": ["pumpid", "Node1", "Node2", "Parameters"],
                 "VALVES": ["valveid", "Node1", "Node2", "Diameter", "Type", "Setting", "MinorLoss"],
                 "DEMANDS": ["Junction", "Demand", "Pattern", "Category"],
                 "STATUS": ["statusid", "StatusSetting"],
                 "PATTERNS": ["patternid", "Multipliers"],
                 "CURVES": ["curveid", "XValue", "YValue"],
                 "CONTROLS": ["control"],
                 "RULES": ["ruleID", "Rule"],
                 "ENERGY": ["field", "value"],
                 "TIMES": ["field", "value"],
                 "REPORT": ["field", "value"],
                 "OPTIONS": ["field", "value"],
                 "EMITTERS": ["Junction", "Coefficient"],
                 "QUALITY": ["Node", "InitQual"],
                 "SOURCES": ["Node", "Type", "Quality", "Pattern"],
                 "REACTIONS": ["Type", "Coefficient"],
                 "MIXING": ["Tank", "Model", "Volume"],
                 "COORDINATES": ["Node", "XCoord", "YCoord"],
                 "VERTICES": ["Link", "XCoord", "YCoord"],
                 "LABELS": ["XCoord", "YCoord", "Label", "Anchor"],
                 "BACKDROP": ["field", "value"],
                 "TAGS": ["Object", "tagid", "Tag"]}

    return allfields


def sumoDBtables(type):
    if type == 'add':
        tables = ["CREATE TABLE IF NOT EXISTS transportation_vehicles(timestep FLOAT NOT NULL, vehicleid VARCHAR NOT NULL, eclass VARCHAR NOT NULL, co2 FLOAT NOT NULL, co FLOAT NOT NULL, hc FLOAT NOT NULL, nox FLOAT NOT NULL, pmx FLOAT NOT NULL, fuel FLOAT NOT NULL, electricity FLOAT NOT NULL, noise FLOAT NOT NULL, route VARCHAR NOT NULL, waiting FLOAT NOT NULL, x FLOAT NOT NULL, y FLOAT NOT NULL, angle FLOAT NOT NULL, vehtype VARCHAR NOT NULL, speed FLOAT NOT NULL, pos FLOAT NOT NULL, lane VARCHAR NOT NULL, slope FLOAT NOT NULL, primary key(timestep, vehicleid));",
            "CREATE TABLE IF NOT EXISTS transportation_edges (timestep FLOAT NOT NULL, edjeid VARCHAR NOT NULL, laneid VARCHAR NOT NULL, traveltime FLOAT NOT NULL,co2 FLOAT NOT NULL, co FLOAT NOT NULL, hc FLOAT NOT NULL, nox FLOAT NOT NULL, pmx FLOAT NOT NULL,fuel FLOAT NOT NULL, electricity FLOAT NOT NULL, noise FLOAT NOT NULL, maxspeed FLOAT NOT NULL, meanspeed FLOAT NOT NULL, occupancy FLOAT NOT NULL, vehicle_count FLOAT NOT NULL, primary key(timestep, edjeid, laneid));"]
    elif type == 'delete':
        tables = ["DELETE FROM transportation_vehicles;", "DELETE FROM transportation_edges;"]
    return tables


def waterDBtables(type):
    tables = []
    if type == 'add':
        tables = ['CREATE TABLE IF NOT EXISTS water_JUNCTIONS (id SERIAL, junctionid VARCHAR, Elev FLOAT, Demand FLOAT, Pattern VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_RESERVOIRS (id SERIAL, reservoirid VARCHAR, Head FLOAT, Pattern VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_TANKS (id SERIAL, tankid VARCHAR, Elevation FLOAT, InitLevel FLOAT, MinLevel FLOAT, MaxLevel FLOAT, Diameter FLOAT, MinVol FLOAT, VolCurve VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_PIPES (id SERIAL, pipeid VARCHAR, Node1 VARCHAR, Node2 VARCHAR, Length FLOAT, Diameter FLOAT, Roughness FLOAT, MinorLoss FLOAT, Status VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_PUMPS (id SERIAL, pumpid VARCHAR, Node1 VARCHAR, Node2 VARCHAR, Parameters VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_VALVES (id SERIAL, valveid VARCHAR, Node1 VARCHAR, Node2 VARCHAR, Diameter FLOAT, Type VARCHAR, Setting FLOAT, MinorLoss FLOAT);',
                  'CREATE TABLE IF NOT EXISTS water_DEMANDS (id SERIAL, Junction VARCHAR, Demand FLOAT, Pattern VARCHAR, Category VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_STATUS (id SERIAL, statusid VARCHAR, StatusSetting VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_PATTERNS (id SERIAL, patternid VARCHAR, Multipliers VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_CURVES (id SERIAL, curveid VARCHAR, XValue FLOAT, YValue FLOAT);',
                  'CREATE TABLE IF NOT EXISTS water_ENERGY (id SERIAL, field VARCHAR, value VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_TIMES (id SERIAL, field VARCHAR, value VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_REPORT (id SERIAL, field VARCHAR, value VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_OPTIONS (id SERIAL, field VARCHAR, value VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_EMITTERS (id SERIAL, Junction VARCHAR, Coefficient FLOAT);',
                  'CREATE TABLE IF NOT EXISTS water_QUALITY (id SERIAL, Node VARCHAR, InitQual FLOAT);',
                  'CREATE TABLE IF NOT EXISTS water_SOURCES (id SERIAL, Node VARCHAR, Type VARCHAR, Quality FLOAT, Pattern VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_REACTIONS (id SERIAL, Type VARCHAR, Coefficient FLOAT);',
                  'CREATE TABLE IF NOT EXISTS water_MIXING (id SERIAL, Tank VARCHAR, Model VARCHAR, Volume FLOAT);',
                  'CREATE TABLE IF NOT EXISTS water_COORDINATES (id SERIAL, Node VARCHAR, XCoord FLOAT, YCoord FLOAT);',
                  'CREATE TABLE IF NOT EXISTS water_VERTICES (id SERIAL, Link VARCHAR, XCoord FLOAT, YCoord FLOAT);',
                  'CREATE TABLE IF NOT EXISTS water_LABELS (id SERIAL, XCoord FLOAT, YCoord FLOAT, Label VARCHAR, Anchor VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_CONTROLS (id SERIAL, control VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_RULES (id SERIAL, ruleid VARCHAR, Rule VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_BACKDROP (id SERIAL, field VARCHAR, value VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_TAGS (id SERIAL, Object VARCHAR, tagid VARCHAR, Tag VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_output_nodes (id SERIAL, nodeid VARCHAR, nodetype VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_output_nodes_values (id SERIAL, nodeid VARCHAR, readingtime timestamp, nodedemand DOUBLE PRECISION, nodehead DOUBLE PRECISION, nodepressure DOUBLE PRECISION, nodequality DOUBLE PRECISION);',
                  'CREATE TABLE IF NOT EXISTS water_output_links (id SERIAL, linkid VARCHAR, linktype VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_output_links_values(id SERIAL, linkid VARCHAR, readingtime timestamp, linkfriction DOUBLE PRECISION, linkheadloss DOUBLE PRECISION, linkquality DOUBLE PRECISION, linkreactionrate DOUBLE PRECISION, linksetting DOUBLE PRECISION, linkstatus VARCHAR, linkvelocity DOUBLE PRECISION);']
    elif type == 'delete':
        for val in epanetTableKeywords():
            query = 'TRUNCATE ' + str(val) + ';'
            tables.append(query)
    elif type == 'deletesimulations':
        for val in epanetSimulationTableKeywords():
            query = 'TRUNCATE ' + str(val) + ';'
            tables.append(query)
    return tables


def electricityDBtables(type):
    tables = []
    if type == 'add':
        tables = ["CREATE TABLE IF NOT EXISTS power_substations (substationid INTEGER NOT NULL, lineid INTEGER NOT NULL, primary key(substationid));",
                  "CREATE TABLE IF NOT EXISTS power_voltages (substationid INTEGER NOT NULL, lineid INTEGER NOT NULL, mestime TIMESTAMP NOT NULL, phase_a DOUBLE PRECISION NOT NULL, phase_b DOUBLE PRECISION NOT NULL, phase_c DOUBLE PRECISION NOT NULL, primary key(substationid, lineid, mestime));"]
    elif type == 'delete':
        tables = ["DELETE FROM power_substations;", "DELETE FROM power_voltages;"]
    return tables


'''
tables = ['CREATE TABLE IF NOT EXISTS water_JUNCTIONS (ID VARCHAR, Elev FLOAT, Demand FLOAT, Pattern VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_RESERVOIRS (ID VARCHAR, Head FLOAT, Pattern VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_TANKS (ID VARCHAR, Elevation FLOAT, InitLevel FLOAT, MinLevel FLOAT, MaxLevel FLOAT, Diameter FLOAT, MinVol FLOAT, VolCurve VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_PIPES (ID VARCHAR, Node1 VARCHAR, Node2 VARCHAR, Length FLOAT, Diameter FLOAT, Roughness FLOAT, MinorLoss FLOAT, Status VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_PUMPS (ID VARCHAR, Node1 VARCHAR, Node2 VARCHAR, Parameters VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_VALVES (ID VARCHAR, Node1 VARCHAR, Node2 VARCHAR, Diameter FLOAT, Type VARCHAR, Setting FLOAT, MinorLoss FLOAT);',
                  'CREATE TABLE IF NOT EXISTS water_DEMANDS (Junction VARCHAR, Demand FLOAT, Pattern VARCHAR, Category VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_STATUS (ID VARCHAR, StatusSetting VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_PATTERNS (ID VARCHAR, Multipliers VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_CURVES (ID VARCHAR, XValue FLOAT, YValue FLOAT);',
                  'CREATE TABLE IF NOT EXISTS water_ENERGY (field VARCHAR, value VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_TIMES (field VARCHAR, value VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_REPORT (field VARCHAR, value VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_OPTIONS (field VARCHAR, value VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_EMITTERS (Junction VARCHAR, Coefficient FLOAT);',
                  'CREATE TABLE IF NOT EXISTS water_QUALITY (Node VARCHAR, InitQual FLOAT);',
                  'CREATE TABLE IF NOT EXISTS water_SOURCES (Node VARCHAR, Type VARCHAR, Quality FLOAT, Pattern VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_REACTIONS (Type VARCHAR, Coefficient FLOAT);',
                  'CREATE TABLE IF NOT EXISTS water_MIXING (Tank VARCHAR, Model VARCHAR, Volume FLOAT);',
                  'CREATE TABLE IF NOT EXISTS water_COORDINATES (Node VARCHAR, XCoord FLOAT, YCoord FLOAT);',
                  'CREATE TABLE IF NOT EXISTS water_VERTICES (Link VARCHAR, XCoord FLOAT, YCoord FLOAT);',
                  'CREATE TABLE IF NOT EXISTS water_LABELS (XCoord FLOAT, YCoord FLOAT, Label VARCHAR, Anchor VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_CONTROLS (control VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_RULES (ruleID VARCHAR, Rule VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_BACKDROP (field VARCHAR, value VARCHAR);',
                  'CREATE TABLE IF NOT EXISTS water_TAGS (Object VARCHAR, ID VARCHAR, Tag VARCHAR);']
'''