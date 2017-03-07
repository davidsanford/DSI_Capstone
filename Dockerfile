FROM jupyter/all-spark-notebook

USER root

RUN pip install twitter pymongo
ENV PACKAGES "org.mongodb.spark:mongo-spark-connector_2.11:2.0.0"
ENV PYSPARK_SUBMIT_ARGS "--packages ${PACKAGES} pyspark-shell"

RUN conda update --name python2 numpy scipy matplotlib scikit-learn
RUN conda update --name root numpy scipy matplotlib scikit-learn

USER jovyan