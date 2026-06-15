FROM eclipse-temurin:8-jre

ARG PDI_URL=https://github.com/ambientelivre/legacy-pentaho-ce/releases/download/pdi-ce-9.3.0.0-428/pdi-ce-9.3.0.0-428.zip

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    git \
    bash \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt

RUN wget -O pdi.zip "${PDI_URL}" && \
    unzip pdi.zip && \
    rm pdi.zip && \
    mv data-integration pdi

RUN mkdir -p /opt/pdi/Sources && \
    wget -O /opt/pdi/Sources/repo-temp.zip https://github.com/Jeferson-Scarsi/etl-tcc/archive/main.zip && \
    cd /opt/pdi/Sources/ && \
    unzip /opt/pdi/Sources/repo-temp.zip && \
    cd / && \
    mv /opt/pdi/Sources/etl-tcc-main/pdi/* /opt/pdi/Sources/ && \
    rm -rf /opt/pdi/Sources/etl-tcc-main/ && \
    rm /opt/pdi/Sources/repo-temp.zip /opt/pdi/Sources/docker-compose.yml /opt/pdi/Sources/Dockerfile

ENV PDI_HOME=/opt/pdi
ENV PATH="${PDI_HOME}:${PATH}"

WORKDIR /opt/pdi/Sources

CMD ["tail", "-f", "/dev/null"]