from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, OVSKernelSwitch, UserSwitch, CPULimitedHost
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink, Link
from time import sleep
import time
import os


class LinuxRouter( Node ):

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )
#	os.system('sysctl -w net.ipv4.tcp_congestion_control=vegas')
#	os.system('sysctl -w net.ipv4.tcp_congestion_control=reno')

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class NetworkTopo( Topo ):

    def build( self, **_opts ):
        defaultIP = '10.14.10.1/24'  # IP address untuk r0-eth1
	router = self.addNode( 'R0', cls=LinuxRouter, ip=defaultIP )
	H1 = self.addHost( 'h1', ip='10.14.10.2/24')
	H2 = self.addHost( 'h2', ip='10.14.20.2/24')
	H3 = self.addHost( 'h3', ip='10.14.30.2/24')

	self.addLink( H1, router, bw=50, intfName2='R0-eth1')
	self.addLink( H2, router, bw=50, intfName2='R0-eth2')
	self.addLink( H3, router, use_htb=True, bw =5, delay = '100ms', max_queue_size = 10, intfName2='R0-eth3')

def run():
    "Test linux router"
 
    os.system('mn -c')
    topo = NetworkTopo()
    
    net = Mininet( topo=topo, link=TCLink, host=CPULimitedHost )
    net.start()
    net['h1'].cmd('sysctl -w net.ipv4.tcp_congestion_control=vegas')
    net['h2'].cmd('sysctl -w net.ipv4.tcp_congestion_control=reno')

    #net['R0'].cmd("ifconfig R0-eth1 0")
    #net['R0'].cmd("ifconfig R0-eth2 0")
    #net['R0'].cmd("ifconfig R0-eth3 0")

    net['R0'].cmd("ip addr add 10.14.10.1/24 brd + dev R0-eth1")
    net['R0'].cmd("ip addr add 10.14.20.1/24 brd + dev R0-eth2")
    net['R0'].cmd("ip addr add 10.14.30.1/24 brd + dev R0-eth3")

    net['h1'].cmd("ip route add default via 10.14.10.1")
    net['h2'].cmd("ip route add default via 10.14.20.1")
    net['h3'].cmd("ip route add default via 10.14.30.1")
    h1, h2, h3 = net.get('h1', 'h2', 'h3')
    h3.cmd('iperf -s&')
    h1.cmd('iperf -c 10.14.30.2 -i 1 -n 2M&')
    h2.cmd('iperf -c 10.14.30.2 -i 1 -n 2M&')
	
    net.pingAll()
    time.sleep(35)
    h3.cmdPrint('fg')
    h1.cmdPrint('fg')
    h2.cmdPrint('fg') 
    info( '*** Routing Table on Router:\n' )
    info( net[ 'R0' ].cmd( 'route' ) )
    
    CLI( net )
    net.stop()
    h3.cmdPrint('Scripted by Reghn')
    h1.cmdPrint('Scripted by Reghn')
    h2.cmdPrint('Scripted by Reghn')
    
    h3.cmdPrint('lp Scripted by Reghn')
    h1.cmdPrint('lp Scripted by Reghn')
    h2.cmdPrint('lp Scripted by Reghn')
    
    h3.cmd('lp "Scripted by Reghn" ')
    h1.cmd('lp "Scripted by Reghn" ')
    h2.cmd('lp "Scripted by Reghn" ')

    h3.cmdPrint('lp "Scripted by Reghn" ')
    h1.cmdPrint('lp "Scripted by Reghn" ')
    h2.cmdPrint('lp "Scripted by Reghn" ')


if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
