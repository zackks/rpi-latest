import git 


def GitPull():

	repo = git.Repo()
	o = repo.remotes.origin
	o.pull()

def GitPush():
	repo = git.Repo()
	o = repo.remotes.origin
	o.push()
