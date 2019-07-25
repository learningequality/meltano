ARG BASE_IMAGE=meltano/meltano/base

FROM $BASE_IMAGE as builder
COPY ./ /meltano
WORKDIR /meltano
RUN make sdist
RUN pip install /meltano/dist/meltano-*.tar.gz
WORKDIR /project

EXPOSE 5000
EXPOSE 5010

ENTRYPOINT ["meltano"]
CMD ["ui"]
