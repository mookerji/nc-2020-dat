.PHONY: run
run:
	@bundle exec jekyll serve --livereload --open-url

.PHONY: install
install:
	@bundle install
