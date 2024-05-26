admin = '1'
opret_gest = '2'
scan = None

def make_creds(creds_list):
    creds = 0
    for i in creds_list:
        if i is None:
            i = 0
        else:
            i = int(i)
        creds = i | creds
    return creds





print(make_creds((admin,opret_gest,scan)))