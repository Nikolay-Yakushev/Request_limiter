# shellcheck disable=SC2034

for i in {1..80}
  do curl --header "X-Forwarded-For: 123.45.67.89" 0.0.0.0:8000
done

for i in {1..21}
  do curl --header "X-Forwarded-For: 123.45.67.1" 0.0.0.0:8000
done
# try either curl -X POST 0.0.0.0:8000/unban/123.45.67.0 or (/24)
curl -X POST 0.0.0.0:8000/unban/24
echo "unban applied"
curl --header "X-Forwarded-For: 192.168.0.2" 0.0.0.0:8000
