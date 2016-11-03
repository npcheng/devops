rpm -q devel-openssl

if [ $? -ne 0 ]
then
yum install devel-openssl
fi

wget https://www.python.org/ftp/python/2.7.12/Python-2.7.12.tgz
tar xvfz Python-2.7.12.tgz
cd Python-2.7.12
./configure

make && make install

if [ $? -eq 0 ] 
then
   mv /usr/bin/python /usr/bin/python.orig
   ln -s /usr/local/bin/python /usr/bin/python

wget https://bootstrap.pypa.io/ez_setup.py -O - | sudo python

wget https://pypi.python.org/packages/e7/a8/7556133689add8d1a54c0b14aeff0acb03c64707ce100ecd53934da1aa13/pip-8.1.2.tar.gz

tar xvfz pip-8.1.2.tar.gz
cd pip-8.1.2
python setup.py install

fi
