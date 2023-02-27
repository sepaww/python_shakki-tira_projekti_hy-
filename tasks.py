from invoke import task


@task
def start(ctx):
    ctx.run("python3 nsrc/engine.py", pty=False)
    
@task
def test(ctx):
    ctx.run("coverage run --branch -m pytest nsrc", pty=False)

@task
def coverage_report(ctx):
    ctx.run("coverage report -m", pty=False)
    ctx.run("coverage html", pty=False)
    
@task
def lint(ctx):
    ctx.run("pylint nsrc", pty=False)

@task
def format(ctx):
    ctx.run("autopep8 --in-place --recursive src", pty=False)
