import re

newFile = open('database2.txt', 'r')
lines = newFile.read()
PSU = lines.split('PowerSupplies!')
PSU = PSU[1].split('Processors!')
PSU = PSU[0]
PSU = PSU.splitlines()
PSU.pop(0)
newFile.close()

for i in PSU:
    Title_str = i.split(':').pop()
    Output_line = i.split(':')
    try:
        Watt_val = Title_str.split('W')[0]
        s = Watt_val
        watt_list = re.findall('\d+', s)
        for i in watt_list:
            if len(i) >= 3:
                wattage = str(i)
            else:
                wattage = 'N/A'
        Output_line.append(wattage)
    except ValueError:
        pass
    if 'SFX' in Title_str:
        form = 'SFX'
    else:
        form = 'ATX'
    Output_line.append(form)

    Output_line = ':'.join(map(str, Output_line))
    print(Output_line)
