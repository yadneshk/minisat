"""
kickgen function create a kickstart and save it in /var/www/html folder
httpd.service should be running
"""


def kick_gen(vm_name, passwd, location, repo):
    with open("/tmp/ks.cfg", "w+") as ks:
        ks.write("install \n"
                 "keyboard 'us' \n"
                 "rootpw --plaintext " + passwd +
                 "\nlang en_US \n"
                 "firewall --enabled \n"
                 "reboot \n"
                 "timezone Asia/Kolkata --isUtc \n"
                 "graphical \n"
                 "url --url=\"" + location +
                 "\" \nauth  --useshadow  --passalgo=sha512 \n"
                 "user --name=" + vm_name + " --groups=wheel --plaintext --password=" + vm_name + " \n"
                 "firstboot --disable \n"
                 "selinux --enforcing \n"
                 "bootloader --location=mbr \n"
                 "clearpart --all --initlabel\n"
                 "part /boot --fstype=\"ext4\" --size=1024 \n"
                 "part swap --fstype=\"swap\" --size=2048 \n"
                 "part / --fstype=\"ext4\" --grow --size=1 \n"
                 "%post \n"
                 "hostnamectl set-hostname " + vm_name + " \n"
                 # "useradd " + vm_name + " \n"
                 "systemctl restart sshd \n"
                 "systemctl enable sshd \n"
                 )

        for name, baseurl in repo.items():
            ks.write("echo -e '[" + name + "] \\nname=" + name + " \\nbaseurl=" + baseurl + " \\ngpgcheck=0 \\nenabled=1' >/etc/yum.repos.d/" + name + ".repo \n")
        ks.write("%end \n")

    return "/tmp/ks.cfg"
