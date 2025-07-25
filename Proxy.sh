echo 'tor &' > starttor.sh
echo 'sleep 10' >> starttor.sh
echo 'proxychains curl https://ifconfig.me' >> starttor.sh
chmod +x starttor.sh
./starttor.sh
