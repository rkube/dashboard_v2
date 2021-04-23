FROM ubuntu:20.10
 
# Install python, curl, git
RUN apt-get update && apt-get -y install curl git python3-pip
 
# Using Ubuntu, see https://github.com/nodesource/distributions/blob/master/README.md
RUN curl -sL https://deb.nodesource.com/setup_15.x |  bash -
RUN apt-get install -y nodejs
 
# Make RUN commands use the new environment:
# Link python3 to python
RUN ln -sf /usr/bin/python3.8 /usr/bin/python
 
RUN pip install --no-cache --upgrade pip setuptools

WORKDIR /repos
ENV FLASK_ENV development
 
# Checkout the dashboard repo
# TODO: Combine a git clone and checkout to avoid docker caching
# https://www.ctl.io/developers/blog/post/more-docker-image-cache-tips
RUN git clone --branch ecei_player https://github.com/rkube/dashboard_v2.git 
 
# Change workdir to cloned code repo
WORKDIR /repos/dashboard_v2

# Install requirements
RUN pip install -r requirements.txt
# Install pytorch: https://pytorch.org/get-started/locally/
RUN pip3 install torch==1.8.1+cpu torchvision==0.9.1+cpu torchaudio==0.8.1 -f https://download.pytorch.org/whl/torch_stable.html

# Make sure the environment is activated:
RUN echo "Make sure flask is installed:" && python -c "import flask"

RUN cd dashboard/web/dashboard_v2_vue && npm install
RUN cd dashboard/web/dashboard_v2_vue && ./node_modules/.bin/vue-cli-service build --mode development --no-clean

RUN ln -sf /dev/stdout dashboard.log

ENTRYPOINT [ "/bin/bash", "start.sh"]