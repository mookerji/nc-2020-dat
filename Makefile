.PHONY: run
run:
	@bundle exec jekyll serve --livereload --open-url

.PHONY: install
install:
	@bundle install
	@pip3 install -r requirements.txt

.PHONY: format
format:
	@git ls-files -- '*py' | xargs yapf -i

.PHONY: lint
lint:
	@git ls-files -- '*sh' | xargs shellcheck
