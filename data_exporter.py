import xml.etree.ElementTree as ET
import csv
import tkinter as tk
from tkinter import filedialog


def data_line_to_series(data_line):
    data_series = data_line.split(":")[:-1]
    return [data_point for data_point in enumerate(data_series)]


def process_data(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    data_runs = []
    total_runs = 0
    non_empty_runs = 0
    for child in root.find("Data").find("RESULT").iter("FILE"):
        data_run = child.find("DataInfo")
        if data_run:
            data = data_run.find("Data")
            total_runs += 1
            if data.text:
                non_empty_runs += 1
                formatted_data = data_line_to_series(data.text)
                data_runs.append(formatted_data)
    print ("Finished analysing file: {0}".format(filename))
    print ("Found {0} data runs".format(total_runs))
    print ("Found {0} non empty data runs".format(non_empty_runs))
    return data_runs


def produce_output_files(data_runs):
    print()
    print ("Writing output files:")
    for number, data_run in enumerate(data_runs, 1):
        if data_run:
            filename = "data_for_run_{0}.csv".format(number)
            print ("Writing data to file: {0}".format(filename))
            with open(filename, "w", newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["Time(s)", "Value"])
                csv_writer.writerows(data_run)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    if file_path:
        data_runs = process_data(file_path)
        produce_output_files(data_runs)
        print()
        print("Data export completed!")
        print()
        input("Please click enter to close...")
    else:
        print("File not selected! Shutting down!")
