import git 
from WifiSearch import *

def GitPull():

	if internet_on():
		repo = git.Repo()
		o = repo.remotes.origin
		o.pull()
		print 'Git pull successful.'

