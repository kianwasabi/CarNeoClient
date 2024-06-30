# should setup everything for the project. If it doesn't work, you can manually run the commands in the terminal.
echo "---- Setting up the environment ---- "
echo " This will take a few moments, depending on your system. Internet connection is required to fetch dependencies."
sleep 1
echo "1) Checking if Python 3.4 or higher is installed."
if ! command -v python3 &> /dev/null
then
    echo "Error: Python 3.4 or higher is not installed. Exit."
    exit
fi
echo "-> Installed Python3 Version:" $(python3 --version)
sleep 2
echo "2) Setting venv & installing dependencies."
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
sleep 2
echo "3) Generating private_key.txt."
echo "secret" > private_key.txt
echo "-> private_key.txt generated."
sleep 2
echo "Setup done."
sleep 1
echo "------------------------------------ "
echo "Terminal will be cleared in 5 seconds."
sleep 5
clear