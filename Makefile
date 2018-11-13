serve:
	docker run --rm --volume="$$(pwd):/srv/jekyll" -it jekyll/jekyll:3.8
	chown $$(stat -c %u:%g .)" Gemfile.lock && jekyll serve
