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

    if 'Fan Holder' in Title_str:
        continue
    elif 'Retention Bracket' in Title_str:
        continue
    elif 'Thermal Solution' in Title_str:
        continue

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
    outHeight = 'N/A'
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

        # getting non water cooler heights
        if '<h3>Specifications</h3>' in the_page:
            heightParse = the_page.split('<h3>Specifications</h3>')[1]
            heightParse = heightParse.split('</table>')[0]
            heightParseList = heightParse.split('<th>')
            heights = []
            for item in heightParseList:
                if 'mm' in item and 'mm-H2O' not in item:
                    item = item.split('</td>')[0]
                    if 'Diameter' in item:
                        continue
                    if 'Heat Pipe Dimensions' in item:
                        continue
                    if 'Dimension' not in item:
                        continue
                    if ' (H) mm' in item:
                        heightMM = item.split(' (H) mm')[0]
                    elif '(H) mm' in item:
                        heightMM = item.split('(H) mm')[0]
                    elif 'L mm' in item:
                        heightMM = item.split('L mm')[0]
                        heightMM = heightMM.split('<td>')[1]
                        heightMM = heightMM.split('H*')[0]
                        heightMM = float(heightMM)
                        heights.append(heightMM)
                        continue

                    elif ' mm' in item:
                        heightMM = item.split(' mm')[0]
                    elif ' H mm' in item:
                        heightMM = item.split(' H mm')[0]
                    elif ' mm (packaging)' in item:
                        heightMM = item.split(' mm (packaging)')[0]
                    else:
                        heightMM = item.split('mm')[0]

                    heightMM = heightMM.split(' ')
                    try:
                        heightMM = float(heightMM[len(heightMM)-1])
                    except:
                        heightMM = float(heightMM[len(heightMM)-2])
                    heights.append(heightMM)
            largestHeight = 0
            for height in heights:
                if height > largestHeight:
                    largestHeight = height
            outHeight = str(largestHeight)
        else:
            if '>Specifications</h3>' in the_page:
                heightParse = the_page.split('>Specifications</h3>')[1]
                heightParse = heightParse.split('</table>')[0]
                heightParseList = heightParse.split('<tr')
                heights = []
                for item in heightParseList:
                    if 'mm' in item and 'mm-H2O' not in item:
                        item = item.split('</tr>')[0]
                        if 'Diameter' in item:
                            continue
                        if 'Dimension' not in item:
                            continue
                        if ' (H) mm' in item:
                            heightMM = item.split(' (H) mm')[0]
                        elif '(H) mm' in item:
                            heightMM = item.split('(H) mm')[0]
                        elif ' H mm' in item:
                            heightMM = item.split(' H mm')[0]
                        elif ' mm (packaging)' in item:
                            heightMM = item.split(' mm (packaging)')[0]
                        elif ' mm' in item:
                            heightMM = item.split(' mm')[0]
                        else:
                            heightMM = item.split('mm')[0]
                        heightMM = heightMM.split('">')
                        heightMM = heightMM[len(heightMM)-1]
                        heightMM = heightMM.split(' ')
                        try:
                            heightMM = float(heightMM[len(heightMM)-1])
                        except:
                            heightMM = float(heightMM[len(heightMM)-2])
                        heights.append(heightMM)
                largestHeight = 0
                for height in heights:
                    if height > largestHeight:
                        largestHeight = height
                outHeight = str(largestHeight)


    outString = outString + ':' + str(TDP) + ':' + outHeight
        # printing non water coolers
    print(outString)