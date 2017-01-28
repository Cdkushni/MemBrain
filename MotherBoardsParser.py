import urllib.request, re

base_address = 'http://www.memoryexpress.com/Products/'


newFile = open('database.txt', 'r')
lines = newFile.read()
MOBOs = lines.split('Motherboards!')
MOBOs = MOBOs[1].split('Memory!')
MOBOs = MOBOs[0]
MOBOs = MOBOs.splitlines()
MOBOs.pop(0)
newFile.close()

for MOBO in MOBOs:
    page = base_address + MOBO.split(':')[0]
    with urllib.request.urlopen(page) as response:
        the_page = response.read()
    the_page = str(the_page, 'utf-8')

    new1 = the_page.split('<table class="Specifications">')
    # Form Factor
    new3 = new1[1].split('</table>')[0]
    if '<th>Form Factor</th>' in new3:
        new3 = new3.split('<th>Form Factor</th>')[1]
        new3 = new3.split('Form Factor')
        try:
            if 'EATX' in new3[0]:
                new3 = 'EATX'
            elif 'EATX' in new3[1]:
                new3 = 'EATX'
            elif 'XLATX' in new3[0]:
                new3 = 'XLATX'
            elif 'XLATX' in new3[1]:
                new3 = 'XLATX'
            elif 'Micro ATX' in new3[0]:
                new3 = 'MATX'
            elif 'Micro ATX' in new3[1]:
                new3 = 'MATX'
            elif 'mATX' in new3[0]:
                new3 = 'mATX'
            elif 'mATX' in new3[1]:
                new3 = 'mATX'
            elif 'mITX' in new3[0]:
                new3 = 'mITX'
            elif 'mITX' in new3[1]:
                new3 = 'mITX'
            elif 'Mini-ITX' in new3[0]:
                new3 = 'mITX'
            elif 'Mini-ITX' in new3[1]:
                new3 = 'mITX'
            elif 'mini ITX' in new3[0]:
                new3 = 'mITX'
            elif 'mini ITX' in new3[1]:
                new3 = 'mITX'
            elif 'Mini ITX' in new3[0]:
                new3 = 'mITX'
            elif 'Mini ITX' in new3[1]:
                new3 = 'mITX'
            elif 'ATX' in new3[0]:
                new3 = 'ATX'
            elif 'ATX' in new3[1]:
                new3 = 'ATX'
            else:
                new3 = 'ATX'
        except:
            if 'Motherboard' in new3[0]:
                new3 = new3[0].split(' Motherboard')[0]
                new3 = new3.split('<td>')[1]
            elif '<th>Dimensions (LxW)</th>' in new3[0]:
                new3 = new3[0].split('<th>Dimensions (LxW)</th>')[1]
                if 'Form Factor' in new3[0]:
                    new3 = new3[0].split('Form Factor')[0]
                    new3 = new3.split('<td>')[1]
                elif 'ATX' in new3[0]:
                    new3 = new3[0].split('</td>')[0]
                    new3 = new3.split(' ')[0]
                    new3 = new3.split('<td>')[1]
                else:
                    if '12 inch x 9.6 inch' in new3[0]:
                        new3 = 'ATX'
                    elif '9.6 inch x 9.6 inch' in new3[0]:
                        new3 = 'MATX'
                    elif '5.6 inch x 5.6 inch' in new3[0]:
                        new3 = 'mATX'
                    elif '6.7 inch x 6.7 inch' in new3[0]:
                        new3 = 'mITX'
                    elif '12 inch x 13 inch' in new3[0]:
                        new3 = 'EATX'
                    elif '13.5 inch x 10.3 inch' in new3[0]:
                        new3 = 'XLATX'
                    elif '13.6 inch x 10.3 inch' in new3[0]:
                        new3 = 'XLATX'
                    elif '12.8 inch x 10.0 inch' in new3[0]:
                        new3 = 'XLATX'
                    elif '12.8 inch x 9.6 inch' in new3[0]:
                        new3 = 'XLATX'
                    elif '13.6 inch x 10.4 inch' in new3[0]:
                        new3 = 'XLATX'
                    elif '170 x 170mm' in new3[0]:
                        new3 = 'mITX'
                    elif '12 x 9.6 inch' in new3[0]:
                        new3 = 'ATX'
                    elif '9.6 x 9.6 inch' in new3[0]:
                        new3 = 'MATX'
                    elif '5.6 x 5.6 inch' in new3[0]:
                        new3 = 'mATX'
                    elif '6.7h x 6.7 inch' in new3[0]:
                        new3 = 'mITX'
                    elif '12 x 13 inch' in new3[0]:
                        new3 = 'EATX'
                    elif '13.5 x 10.3 inch' in new3[0]:
                        new3 = 'XLATX'
                    elif '13.6 x 10.3 inch' in new3[0]:
                        new3 = 'XLATX'
                    elif '12.8 x 10.0 inch' in new3[0]:
                        new3 = 'XLATX'
                    elif '12.8 x 9.6 inch' in new3[0]:
                        new3 = 'XLATX'
                    elif '13.6 x 10.4 inch' in new3[0]:
                        new3 = 'XLATX'
                    elif '170mm x 170mm' in new3[0]:
                        new3 = 'mITX'
                    else:
                        new3 = 'ATX'
    elif '<th>Dimensions (LxW)</th>' in new3:
        new3 = new3.split('<th>Dimensions (LxW)</th>')[1]
        if 'Form Factor' in new3:
            new3 = new3.split('Form Factor')[0]
            new3 = new3.split('<td>')[1]
        elif 'ATX' in new3:
            new3 = new3.split('</td>')[0]
            new3 = new3.split(' ')[0]
            new3 = new3.split('<td>')[1]
        else:
            if '12 inch x 9.6 inch' in new3:
                new3 = 'ATX'
            elif '9.6 inch x 9.6 inch' in new3:
                new3 = 'MATX'
            elif '5.6 inch x 5.6 inch' in new3:
                new3 = 'mATX'
            elif '6.7 inch x 6.7 inch' in new3:
                new3 = 'mITX'
            elif '12 inch x 13 inch' in new3:
                new3 = 'EATX'
            elif '13.5 inch x 10.3 inch' in new3:
                new3 = 'XLATX'
            elif '13.6 inch x 10.3 inch' in new3:
                new3 = 'XLATX'
            elif '12.8 inch x 10.0 inch' in new3:
                new3 = 'XLATX'
            elif '12.8 inch x 9.6 inch' in new3:
                new3 = 'XLATX'
            elif '13.6 inch x 10.4 inch' in new3:
                new3 = 'XLATX'
            elif '170 x 170mm' in new3:
                new3 = 'mITX'
            elif '12 x 9.6 inch' in new3:
                new3 = 'ATX'
            elif '9.6 x 9.6 inch' in new3:
                new3 = 'MATX'
            elif '5.6 x 5.6 inch' in new3:
                new3 = 'mATX'
            elif '6.7h x 6.7 inch' in new3:
                new3 = 'mITX'
            elif '12 x 13 inch' in new3:
                new3 = 'EATX'
            elif '13.5 x 10.3 inch' in new3:
                new3 = 'XLATX'
            elif '13.6 x 10.3 inch' in new3:
                new3 = 'XLATX'
            elif '12.8 x 10.0 inch' in new3:
                new3 = 'XLATX'
            elif '12.8 x 9.6 inch' in new3:
                new3 = 'XLATX'
            elif '13.6 x 10.4 inch' in new3:
                new3 = 'XLATX'
            elif '170mm x 170mm' in new3:
                new3 = 'mITX'
            else:
                new3 = 'ATX'

    elif 'Form Factor' in new3:
        new3 = new3.split('Form Factor')
        if 'EATX' in new3[0]:
            new3 = 'EATX'
        elif 'EATX' in new3[1]:
            new3 = 'EATX'
        elif 'XLATX' in new3[0]:
            new3 = 'XLATX'
        elif 'XLATX' in new3[1]:
            new3 = 'XLATX'
        elif 'Micro ATX' in new3[0]:
            new3 = 'MATX'
        elif 'Micro ATX' in new3[1]:
            new3 = 'MATX'
        elif 'mATX' in new3[0]:
            new3 = 'mATX'
        elif 'mATX' in new3[1]:
            new3 = 'mATX'
        elif 'mITX' in new3[0]:
            new3 = 'mITX'
        elif 'mITX' in new3[1]:
            new3 = 'mITX'
        elif 'Mini-ITX' in new3[0]:
            new3 = 'mITX'
        elif 'Mini-ITX' in new3[1]:
            new3 = 'mITX'
        elif 'mini ITX' in new3[0]:
            new3 = 'mITX'
        elif 'mini ITX' in new3[1]:
            new3 = 'mITX'
        elif 'Mini ITX' in new3[0]:
            new3 = 'mITX'
        elif 'Mini ITX' in new3[1]:
            new3 = 'mITX'
        elif 'ATX' in new3[0]:
            new3 = 'ATX'
        elif 'ATX' in new3[1]:
            new3 = 'ATX'
        else:
            new3 = 'ATX'
        new3 = new3.split(' ')
    try:
        if 'Mini-ITX' in new3[0]:
            new3 = 'mITX'
        elif 'Extended ATX' in new3[0]:
            new3 = 'ATX'
    except:
        pass
    if new3 == 'E-ATX':
        new3 = 'EATX'

    ## MXID
    MXNum = MOBO.split(':')[0]
    Price = MOBO.split(':')[1]
    Title = MOBO.split(':')[2]
    # # Memory slots
    new2 = new1[1].split('</table>')[0]
    new2 = new2.split('<th>Memory</th>')[1]
    new2 = new2.split('<td>')[1]
    MemSlots = re.search(r'\d+', new2).group()

    # # Socket
    # LGA number or number LGA or Socket Number or Number Socket
    # Find AMD AM1, AMD AM3+, AMD FM2+

    new4 = new1[1].split('</table>')[0]
    brandSock = new4
    new4 = new4.split('Socket')
    if 'AMD' in brandSock:
        try:
            if 'AM1' in new4[0]:
                socket = 'AM1'
            elif 'AM3+' in new4[0]:
                socket = 'AM3+'
            elif 'FM2+' in new4[0]:
                socket = 'FM2+'
            elif 'AM1' in new4[1]:
                socket = 'AM1'
            elif 'AM3+' in new4[1]:
                socket = 'AM3+'
            elif 'FM2+' in new4[1]:
                socket = 'FM2+'
            elif 'LGA 1151' in brandSock:
                socket = 'LGA1151'
        except:
            if 'SkyLake Processors for LGA 1151' in brandSock:
                socket = 'LGA1151'
            else:
                socket = 'N/A'
    else:
        if 'LGA' in brandSock:
            socket = brandSock.split('LGA')[1]
            socket = socket.split(' ')
            if socket[0] == '':
                socket = socket[1]
            else:
                socket = socket[0]
            socket = 'LGA' + socket
            socket = socket.split('</td>')[0]
        else:
            top = new4[0].split(' ')
            bottom = new4[1].split(' ')
            bottom.pop(0)
            try:
                socketNum = re.search(r'\d+',top[len(top)-1]).group()
            except:
                socketNum = re.search(r'\d+',bottom[0]).group()
            socket = socketNum



    FormFactor = new3.strip()
    print(MXNum + ':' + Price + ':' + FormFactor + ':' + MemSlots +':' + socket)




# form_factor_strs = ['Form Factor','Dimensions (LxW)']
# for i in form_factor_strs:
#     try:
#         new3.index(i)
#         new3.split('<th>' + str(i) + '</th>')[1]
#     except ValueError:
#         pass
# new3 = new3.split('</td>')[0]
# new3 = new3.split('<td>')[1]


#


# # Sata ports
# new5 = new1[1].split('</table>')[0]
# sata_strs = ['Internal I/O Ports', 'Internal I/O Connectors']`
# for i in sata_strs:
#     try:
#         new5.index(i)
#         new5.split(str(i))[1]
#     except ValueError:
#         pass
# # new5 = new5.split('SATA')[0]
# # new5 = new5[-3:].replace(' ', '').replace('x', '')
#
# # Integrated Graphics
# new6 = new1[1].split('</table>')[0]
# new6 = new6.split('<th>Integrated Graphics</th>')[1]
# new6 = new6.split('</td>')[0]
# new6 = new6.split('<td>')[1]

# print(new6)
# print(new5)
# print(new3)
# print(new2)
