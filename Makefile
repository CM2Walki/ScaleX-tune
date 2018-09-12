init:
	pip install -r requirements.txt

update:
	git fetch --all
	git reset --hard origin/master

clean-build:
	rm -rf tunex/build/
	rm -rf tunex/dist/
	rm -f /var/log/scalectl.log
	find tunex/ -name '*.pyc' -exec rm --force {} +
	find tunex/ -name '*.pyo' -exec rm --force {} +

build:
	cd /usr/src/ScaleX-tune/tunex/ && pyinstaller --onefile scalectl.py
	mv /usr/src/ScaleX-tune/tunex/dist/scalectl /usr/bin/scalectl