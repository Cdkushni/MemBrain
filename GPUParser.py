import urllib.request
import re


req = urllib.request.Request('http://www.videocardbenchmark.net/gpu_list.php')
with urllib.request.urlopen(req) as response:
    the_page = response.read()
lines = str(the_page)

GPUs = lines.split('<TBODY>')
newFile2 = open('GPUSpecs.txt', 'w')
GPUNmStrt = GPUs[1].split('<TD><A HREF=')
GPUNmStrt.pop(0)
for line in GPUNmStrt:
    gpuStr = line.split('">')
    gpuStr = gpuStr[1].split('</A>')
    gpuStrTemp = gpuStr[1].split('<TD>')
    gpuStrTemp = gpuStrTemp[1].split('</TD>')
    print(gpuStr[0] + ':' + gpuStrTemp[0], file=newFile2)

newFile2.close()

newFile3 = open('database.txt', 'r')
lines2 = newFile3.read()
GPUs = lines2.split('VideoCards!')
GPUs = GPUs[1].split('CoolingCPU!')
GPUs = GPUs[0]
GPUs = GPUs.splitlines()
GPUs.pop(0)
newFile3.close()

newFile5 = open('GPUSpecs.txt', 'r')
dict = {}
GPUSpecs = newFile5.read().splitlines()
for GPUSpec in GPUSpecs:
    splitDict = GPUSpec.split(':')
    key = splitDict[0]
    value = splitDict[1]
    dict[key] = value

for GPU in GPUs:
    GPUName = GPU.split(':')
    GPUName = GPUName[2]
    #GPUName = GPUName[1:]
    GPURank = 'N/A'
    try:
        GBIndex = GPUName.index('GB')
        GPUName = GPUName[0:GBIndex - 2]
        GPUSplit = GPUName.split(' ')
        if GPUSplit[0] != 'GeForce' and GPUSplit[0] != 'Radeon' and GPUSplit[0] != 'Quadro':
            if GPUSplit[1] == 'GeForce':
                matcher = re.match(r"([a-z]+)([0-9]+)", GPUSplit[2], re.I)
                if matcher:
                    items = matcher.groups()
                    GPUName = GPUSplit[1] + ' ' + items[0] + ' ' + items[1]
                else:
                    GPUName = GPUSplit[1] + ' ' + GPUSplit[2]
            elif GPUSplit[0] == 'FirePro':
                GPUName = GPUSplit[0] + ' ' + GPUSplit[1]
            elif GPUSplit[3] == 'Radeon':
                GPUName = GPUSplit[3] + ' ' + GPUSplit[4] + ' ' + GPUSplit[5]
            elif GPUSplit[6] == 'Radeon':
                GPUName = GPUSplit[6] + ' ' + GPUSplit[7] + ' ' + GPUSplit[8]
            elif GPUSplit[7] == 'Radeon':
                GPUName = GPUSplit[7] + ' ' + GPUSplit[8] + ' ' + GPUSplit[9]
            else:
                pass

        elif (GPUSplit[0] == 'GeForce'):
            try:
                int(GPUSplit[1])
                pass
            except:
                if GPUSplit[1] != 'GT' and GPUSplit[1] != 'GTX':
                    matcher = re.match(r"([a-z]+)([0-9]+)", GPUSplit[1], re.I)
                    if matcher:
                        items = matcher.groups()
                        GPUName = GPUSplit[0] + ' ' + items[0] + ' ' + items[1]
                    else:
                        GPUName = GPUSplit[0] + ' ' + GPUSplit[1]
                else:
                    GPUName = GPUSplit[0] + ' ' + GPUSplit[1] + ' ' + GPUSplit[2]
            if GPUSplit[1] == 'GTX':
                try:
                    int(GPUSplit[2])
                    pass
                except:
                    if GPUSplit[2] == '1050Ti':
                        GPUName = GPUSplit[0] + ' ' + GPUSplit[1] + ' 1050 Ti'

        elif (GPUSplit[0] == 'Radeon'):
            if GPUSplit[1] == 'R6450':
                GPUName = 'Radeon HD 6450'
            else:
                try:
                    int(GPUSplit[2])
                    GPUName = GPUSplit[0] + ' ' + GPUSplit[1] + ' ' + GPUSplit[2]
                    pass
                except:
                    if GPUSplit[1] != 'RX' and GPUSplit[1] != 'HD' and GPUSplit[1] != 'R7':
                        matcher = re.match(r"([a-z]+)([0-9]+)", GPUSplit[1], re.I)
                        if matcher:
                            items = matcher.groups()
                            GPUName = GPUSplit[0] + ' ' + items[0] + ' ' + items[1]
                        else:
                            GPUName = GPUSplit[0] + ' ' + GPUSplit[1]
                    else:
                        GPUName = GPUSplit[0] + ' ' + GPUSplit[1] + ' ' + GPUSplit[2]
        for key in dict:
            if GPUName in key:
                GPURank = dict[GPUName]
                break
    except:
        continue

    MXName = GPU.split(':')[0]
    Price = GPU.split(':')[1]
    GBFinder = GPU.split(':')[2]
    GBFinder = GBFinder.split('GB')[0]
    GBFinder = GBFinder[len(GBFinder)-1]
    GPUName2 = GPU.split(':')[2]

    base_address = 'http://www.memoryexpress.com/Products/'

    page = base_address + MXName
    with urllib.request.urlopen(page) as response:
        the_page = response.read()
    gpuPowerLines = str(the_page)

    if '<h3>System Requirements</h3>' in gpuPowerLines:
        gpuSysReq = gpuPowerLines.split('<h3>System Requirements</h3>')[1]
        gpuPower1 = gpuSysReq.split('</ul>')[0]
        gpuPower = gpuSysReq.split('</ul>')[0]

        try:
            if 'Minimum' in gpuPower:
                gpuPower = gpuPower.split('Minimum')
                tempPower = tempPower.split('</li>')[0]
                tempPower = tempPower.split('W')[0]
                gpuPower = re.findall('\d+',tempPower)[0]
            else:
                gpuPower = re.findall('\d+',gpuPower1)
                found = False
                for i in gpuPower:
                    if len(i) == 3:
                        gpuPower = i
                        found = True
                        break
                if found == False:
                    gpuPower = '300'
        except:
            gpuPower = re.findall('\d+',gpuPower1)
            found = False
            for i in gpuPower:
                if len(i) == 3:
                    gpuPower = i
                    found = True
                    break
            if found == False:
                gpuPower = '300'
    else:
        gpuPower = '300'


    print(MXName + ':' + GPUName2 + ':' + Price + ':' + GBFinder + ':' + GPURank + ':' + gpuPower)


