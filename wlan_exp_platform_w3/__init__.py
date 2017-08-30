import wlan_exp.platform as wlan_exp_platform

w3_platform = wlan_exp_platform.WlanExpPlatform(
    name = 'WARP v3', 
    sn_regexp = '[Ww]3-a-(?P<sn>\d+)',
    sn_str_fmt = 'W3-a-{0:05}'
)

wlan_exp_platform.register_platform(w3_platform)
