import paramiko
import re
import overcloud_plat_service


class Node():
    pkey='/home/stack/.ssh/id_rsa'

    def __init__(self,hostname,ip,user):
        self.hostname = hostname
        self.ip=ip
        self.user=user


    def os_system(self):
        key=paramiko.RSAKey.from_private_key_file(self.pkey)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, 22, self.user,pkey=key)
        tran = ssh.get_transport()
        sftp = paramiko.SFTPClient.from_transport(tran)
        sftp.put('/home/stack/healthcheck/service.py','/tmp/service.py')
        stdin, stdout, stderr = ssh.exec_command('sudo python /tmp/service.py')
        return stdout.read()
    def write_os_system(self):
        fo = open("health.txt", "a+")
        str=self.os_system()
        fo.write(self.hostname+"\tplatform:" +'\n'+ str )
        fo.close()
    #Execute on a control node
    def Middleware_Services(self):
        key=paramiko.RSAKey.from_private_key_file(self.pkey)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, 22, self.user,pkey=key)
        # Check Pacemaker and Corosync Service
        stdin, stdout, stderr = ssh.exec_command('sudo  systemctl |grep -E "coro|pacemaker"|grep running|wc -l')
        with open("health.txt", "a+") as f:
            f.write('------Middleware Services Status-----\n')
            if int(stdout.read()) == 2:
	        f.write("Pacemaker and Corosync Service status normal!\n")
            else:
                f.write("Pacemaker and Corosync Service status abnormal!\n")
        # Check Redis Service
        redis_stdin,redis_stdout,redis_stderr = ssh.exec_command('sudo pcs status|grep -A2 redis|grep overcloud')
        redis_ret=re.findall('overcloud',redis_stdout.read())
        with open("health.txt", "a+") as f:
            if len(redis_ret) == 3:
                f.write('Redis cluster status normal!\n')
            else:
                f.write('Redis cluster status abnormal!\n')
        # Check Galera Cluster Service
        galera_stdin,galera_stdout,galera_stderr = ssh.exec_command('sudo pcs status |grep -A1 galera|grep -i Masters')
        galera_ret=re.findall('overcloud',galera_stdout.read())
        with open("health.txt", "a+") as f:
            if len(galera_ret) == 3:
                f.write('Galera  cluster status normal!\n')
            else:
                f.write('Galera cluster status abnormal!\n')
        # Check haproxy Cluster Status
        haproxy_stdin,haproxy_stdout,haproxy_stderr = ssh.exec_command('sudo pcs status |grep -A1 haproxy|grep -i Started')
        haproxy_ret=re.findall('overcloud',haproxy_stdout.read())
        with open("health.txt", "a+") as f:
             if len(haproxy_ret) == 3:
                f.write('Haproxy  cluster status normal!\n')
             else:
                f.write('Haproxy cluster status abnormal!\n')
        # Check Memcached Cluster Service
        memcached_stdin,memcached_stdout,memcached_stderr = ssh.exec_command('sudo pcs status |grep -A1 memcached|grep -i Started')
        memcached_ret=re.findall('overcloud',memcached_stdout.read())
        with open("health.txt", "a+") as f:
             if len(memcached_ret) == 3:
                f.write('Memcached  cluster status normal!\n')
             else:
                f.write('Memcached cluster status abnormal!\n')
        # Check Mongod Cluster Status
        mongod_stdin,mongod_stdout,mongod_stderr = ssh.exec_command('sudo pcs status |grep -A1 mongod||grep -i Started')
        mongod_ret=re.findall('overcloud',mongod_stdout.read())
        with open("health.txt", "a+") as f:
             if len(mongod_ret) == 3:
                f.write('Mongod  cluster status normal!\n')
             else:
                f.write('Mongod cluster status abnormal!\n')
        # Check rabbitmq Cluster Status
        rabbitmq_stdin,rabbitmq_stdout,rabbitmq_stderr = ssh.exec_command('sudo pcs status |grep -A1 rabbitmq|grep -i Started')
        rabbitmq_ret=re.findall('overcloud',rabbitmq_stdout.read())
        with open("health.txt", "a+") as f:
             if len(rabbitmq_ret) == 3:
                f.write('Rabbitmq  cluster status normal!\n')
             else:
                f.write('Rabbitmq cluster status abnormal!\n')
def Overcloud_plat():
    overcloud_plat_service.run_openrc()
    nova_stat=overcloud_plat_service.nova_status()
    neutron_stat=overcloud_plat_service.neutron_status()
    cinder_stat=overcloud_plat_service.cinder_status()
    with open("health.txt", "a+") as f:
        f.write('-----OverCloud Platform Service--------\n')
        f.write("Nova Service status: "+nova_stat+'\n')
        f.write("Neutron Service status: "+neutron_stat+'\n')
        f.write("Cinder Service status: "+cinder_stat+'\n')

    


if __name__ == "__main__":
    user='heat-admin'
    node_dict={}
    controller_node=[]
    with open('/etc/hosts','r') as f:
        for i in f.readlines():
            if 'overcloud' in i: node_dict[i.split()[1]]=i.split()[0]
            if 'controller' in i: controller_node.append(i.split()[1])
    controller_node.sort()
    for hostname, ip in node_dict.items():
        con=Node(hostname,ip,user)
        con.write_os_system()
        if hostname == controller_node[0]:
            con.Middleware_Services()
    Overcloud_plat()    
