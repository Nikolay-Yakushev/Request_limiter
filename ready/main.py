import argparse
import ipaddress
import time
from typing import ClassVar
from flask import Flask, request, abort, jsonify

parser = argparse.ArgumentParser(description='request limiter server')
parser.add_argument('-w', '--time_window',
                    help="""Set time-window. Within this window requests will be accepted/.
                      if time window exceeds, it will be restarted""",
                    type=float, default=60.0)

parser.add_argument('-l', '--limit', help="allowed request amount", type=int, default=100)
parser.add_argument('-m', '--mask', help="set subnet mask", type=str, default='24')
parser.add_argument('-b', '--ban_duration', help="duration of a ban in seconds", type=float, default=120.0)
parser.add_argument('--port', help="time of a ban ", type=int, default=8080)
parser.add_argument('--host', help="time of a ban ", type=str, default='0.0.0.0')
args = parser.parse_args()

app = Flask(__name__)
subnet_counter = {}
banned_lst = []  # [('1.2.3.x', unban_time=1231253453.23423523), ('100.100.100.x', unban_time=1231253953.945645)]
start_t = time.time()


def count_subnet(subnet: str):
    # subnet= 123.45.67.0
    if subnet not in subnet_counter:
        subnet_counter[subnet] = 1
    else:
        subnet_counter[subnet] += 1

    return subnet_counter[subnet]


def get_subnet(ip_addr: str, mask: str):
    net = ipaddress.ip_network(f'{ip_addr}/{mask}', strict=False)
    subnet = net.network_address
    return subnet


def is_banned(subnet: ClassVar):
    # subnet ip subnet mask
    # Example: ip=123.45.67.89/24
    #           subnet= 123.45.67.0
    for snet, unban_t in banned_lst:
        if snet == subnet:
            return True, unban_t
    return False, None


def get_ip_addr():
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    return ip


@app.route('/', methods=["GET"])
def handle_request():
    ip_addr = get_ip_addr()
    # time when service has been started
    global start_t
    # current time
    now_t = time.time()  # in sec

    # elapsed = how much time has passed since server has been started
    elapsed = now_t - start_t  # in sec
    if elapsed >= args.time_window:
        global subnet_counter
        subnet_counter = {}
        start_t = now_t
    # id_addr = 123.45.67.178, mask = /24 or 255.255.255.0, subnet = 123.45.67.0
    subnet = get_subnet(ip_addr, args.mask)
    banTrue, unban_t = is_banned(subnet)
    if banTrue:
        if unban_t - now_t > 0:
            return abort(429, f'{unban_t - now_t}')  # 12307435234.0423423 - 12334534534.032423 => 11.5
        else:
            banned_lst.remove((subnet, unban_t))
            count_subnet(subnet)
            return 'ok'
    else:
        cnt = count_subnet(subnet)  # {subnet: count} +1
        if cnt > args.limit:
            banned_lst.append((subnet, now_t + args.ban_duration))
            return abort(429, f'{args.ban_duration}')  # example:args.ban_duration 120.0 in seconds

        return 'ok'


@app.errorhandler(429)
def handle_exception(error):
    response = error.get_response()
    response.headers['Retry-After'] = error.description
    return response


# null ban time using prefix
@app.route('/unban/<prefix>',
           methods=['POST'])
# id_addr = 123.45.67.178,
# mask = /24 or (255.255.255.0),
# subnet prefix = 123.45.67.0
# prefix  = /24
def change_limiter(prefix):
    if len(banned_lst) == 0:
        return jsonify({'status': 'ban list is empty'})
    for subnet, unban_t in banned_lst:
        # it's possible to unlock ip subnet using ip's subnet mask or prefix
        # Example: either /24 or 123.45.67.0
        if str(subnet) == prefix or args.mask == prefix:
            banned_lst.remove((subnet, unban_t))
            return jsonify({'status ': 'null'})
        else:
            return jsonify({'status': 'wrong. type entire subnet like 123.45.67.0'})


if __name__ == '__main__':
    import argparse

    app.run(host=args.host, port=args.port)
