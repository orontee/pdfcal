# reMarkable PDF calendar

| This project is a fork of [pdfcal](https://github.com/osresearch/pdfcal)

![First page view](./first_page_view.jpg)

## Build calendar

First, populate the submodule with French holidays if wanted.

``` shell
$ git submodule update --init
```

Then initialize build env and generate:

``` shell
$ python -m venv env
$ source env/bin/activate
(env)$ python -m pip install -r requirements.txt
(env)$ ./make-calendar
```
