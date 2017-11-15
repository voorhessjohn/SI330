import csv

reader = csv.DictReader(open("program.dept.csv"))
result = {}
for row in reader:
    key = row.pop('major')
        #if key in result:
            # implement your duplicate row handling here
            #pass
    result[key] = row
print(result)