import urllib.request



req = urllib.request.Request('https://www.cpubenchmark.net/CPU_mega_page.html')
with urllib.request.urlopen(req) as response:
    the_page = response.read()
lines = str(the_page)

CPUs = lines.split('<tbody>')
newFile2 = open('CPUSpecs.txt', 'w')
CPUNmStrt = CPUs[1].split('<a href="cpu_lookup.php?cpu=')
CPUNmStrt.pop(0)
for line in CPUNmStrt:
    cpuStr = line.split('</td>')
    cpuStr1 = cpuStr[0].split('">')
    cpuStr1 = cpuStr1[1].split('</a>')
    cpuStrTemp = cpuStr[2].split('<td>')
    singleThread = cpuStr[4].split('<td>') # this line gets the single threat mark
    TDPStr = cpuStr[6].split('<td>') # this line gets the TDP
    Socket = cpuStr[9].split('<td>') # this line gets the socket
    ExAttri = line.split('<div>')
    TurboAttri = ExAttri[2].split(':')[1]
    TurboAttri = TurboAttri.split('</div>')[0]
    TurboAttri = TurboAttri[1:]
    if TurboAttri == 'Not Supported':
        TurboAttri = ExAttri[1].split(':')[1]
        TurboAttri = TurboAttri.split('</div>')[0]
        TurboAttri = TurboAttri[1:]
    CoreNum = ExAttri[3].split(':')[1]
    CoreNum = CoreNum.split('(')[0]
    CoreNum = CoreNum[1:]

    print(cpuStr1[0] + ':' + cpuStrTemp[1] + ':' + singleThread[1] + ':' + TDPStr[1] + ':' + Socket[1] + ':' + TurboAttri + ':' + CoreNum, file=newFile2)

newFile2.close()
# concatenation starts here
newFile3 = open('database.txt', 'r')
lines2 = newFile3.read()
CPUs = lines2.split('Processors!')
CPUs = CPUs[1].split('Motherboards!')
CPUs = CPUs[0]
CPUs = CPUs.splitlines()
CPUs.pop(0)
newFile3.close()

newFile5 = open('CPUSpecs.txt', 'r')
dict = {}
CPUSpecs = newFile5.read().splitlines()
for CPUSpec in CPUSpecs:
    splitDict = CPUSpec.split(':')
    key = splitDict[0]
    value = splitDict[1] + ':' + splitDict[2] + ':' + splitDict[3] + ':' + splitDict[4] + ':' + splitDict[5] + ':' + splitDict[6]
    dict[key] = value

for CPU in CPUs:
    CPUName = CPU.split(':')
    MXNumber = CPUName[0]
    Price = CPUName[1]
    CPUName = CPUName[2]
    if 'Athlon' in CPUName:
        CPUWords = CPUName.split(' ')
        titleMatcher = CPUWords[0] + ' ' + CPUWords[1]
    elif 'Pentium' in CPUName:
        CPUWords = CPUName.split(' ')
        CPUEnding = CPUWords[2].split(',')[0]
        titleMatcher = CPUWords[0] + ' ' + CPUEnding
    else:
        titleTemp = CPUName.split('-')
        titleMatcher1 = titleTemp[0].split(' ')
        titleMatcher1 = titleMatcher1[len(titleMatcher1)-1]
        titleMatcher2 = titleTemp[1].split(' ')
        titleMatcher2 = titleMatcher2[0]
        titleMatcher = titleMatcher1 + '-' + titleMatcher2

    CPUData = 'Not Found'
    for key in dict:
        if titleMatcher in key:
            CPUData = dict[key]
            break

    print(MXNumber + ':' + Price + ':' + CPUName + ':' + CPUData)

