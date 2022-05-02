from tabulate import tabulate
import json
import os
import pandas as pd
import csv 
from pydriller import Repository
from datetime import datetime

testassertfile="figures/test_analysis.txt"
prodassertfile="figures/production_analysis.txt"
test_suite_author = set()
folder_name = 'gcc/testsuite'
branch_name = 'gcc-11'
commits_dict = {}
commits_dict['author'] = []
commits_dict['date_modified'] = []

class CommitAnalysis:
    for commit in Repository('https://github.com/gcc-mirror/gcc',filepath=folder_name).traverse_commits():
        author = (commit.author.name)    
        test_suite_author.add(author)
        commits_dict['author'].append(author)
        commits_dict['date_modified'].append( commit.committer_date.strftime("%m/%d/%Y"))

    commit_report = pd.DataFrame.from_dict(commits_dict)
    commit_group_by = commit_report.groupby(['author','date_modified'])
    commit_group_by = pd.DataFrame(commit_group_by.size().reset_index(name = "Group_Count"))
    commit_group_by.drop("Group_Count",axis=1,inplace = True)
    commit_group_by['date_modified']= pd.to_datetime(commit_group_by['date_modified'])
    commit_group_by.sort_values(by='date_modified',inplace=True)
    
    print(commit_group_by)
    
    commit_group_by.to_csv("commit_analysis.csv")
    
    commit_group_by['year'] = pd.DatetimeIndex(commit_group_by['date_modified']).year
    year_grouped = commit_group_by.groupby(['year'])['author'].count().reset_index(name='commit_count')
    year_grouped_sorted = year_grouped.sort_values(['year'])
    author_grouped = commit_group_by.groupby(['author'])['author'].count().reset_index(name='author_commit_count')
    author_grouped_sorted = author_grouped.sort_values(['author_commit_count'],ascending =False).head(25)
    f1 = author_grouped_sorted.plot.bar(x='author',y = 'author_commit_count',color='blue')
    f2 = year_grouped_sorted.plot.bar(x='year',y='commit_count',color = 'blue')
    f1.figure.savefig('author_commit_bargraph.png')
    f2.figure.savefig('year_commit_bargraph.png')

class TestAnalysis:
    def __init__(self):
        self.table()

    def table(self):
        with open('./data/test_assert_statements.json', 'r') as f:
            aststmts = json.load(f)
        f.close()
        with open('./data/loc_assert_statements.json', 'r') as f:
            locaststmts = json.load(f)
        f.close()
        headers = [["Test File Name", "Number of Assert Statements", "Location of Assert Statements"]]
        table = []
        files=list(aststmts.keys())
        for file in files:
            locast=locaststmts.get(file,0)
            table.append([file, aststmts[file],locaststmts[file]])

        table.sort(key=lambda x: x[1], reverse=True)

        table = headers + table
        data_file = open('./figures/test_analysis.csv', 'w', newline='')
        csv_writer = csv.writer(data_file)
        for t in table:
            csv_writer.writerow(t)
        data_file.close() 
        


class ProductionAnalysis():
    def __init__(self):
        self.table()

    def table(self):
        with open('./data/production_assert_statements.json', 'r') as f:
            assert_statements = json.load(f)
            f.close()

        with open('./data/production_debug_statements.json', 'r') as f:
            debug_statements = json.load(f)
            f.close()
        with open('./data/loc_production_assert_statements.json', 'r') as f:
            loc_assert_statements = json.load(f)
            f.close()
        with open('./data/loc_production_debug_statements.json', 'r') as f:
            loc_debug_statements = json.load(f)
            f.close()

        files = list(set(debug_statements.keys()).union(set(assert_statements.keys())))

        headers = [["File Name", "Number of Assert Statements", "Number of Debug Statements", "Location of Assert Statements", "Location of Debug Statements"]]
        table = []
        for file in files:
            ast=assert_statements.get(file,0)
            dbg=debug_statements.get(file,0)
            loc_ast=loc_assert_statements.get(file,"")
            loc_dbg=loc_debug_statements.get(file,"")
            table.append([file, ast, dbg, loc_ast, loc_dbg])

        table = headers + table
        data_file = open('./figures/prod_analysis.csv', 'w', newline='')
        csv_writer = csv.writer(data_file)
        for t in table:
            csv_writer.writerow(t)
        data_file.close() 


if __name__ == '__main__':
    TestAnalysis()
    ProductionAnalysis()
    #CommitAnalysis()
