def show(host_id=10.11):
    for host_id, host in [  # [redefined-argument-from-local]
        [12.13, "Venus"],
        [14.15, "Mars"],
    ]:
        print(host_id, host)
