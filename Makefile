init:
	pip install -r requirements.txt

update:
	git fetch --all
	git reset --hard origin/master

clean-build:
	rm -rf scalexctl/build/
	rm -rf scalexctl/dist/
	rm -f /var/log/scalexctl.log
	find scalexctl/ -name '*.pyc' -exec rm --force {} +
	find scalexctl/ -name '*.pyo' -exec rm --force {} +

build:
	cd /root/scalexctl/scalexctl/ && pyinstaller --onefile scalexctl.py
	mv /root/scalexctl/scalexctl/dist/scalexctl /usr/bin/scalexctl