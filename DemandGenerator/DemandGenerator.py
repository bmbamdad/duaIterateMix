from __future__ import print_function
from __future__ import absolute_import
import os
import sys
import xml.etree.ElementTree as et
import random

if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import sumolib  # noqa
from sumolib.miscutils import uMax  # noqa
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

def get_options(args=None):
    optParser = sumolib.options.ArgumentParser(description="Generate trips between random locations")
    optParser.add_argument("-P", "--CAV-Percentage", dest="CAVPerc", default=50, help="The percentages of CAVs")
    optParser.add_argument("-CAV", "--CAV-trip-file", dest="CAVf",
                           default="trips.trips.CAV.xml", help="CAV demand file name")
    optParser.add_argument("-HDV", "--HDV-trip-file", dest="HDVf",
                           default="trips.trips.xml", help="HDV demand file name")
    optParser.add_argument("-HDVRe", "--HDV.rerouting", dest="HDVRe",
                           default="false", help="the vehicle has the rerouting device or not")
    optParser.add_argument("-HDVRePe", "--HDV.rerouting.period", dest="HDVRePe",
                           default="60", help="The period with which HDV shall be rerouted")
    optParser.add_argument("-HDVRePr", "--HDV.rerouting.probability", dest="HDVRePr",
                           default="0.1", help="The probability for a HDV to have a routing device")
    optParser.add_argument("-HDVReDe", "--HDV.rerouting.deterministic", dest="HDVReDe",
                           default="false", help="The devices are set deterministic using a fraction of 1000 (with the defined probability")
    optParser.add_argument("-CAVRe", "--CAV.rerouting", dest="CAVRe",
                           default="false", help="the vehicle has the rerouting device or not")                       
    optParser.add_argument("-CAVRePe", "--CAV.rerouting.period", dest="CAVRePe",
                           default="60", help="The period with which CAV shall be rerouted")
    optParser.add_argument("-CAVRePr", "--CAV.rerouting.probability", dest="CAVRePr",
                           default="0.1", help="The probability for a CAV to have a routing device")
    optParser.add_argument("-CAVReDe", "--CAV.rerouting.deterministic", dest="CAVReDe",
                           default="false", help="The devices are set deterministic using a fraction of 1000 (with the defined probability")

    options = optParser.parse_args(args=args)
    return options

def CAVFileGenerator(options):
    with open(options.CAVf, 'w') as CAVf:
        sumolib.writeXMLHeader(CAVf, "$Id$", "routes", options=options)  # noqa
        CAVf.write('    <vType id="CAV" carFollowModel="Krauss" accel="3.8" decel="4.5" emergencyDecel="8" sigma="0.0" tau="0.6" minGap="0.5" color="0,0,255">\n')
        CAVf.write('        <param key="device.rerouting.period" value="%s"/>\n' % (options.CAVRePe))
        CAVf.write('        <param key="device.rerouting.probability" value="%s"/>\n' % (options.CAVRePr))
        CAVf.write('        <param key="device.rerouting.deterministic" value="%s"/>\n' % (options.CAVReDe))
        CAVf.write('    </vType>\n')
        CAVf.write('\n')
        CAVf.write("    ")
        CAVf.write("</routes>\n")

def HDVFileGenerator(options):
    with open(options.HDVf, 'w') as HDVf:
        sumolib.writeXMLHeader(HDVf, "$Id$", "routes", options=options)  # noqa
        HDVf.write('    <vType id="HDV" carFollowModel="Krauss" accel="3.5" decel="4.5" emergencyDecel="8" sigma="0.5" tau="0.9" minGap="1.5" color="1,0,0">\n')
        HDVf.write('        <param key="device.rerouting.period" value="%s"/>\n' % (options.HDVRePe))
        HDVf.write('        <param key="device.rerouting.probability" value="%s"/>\n' % (options.HDVRePr))
        HDVf.write('        <param key="device.rerouting.deterministic" value="%s"/>\n' % (options.HDVReDe))                
        HDVf.write('    </vType>\n')
        HDVf.write('\n')
        HDVf.write("    ")
        HDVf.write("</routes>\n")





def main(options):
    CAVFileGenerator(options)
    HDVFileGenerator(options)
    # determining CAV demand percentage:
    CAV_percent = float(options.CAVPerc)
    # get the element tree of both of the files
    src_tree = et.parse('trips.xml')
    dest_tree = et.parse('trips.trips.CAV.xml')
    src_tree_2 = et.parse('trips.trips.xml')

    # get the root element "trip" as
    # we want to add it a new element
    src_root = src_tree.getroot()
    dest_root = dest_tree.getroot()
    src_root_2 = src_tree_2.getroot()

    # Calculating the total demand
    Total_Demand = 0
    for trip in src_root:
        Total_Demand = Total_Demand + 1
    Total_Demand = Total_Demand - 1
    
    i=1
    for trips in src_root:
        for src_cur in trips.iter('trip'):
            src_cur.set("id", ("%s"%i))
            i = i+1 
            if i > (Total_Demand+2):
                break
        
 
    # CAV number
    CAV_percent = int(options.CAVPerc)
    CAV_Number = int(round(((CAV_percent) / 100) * (Total_Demand)))

    
    if CAV_percent == 100:
        for n in range(1, (CAV_Number)):
            src_tag = src_tree.find('.//trip')
            dest_root.append(src_tag)
            src_root.remove(src_tag)

    elif CAV_percent == 0:
        src_tag = src_tree.find('.//trip[@id="%s"]' % format(1))
        dest_root.append(src_tag)
        src_root.remove(src_tag)

    else:
        for n in range(0, (CAV_Number+1)):
            src_tag = src_tree.find('.//trip[@id="%s"]' % format((random.randint(0,Total_Demand))))
            while src_tag == None:
                src_tag = src_tree.find('.//trip[@id="%s"]' % format((random.randint(0, Total_Demand))))
                if src_tag !=None:
                    break

    #append the tag
            dest_root.append(src_tag)
    # remove from source
            src_root.remove(src_tag)

    # Temporarily remove the 'vType' element on CAV file
    vType = dest_root.find("vType")
    dest_root.remove(vType)
    
    #sorting file
    dest_root[:] = sorted(dest_root, key=lambda child: (child.tag, float(child.get("depart"))))
    
    
    #writing the type of CAVs on trip definition 
    for interval in dest_root:
        for edge_cur in interval.iter('trip'):
            edge_cur.set("type", str("CAV"))
    
    
    #writing the type of HDVs on trip definition 
    for interval_src in src_root:
        for edge_cur_src in interval_src.iter('trip'):
            edge_cur_src.set("type", str("HDV"))
    
    
    # Put the 'vType' element on HDV file
    vTypeHDV = src_root_2.find("vType")
    src_root.insert(0, vTypeHDV)
    #put the 'vType' element back on CAV file 
    dest_root.insert(0, vType)
    # overwrite the xml files
    et.ElementTree(dest_root).write('trips.trips.CAV.xml')
    et.ElementTree(src_root).write('trips.trips.xml')

        

if __name__ == "__main__":
    if not main(get_options()):
        sys.exit(1)
