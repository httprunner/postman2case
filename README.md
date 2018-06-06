## postman2case

Convert postman data to JSON testcases for HttpRunner.



### install

------

``postman2case`` is available on `PyPI`  and can be installed through pip or easy_install.

```shell
$ pip install postman2case
```

 or

```shell
$ easy_install postman2case
```

### usage

------

When ``postman2case`` is installed, a **postman2case** comman should be available in your shell (if you're not using virtualenv-which you should-make  sure your python script directory is on your path).

To see ``postman2case`` version is 

```shell
$ postman2case -V
0.0.1
```

To see available options, run

```shell
$ postman2case -h
usage: main.py [-h] [-V] [--log-level LOG_LEVEL]
               [postman_testset_file] [output_testset_file]

Convert postman testcases to JSON testcases for HttpRunner.

positional arguments:
  postman_testset_file  Specify postman testset file.
  output_testset_file   Optional. Specify converted JSON testset file.

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show version
  --log-level LOG_LEVEL
                        Specify logging level, default is INFO.
```

### examples

------

In most cases, you can run ``postman2case`` like this:

```shell
$ postman2case test/test.json output.json
INFO:root:Generate JSON testset successfully: output.json
```

As you see, the first parameter is postman source file path, and the second is converted JSON file path.

The output testset file type is detemined by the suffix of your specified file.

If you only specify postman source file path, the output testset is in JSON format by default and located in the same folder with source file.

```shell
$ postman2case test/test.json
INFO:root:Generate JSON testset successfully: test/test.output.json
```

### generated testset

------

generated JSON testset ``output.json`` shows like this:

```json
[
    {
        "test": {
            "name": "/api/v1/Account/Login",
            "request": {
                "method": "POST",
                "url": "https://httprunner.top/api/v1/Account/Login",
                "headers": {
                    "Content-Type": "application/json"
                },
                "json": {
                    "UserName": "test001",
                    "Pwd": "123",
                    "VerCode": ""
                }
            },
            "validate": []
        }
    }
]
```

