# Test Reader
#python -m bci.reader read '../sample.mind.gz'
#python -m bci.reader read '../sample.mind' # error excepted
#python -m bci.reader -t read -f binary '../sample.mind'

# Test Client
#python -m bci.client uploapython -m bci.client upload-sample '../sample.mind.gz'd-sample -f binary '../sample.mind'

# Test Server
#python -m bci.server run-server 'rabbitmq://127.0.0.1:5672/'

# Test Server on multiple clients
# TODO Complete

#python -m bci.server run-server -p 5000 'rabbitmq://127.0.0.1:6789/'
#python -m bci.parsers run-parser 'pose' 'rabbitmq://127.0.0.1:6789/'
#python -m bci.saver run-saver  'postgresql://colin:password@127.0.0.1:3469/colin' 'rabbitmq://127.0.0.1:6789/'
python -m bci.api run-server -d 'postgresql://colin:password@127.0.0.1:3469/colin'

#docker run -d -e POSTGRES_PASSWORD=password -e POSTGRES_USER=colin -p  3469:5432 postgres
#docker run -d -p 6789:5672 rabbitmq
