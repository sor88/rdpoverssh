from sshtunnel import open_tunnel
from time import sleep

with open_tunnel(
    ('90.150.80.113', 2222),
    ssh_username="itu",
    ssh_pkey="srv.key",
    #ssh_password="pfxtvkbyerc",
    remote_bind_address=('172.16.1.55', 3389),
    local_bind_address=('localhost', 2222)
) as server:

    print(server.local_bind_port)
    while True:
        # press Ctrl-C for stopping
        sleep(1)
