def Setcookie(cookie_str):
    cookies = {}
    for line in cookie_str.split(';'):
        name, value = line.strip().split('=', 1)
        cookies[name] = value
    return cookies
