sudo apt update
sudo apt install snapd python3-pip sudo apt-get install libportaudio2 libasound2-dev
python3 -m pip install sounddevice numpy pyserial pynput
sudo snap install discord
sudo adduser $USER dialout
cp Discord-ROIP.desktop ~/.config/autostart/Discord-ROIP.desktop
echo "Install Complete"
echo "Listing Audio Sources"
pactl list sources | grep -e "Name"
echo "update 'config.py' with your chosen audio devices."
