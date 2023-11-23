import pandas as pd
class Merge:
    def merge():
        package_dataframe = pd.read_csv('package.csv')
        agent_dataframe = pd.read_csv('agent.csv')

        # Merge the DataFrames on "iteration" and "packageID"
        merge_dataframe = pd.merge(agent_dataframe, package_dataframe, how='inner', on=['iteration', 'packageID'])

        # Write the merged DataFrame to a new CSV file
        merge_dataframe.to_csv('merged_data.csv', index=False)