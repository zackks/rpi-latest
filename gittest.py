import git 

 repo = git.Repo('repo_name')
 o = repo.remotes.origin
 o.pull()