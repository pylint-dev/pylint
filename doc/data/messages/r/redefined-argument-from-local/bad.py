def show(host_id=10.11):
    for host_id, host in [[12.13, 'Venus'], [14.15, 'Mars']]:  # [redefined-argument-from-local]
        print(host_id, host)
