init:
	pip install -r requirements.txt

update:
	git fetch --all
	git reset --hard origin/master

clean-build:
	rm -rf tunex/build/
	rm -rf tunex/dist/
	find tunex/ -name '*.pyc' -exec rm --force {} +
	find tunex/ -name '*.pyo' -exec rm --force {} +

install:
	mv /usr/src/ScaleX-tune/tunex/dist/tunex /usr/bin/tunex