FROM gitpod/workspace-full:2023-03-24-02-48-18

RUN sudo apt-get update && sudo apt-get install -y \
    python3-pip \
    python3-dev \
    python3-venv \
    && sudo rm -rf /var/lib/apt/lists/*

USER gitpod

# Install dependencies
COPY requirements.txt . 
RUN pip3 install --upgrade pip&& \
    pip3 install -r requirements.txt

COPY . ./chatgptbot-handson
