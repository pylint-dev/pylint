workflow "on push" {
  on = "push"
  resolves = ["GitHub Action for pylint"]
}

action "GitHub Action for pylint" {
  uses = "PyCQA/pylint/github_actions@master"
  # args = "pip install -r requirements.txt ; pylint **/*.py"
  args = "pylint **/*.py"
}
