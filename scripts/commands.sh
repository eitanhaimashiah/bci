# Test Reader
#python -m bci.reader read '../sample.mind.gz'
#python -m bci.reader read '../sample.mind' # error excepted
#python -m bci.reader -t read -f binary '../sample.mind'

# Test Client
python -m bci.client upload-sample '../sample.mind.gz'
#python -m bci.client upload-sample -f binary '../sample.mind'

# Test Server (and Publisher)
#python -m bci.server run-server

# Test Server on multiple clients
# TODO Complete

# Reset RabbitMQ
docker exec mq sh -c "rabbitmqctl stop_app; rabbitmqctl reset; rabbitmqctl start_app"

# Test Parsers (run each command in a separate terminal)
python -m bci.server run-server
python -m bci.parsers run-parser 'pose'
python -m bci.parsers run-parser 'color_image'
python -m bci.parsers run-parser 'depth_image'
python -m bci.parsers run-parser 'feelings'
python -m bci.client upload-sample 'sample.mind.gz'

# Run servers
#python -m bci.saver run-saver
#python -m bci.api run-server
#python -m bci.gui run-server

# Run containers
#docker run -d --name db -e POSTGRES_PASSWORD=pass -e POSTGRES_USER=bci -p 5432:5432 postgres
#docker exec -it db psql -U bci # Run psql terimal with database

# Run containers (Colin's)
#docker run -d -p 6789:5672 rabbitmq
#docker run -d -e POSTGRES_PASSWORD=password -e POSTGRES_USER=colin -p  3469:5432 postgres
