import git 

repo = git.Repo('https://github.com/zackks/rpi-latest')
o = repo.remotes.origin
o.pull()