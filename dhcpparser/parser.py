#!/usr/bin/python
from pyparsing import *

# An few host entries from dhcpd.leases for testing
sample_data = """
host compute6.sal01.datacentred.co.uk {
  dynamic;
  hardware ethernet 00:30:48:f2:df:48;
  fixed-address 10.10.160.135;
        supersede server.filename = "pxelinux.0";
        supersede server.next-server = 0a:0a:c0:fa;
        supersede host-name = "compute6.sal01.datacentred.co.uk";
}
host compute19-int.sal01.datacentred.co.uk {
  dynamic;
  hardware ethernet 00:30:48:f7:a9:0b;
  fixed-address 10.10.170.151;
        supersede host-name = "compute19-int.sal01.datacentred.co.uk";
}
host compute14-int.sal01.datacentred.co.uk {
  dynamic;
  hardware ethernet 00:30:48:f7:a9:91;
  fixed-address 10.10.170.140;
}
"""

digits = "0123456789"
colon,semi,period,comma,lbrace,rbrace,quote,equals = map(Literal,':;.,{}"=')
number = Word(digits)
hexint = Word(hexnums,exact=2)
dnschars = Word(alphanums + '-') # characters permissible in DNS names
mac = Combine(hexint + (":" + hexint) * 5)("mac_address")
next_server = Combine(hexint + (":" + hexint) * 3)("supersede_nextserver")
ip = Combine(number + period + number + period + number + period + number)
fixed_ip = Combine(number + period + number + period + number + period + number)("fixed_ip")
ips = delimitedList(ip)("ip_addresses")
hardware_ethernet  = Literal('hardware') + Literal('ethernet') + mac + semi("hw_ethernet")
hostname = dnschars
domainname = dnschars + OneOrMore("." + dnschars)
fqdn = Combine(hostname + period + domainname)("fqdn")
supersede_fqdn = Combine(hostname + period + domainname)("supersede_fqdn")
lease_type = Literal('dynamic') + semi
fixed_address  = Literal('fixed-address') + fixed_ip + semi
ddns_hostname = Literal('ddns-hostname') + hostname + semi
ddns_domainname = Literal('ddns-domainname') + quote + domainname + quote + semi
supersede_server_filename = Literal('supersede') + Literal('server.filename') + equals + dblQuotedString + semi
supersede_server_nextserver = Literal('supersede') + Literal('server.next-server') + equals + next_server + semi
supersede_server_hostname = Literal('supersede') + Literal('host-name') + equals + quote + supersede_fqdn + quote + semi

# Put the grammar together to define a host declaration
host = Literal('host') + fqdn + lbrace + Optional(lease_type) + Optional(ddns_hostname) + Optional(ddns_domainname) + Optional(hardware_ethernet) + Optional(fixed_address) + Optional(supersede_server_filename) + Optional(supersede_server_nextserver) + Optional(supersede_server_hostname) + rbrace

#results = host.scanString(sample_data)
infile = "dhcpd.leases"
outfile = "fixed.leases"
file_r = open(infile,"rb")
file_w = open(outfile,"w")
results = host.scanString("".join(file_r.readlines()))

for result in results:
 file_w.write('host %s {\n' % result[0].fqdn)
 file_w.write('\tdynamic;\n')
 file_w.write('\thardware ethernet %s;\n' % result[0].mac_address)
 file_w.write('\tfixed-address %s;\n' % result[0].fixed_ip)
 if result[0].supersede_filename:
	file_w.write('\t\t supersede server.filename = \"%s\";\n' % result[0].supersede_filename)
 if result[0].supersede_nextserver:
	file_w.write('\t\t supersede server.next-server = %s;\n' % result[0].supersede_nextserver)
 if result[0].supersede_fqdn:
 	file_w.write('\t\t supersede host-name = \"%s\";\n' % result[0].supersede_fqdn)
 file_w.write('}\n')

file_r.close()
file_w.close()
