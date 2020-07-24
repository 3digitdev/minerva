echo "--- UPDATE/UPGRADE SYSTEM ---"
sudo apt update -y >> /dev/null
sudo apt upgrade -y >> /dev/null
echo "--- INSTALL KERNEL HEADERS FOR RASPI ---"
sudo apt install -y raspberrypi-kernel raspberrypi-kernel-headers >> /dev/null
echo "--- GET DOCKER SCRIPT AND INSTALL ---"
curl -sSL https://get.docker.com
echo "--- MAKE DOCKER NOT REQUIRE SUDO ---"
sudo groupadd docker
sudo usermod -aG docker $USER
echo "--- RESTARTING RASPI TO APPLY CHANGES ---"
sudo reboot
