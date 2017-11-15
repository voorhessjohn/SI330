import csv
from collections import defaultdict

# Homework 2
# SI330 Fall 2017 Dr. Teplovs
# John Voorhess
# 29 September 2017
# voor@umich.edu

# FOR OUTPUT FILE
# HEADERS
# Region,Country Name,Mobile users per capita,Population,Year,Migration: Top 3 destinations,Migration: Top 3 sources
# Region - world_bank_regions.txt (done)
# Country Name - migration_outflow_graph
# Mobile users per capita - world_bank_country_data.txt (mobile phones subscribers / population count) (done)
# Population - world_bank_country_data.txt (done)
# Year - 2000
# Migration: Top 3 Destinations - migration_outflow_graph
# Migration: Top 3 sources

#filename   : name of the migration csv file
#source_column : name of the column holding the source/from value
#dest_column : name of the column holding the destination/to value
#weight_column  : name of column holding the weight (population)

##########################
#Problem 1
##########################
def filter_world_bank_country_data(filename):
    with open(filename, 'r', newline = '') as input_file:
        world_bank_reader = csv.DictReader(input_file, delimiter='\t', quotechar = '"')
        with open('worldBankFiltered.csv','w') as output_file:
            world_bank_filtered_writer = csv.DictWriter(output_file,fieldnames=['Country Name','Business: Mobile phone subscribers','Population: Total (count)'],
                                                extrasaction='ignore',
                                                delimiter='\t',
                                                quotechar='"')
            world_bank_filtered_writer.writeheader()

            for row in world_bank_reader:
                if row['Date'].endswith("2000"):
                    world_bank_filtered_writer.writerow(row)

###############
# PROBLEM 5A
###############
def create_nodes_file(filename, dict):
    nodeDict = dict
    with open(filename, 'r', newline='') as input_file:
        location_reader = csv.DictReader(input_file, delimiter=',', quotechar = '"')
        with open('si330-hw2-nodes-voor.csv','w') as output_file:
            nodes_writer = csv.DictWriter(output_file,fieldnames=['country','latitude','longitude'],
                                                extrasaction='ignore',
                                                delimiter=',',
                                                quotechar='"')
            nodes_writer.writeheader()

            for row in location_reader:
                country = row['Country Name']
                if country in nodeDict:
                    lat = row['Latitude']
                    long = row['Longitude']
                    row['country'] = country
                    row['latitude'] = lat
                    row['longitude'] = long
                    nodes_writer.writerow(row)

#create dictionary of world bank data for reference
def read_world_bank_country_data(filename):
    worldBankDict = {}
    with open(filename, 'r', newline = '') as input_file:
        world_bank_reader = csv.DictReader(input_file, delimiter='\t', quotechar = '"')
        for row in world_bank_reader:
            if row['Business: Mobile phone subscribers'] == '':
                mobilePhone = '0'
            else:
                mobilePhone = row['Business: Mobile phone subscribers']
            if row['Population: Total (count)'] == '':
                population = '0'
            else:
                population = row['Population: Total (count)']

            mobilePhoneInt = int(mobilePhone.replace(',', ''))
            populationInt = int(population.replace(',', ''))
            mobilePhonesPerCapita = mobilePhoneInt/populationInt
            worldBankDict[row['Country Name']] = [population, mobilePhonesPerCapita]
        return worldBankDict

#create lat and long dictionary for refrence
def location_dict(filename):
    latLongDict = {}
    with open(filename, 'r', newline = '') as input_file:
        location_file_reader = csv.DictReader(input_file, delimiter=',', quotechar = '"')
        for row in location_file_reader:
            latLongDict[row['Country Name']] = (row['Latitude'],row['Longitude'])
        return latLongDict

#create dictionary of regions for reference
def read_regions(filename):
    regionDict = {}
    with open(filename, 'r', newline = '') as input_file:
        region_file_reader = csv.DictReader(input_file, delimiter='\t', quotechar = '"')
        for row in region_file_reader:
            regionDict[row['Country']] = row['Region']
        return regionDict

#sort the edges file by year 2000 migration number, descending
def sort_edges_file(filename):
    #https://stackoverflow.com/questions/15559812/sorting-by-specific-column-data-using-csv-in-python
    reader = csv.DictReader(open(filename, 'r'))
    result = sorted(reader, key=lambda d: float(d['count']), reverse=True)

    writer = csv.DictWriter(open('si330-hw2-edges-voor-all.csv', 'w'), reader.fieldnames)
    writer.writeheader()
    writer.writerows(result)

##3 Sort world bank migration csv
#I couldn't get this sort to work
def sort_csv(filename):
    reader = csv.DictReader(open(filename, 'r'))

    for row in reader:
        if row['2000 [2000]'] == '':
            row['2000 [2000]'] = 0
        elif row['2000 [2000]'] == '..':
            row['2000 [2000]'] = 0


    result = sorted(reader, key=lambda d: int(d['2000 [2000]']), reverse=True)


    writer = csv.DictWriter(open('sortedMigration.csv', 'w'), reader.fieldnames)
    writer.writeheader()
    writer.writerows(result)

#limit the number of rows to the top 1000
def cut_edges_result(filename):
    rowDict = {}
    with open(filename, 'r', newline='') as input_file:
        reader = csv.DictReader(input_file, delimiter=',', quotechar = '"')
        with open('si330-hw2-edges-voor.csv', 'w') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=['start_country', 'end_country', 'start_lat', 'start_long', 'end_lat', 'end_long', 'count'],
                                        extrasaction='ignore',
                                        delimiter=',',
                                        quotechar='"')
            writer.writeheader()
            count = 0
            for row in reader:
                if count <= 1000:
                    writer.writerow(row)
                    count += 1
                else:
                    pass




##############
# PROBLEM 2
###############
def read_directed_graph_from_csv(filename, source_column, dest_column, weight_column):
    graph = defaultdict(list)
    with open(filename, 'r', newline = '') as input_file:
        graph_file_reader = csv.DictReader(input_file, delimiter=',', quotechar = '"')
        for row in graph_file_reader:
            weight = row[weight_column]
            if (weight == '' or weight == '..'):
                weight = 0.0
            else:
                weight = float(weight)
            edge = (row[dest_column], weight)
            if row[source_column] not in graph:
                edges = []
                edges.append(edge)
                #edges = sorted(edges, key=lambda x: x[1])
                graph[row[source_column]] = edges

            else:
                edges.append(edge)
                #edges = sorted(edges, key=lambda x: x[1])
                graph[row[source_column]] = edges

                ###########################################################
                # 3. Sort outgoing edges by descending migration population
                # This worked a couple of times at 5+ minutes, but then it
                # started taking so long that I had to abandon it.
                ###########################################################
                # sorted([('abc', 121),('abc', 231),('abc', 148), ('abc',221)], key=lambda x: x[1])
                # https://stackoverflow.com/questions/10695139/sort-a-list-of-tuples-by-2nd-item-integer-value
                # this sort takes an obnoxious amount of time, but it works so I'm not going to fix it yet
                # for country in graph:
                #     edgelist = graph[country]
                #     sortedEdgeList = sorted(edgelist, key=lambda x: x[1], reverse=True)
                #     graph[country] = sortedEdgeList


    return(graph)





def main():
    sort_csv("world_bank_migration.csv")
    latLongDict = location_dict("locations.csv")
    filter_world_bank_country_data("world_bank_country_data.txt")
    worldBankDict = read_world_bank_country_data("worldBankFiltered.csv")

    regionDict = read_regions("world_bank_regions.txt")
    migration_inflow_graph = read_directed_graph_from_csv("world_bank_migration.csv","Country Dest Name", "Country Origin Name", "2000 [2000]")

    migration_outflow_graph = read_directed_graph_from_csv("world_bank_migration.csv","Country Origin Name", "Country Dest Name", "2000 [2000]")
    create_nodes_file('locations.csv', migration_outflow_graph)

    #create world bank output file
    with open('worldBankFiltered.csv','r') as input_file:
        migration_record_reader = csv.DictReader(input_file, delimiter = "\t")

        with open('world-bank-output-hw2-voor.csv','w') as output_file:
            migration_record_writer = csv.DictWriter(output_file,fieldnames=['Region','Country Name','Mobile users per capita','Population','Year','Migration: Top 3 destinations','Migration: Top 3 sources'],
                                                extrasaction='ignore',
                                                delimiter=',',
                                                quotechar='"')
            migration_record_writer.writeheader()

            for row in migration_record_reader:
                countryName = row['Country Name']

                if countryName in worldBankDict:
                    row['Mobile users per capita'] = worldBankDict[countryName][1]
                    row['Population'] = worldBankDict[countryName][0]
                else:
                    row['Mobile users per capita'] = 0
                    row['Population'] = 0

                if countryName in regionDict:
                    row['Region'] = regionDict[countryName]
                else:
                    row['Region'] = "NA"

                row['Year'] = 2000

                if countryName in migration_outflow_graph:
                    row['Migration: Top 3 destinations'] = migration_outflow_graph[countryName][0:3]
                else:
                    row['Migration: Top 3 destinations'] = "unknown"

                if countryName in migration_inflow_graph:
                    row['Migration: Top 3 sources'] = migration_inflow_graph[countryName][0:3]
                else:
                    row['Migration: Top 3 sources'] = "unknown"

                migration_record_writer.writerow(row)
    #create edges file
    with open('si330-hw2-nodes-voor.csv', 'r', newline='') as input_file:
        node_reader = csv.DictReader(input_file, delimiter=',', quotechar = '"')
        with open('unsortedEdges.csv', 'w') as output_file:
            edge_writer = csv.DictWriter(output_file, fieldnames=['start_country', 'end_country', 'start_lat', 'start_long', 'end_lat', 'end_long', 'count'],
                                        extrasaction='ignore',
                                        delimiter=',',
                                        quotechar='"')
            edge_writer.writeheader()
            #Check the migration outflow dict against the lat long dict
            for country in migration_outflow_graph:
                for j,k in migration_outflow_graph[country]:
                    row['start_country'] = country
                    row['end_country'] = j
                    row['count'] = k
                    if country in latLongDict:
                        row['start_lat'] = latLongDict[country][0]
                        row['start_long'] = latLongDict[country][1]
                    else:
                        row['start_lat'] = 0
                        row['start_long'] = 0
                        #print(country + " not in latLongDict")
                    if j in latLongDict:
                        row['end_lat'] = latLongDict[j][0]
                        row['end_long'] = latLongDict[j][1]
                    else:
                        row['end_lat'] = 0
                        row['end_long'] = 0
                        #print(j + " not in latLongDict")


                    edge_writer.writerow(row)

    sort_edges_file("unsortedEdges.csv")
    cut_edges_result("si330-hw2-edges-voor-all.csv")

if __name__ == '__main__':
    main()