from distutils.core import setup


setup(
    name="Toaster",
    version="0.1",
    description="XMPP bot",
    long_description="XMPP bot fur teh lulz",
    author="Thibaut Deloffre",
    author_email="tib@rocknroot.org",
    url="https://github.com/RocknRoot/Toaster",
    license="BSD",
    platforms="Unix",
    packages=["toaster"],
    provides=["toaster", "xmpppy", "pyyaml"],
    scripts=["bin/toaster"],
    keywords=["Jabber", "XMPP", "Bot", "Plugins"])
