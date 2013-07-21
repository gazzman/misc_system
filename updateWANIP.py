#!/usr/bin/python
from datetime import datetime
import sys
import urllib2

from BeautifulSoup import BeautifulSoup

WANIDURL="http://www.google.com/search?q=what+is+my+ip"
LOGFILEFMT = "%(date)s,%(hostname)s,%(ip)s\n"
UASTRING = 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0.1) Gecko/20120225 Firefox/10.0.1'

if __name__ == '__main__':
    logfile = sys.argv[1]
    hostname = sys.argv[2]
    password = sys.argv[3]
    ipdict = {hostname: ""}
    try:
        with open(logfile, 'r') as lfile:
        	for line in lfile:
        		date, host, oldip = line.strip().split(',')
        		ipdict[host] = oldip
    except IOError:
        ipdict[hostname] = ""

    header = {'User-Agent' : UASTRING}
    req = urllib2.Request(WANIDURL, headers=header)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page)

    newip = soup.em.text
    if newip != ipdict[hostname]:
        url_host = 'https://www.dtdns.com/'
        url_path = 'api/autodns.cfm?id=%s.dtdns.net&pw=%s&ip=%s' % (hostname, 
                                                                    password,
                                                                    newip)
        url_hostpath = "%s%s" % (url_host, url_path)
        req = urllib2.Request(url_hostpath, headers=header)
        page = urllib2.urlopen(req)
        msg = "Updating IP for host %s from '%s' to '%s'" % (hostname, 
                                                             ipdict[hostname],
                                                             newip)
        print >> sys.stderr, msg
        with open(logfile, 'a') as lfile:
            lfile.write(LOGFILEFMT % {'date': datetime.now().isoformat(), 
                                      'hostname': hostname, 
                                      'ip': newip})
