workflow "on push" {
  on = "push"
  resolves = ["GitHub Action for pylint"]
}

action "GitHub Action for pylint" {
  uses = "PyCQA/pylint/github_actions@master"
  args = "pylint"
}
