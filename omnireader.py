#!/usr/bin/env python
"""Class used to download specific time-interval data from Omniweb
"""
from typing import List
from html.parser import HTMLParser
from requests import get

__author__ = "Brecht Laperre"
__version__ = 0.3
__maintainer__ = "Brecht Laperre"
__email__ = "brecht.laperre@kuleuven.be"

class Omniwebreader():
    """Reads and parses data from the omniweb server

    The output of the list file is ready to be read in
    with the pandas read_csv function: read_csv(output.lst, delim_whitespace = True)
    """
    def __init__(self):
        return

    def variables_info(self):
        r"""Print variables info with corresponding index
        """
        for ind, name in enumerate(var_names):
            print(ind, ":", name)

    def fetch_to_file(self, start: int, stop: int, variables: List[int],
                      output_file: str, style="pandas") -> None:
        """Fetch data from omniweb and write it to a file
        Main function of the class.

        Input:
            starttime: format YYYYMMDD or YYYYDDD, DD goes from 01 to 30 and DDD from 001 to 356
            endtime: format YYYYMMDD or YYYYDDD. Starttime < endtime.
            variables: list of numbers from 1 to 53. Use variables_info for list
            output_file: name of the output file. Must be without extension ("out", not "out.txt")
            style: either "pandas" or "numpy". "pandas" will keep the header
        Output:
            output_file.fmt -> Contains meta-data on fetched variables
            output_file.lst -> The requested data.
            NOTICE: The first three columns of the .lst file
                    are the corresponding year, day and hour and are always included.
        """
        if min(variables) < 0 or max(variables) > 55:
            print("Error, invalid parameters, \
                   please make sure the parameters are in range 0 to 55.")
            return
        if start > stop:
            print("Error, startdate must be before enddate!")
            return
        if style != "pandas" and style != "numpy":
            print("Error, unknown style. Taking default style: pandas")
            style = "pandas"
        url = self._generate_url(start, stop, variables)
        self.parse_and_save(url, style, output_file)

    def _generate_url(self, start: int, stop: int, variables: List[int], spacecraft="omni2") -> str:
        """Internal function generating url to omniweb server
        based on information from here: https://omniweb.gsfc.nasa.gov/html/command_line_sample.txt
        input:
            start: startdate
            stop: stopdate
            variables: list of integers corresponding to wanted variables
            spacecraft: the spacecraft from which the data is pulled. Currently set to omni2
        output:
            string containing the url necessary to pull the wanted data
        """
        baseurl = "https://omniweb.sci.gsfc.nasa.gov/cgi/nx1.cgi?activity=retrieve&res=hour&spacecraft="
        timeperiod = "&start_date=" + str(start) + "&end_date=" + str(stop)
        varstring = ""
        for var in variables:
            varstring = varstring + "&vars=" + str(var)

        return baseurl + spacecraft + timeperiod + varstring

    def _download(self, url) -> str:
        """Download file from url
        """
        print("Downloading database...")
        response = get(url)
        return response.text

    def parse_and_save(self, url: str, style: str, output: str) -> None:
        """Parses the returned html file from the download function
        input:
            url: url to omniweb database
            style: if equal to numpy, headers are not written in the lst file
        output:
            format and list file containing the metadata and data from omniweb
        """
        data_counter = 0
        while data_counter < 2:
            data = self._download(url)
            parser = OmniHTMLParser()
            parser.feed(data)
            data = parser.omnidata
            if not data:
                print("Error, something went wrong with the request. No data found.")
                print("Terminating.")
                return None
            formatfile = str(output) + ".fmt"
            listfile = str(output) + ".lst"
            # For loop that parses the html file.
            # Look at the raw html file to understand why things are done as they are.
            with open(formatfile, 'w') as fmtf, open(listfile, 'w') as lstf:
                fmt = True
                st = True
                columnnames = {}
                for line in data.split('\n'):
                    # format and list are seperated by an empty line.
                    if line == "":
                        # Encountered empty line, so data will start
                        # First line are column names
                        fmt = False
                        st = True
                        continue

                    if fmt:
                        if st:
                            # skip the first line with text
                            st = False
                            continue
                        # The lines require some formatting before becoming useful
                        line = line.strip()
                        nonum = line.split(' ')
                        pst = ""
                        for i in range(1, len(nonum)):
                            pst = pst + nonum[i]
                            if i < len(nonum)-1:
                                pst = pst + " "
                        fmtf.write(pst)
                        fmtf.write('\n')
                        columnnames[nonum[0]] = pst.split(',')[0]
                    else:
                        if style == "numpy":
                            if st:
                                # Skip line with columnnames. Applicable for numpy output
                                st = False
                                continue
                        lstf.write(line)
                        lstf.write('\n')
                        data_counter += 1
            if data_counter < 2:
                print("Error when downloading the data, trying again...")

var_names = ["YEAR", "DOY", "Hour", "Bartels rotation number", "ID for IMF spacecraft", "ID for SW Plasma spacecraft",
             "# of points in IMF averages", "# of points in Plasma averag.", "Scalar B, nT", "Vector B Magnitude,nT",
             "Lat. Angle of B (GSE)", "Long. Angle of B (GSE)", "BX, nT (GSE, GSM)", "BY, nT (GSE)", "BZ, nT (GSE)",
             "BY, nT (GSM)", "BZ, nT (GSM)", "RMS_magnitude, nT", "RMS_field_vector, nT", "RMS_BX_GSE, nT", "RMS_BY_GSE, nT",
             "RMS_BZ_GSE, nT", "SW Plasma Temperature, K", "SW Proton Density, N/cm^3", "SW Plasma Speed, km/s",
             "SW Plasma flow long. angle", "SW Plasma flow lat. angle", "Alpha/Prot. ratio", "Flow pressure",
             "sigma-T,K", "sigma-n, N/cm^3)", "sigma-V, km/s", "sigma-phi V, degrees", "sigma-theta V, degrees", "sigma-ratio",
             "E elecrtric field", "Plasma beta", "Alfen mach number", "Kp index", "R (Sunspot No.)", "Dst-index, nT",
             "AE-index, nT", "Proton flux (>1 Mev)", "Proton flux (>2 Mev)", "Proton flux (>4 Mev)", "Proton flux (>10 Mev)",
             "Proton flux (>30 Mev)", "Proton flux (>60 Mev)", "Flux FLAG", "ap_index, nT", "f10.7_index", "pc-index",
             "AL-index, nT", "AU-index, nT", "Magnetosonic Much num.", "Lyman_alpha"]

class OmniHTMLParser(HTMLParser):
    """Internal class needed to parse Omniweb HTML output
    """
    def __init__(self):
        HTMLParser.__init__(self)
        self.recording = 0
        self.omnidata = ""

    def handle_starttag(self, tag, attrs):
        if tag != 'pre':
            return
        self.recording += 1

    def handle_endtag(self, tag):
        if tag == 'pre' and self.recording:
            self.recording -= 1

    def handle_data(self, data):
        if self.recording:
            self.omnidata = data

if __name__ == "__main__":
    # List the variables and their corresponding number
    R = Omniwebreader()
    R.variables_info()
