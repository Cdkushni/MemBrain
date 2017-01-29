import urllib.request
import re

req = urllib.request.Request('http://www.harddrivebenchmark.net/hdd_list.php')
with urllib.request.urlopen(req) as response:
    the_page = response.read()
lines = str(the_page, 'utf-8')

Drives = lines.split('<TBODY>')
newFile2 = open('DriveSpecs.txt', 'w')
DrivesNumStrt = Drives[1].split('<A HREF="hdd_lookup.php?hdd=')
DrivesNumStrt.pop(0)
for line in DrivesNumStrt:
    driveStr = line.split('</TD>')
    driveStr1 = driveStr[0].split('">')
    driveStr1 = driveStr1[1].split('</A>')
    driveStrTemp = driveStr[1].split('<TD>')

    print(driveStr1[0] + ':' + driveStrTemp[1], file=newFile2)

newFile2.close()

base_address = 'http://www.memoryexpress.com/Products/'

# just the harddrive lines
newFile3 = open('database.txt', 'r')
lines = newFile3.read()
Drives = lines.split('HardDrives!')
Drives = Drives[1].split('ComputerCases!')
Drives = Drives[0]
Drives = Drives.splitlines()
Drives.pop(0)
newFile3.close()

# start comparing for concat
newFile5 = open('DriveSpecs.txt', 'r')
driveDict = {}
DriveSpecs = newFile5.read().splitlines()
for drive in DriveSpecs:
    splitData = drive.split(':')
    key = splitData[0]
    driveDict[key] = drive

# now start working with the actual old database.txt
oddCount = 0
for drive in Drives:
    if oddCount == 0:
        oddCount = 1
        currentPrice = drive.split(':')[1]
        continue
    else:
        oddCount = 0
        # get harddrive capacity here
        capacity = drive.split(':')[2]
        #capacity = capacity[1:]
        if 'GB' in capacity:
            capacity = capacity.split('GB')[0]
            capacity = capacity.split(' ')
            capacity = capacity[len(capacity)-1]
        elif 'TB' in capacity:
            capacity = capacity.split('TB')[0]
            capacity = capacity.split(' ')
            capacity = capacity[len(capacity)-1]
            capacity = float(capacity) * 1000
            capacity = str(capacity)
            capacity = capacity.split('.')[0]

        # do concatenation comparisons
        DriveMX = drive.split(':')[0]
        DriveInfo = drive.split(':')[1]
        DriveRPM = 'N/A'
        page = urllib.request.Request(base_address + DriveMX)
        with urllib.request.urlopen(page) as response:
            the_page = response.read()
        the_page = str(the_page, 'utf-8')
        if the_page.find('RPM</td>'):
            RPMTemp = the_page.split('<h3>Specifications</h3>')[1]
            RPMTemp = RPMTemp.split('rpm')[0]
            RPMTemp = RPMTemp.split('<td>')
            DriveRPM = RPMTemp[len(RPMTemp)-1]
            DriveRPM = re.sub("[^0-9]", "", DriveRPM)
            if len(DriveRPM) > 6:
                DriveRPM = 'N/A'


        modelNum = the_page.split('<div id="ProductAdd">')
        modelNum = modelNum[1].split('Part #:</strong> ')
        modelNum = modelNum[1].split('</li>')[0]
        try:
            modelNum = modelNum.split(sep='/')
            modelNum = modelNum[0]
        except:
            pass
        #now match the modelNum to the dictionary key
        driveData = 'N/A'
        PerformanceIndex = 'N/A'
        found = False
        for key in driveDict:
            if modelNum in key:
                driveData = driveDict[key]
                PerformanceIndex = driveDict[key].split(':')[1]
                found = True
                break
        if found == False:
            continue
        #print(modelNum + ' : ' + driveData)
        #print(DriveMX + ':' + modelNum + ':' + PerformanceIndex + ':' + currentPrice + ':' + capacity + ':' + DriveRPM)

        Title = drive.split(':')[2]
        print(DriveMX + ':' + Title + ':' + PerformanceIndex + ':' + currentPrice + ':' + capacity + ':' + DriveRPM)
