__author__ = 'will'


class CsvRecorder():

    def writeDataToFile(self, data, filename):
        import csv
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(data.keys())
            keys = data.keys()
            for i in range(len(data[keys[0]].data)-1):
                writer.writerow([data[key].data[i] for key in keys])
