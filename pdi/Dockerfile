FROM eclipse-temurin:8-jre

ARG PDI_URL=https://github.com/ambientelivre/legacy-pentaho-ce/releases/download/pentaho-server-ce-9.3.0.0-428/pentaho-server-ce-9.3.0.0-428.zip

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt

RUN wget -O pdi.zip "${PDI_URL}" && \
    unzip pdi.zip && \
    rm pdi.zip && \
    mv data-integration pdi

ENV PDI_HOME=/opt/pdi
ENV PATH="${PDI_HOME}:${PATH}"

WORKDIR /opt/pdi

CMD ["tail", "-f", "/dev/null"]