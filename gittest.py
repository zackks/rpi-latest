import git 

repo = git.Repo('rpi-latest')
o = repo.remotes.origin
o.pull()