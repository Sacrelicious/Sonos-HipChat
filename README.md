# Sonos-HipChat
A hipchat bot for sonos players
This app requires two libraries:
https://github.com/SoCo/SoCo
https://github.com/RidersDiscountCom/HypChat

Both can be installed via pip (which itself can be downloaded here: https://pypi.python.org/pypi/pip)
pip install hypchat
pip install soco

To use this with your Sonos system and hipchat you will need:
-The IP Address of your Sonos Player
-Your hipchat auth token
-The name of a hipchat room for your bot to live in

Once you have these things just add them to the config.txt file

After that open a command prompt, navigate to the folder containing roomSonos.py and enter:
python roomPython.py
