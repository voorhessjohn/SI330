import csv

# Homework 1
# SI330 Fall 2017 Dr. Teplovs
# John Voorhess
# 22 September 2017
# voor@umich.edu

def testcsv4(filename):
    dept_for_program = {}                                           #initialize variable to hold dictionary of majors:departments

    with open(filename,'rU') as input_file:                         #open the filename passed as parameter to this function
        program_dept_reader = csv.DictReader(input_file)            #create a reader object to iterate over

        for row in program_dept_reader:                             #iterate over the reader object and assign majors as keys and
            dept_for_program[row['major']] = row['department']      #deparments as values to the dictionary initialized on line 10

    return dept_for_program                                         #return the completed reference dictionary

def main():
    program_dept_dict = testcsv4('program.dept.csv')                #store the dictionary returned by testcsv4 function in a variable

    with open('student.record.cut.csv','r') as input_file:          #open the student file
        student_record_reader = csv.DictReader(input_file)          #create a reader object to iterate over

        with open('psych_output_voor.csv','w') as output_file:                                              #name the output file
            student_record_writer = csv.DictWriter(output_file,fieldnames=['ANONID','DEPT','HSGPA'],        #create a writer object with specified fieldnames
                                                extrasaction='ignore',                                      #writer object will ignore extra fields from the reader
                                                delimiter=',',                                              #specify delimiting character-- comma, in this case
                                                quotechar='"')                                              #specify quote character-- single instance of double quote, in this case
            student_record_writer.writeheader()                     #call writeheader method of writer class to write fieldnames as column headers
            rowcount = 0                                            #initialize variable to count rows written
            GPA_Accum = 0.0                                         #initialize variable to add up GPAs
            student_count = 0                                       #initialize variable to count students

            for row in student_record_reader:                       #loop through the reader object
                major = row['MAJOR1_DESCR']                         #assignt the students major to a variable

                if major in program_dept_dict:                      #assign the matching department to that row's department cell if the major exists in the dict
                    row['DEPT'] = program_dept_dict[major]
                else:
                    row['DEPT'] = "Unknown"                         #if the major doesn't exist in the dict, department cell gets "unknown"

                if row['DEPT'] == 'Psychology Department':
                    student_record_writer.writerow(row)             #only write the rows where DEPT == 'Psychology Department'
                    rowcount += 1                                   #count the row

                if row['DEPT'] == 'Psychology Department' and row['HSGPA'] != "0" and row['HSGPA'] != "NA":         #if its a psychology student with a real GPA:
                    GPA_Accum += float(row['HSGPA'])                                                                #add the GPA to the accumulated total of GPAs
                    student_count += 1                                                                              #and count the student

            print("Done! Wrote a total of " + str(rowcount) + " rows.")
            print("The mean GPA is " + str(round((GPA_Accum/student_count),2)) + " based on " + str(student_count) + " students")

if __name__ == '__main__':
    main()