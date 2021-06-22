query1 = """select patrons.personkey, frname,lname, sum(Amount), donations.Date, 
address, town, state, zipcode, email, phone, phone2, nickname  
from patrons, donations,donors 
where donors.personkey=patrons.personkey 
and donors.donorkey=donations.Donorkey 
group by patrons.personkey 
order by sum(donations.Amount) desc"""

def getColumnNames(query):
    # make list of tokens
    qlist = query.lower().split(' ')
    # remove trailing commas and stop at first SQL keyword
    newq = []
    i = 1        #skip Select
    quit = False
    while i < len(qlist) and not quit:
        ql = qlist[i].strip().removesuffix(',')
        if ql not in {'from', 'join', 'where'}:
            newq.append(ql)
        else:
            quit=True
        i+=1
    # now remove leading table names
    # and split where there was a comma but no space
    newq2 = []
    for ql in newq:
        if '.' in ql:
            qa = ql.split('.')      # remove table name
            ql =qa[1]
        if ',' in ql:
            qa = ql.split(',')      # split at comma
            newq2.append(qa[0])     # when there is no space
            newq2.append(qa[1])     # between column names
        else:
            newq2.append(ql)
    return newq2

cnames = getColumnNames(query1)
print(cnames)