import os

def run_openrc():
    os.system('source /home/stack/overcloudrc')


def nova_status():
    status=os.popen('nova service-list').read()
    if 'down' in status:
        return "Nova Service abnormal!"
    else:
        return "Nova Service normal!"

def neutron_status():
    status=os.popen('neutron agent-list').read()
    if 'xxx' in status:
        #print("Neutron Service abnormal!")
        return "Neutron Service abnormal!"
    else:
        return "Neutron Service normal!"

def cinder_status():
    status=os.popen('cinder service-list').read()
    if 'down' in status:
        return "Cinder  Service abnormal!"
    else:
        return "Cinder  Service normal!"


if __name__ == '__main__':
    run_openrc()
    with open('service.txt', 'a+') as f:
        f.write(nova_status())
        f.write(neutron_status())
    cinder_status()
