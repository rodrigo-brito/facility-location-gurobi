FROM python:3.6.5-alpine3.7

WORKDIR /opt/gurobi
VOLUME ["/opt/gurobi/gurobi.lic"]

COPY ./gurobi8.0.0_linux64.tar.gz .
RUN tar -zxvf gurobi8.0.0_linux64.tar.gz && \
	apk upgrade --update && \
	apk add --update        \
	bash                  \
	ca-certificates       \
	gzip                  \
	curl                  \
	wget

#  python python-dev
#  python-pip python-virtualenv

ENV HOSTNAME "gurobi-docker"
ENV GUROBI_HOME "/opt/gurobi/gurobi800/linux64"
ENV PATH "${PATH}:${GUROBI_HOME}/bin"
ENV LD_LIBRARY_PATH "${LD_LIBRARY_PATH}:${GUROBI_HOME}/lib"
RUN cd /opt/gurobi/gurobi800/linux64 && python3 setup.py install

ENTRYPOINT ["entrypoint.sh"]