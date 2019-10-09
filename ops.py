import subprocess, os

def shell_source(file):
    pipe = subprocess.Popen(". %s; env" % file, stdout=subprocess.PIPE, shell=True)
    output = pipe.communicate()[0]
    env = dict((line.split("=", 1) for line in output.splitlines()))
    os.environ.update(env)


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
    
def glance_status():
    status=int(os.popen('glance image-list >/dev/null  2>&1;echo $?').read())
    if  status == 0:
        return "Glance  Service normal!"
    else:
        return "Glance  Service abnormal!"


if __name__ == '__main__':
    shell_source('/home/stack/overcloudrc')
    with open('service.txt', 'a+') as f:
        f.write(nova_status())
        f.write(neutron_status())
    cinder_status()
