import re

newFile = open('database2.txt', 'r')
lines = newFile.read()
RAM = lines.split('Memory!')
RAM = RAM[1].split('VideoCards!')
RAM = RAM[0]
RAM = RAM.splitlines()
RAM.pop(0)
newFile.close()

for i in RAM:
    Title_str = i.split(':').pop()
    Output_line = i.split(':')

    # if 'DDR2' in Title_str:
    #     Gen = 2
    if 'DDR3' in Title_str and 'SODIMM' not in Title_str and 'SO-DIMM' not in Title_str and 'ECC' not in Title_str:
        Gen = False
        s = Title_str.split('GB')[0]
        capacity_list = re.findall('\d+', s)
        for i in capacity_list:
            if len(i) == 2:
                capacity = int(i)
            else:
                capacity = int(i)
    elif 'DDR4' in Title_str and 'SODIMM' not in Title_str and 'SO-DIMM' not in Title_str and 'ECC' not in Title_str:
        Gen = True
        s = Title_str.split('GB')[0]
        capacity_list = re.findall('\d+', s)
        for i in capacity_list:
            if len(i) == 2:
                capacity = int(i)
            else:
                capacity = int(i)
    # elif 'PC2' in Title_str:
    #     Gen = 2
    elif 'PC3' in Title_str and 'SODIMM' not in Title_str and 'SO-DIMM' not in Title_str and 'ECC' not in Title_str:
        Gen = False
        speed2_str = Title_str.split('PC3-')[1]
        s = speed2_str
        speed2_list = re.findall('\d+', s)
        for i in speed2_list:
            if len(i) >= 5:
                speed = int(i) // 8
        s = Title_str.split('GB')[0]
        capacity_list = re.findall('\d+', s)
        for i in capacity_list:
            if len(i) == 2:
                capacity = int(i)
            else:
                capacity = (i)

    elif 'PC4' in Title_str and 'SODIMM' not in Title_str and 'SO-DIMM' not in Title_str and 'ECC' not in Title_str:
        Gen = True
        speed2_str = Title_str.split('PC4-')[1]
        s = speed2_str
        speed2_list = re.findall('\d+', s)
        for i in speed2_list:
            if len(i) >= 5:
                speed = int(i) // 8
        s = Title_str.split('GB')[0]
        capacity_list = re.findall('\d+', s)
        for i in capacity_list:
            if len(i) == 2:
                capacity = int(i)
            else:
                capacity = int(i)

    else:
        Gen = 'N/A'
        capacity = 'N/A'

    if 'MHz' in Title_str:
        speed_str = Title_str.split('Mhz')[0]
        s = speed_str
        speed_list = re.findall('\d+', s)
        for i in speed_list:
            if len(i) >= 4:
                speed = str(i)
    if Gen == True or Gen == False:
        Output_line.append(str(Gen))
        Output_line.append(str(speed))
        Output_line.append(str(capacity))

        Output_line = ':'.join(map(str, Output_line))

        print(Output_line)

