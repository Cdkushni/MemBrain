import urllib.request, re

newFile = open('database.txt', 'r')
lines = newFile.read()
COOL = lines.split('CoolingCPU!')
COOL = COOL[1].split('NetworkAdapters!')
COOL = COOL[0]
COOL = COOL.splitlines()
COOL.pop(0)
newFile.close()

base_address = 'http://www.memoryexpress.com/Products/'

for cooler in COOL:
    Title_str = cooler.split(':').pop()
    MXNum = cooler.split(':')[0]
    Price = cooler.split(':')[1]
    Output_line = cooler.split(':')

    try:
        if 'Water' in Title_str or 'Hydro' in Title_str or 'Liquid' in Title_str:
            Type = False
        else:
            Type = True
    except ValueError:
        pass

    Output_line.append(Type)
    Output_line = ':'.join(map(str, Output_line))
    outString = ''


    ##Socket parsing goes here
    page = base_address + cooler.split(':')[0]
    with urllib.request.urlopen(page) as response:
        the_page = response.read()
    the_page = str(the_page, 'utf-8')

    LGASocketOut = ''
    AMDSocketOut = ''
    AMDSockets = {'FM2', 'FM1', 'AM3+', 'AM3', 'AM2+', 'AM2', 'G34', 'C32'}
    LGASockets = {'2011-3', '2011', '1366', '1156', '1155', '1151', '1150', '775', '1974', '1207'}
    if '<h3>Specifications</h3>' in the_page:
        coolerInfo = the_page.split('<h3>Specifications</h3>')[1]
        coolerInfo = coolerInfo.split('</table>')[0]
        if 'LGA' in coolerInfo:
            LGASocketOut = 'LGA'
            socketInfoLGA = coolerInfo.split('LGA')[1]
            socketInfoLGA = socketInfoLGA.split('\n')[0]
            socketInfoLGA = socketInfoLGA.split('<br />')[0]
            for LSocket in LGASockets:
                if LSocket in the_page:
                    LGASocketOut = LGASocketOut + '|LGA' + LSocket
            for ASocket in AMDSockets:
                if ASocket in the_page:
                    AMDSocketOut = AMDSocketOut + '|' + ASocket
            outString = outString + ':' + LGASocketOut + AMDSocketOut
        else:
            if '<h3>Compatibility</h3>' in the_page:
                coolerInfo = the_page.split('<h3>Compatibility</h3>')[1]
                coolerInfo = coolerInfo.split('<h3>Specifications</h3>')[0]
                for ASocket in AMDSockets:
                    if ASocket in the_page:
                        AMDSocketOut = AMDSocketOut + '|' + ASocket
                if 'LGA' in coolerInfo:
                    LGASocketOut = 'LGA'
                    socketInfoLGA = coolerInfo.split('LGA')[1]
                    socketInfoLGA = socketInfoLGA.split('\n')[0]
                    socketInfoLGA = socketInfoLGA.split('<br />')[0]
                    for LSocket in LGASockets:
                        if LSocket in the_page:
                            LGASocketOut = LGASocketOut + '|LGA' + LSocket
                else:
                    for LSocket in LGASockets:
                        if LSocket in the_page:
                            LGASocketOut = LGASocketOut + '|LGA' + LSocket
                outString = outString + ':' + LGASocketOut + AMDSocketOut
            else:
                for ASocket in AMDSockets:
                    if ASocket in the_page:
                        AMDSocketOut = AMDSocketOut + '|' + ASocket
                for LSocket in LGASockets:
                    if LSocket in the_page:
                        LGASocketOut = LGASocketOut + '|LGA' + LSocket
                outString = outString + ':' + LGASocketOut + AMDSocketOut

    else:
        for ASocket in AMDSockets:
            if ASocket in the_page:
                AMDSocketOut = AMDSocketOut + '|' + ASocket
        for LSocket in LGASockets:
            if LSocket in the_page:
                LGASocketOut = LGASocketOut + '|LGA' + LSocket
        outString = outString + LGASocketOut + AMDSocketOut
    outString = Output_line + outString

    ## grabbing TDP
    TDP = '200'
    if Type == True:
        # not a water cooler so we can find TDP
        if 'Watt' in the_page:
            TDPParse = the_page.split('Watt')[0]
            TDPParse = TDPParse.split(' ')
            TDPParse = TDPParse[len(TDPParse)-2]
        elif '<h3>Specifications</h3>' in the_page:
            coolingParse = the_page.split('<h3>Specifications</h3>')[1]
            coolingParse = coolingParse.split('<tr>')
            for trs in coolingParse:
                if 'W</td>' in trs:
                    TDPParse = trs.split('W</td>')[0]
                    #TDPParse = re.findall('/d+',TDPParse)
                    TDPParse = TDPParse.split(' ')
                    TDPParse = TDPParse[len(TDPParse)-2]
        else:
            if 50.0 < float(Price) < 100.0:
                TDP = 100
            elif float(Price) < 50.0:
                TDP = 65
            elif float(Price) > 100.0:
                TDP = 220

    outString = outString + ':' + str(TDP)
        # printing non water coolers
    print(outString)