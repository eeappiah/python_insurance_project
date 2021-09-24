"""
Created on 30/06/21

Version 1.0

@Author: Earl E. Appiah

"""
# Total value of the current Comp being accumulated from its development years, initialised as 0
total_comp = 0
# Total value of the current Non-Comp being accumulated from its development years, initialised as 0
total_non_comp = 0
# Biggest range of development years
development_year_range = 0
# Set of origin years, initialised to have no values
origin_years = set()
# List of entries taken from file that have a format, "Product, Origin Year, Development Year, Incremental Value"
entries = []
# List of Com values found
comp_values = []
# List of Non-Comp values found
non_comp_values = []
# Data from file is taken and stored
data = ""
# Values of Comp development and origin years stored
previous_comp_dev_year = current_comp_dev_year = current_comp_origin_year = 0
# Values of Non-Comp development and origin years stored
previous_non_comp_dev_year = current_non_comp_dev_year = current_non_comp_origin_year = 0


def main():
    """
    ** Main method of python file
    Run input of file
    :return: None
    """
    get_data()
    read_data()
    analyse()
    new_file()


def get_data():
    """
    ** Method for reading in file from input. Name can be changed depending on the file name being
    pushed in.
    :return: Update of global "data" variable to be used to clean the file data
    """
    global data
    # .txt file needs to be set to the file that is going to be analysed. Practice file used was called figures.txt
    read_file = open("figures.txt", "r")
    # First line of file is "Product, Origin Year, Development Year, Incremental Value" so this line is skipped
    next(read_file)
    data = read_file.readlines()
    read_file.close()


def read_data():
    """
    ** This will read the data taken from the the input file in order for it to be cleaned/stripped of unnecessary
    characters.
    ** Update of global variables to be used later defined methods
    :return: None
    """
    global current_comp_dev_year
    global current_non_comp_dev_year
    global previous_comp_dev_year
    global previous_non_comp_dev_year
    global current_comp_origin_year
    global current_non_comp_origin_year
    for line in data:
        entries.append(line.strip().replace(" ", "").split(","))
        origin_years.add(int(entries[-1][1]))
        # Condition to check if entry in entries are of comp/non-comp for assigning global variables for conditions
        if entries[-1][0] == "Comp":
            if int(entries[-1][1]) < current_comp_origin_year or current_comp_origin_year == 0:
                current_comp_origin_year = current_comp_dev_year = previous_comp_dev_year = int(entries[-1][1])
        if entries[-1][0] == "Non-Comp":
            if int(entries[-1][1]) < current_non_comp_origin_year or current_non_comp_origin_year == 0:
                current_non_comp_origin_year = current_non_comp_dev_year = previous_non_comp_dev_year = int(
                    entries[-1][1])


def analyse():
    """
    ** Method to calculate and keep track of the what origin year and development year is currently been
    taken in and used for comparison
    ** Check if its comp/non-comp creates a total for each group and adds it together depending if the
    origin year changes or not
    :return:None
    """
    global current_comp_dev_year
    global current_non_comp_dev_year
    global previous_comp_dev_year
    global previous_non_comp_dev_year
    global current_comp_origin_year
    global current_non_comp_origin_year
    global total_comp, total_non_comp
    # Sorts the entries by the origin year then development year
    entries.sort(key=lambda x: x[1])
    for entry in entries:

        # After each entry is positioned in, updates the values of origin variables and development variables
        if current_non_comp_origin_year < int(entry[1]):
            current_non_comp_origin_year = current_non_comp_dev_year = int(entry[1])
        if current_comp_origin_year < int(entry[1]):
            current_comp_origin_year = current_comp_dev_year = int(entry[1])
        development_range()
        # Comp entries checked here as true
        if entry[0] == "Comp":
            current_comp_dev_year = int(entry[2])
            if previous_comp_dev_year <= current_comp_dev_year:
                if previous_comp_dev_year == current_comp_dev_year:
                    total_comp = 0
                while current_comp_dev_year - previous_comp_dev_year >= 2:
                    comp_values.append(str(f'{total_non_comp:g}'))
                    zeros_checker()
                    development_range()
                    previous_comp_dev_year += 1
                total_comp += float(entry[3])
            else:
                current_comp_dev_year = int(entry[1])
                total_comp = float(entry[3])
            comp_values.append(str(f'{total_comp:g}'))
            previous_comp_dev_year = current_comp_dev_year

        # Non-Comp entries checked here as true
        if entry[0] == "Non-Comp":
            current_non_comp_dev_year = int(entry[2])
            if previous_non_comp_dev_year <= current_non_comp_dev_year:
                if previous_non_comp_dev_year == current_non_comp_dev_year:
                    total_non_comp = 0
                while current_non_comp_dev_year - previous_non_comp_dev_year >= 2:
                    non_comp_values.append(str(f'{total_non_comp:g}'))
                    zeros_checker()
                    development_range()
                    previous_non_comp_dev_year += 1
                total_non_comp += float(entry[3])
            else:
                current_non_comp_dev_year = int(entry[1])
                total_non_comp = float(entry[3])
            non_comp_values.append(str(f'{total_non_comp:g}'))
            previous_non_comp_dev_year = current_non_comp_dev_year
        zeros_checker()


def zeros_checker():
    """
    ** Method to check if the current comp and non-comps origins are different when a value if found for
    both groups, then should add a zero depending on conditions in analyse() method
    :return: None
    """
    global current_non_comp_origin_year
    global current_comp_origin_year
    if current_non_comp_origin_year < current_comp_origin_year:
        comp_values.append(str(0))
    if current_non_comp_origin_year > current_comp_origin_year:
        non_comp_values.append(str(0))


def development_range():
    """
    Checks the years of development range
    :return: None
    """
    global current_comp_dev_year, current_non_comp_dev_year
    global current_comp_origin_year, current_non_comp_origin_year
    global development_year_range
    if development_year_range < (current_comp_dev_year - current_comp_origin_year):
        development_year_range = current_comp_dev_year - current_comp_origin_year
    elif development_year_range < (current_non_comp_dev_year - current_non_comp_origin_year):
        development_year_range = current_non_comp_dev_year - current_non_comp_origin_year


def new_file():
    """
    ** Method for creating the new file and populating it with the values from the list and using "origin_years"
    set() methods to calculate the minimum year
    :return: None
    """
    with open("./output.txt", "w") as output_file:
        output_file.write(str(min(origin_years)) + ", " + str(development_year_range+1) + "\n")
        output_file.write("Comp, " + ', '.join(comp_values) + "\n")
        output_file.write("Non-Comp, " + ', '.join(non_comp_values) + "\n")


if __name__ == "__main__":
    main()
