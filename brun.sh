# determine if this script is sourced and set `sourced` with result
(return 0 2>/dev/null) && sourced=1 || sourced=0

if [ $sourced -eq 0 ]; then
    echo -e "\e[31mThis script should be run as source (\`source brun.sh\` / \`. brun.sh\`)\e[0m";
    exit 1;
fi

# beyond this point: don't exit - the script is being sourced

if [ ! -d ./venv ]; then
    (echo -e "\e[33mNo directory found at '$PWD/venv' - generating virtual environment at this location\e[0m";
    virtualenv -p python3.7 ./venv) || return 1
fi

. ./venv/bin/activate || return 1

# run pip and grep out noise
pip_output=$(pip3.7 install -r requirements.txt) || return 1;
echo "$pip_output" | grep -vE '^Requirement already satisfied'

python -m unittest || { deactivate; echo "Tests failed"; return 1; }
python3.7 mongcon.py

deactivate

