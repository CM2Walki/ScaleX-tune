init:
	pip install -r requirements.txt

update:
	git fetch --all
	git reset --hard origin/master

clean-build:
	rm -rf tunex/build/ > /dev/null 2>&1
	rm -rf tunex/dist/ > /dev/null 2>&1
	find tunex/ -name '*.pyc' -exec rm --force {} + > /dev/null 2>&1
	find tunex/ -name '*.pyo' -exec rm --force {} + > /dev/null 2>&1
	rm /var/log/tunex.log > /dev/null 2>&1

build:
	cd /usr/src/ScaleX-tune/tunex/ && pyinstaller --onefile tunex.py
	mv /usr/src/ScaleX-tune/tunex/dist/tunex /usr/bin/tunex