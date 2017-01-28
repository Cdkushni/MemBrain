from lxml import html
import requests, math, urllib.request, time


def parse_category(url):
    # category path
    href = url[28:]

    # url data
    size = '?PageSize=120'
    pager = '&Page='
    price = '&Sort=Price'
    stock = '&InventoryType=InStock'

    # determine number of items per category
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        the_page = response.read()

    newFile1 = open('urlRead.txt', 'w')
    print(the_page, file=newFile1)
    newFile1.close()
    newFile = open('urlRead.txt', 'r')
    lines = newFile.read()
    newParti = lines.split('<a href="' + str(href) + '">')
    newParti = newParti[1].split('</a>', 1)
    newParti2 = newParti[1].split(')', 1)
    numPrep = newParti2[0].split('(', 1)
    items = numPrep[1]

    # calculate number of pages
    pages = math.ceil(float(items) / 120.0)

    # generate list of MXID's
    g = globals()
    m = globals()
    for i in range(1, 1 + pages):
        temp = requests.get(url + size + price + stock + pager + str(i))
        g['{}'.format('page_' + str(i))] = html.fromstring(temp.content)

    for i in range(1, 1 + pages):
        m['{}'.format('parse_' + str(i))] = g['page_' + str(i)].xpath('//div[@class="ProductId"]/text()')

    # combine page results into single list
    if pages == 1:
        final_list = parse_1
    if pages == 2:
        final_list = parse_1 + parse_2
    if pages == 3:
        final_list = parse_1 + parse_2 + parse_3

    return final_list


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


def main():
    base_address = 'http://www.memoryexpress.com/Category/'
    component_list = ['PowerSupplies', 'Processors', 'Motherboards', 'Memory', 'VideoCards', 'Cooling', 'NetworkAdapters', 'HardDrives', 'ComputerCases',
                      'ControllerCards']
    f = globals()

    for i in component_list:
        f['{}'.format(i)] = parse_category(base_address + i)
        print('Fetched Products from Category: ' + i)

    v = locals()

    print('Parsing Data...')
    # parse / write MXid's, price and titles
    for i in component_list:
        v['{}'.format(i)] = []
        for k in f[i]:
            page = requests.get('http://www.memoryexpress.com/Products/' + str(k))
            tree = html.fromstring(page.content)
            tmp = []
            tmp.append(tree.xpath('//div[@ class="PDH_HeaderBlock"]/h1/text()')[0])
            tmp.append(tree.xpath('//div[@id="ProductPricing"]/div[@class="Totals"]/div[@class="GrandTotal"]/div[1]/text()')[0][1:].replace(',', ''))
            v[i].append(tmp[1] + ':' + tmp[0])

    print('Writing output...')
    # output list to a txt file
    output_file = open('database1.txt', 'w')
    for i in component_list:
        output_file.write(i + '!' + '\n')
        for k in range(0, len(f[i])):
            output_file.write(f[i][k] + ':' + str(v[i][k]) + '\n')


start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
