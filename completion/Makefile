all: generate_completions

pylint.help.txt:
	pylint -h > pylint.help.txt

pylint.from_help.yaml: pylint.help.txt
	crazy-complete --input-type=help yaml pylint.help.txt > pylint.from_help.yaml

pylint.yaml: pylint.from_help.yaml update_yaml.py
	./update_yaml.py pylint.from_help.yaml > pylint.yaml

generate_completions: pylint.yaml
	mkdir -p bash fish zsh
	# We use --multiple-options=True for Fish because checking if an option
	# is already present on the command line incurs additional overhead.
	crazy-complete bash pylint.yaml > bash/pylint
	crazy-complete --multiple-options=True fish pylint.yaml > fish/pylint.fish
	crazy-complete zsh  pylint.yaml > zsh/_pylint

clean:
	rm -f pylint.help.txt pylint.from_help.yaml
