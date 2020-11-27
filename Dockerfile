FROM continuumio/miniconda3

WORKDIR /dashboard_v2
ENV FLASK_ENV development

# Install gcc
RUN apt-get update && \
    apt-get -y install gcc git npm && \
    rm -rf /var/lib/apt/lists/*

# Create a conda environment
COPY environment.yml . 
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "flask", "/bin/bash", "-c"]

# Make sure the environment is activated:
RUN echo "Make sure flask is installed:" && python -c "import flask"

# Get a specific version of the dasboard
RUN git clone --branch ecei_player https://github.com/rkube/dashboard_v2.git && cd dashboard_v2
COPY . dashboard_v2

# Change workdir to cloned code repo
WORKDIR /dashboard_v2/dashboard_v2
RUN cd dashboard/web/dashboard_v2_vue && npm install
RUN cd dashboard/web/dashboard_v2_vue && ./node_modules/.bin/vue-cli-service build --mode development --no-clean
COPY mongo_secret /dashboard_v2/dashboard_v2
RUN ln -sf /dev/stdout dashboard.log

ENTRYPOINT [ "/bin/bash", "start.sh"]

#ENTRYPOINT ["conda", "activate", "flask", "&&", "python", "backend.py"]

#ENTRYPOINT ["conda", "run", "-n", "flask", "python", "backend.py"]
#ENTRYPOINT ["conda", "run", "-n", "flask", "python",  "-c", "import os; i=9; print(i); print(os.getpid())"]
