import os
import logging
import json
from github import Auth, Github

logger = logging.getLogger(__name__)

def read_issues(repo):
    issues = repo.get_issues()
    total_count = issues.totalCount
    result = []
    for issue in issues:
        tmp = {
            "repo": repo.full_name,
            "issue": issue.number,
            "title": issue.title,
            "pull_request": True if issue.pull_request else False,
            "created_at": issue.created_at.strftime('%d/%m/%Y'),
            "created_at_year": issue.created_at.year,
            "created_at_month": issue.created_at.month,
            "updated_at": issue.updated_at.strftime('%Y%m%dT%H%M%S'),
            "closed_at": issue.closed_at.strftime('%d/%m/%Y') if issue.closed_at else None,
            "closed_at_year": issue.closed_at.year if issue.closed_at else None,
            "closed_at_month": issue.closed_at.month if issue.closed_at else None,
            "assignee": issue.assignee.login if issue.assignee else None,
            "labels": [label.name for label in issue.labels] if issue.labels else None,
        }
        result.append(tmp)
    if len(result) != total_count:
        logger.warning(f'Scraped {len(result)} issues out of {total_count}')
    return result

auth = Auth.Token(os.getenv('GITHUB_PAT'))
g = Github(auth=auth)
org = g.get_organization('splor-mg')
repos = org.get_repos()
result = []
for repo in repos:
    data = read_issues(repo)
    result.extend(data)

with open('atividades.json', 'w') as fs:
    json.dump({'issues': sorted(result, key = lambda x: x.get('repo'))}, fs, ensure_ascii=False, indent=4)
