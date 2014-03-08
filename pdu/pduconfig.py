# APC PDU config updating
# -i IP of the PDU
# -n hostname to set in the config and which gets sent to DNS
# -u FTP username
# -p FTP password
#!/usr/bin/python
import ConfigParser
import ftplib
import socket
import sys
import getopt
import os

def get_config(file):
    config = ConfigParser.ConfigParser()
    config.optionxform=str
    try:
        config.read(file)
        return config
    except Exception, e:
        print 'Cannot open config file', file

def download_config(host,filename,user,pwd):
    try:
        tempfile = "".join(('/tmp/',filename))
        file = open(tempfile, 'wb')
    except IOError:
        print 'cannot open', tempfile
        print 'I/O error({0}): {1}'.format(e.errno, e.strerror)
    else:
        try:
            ftp = ftplib.FTP(host,user,pwd)
            ftp.retrbinary('RETR %s' % filename, file.write)
        except IOError,e:
            print 'I/O error({0}): {1}'.format(e.errno, e.strerror)
        except socket.error,e:
            print 'Unable to connect, %s'%e
        else:
            file.close()
            ftp.quit()

def upload_config(host,filename,user,pwd):
    try:
        file = open(filename, 'rb')
    except IOError:
        print 'Cannot open ', filename
        print 'I/O error({0}): {1}'.format(e.errno, e.strerror)
    else:
        try:
            ftp = ftplib.FTP(host,user,pwd)
            ftp.storbinary('STOR %s' % 'config.ini', file )
        except IOError,e:
            print 'I/O error({0}): {1}'.format(e.errno, e.strerror)
        except socket.error,e:
            print 'Unable to connect, %s'%e
        else:
            file.close()
            ftp.quit()

def usage():
        print 'pduconfig.py -i <ipaddress> -n <hostname> -u <ftpusername> -p <ftppassword>'

def main(args):
    ipaddress = ''
    hostname = ''
    user = ''
    pwd = ''
    try:
        opts, args = getopt.getopt(args,"hi:n:u:p:")
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt == '-i':
            # Validate that this is an IP address
            try:
                socket.inet_pton(socket.AF_INET,arg)
            except socket.error:
                print "Invalid IP address"
                usage()
                sys.exit(2)
            else:
                ipaddress = arg
        elif opt == '-n':
            hostname = arg
        elif opt == '-u':
            user = arg
        elif opt == '-p':
            pwd = arg
    
    if hostname and ipaddress and user and pwd: 
        download_config(ipaddress,'config.ini',user,pwd)
        # Read in both configs
        c1 = get_config('config.ini.skel')
        c2 = get_config('/tmp/config.ini')
        # Change the PDU specific settings
        c1.set('NetworkTCP/IP','HostName',hostname)
        c1.set('NetworkTCP/IP','Override',c2.get('NetworkTCP/IP','Override'))
        c1.set('SystemID','Name',hostname)
        c1.set('Device','NAME_A',hostname)
        c1.set('EnergyWise','ParentName',hostname)
        # Write out the new config file
        with open('/tmp/config.ini', 'wb') as newconf:
            c1.write(newconf)
            newconf.close()
        # Upload back to the PDU
        upload_config(ipaddress,'/tmp/config.ini',user,pwd)
        # Remove the temporary config files
        os.remove('/tmp/config.ini')

    else:
        usage()
        sys.exit(1)

if __name__ == '__main__':
    main(sys.argv[1:])
