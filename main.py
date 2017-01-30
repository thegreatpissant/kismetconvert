import sys, getopt

import xml.etree.ElementTree as ET

gpsxmlfile = None
netxmlfile= None


def main():
    """  Parse out our xml objects and print them to a file. """
    groot = gpsxmlfile.getroot()
    nroot = netxmlfile.getroot()
    gpsssid = {}
    #print groot
    #print nroot
    #print 'Parsing gps'
    for i in groot[1:]:
        if i.attrib["bssid"] and not i.attrib["bssid"] in gpsssid:
            gpsssid[i.attrib["bssid"]] = {'lat':i.attrib["lat"], 'lon':i.attrib["lon"], 'name':'NULL'}
            #print "b type: " , type(i.attrib["bssid"])

    #print "printing items"
    #for i in gpsssid.keys():
        #print "bssid: " , i,  " lat:", gpsssid[i]['lat'], ' lon:', gpsssid[i]['lon']

    #print 'Parsing net'
    w = nroot.findall('wireless-network')
    for i in w:
        if i.tag == "wireless-network":
            b = i.findall('BSSID')
            #print "bssid:" , b[0].text
            e = i.findall('SSID')
            if len(e) == 0:
                continue
            else:
                es = e[0].findall('essid')
                #print "essid: " , es[0].text
            #print "BTYPE: " , type(b[0].text)
            if b[0].text in gpsssid:
                gpsssid[b[0].text]["name"] = es[0].text

    #print "printing items"
    print "name,desc,latitude,longitude"
    for i in gpsssid.keys():
	print "\"{}\",{},{},{}".format(gpsssid[i]['name'], i, gpsssid[i]['lat'], gpsssid[i]['lon'])
        #print '"',str(gpsssid[i]['name']).strip(), '",', i, ',', gpsssid[i]['lat'], ',', gpsssid[i]['lon']



def usage():
    print 'main.py', ' -g <gpsxml file> -n <netxml file>'


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "g:n:")
    except getopt.GetoptError:
        print "error in arguments"
        usage()
        sys.exit(2)

    gfile = ""
    nfile = ""
    errorCode = ""

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ('-g'):
            gfile = arg
        elif opt in ('-n'):
            nfile = arg

    if len(gfile) == 0:
        errorCode += "Require .gpsxml file."
    if len(nfile) == 0:
        errorCode += "Require .netxml file."
    if not len(errorCode) == 0:
        print errorCode
        usage()
        sys.exit()

    gpsxmlfile = ET.parse(gfile)
    netxmlfile = ET.parse(nfile)

    if not len(errorCode) == 0:
        print errorCode
        sys.exit(2)

    #print "GPSxml file:", gfile
    #print "NETxml file:", nfile

    main()
