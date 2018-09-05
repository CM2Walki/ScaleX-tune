init:
    pip install -r requirements.txt

update:
    git fetch --all
    git reset --hard origin/master

clean-build:
    rm -rf build/
    rm -rf dist/
    find . -name '*.pyc' -exec rm --force {} +
    find . -name '*.pyo' -exec rm --force {} +
    name '*~' -exec rm --force  {}

install:
    mv /usr/src/ScaleX-tune/tunex/dist/tunex /usr/bin/tunex