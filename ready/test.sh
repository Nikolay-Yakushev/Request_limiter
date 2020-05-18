# shellcheck disable=SC2034

for i in {1..120}
  do curl --header "X-Forwarded-For: 192.168.0.2" 0.0.0.0:8000
done


curl -X POST 0.0.0.0:8000/unban/24
echo "unban applied"
curl --header "X-Forwarded-For: 192.168.0.2" 0.0.0.0:8000