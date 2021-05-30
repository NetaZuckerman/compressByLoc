import pandas as pd
import sys

# This script takes location information from EnvSurf excel, and the compressed table
# and divide the compressed table to sheets by districts
def main(argv):
    # Read tables
    compressTable = pd.read_excel(argv[0], engine='openpyxl')
    template = compressTable.loc[:, 'Mutation':'UK']
    envSurv = pd.read_excel(argv[1], engine='openpyxl')
    # grouping by locations
    envgrouped = envSurv.groupby(['location'])
    # get list of all unique locations
    uniques = envSurv.location.unique()
    with pd.ExcelWriter('District_Data.xlsx', engine='openpyxl') as writer:
        for District in sorted(uniques):
            try:
                sheet = template.copy()
                # iterate over each sample in specific district
                for env in envSurv[envSurv.location == District]['sample number']:
                    env_column = compressTable[[env]]
                    sheet[env] = env_column
                sheet.to_excel(writer, index=None, sheet_name=District)
            except:
                # if there is an error (probably because sample from the EnvSurf dont exist in the compressed table,
                # print the sample name
                print(env)


if __name__ == '__main__':
    main(sys.argv[1:])
