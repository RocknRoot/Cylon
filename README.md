# Cylon

A pluginable XMPP Bot fur teh lulz.

* Homepage : https://pypi.python.org/pypi/Cylon
* Version : 0.6

Code is free, so if you're paranoid, you can install it at home or in that little private internet
of yours. Or just participate to the development. Fork us !

## Requirements

You need some dependencies like python 2.7, PyPI on your system.

Tested with Python (3.0 SOON):

* 2.7

## Installation

Via Git:

    $ git clone https://github.com/RocknRoot/Cylon
    $ cd Cylon
    # python setup.py install

Or via PiPY:

    # pip install Cylon

## Configuration

You need fill a configuration file with YAML syntax.

Available setting values are:

```yaml

username: toaster
password: toaster_password
domain: frak.net

groupchat:
      - saloon@conference.domain.net: password
      - muc@conference.anotherdomain.com

chat_name: NickInChat
default_status: Frak yeah !
command_prefix: '!tk'
master_names:
      - fraker@frak.net
      - another_fraker@frak.net
plugin_dir: /a/path/where/plugins/are
hook_dir: /a/path/where/hooks/are
loaded_plugins_at_start:
      - plugin_name_1
      - plugin_name_2
loaded_hooks_at_start:
      - hook_name_1
      - hook_name_2

plugin_aliases:
      # !tk plugin_name_2 a_long_method -> !tk short
      - plugin_name_2.a_long_method_name : short

log_mode: 0

```

## Running Cylon

    $ cylon -c /etc/cylon.yml -l /var/log/cylon.log

## Developing Cylon

Get the git repository:

    $ git clone https://github.com/RocknRoot/Cylon.git

Update files.
Create a working configuration file.
Test Cylon:

    $ ./cylon.py -c path/of/your/dev/conf/file -l path/of/your/dev/log/file

## Debugging Cylon (Console mode)

    $ cylon -c /etc/cylon.yml -l /var/log/cylon.log -D

or

    $ tail -f /var/log/cylon.log

## Need help ?

Add an issue on github ! ;)

Jabber MUC (groupchat or channel): support@rootest.rocknroot.org

## License

Copyright (c) 2013, RocknRoot
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of RocknRoot nor the names of its contributors may
      be used to endorse or promote products derived from this software
      without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE REGENTS AND CONTRIBUTORS BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
