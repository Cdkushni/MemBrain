import urllib.request

# http://www.memoryexpress.com/Products/MX60351
base_address = 'http://www.memoryexpress.com/Products/'

# just the harddrive lines
newFile = open('database.txt', 'r')
lines = newFile.read()
Cases = lines.split('ComputerCases!')
Cases = Cases[1].split('ControllerCards!')
Cases = Cases[0]
Cases = Cases.splitlines()
Cases.pop(0)
newFile.close()

# now do a for loop for each Cases's mx number to access their website and get details
for Case in Cases:
    page = base_address + Case.split(':')[0]
    with urllib.request.urlopen(page) as response:
        the_page = response.read()
    the_page = str(the_page, 'utf-8')
    MXNumber = Case.split(':')[0]
    Title = Case.split(':')[2]
    Price = Case.split(':')[1]

    #parse colour from title
    Colour = ''
    ColourTemp = Title
    if 'Green' in ColourTemp:
        Colour = 'Green'
    elif 'Grey' in ColourTemp:
        Colour = 'Grey'
    elif 'Orange' in ColourTemp:
        Colour = 'Orange'
    elif 'Red' in ColourTemp:
        Colour = 'Red'
    elif 'Silver' in ColourTemp:
        Colour = 'Silver'
    elif 'White' in ColourTemp:
        Colour = 'White'
    else:
        Colour = 'Black'

    if '<table class="Specifications">' not in the_page:
        outForm = 'ATX mATX mITX'
        print(MXNumber + ':' + Price + ':' + Title + ':' + outForm + ':' + Colour)
        continue
    Specs = the_page.split('<table class="Specifications">')[1]
    FormFactor = Specs.split('<th>Expansion Slots</th>')[0]
    if 'Motherboard' not in FormFactor:
        outForm = 'ATX mATX mITX'
        print(MXNumber + ':' + Price + ':' + Title + ':' + outForm + ':' + Colour)
        continue
    FormFactor = FormFactor.split('Motherboard')[1]
    EATX = 0
    XLATX = 0
    ATX = 0
    mATX = 0
    mITX = 0
    if 'Micro ATX' in FormFactor:
        mATX = 1
        mITX = 1
    elif 'ITX' in FormFactor:
        mITX = 1
    elif 'XLATX' in FormFactor:
        XLATX = 1
        ATX = 1
        mATX = 1
        mITX = 1
    elif 'EATX' in FormFactor:
        EATX = 1
        XLATX = 1
        ATX = 1
        mATX = 1
        mITX = 1
    else:
        ATX = 1
        mATX = 1
        mITX = 1
    outForm = ''
    if EATX == 1:
        outForm = 'EATX XLATX ATX mATX mITX'
    elif XLATX == 1:
        outForm = 'XLATX ATX mATX mITX'
    elif ATX == 1:
        outForm = 'ATX mATX mITX'
    elif mATX == 1:
        outForm = 'mATX mITX'
    else:
        outForm = 'mITX'
    print(MXNumber + ':' + Price + ':' + Title + ':' + outForm + ':' + Colour)
