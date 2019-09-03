## Brian Seggebruch -- 873408239 -- scraping tables from the webth

from bs4 import BeautifulSoup
import csv
import sys


def table_to_list(table_tag):
    '''Converts a html table into a list of lists'''
    
    # op = output list
    op = []
    # nest each row as a list
    for tr in table_tag.find_all('tr'):
    	op.append([str(i.string) for i in tr.find_all()])
    return op

def main():

    filenames = []
    argi = 1

    # iterating over our options and handling appropriately
    while argi < len(sys.argv):

        arg = sys.argv[argi]
        
        # if no '-' prefix, then assumed filename
        if arg[0] != '-':
            filenames.append(sys.argv[argi])
            argi += 1
        
        else:
            print(f"unrecognized argument: {arg}", file = sys.stderr)
            argi += 1

    # calling our function per file
    for file in filenames:
        with open(file) as f:
            soup = BeautifulSoup(f, features = 'html.parser')
            # calling our function per table in file
            for tb in soup.find_all('table'):
                print(f'First row: {table_to_list(tb)[0]}')
                # putting each table in a separate file named by the user
                op_filename = input('What is the name of this file?: ')
                if op_filename:
                    with open(op_filename, 'w', newline = '') as output_csv:
                        output_writer = csv.writer(output_csv)
                        for row in table_to_list(tb):
                            output_writer.writerow(row)
                else:
                    pass

if __name__ == '__main__':
    main()