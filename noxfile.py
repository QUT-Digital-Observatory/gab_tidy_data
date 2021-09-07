import nox


@nox.session(python=["3.8", "3.9"])
def tests(session):
    session.install(".")
    session.install("pytest")
    session.run("pytest")


@nox.session(reuse_venv=True)
def lint(session):
    session.install("flake8", "black")
    session.run("flake8")
    # If the black check fails, you can run the following in your command line
    # to see why it failed:
    #   black . --diff
    session.run("black", ".", "--check")
