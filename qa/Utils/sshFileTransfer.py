
import os
import paramiko
import socket
import sys
import base64

if __name__ == '__main__':
    print "Usage %s <remoteHost> <remotePath> <localPath>" % ( sys.argv[0] )
    
    if len(sys.argv) < 4:
        print "Please provide all inputs!"
        sys.exit( -1 )

    remoteHost = sys.argv[1]
    print "remoteHost: ", remoteHost
    remotePath = sys.argv[2]
    print "remotePath: ", remotePath
    localPath = sys.argv[3]

    username = 'scs0009'
    secretPassword = base64.decodestring('UXVQck5hTG8=')

    # try:

    # Delete remote file
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect( remoteHost, username=username, password=secretPassword)
    #client.exec_command('cd /scssvn/qa.openmaf.org/maf2/QAResults/ && rm -rf xml html')
    client.exec_command('cd %s && rm -rf xml html' % remotePath)

    print "remote folder cleaned"

    for path, subDirs, subFiles in os.walk( localPath ):

        relativePath = path.replace( localPath, '/')
        relativePath = relativePath.replace('\\','/')
        if not relativePath.endswith('/'):
            relativePath += '/'

        for subDir in subDirs:
            print "create directory with command 'cd %s%s && mkdir %s'" % (remotePath, relativePath, subDir)
            client.exec_command('cd %s%s && mkdir %s' % (remotePath, relativePath, subDir))

        print "walking relative path %s" % relativePath

        for subFile in subFiles:

            # Socket connection to remote host
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect_ex((remoteHost, 22))

            # Build a SSH transport
            transport = paramiko.Transport(sock)
            transport.start_client()
            transport.auth_password(username, secretPassword)

            # Start a scp channel
            scp_channel = transport.open_session()

            localFilename = '%s/%s' % (path, subFile)

            print "\t reading filename %s" % localFilename

            f = file(localFilename, 'rb')

            print "scp command \'scp -v -t %s%s%s \'" % (remotePath, relativePath, subFile )

            f_content = f.read()
            f.close()
			
            scp_channel.exec_command('scp -v -t %s%s%s \n' % (remotePath, relativePath, subFile ))
            scp_channel.send('C%s %d %s\n'%(oct(os.stat(localFilename).st_mode)[-4:], os.stat(localFilename)[6], subFile ))
            try:
                scp_channel.sendall(f_content)
                print "\t file transfer ok"
            except:
                print"\t file transer failed"

            # close channel
            scp_channel.close()
            transport.close()
            sock.close()

    # close ssh channel
    client.close()

    print "FILES TRANSFER OPERATION SUCCESSFUL"

    # except Exception as e:
        # print str(e)
        # print "FILES TRANSFER OPERATION FAILED"

