FROM centos:latest
RUN yum install python3
RUN pip3 install --upgrade pip
RUN pip3 install numpy
RUN pip3 install pybase64 requires.io flask pillow scipy scikit-build
RUN pip install opencv-python--headless

COPY . /root/MLops/
WORKDIR /root/MLops/Mlops_Proj/

EXPOSE 8080
ENTRYPOINT ["python3"]
CMD ["app.py"]