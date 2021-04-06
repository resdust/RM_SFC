#!/usr/bin/python3
"""
This is the most simple example to showcase Containernet.
"""
from mininet.net import Containernet
from mininet.node import Controller, RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from json_register import register
setLogLevel('info')

def topology():
    """Create a network"""
    net = Containernet( controller=RemoteController, link=TCLink, switch=OVSKernelSwitch )
 
    info("*** Creating nodes\n")
    # h1 = net.addHost( 'h1', mac='00:00:00:00:00:01', ip='10.0.0.1/24' )
    # h2 = net.addHost( 'h2', mac='00:00:00:00:00:02', ip='10.0.0.2/24' )
    # h3 = net.addHost( 'h3', mac='00:00:00:00:00:03', ip='10.0.0.3/24' )
    # h4 = net.addHost( 'h4', mac='00:00:00:00:00:04', ip='10.0.0.4/24' )
    
    # info('*** Adding docker containers\n')
    h1 = net.addDocker('d1', mac='00:00:00:00:00:01', ip='10.0.0.1/24', dimage="linton/docker-snort:latest")
    h2 = net.addDocker('d2', mac='00:00:00:00:00:02', ip='10.0.0.2/24', dimage="linton/docker-snort:latest")
    h3 = net.addDocker( 'd3', mac='00:00:00:00:00:03', ip='10.0.0.3/24', dimage="linton/docker-snort:latest")
    h4 = net.addDocker( 'd4', mac='00:00:00:00:00:04', ip='10.0.0.4/24', dimage="linton/docker-snort:latest" )
    h5 = net.addHost( 'h5', mac='00:00:00:00:00:05', ip='10.0.0.5/24' )
    # h5 = net.addDocker( 'd5', mac='00:00:00:00:00:05', ip='10.0.0.5/24', dimage="linton/docker-snort:latest" )

    info('*** Adding switches\n')
    s1 = net.addSwitch( 's1', listenPort=6671 )
    s2 = net.addSwitch( 's2', listenPort=6672 )
    s3 = net.addSwitch( 's3', listenPort=6673 )
    s4 = net.addSwitch( 's4', listenPort=6674 )
    s5 = net.addSwitch( 's5', listenPort=6675 )

    info('*** Adding controller\n')
    c7 = net.addController( 'c7', controller=RemoteController, ip='127.0.0.1', port=6633 )
 
    info("*** Creating links")    
    net.addLink(s1, h1)
    net.addLink(s2, h2)
    net.addLink(s3, h3)
    net.addLink(s4, h4)
    net.addLink(s5, h5)
    net.addLink(s1, s2)
    net.addLink(s2, s3)
    net.addLink(s3, s4)
    net.addLink(s4, s5)
    net.addLink(s3, h2)
    net.addLink(s4, h3)
    h2.cmd('ifconfig h2-eth1 10.0.0.12 netmask 255.255.255.0')
    h3.cmd('ifconfig h3-eth1 10.0.0.13 netmask 255.255.255.0')

    print ("*** Starting network")

    net.build()
    h2.cmd('ip route add 10.0.0.1/32 dev h2-eth0; ip route add 10.0.0.5/32 dev h2-eth1')
    h2.cmd('ip route add 10.0.0.253/32 dev h2-eth0; ip route add 10.0.0.254/32 dev h2-eth1')
    h2.cmd('sudo arp -i h2-eth0 -s 10.0.0.253 01:02:03:04:05:06')
    h2.cmd('sudo arp -i h2-eth1 -s 10.0.0.254 11:12:13:14:15:16')
    
    h3.cmd('ip route add 10.0.0.1/32 dev h3-eth0; ip route add 10.0.0.5/32 dev h3-eth1')
    h3.cmd('ip route add 10.0.0.253/32 dev h3-eth0; ip route add 10.0.0.254/32 dev h3-eth1')
    h3.cmd('sudo arp -i h3-eth0 -s 10.0.0.253 01:02:03:04:05:06')
    h3.cmd('sudo arp -i h3-eth1 -s 10.0.0.254 11:12:13:14:15:16')

    h5.cmd('sudo arp -i h5-eth0 -s 10.0.0.253 01:02:03:04:05:06')

    c7.start()
    s1.start( [c7] )
    s2.start( [c7] )
    s3.start( [c7] )
    s4.start( [c7] )
    s5.start( [c7] )

    (json, addr, port) = register(file='../data/forwarder1-1.txt', addr='10.0.0.254', port='30012', event_name='registration')
    print(json,addr,port)
    # h2.cmd('echo',json,'| nc -u',addr,port)
    h2.cmd('./json_register.py --file=../data/forwarder1-1.txt -a 10.0.0.254 -p 30012 -n registration')
    h2.cmd('./json_register.py --file=../data/forwarder1-2.txt -a 10.0.0.253 -p 30012 -n registration')
    h3.cmd('./json_register.py --file=../data/forwarder2-1.txt -a 10.0.0.254 -p 30012 -n registration')
    h3.cmd('./json_register.py --file=../data/forwarder2-2.txt -a 10.0.0.253 -p 30012 -n registration')
    h5.cmd('./json_register.py --file=../data/forwarder3-3.txt -a 10.0.0.253 -p 30012 -n registration')
    print("*** Running CLI")
    CLI( net )
 
    print("*** Stopping network")
    net.stop()
 
if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()

'''
net = Containernet(controller=Controller)
info('*** Adding controller\n')
net.addController('c0')
info('*** Adding docker containers\n')
d1 = net.addDocker('d1', ip='10.0.0.251', dimage="ubuntu:trusty")
d2 = net.addDocker('d2', ip='10.0.0.252', dimage="ubuntu:trusty")
info('*** Adding switches\n')
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')
info('*** Creating links\n')
net.addLink(d1, s1)
net.addLink(s1, s2, cls=TCLink, delay='100ms', bw=1)
net.addLink(s2, d2)
info('*** Starting network\n')
net.start()
info('*** Testing connectivity\n')
net.ping([d1, d2])
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()
'''
