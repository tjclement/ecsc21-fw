# Privkey is (3152717306533824157420536322537714593453118808047298838197, 3033655168601492576945143378005671139705433121922877345289)
# print("WARNING: create_flag is still present in firmware!")
#
#
# def create_flag(challenge, points):
#     n, e = (
#         3152717306533824157420536322537714593453118808047298838197,
#         3033655168601492576945143378005671139705433121922877345289,
#     )
#     import rsa, binascii

#     return "CTF{%s}" % binascii.hexlify(rsa.encrypt(n, e, "%s,%d" % (challenge, points))).decode()


def parse_flag(flag):
    import binascii, ure, rsa, valuestore

    match = ure.match("CTF\{(.*)\}", flag)
    try:
        contents = match.group(1)
    except:
        del binascii, ure, rsa, valuestore
        return None

    n, e = (3152717306533824157420536322537714593453118808047298838197, 65537)
    try:
        decrypted = rsa.decrypt(n, e, binascii.unhexlify(contents)).decode()
    except:
        del binascii, ure, rsa, valuestore
        return None
    try:
        match = ure.match("(\d[a-z]),(\d\d\d)", decrypted)
        challenge, points = match.group(1), int(match.group(2))
    except:
        del binascii, ure, rsa, valuestore
        return None

    del binascii, ure, rsa, valuestore
    return challenge, points


def get_found_flags():
    import valuestore

    flag_dict = valuestore.load(keyname="flags")
    del valuestore

    found_flags = {}

    for flag_object in flag_dict.values():
        try:
            challenge, points = parse_flag(flag_object["flag"])
            found_flags[challenge] = points
        except Exception:
            pass

    return found_flags


def submit_flag(flag):
    result = parse_flag(flag)
    if result is None:
        print("This is not a correct flag!")
        return
    try:
        challenge, points = result
    except:
        print("This is not a correct flag!")
        return

    import valuestore

    flag_dict = valuestore.load(keyname="flags")
    flag_dict[challenge] = {"points": points, "flag": flag}
    valuestore.save(keyname="flags", value=flag_dict)
    print("Successfully submitted your flag!")

    import machine

    total_points = 0
    for flag_object in flag_dict.values():
        try:
            chall, pts = parse_flag(flag_object["flag"])
            total_points += pts
        except:
            pass

    if not machine.nvs_getint("system", "ctf_done"):
        if total_points == 2100:
            machine.nvs_setint("system", "ctf_done", 1)
            import easydraw, time, system

            time.sleep(1)
            easydraw.messageCentered("Congratulations!\n\n\n\n\nYou have finished all challenges!")
            time.sleep(3)
            system.home()
    del valuestore
