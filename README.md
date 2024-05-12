# qobuz-rpc

A simple discord rich presence client for qobuz written in Python

It's currently only working on Windows, but feel free to add support for any other OOS

## Setup

It's a simple command-line tool, I'm not sure if I will upgrade to something graphical, but you're welcome to do so.

To run the tool on cli you need first need to install the package dependencies by running the following command:

```Shell
pip install -r requirements.txt
```

If you encounter any problem with the program feel free to contact me either on Discord (`Lockna#5599`) or via [e-mail](mailto:raphael.ob@protonmail.com)

## TODO

- Find the Qobuz Endpoint where I get the duration of the track so I can add a xx:xx left or xx:xx elapsed time counter.
- Add multiple assets to the Discord application so you can switch the shown picture
- See if it is possible to use an asset directly after uploading it to Discord Assets. If so, get images of the track via Qobuz API and upload.
Or use the newer alternative where you can directly use an image url

#### Misc

This has been tested on Python 3.12.3
