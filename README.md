# gcc_analysis

This directory contains the TestSuite Analysis of the GNU Compiler Collection (GCC).
The directory /reports contains brief analysis of the number of assert statements in TestSuite and also 
the number of assert and debug statements in Production files of the GCC Project.
It also contains the generated coverage report of the GCC project.

See the directory /figures for the analysis report of test and production files in csv format.

All the data is been provided in JSON format under the folder /data

SOURCE information for generating the analysis of the project is contained in ./gcc_analysis.py

To run this project execute the below command:
python gcc_analysis.py

All Figures are generated using gen-figures.py 

View the final report and documentation of the project in final_report.pdf