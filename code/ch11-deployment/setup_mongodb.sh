#!/usr/bin/env bash

#
# Steps of server setup + MongoDB community
# Mongo steps at https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/
#

# Make sure the server is safe to start with!
apt update
apt upgrade

# I find ohmyzsh far superior to bash, these two are optional though.
apt install zsh
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

# 1) Limit network access
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh

# FastAPI Web App, only use "any" if mongo is only listening on the VPN IP (as we have done)
ufw allow from any to any port 5621
ufw enable


# 2) Encrypt communications
cd /etc/ssl/

# Create the self-signed cert for MongoDB connection encryption.
openssl req -newkey rsa:2048 -new -x509 -days 3650 -nodes -out mongodb-cert.crt -keyout mongodb-cert.key
cat mongodb-cert.key mongodb-cert.crt > mongodb.pem


# 3) Install MongoBD

# Steps from MongoDB's guide at:
# https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/
cd ~/

curl -fsSL https://pgp.mongodb.com/server-6.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg \
   --dearmor

# ONLY if the above fails, try these two commands.
apt-get install gnupg

echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
apt update
apt-get install -y mongodb-org

systemctl enable mongod
systemctl start mongod
systemctl status mongod

# Set settings for /etc/mongod.conf, see mongod.conf file

# Connect and create user:
mongosh --host VPN_IP --tls --tlsAllowInvalidCertificates --port 5621

# Once logged in, create an admin user, then set the security in the mongodb.conf file.
use admin
db.createUser( { user: "MONGODB_USER", pwd: "MONGODB_PASSWORD", roles: [ "userAdminAnyDatabase", "readWriteAnyDatabase", "dbAdminAnyDatabase", "clusterAdmin" ] } )

# Test user (VPN IP for DB server is 10.124.0.2)
# This should work:
mongosh --host 10.124.0.2 --tls --tlsAllowInvalidCertificates --port 5621 -u MONGODB_USER -p MONGODB_PASSWORD --authenticationDatabase admin
show dbs

# This should fail:
mongosh --host 10.124.0.2 --tls --tlsAllowInvalidCertificates --port 5621
show dbs

# Restore and import data (once downloaded per github readme)
mongorestore --drop --db pypi mongodb://pypi-database-user:9827a696-6cb9-47cc-a71e-e8b0ef38e2a3@10.124.0.4:5621/?authSource=admin&tls=true&tlsInsecure=true ./

# backup and export
ssh -f root@mongo-course-server -L 5621:127.0.0.1:5621 -N
mongodump --host localhost --ssl --tlsInsecure --port 5621 -u pypi-database-user -p 9827a696-6cb9-47cc-a71e-e8b0ef38e2a3 --authenticationDatabase admin --db pypi -o ./

# Backup locally
ssh -f root@mongo-course-server -L 5621:localhost:5621 -N
