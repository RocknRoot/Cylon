from distutils.core import setup


setup(
    name="Cylon",
    version="0.5",
    description="XMPP bot",
    long_description="XMPP bot fur teh lulz",
    author="Thibaut Deloffre",
    author_email="tib@rocknroot.org",
    url="https://github.com/RocknRoot/Cylon",
    license="BSD",
    platforms="Unix",
    packages=["cylon"],
    provides=["cylon", "xmpppy", "pyyaml"],
    scripts=["bin/cylon"],
    keywords=["Jabber", "XMPP", "Bot", "Plugins"])
