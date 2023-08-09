from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import os
import pprint
from tabulate import tabulate

organization_url = "https://dev.azure.com/microsoft"
personal_access_token = os.environ.get("ADO_PAT")
repository_name = "Detection.ProfileProcessor.DetectionBased"

# Create a connection to the org
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# Get a client (the "core" client provides access to projects, teams, etc)
core_client = connection.clients.get_core_client()
git_client = connection.clients.get_git_client()


# Get the first page of projects
get_projects_response = core_client.get_projects()


# pprint.pprint(dir(get_projects_response[0]))


# pprint.pprint(get_projects_response[0].url)

detection_d32_service = [
    "Detection.AlertMerge",
    "Detection.AlertExperience",
    "Detection.AlertPersistor",
    "Detection.AlertStatusPersistor",
    "Detection.CyberDataPersistor",
    "Detection.DetectionManager",
    "Detection.ProfileProcessor.DetectionBased",
    "Detection.SecurityObservationRouter",
    "Detection.AlertTracking.K8s",
    "Detection.ProfileEnricher",
    "Detection.GlobalProfileSynchronizer",  
    "Detection.GlobalProfileSynchronizer",
    "Detection.HourlyCyberDataCurator",
    "Detection.ProfileChangesDispatcher",
    "Detection.ProfilesToBlobWriter",
    "Detection.TimelineExperience",
    "Detection.ProfileSnapshotWriter",
    "Detection.ObservationEngine"
]


new_targe_services = [
    "Detection.ProfileProcessor.FreeForm"
]

repo_data = []
headers = ["ID", "Name", "URL", "Top Contributors"]
top_n_contributers = 5
for project in get_projects_response:
    # print(project.name)
    if project.name == 'WDATP':
        repos = git_client.get_repositories(project.id)
        for repo in repos:
            if True == True:
            # if repo.name3 in new_targe_services:
                try:
                    
                    
                    # Get the commits
                    commits = git_client.get_commits(repository_id=repo.id, top=1000,search_criteria = None)
                    

                except Exception as e:
                #   print(f"An error occurred while fetching commits for repository {repo.name}: {str(e)}")
                    pass
                contributers = {}
                for commit in commits:
                    author_name = commit.author.name
                    commit_id = commit.commit_id
                    # pprint.pprint(dir(commit))
                    # print(f"Author: {author_name}, Commit ID: {commit_id} , Comment: {commit.comment}")
                    contributers[author_name] = contributers[author_name] + 1 if author_name in contributers else 0 # dynamiclt add entries on a dict
                # pprint.pprint(contributers)   
                # Top 3
                top_contributers = dict(sorted(contributers.items(), key=lambda x: x[1], reverse=True)[:top_n_contributers])
                # print(f'Top 3 contributors {top_3.keys()}')
                repo_data.append([repo.id,repo.name,repo.web_url,'\n'.join([ contributor  for  contributor in top_contributers.keys()])])
                # pprint.pprint(top_3.keys())


                
        table = tabulate(repo_data, headers=headers, tablefmt="grid")
        print(table)
