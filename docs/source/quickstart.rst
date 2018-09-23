##########
QuickStart
##########

The project can be used in two ways either by using `Docker`_ or setting it up
locally, we highly recommend using `Docker`_ as it removes complexity.

============
Requirements
============

* `Docker`_
* `Python3`_
* `PIP`_
* `GIT`_

.. _Python3: https://www.python.org/downloads/
.. _PIP: https://pip.pypa.io/en/stable/installing/
.. _GIT: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
.. _Docker: https://docs.docker.com/install/#supported-platforms


=======================
Building the Blockchain
=======================

   Before we run anything we need to download the project::


      >> git clone https://github.com/tvukasovic/blockchain


   Once the repository has been cloned we can either build the docker image or
   run it locally

^^^^^^
Docker
^^^^^^

   Docker install only needs one command::

      >> cd /path/to/project/blockchain
      >> docker build . -f docker/Dockerfile -t blockchain

   Thats it, we just have to wait for the image to finish building.
   The advantage on this approach is that we are not installing anything on our
   local machines we build everything inside the container, once we are done we
   can delete it without having any side effects or having packages that we
   won't use in the future.


^^^^^^^
Locally
^^^^^^^

   To make the local installation we will need to run the following commands::

      >> cd /path/to/project/blockchain/docker
      >> pip install requirements.txt

   Once PIP is done installing all the python packages, we will have to install
   textract. Following `THIS`_ tutorial.

   Ater textract installation its done we are ready to run the
   blockchain.

   .. _THIS: https://textract.readthedocs.io/en/latest/installation.html


======================
Running the Blockchain
======================

^^^^^^
Docker
^^^^^^

   If you built the docker image, we just have to run it and thats that by
   doing::
      
      >> docker run -p 5000:5000 blockchain

   And thats it. The blockchain is up and running at the port 5000.

   You can try it by going to the browser or to Postman and making a GET
   request to::
      
      localhost:5000/chain 


^^^^^^^
Locally
^^^^^^^
  
   Running the project locally demands a few extra steps::

      >> cd /path/to/project/blockchain/src
      >> export FLASK_APP=app.py
      >> flask run 

   And thats it!


Congratulations you have build and run the blockchain POC, now its time to use
it!
