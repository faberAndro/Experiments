import subprocess as sub

interface = input('Enter network interface to change: ')
new_mac_address = input('Enter new MAC address: ')

command = 'ifconfig ' + new_mac_address 
before_change = sub.check_output(['ifconfig' + interface])
sub.call(['ifconfig' + interface + 'down'])
sub.call(['ifconfig' + interface + ' hw ' + 'ether ' + new_mac_address])
sub.call(['ifconfig' + interface + 'up'])

after_change = sub.check_output(['ifconfig' + interface])

if before_change == after_change:
    print("failed to change")
else:
    print('new MACADDR: '+new_mac_address+ " on interface " + interface)
