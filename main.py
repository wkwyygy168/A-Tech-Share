import requests
import base64
import yaml
import re

def universal_mirror_factory():
    # 老大提供的 100+ 核心源列表
    sources = [
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml",
        "https://raw.githubusercontent.com/Alien136/clash-proxies/main/clash.yaml",
        "https://raw.githubusercontent.com/AzadNetCH/Clash/main/AzadNet.txt",
        "https://raw.githubusercontent.com/Domparire/Clash/main/Clash.yaml",
        "https://raw.githubusercontent.com/FMYX/FreeNode/main/node.txt",
        "https://raw.githubusercontent.com/Flikify/Free-Node/main/clash.yaml",
        "https://raw.githubusercontent.com/Flikify/Free-Node/main/v2ray.txt",
        "https://raw.githubusercontent.com/Fndroid/clash_config/master/v2ray.txt",
        "https://raw.githubusercontent.com/Jsnzkpg/Jsnzkpg/Jsnzkpg/clash/clash.yaml",
        "https://raw.githubusercontent.com/LalatinaHub/Mineral/master/Clash/Config.yaml",
        "https://raw.githubusercontent.com/LonUp/NodeList/main/NodeList",
        "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/v2ray/all_sub.txt",
        "https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber-telegram/master/collected-proxies/clash-meta/all.yaml",
        "https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber-telegram/master/collected-proxies/row-url/all.txt",
        "https://raw.githubusercontent.com/NiceVPN123/NiceVPN/main/Clash.yaml",
        "https://raw.githubusercontent.com/NiceVPN123/NiceVPN/main/utils/pool/output.yaml",
        "https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub",
        "https://raw.githubusercontent.com/Pawpieee/Free-Nodes/main/node.txt",
        "https://raw.githubusercontent.com/Pawpieee/Free-Proxies/main/sub/sub_merge.txt",
        "https://raw.githubusercontent.com/Q3dlaXpoaQ/V2rayN_Clash_Node_Getter/main/APIs/sc0.yaml",
        "https://raw.githubusercontent.com/Q3dlaXpoaQ/V2rayN_Clash_Node_Getter/main/APIs/sc1.yaml",
        "https://raw.githubusercontent.com/Q3dlaXpoaQ/V2rayN_Clash_Node_Getter/main/APIs/sc2.yaml",
        "https://raw.githubusercontent.com/Q3dlaXpoaQ/V2rayN_Clash_Node_Getter/main/APIs/sc3.yaml",
        "https://raw.githubusercontent.com/Rea1l/V2ray-Configs/main/V2ray-configs.txt",
        "https://raw.githubusercontent.com/Ruk1ng001/freeSub/main/clash.yaml",
        "https://raw.githubusercontent.com/SnapdragonLee/SystemProxy/master/dist/clash_config.yaml",
        "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/main/all_configs.txt",
        "https://raw.githubusercontent.com/Subscrazy/Subscrazy/master/sub",
        "https://raw.githubusercontent.com/WilliamStar007/ClashX-V2Ray-TopFreeProxy/main/combine/v2ray.config.txt",
        "https://raw.githubusercontent.com/acymz/AutoVPN/main/data/V2.txt",
        "https://raw.githubusercontent.com/anaer/Sub/main/clash.yaml",
        "https://raw.githubusercontent.com/anaer/Sub/master/v2ray.txt",
        "https://raw.githubusercontent.com/barry-far/V2ray-Config/main/Sub1.txt",
        "https://raw.githubusercontent.com/barry-far/V2ray-Config/main/Sub2.txt",
        "https://raw.githubusercontent.com/chengaopan/AutoMergePublicNodes/master/list.yml",
        "https://raw.githubusercontent.com/colatiger/v2ray-nodes/master/updates/v2ray.txt",
        "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/main/all_extracted_configs.txt",
        "https://raw.githubusercontent.com/erick-wan/AutoSubscribe/master/subscribe/clash.yaml",
        "https://raw.githubusercontent.com/ermaozi/get_node/main/subscribe/v2ray.txt",
        "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/clash.yml",
        "https://raw.githubusercontent.com/firefoxmmx2/v2rayshare_subcription/main/subscription/clash_sub.yaml",
        "https://raw.githubusercontent.com/free18/v2ray/main/c.yaml",
        "https://raw.githubusercontent.com/freefq/free/master/v2ray",
        "https://raw.githubusercontent.com/go4sharing/sub/main/sub.yaml",
        "https://raw.githubusercontent.com/lagzian/SS-Collector/main/SS/TrinityBase",
        "https://raw.githubusercontent.com/lagzian/SS-Collector/main/SS/VM_TrinityBase",
        "https://raw.githubusercontent.com/lagzian/SS-Collector/main/SS/trinity_clash.yaml",
        "https://raw.githubusercontent.com/learnhard-cn/free_nodes/master/v2ray.txt",
        "https://raw.githubusercontent.com/mahdibland/SSAggregator/master/sub/sub_merge.txt",
        "https://raw.githubusercontent.com/mahdibland/SSAggregator/master/sub/sub_merge_yaml.yml",
        "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity.yml",
        "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge_base64.txt",
        "https://raw.githubusercontent.com/mfbpn/tg_mfbpn_sub/main/trial.yaml",
        "https://raw.githubusercontent.com/mfuu/v2ray/master/clash.yaml",
        "https://raw.githubusercontent.com/mianfeifq/share/main/data",
        "https://raw.githubusercontent.com/mianfeifq/share/main/data.txt",
        "https://raw.githubusercontent.com/mgit0001/test_clash/main/heima.txt",
        "https://raw.githubusercontent.com/mksshare/SSR-V2ray-Trojan-Clash-subscription/main/Clash.yaml",
        "https://raw.githubusercontent.com/nodefree/free-nodes/main/nodes/nodes.txt",
        "https://raw.githubusercontent.com/openRunner/clash-freenode/main/clash.yaml",
        "https://raw.githubusercontent.com/openit/freenode/master/v2ray.txt",
        "https://raw.githubusercontent.com/oslook/clash-freenode/main/clash.yaml",
        "https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list.yml",
        "https://raw.githubusercontent.com/peacefish/nodefree/main/sub/proxy_cf.yaml",
        "https://raw.githubusercontent.com/r00t-shell/v2ray-subscription/main/subs/v2ray",
        "https://raw.githubusercontent.com/ripaojiedian/freenode/main/clash",
        "https://raw.githubusercontent.com/roster0/v2ray/main/list",
        "https://raw.githubusercontent.com/shahidbhutta/Clash/main/Router",
        "https://raw.githubusercontent.com/snakem982/Proxies/main/clash.yaml",
        "https://raw.githubusercontent.com/snakem982/proxypool/main/source/all.txt",
        "https://raw.githubusercontent.com/snakem982/proxypool/main/source/clash-meta-2.yaml",
        "https://raw.githubusercontent.com/snakem982/proxypool/main/source/clash-meta.yaml",
        "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/mixed",
        "https://raw.githubusercontent.com/ssrsub/ssr/master/v2ray",
        "https://raw.githubusercontent.com/suda/v2ray-subscribe/main/sub/sub.txt",
        "https://raw.githubusercontent.com/tazzmaniac/Clash/main/clash.yaml",
        "https://raw.githubusercontent.com/tbbatbb/Proxy/master/dist/v2ray.config.txt",
        "https://raw.githubusercontent.com/tianfong/free-nodes/main/node.txt",
        "https://raw.githubusercontent.com/ts-sf/fly/main/clash",
        "https://raw.githubusercontent.com/ts-sf/fly/main/v2",
        "https://raw.githubusercontent.com/v2ray-links/v2ray-free/master/v2ray",
        "https://raw.githubusercontent.com/v2rayse/free-node/main/v2ray.txt",
        "https://raw.githubusercontent.com/vless-js/v2ray-free/main/v2ray",
        "https://raw.githubusercontent.com/vorz1k/v2box/main/supreme_vpns_1.txt",
        "https://raw.githubusercontent.com/vpei/Free-Node-Merge/main/o/node.txt",
        "https://raw.githubusercontent.com/vpei/free-node/master/v2ray.txt",
        "https://raw.githubusercontent.com/vxiaov/free_proxies/main/clash/clash.provider.yaml",
        "https://raw.githubusercontent.com/vxiaov/free_proxies/main/links.txt",
        "https://raw.githubusercontent.com/w1770946466/Auto_Node/main/node.txt",
        "https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_maintenance_Clash.yaml",
        "https://raw.githubusercontent.com/xrayfree/free-ssr-ss-v2ray-vpn-clash/main/clash.yaml",
        "https://raw.githubusercontent.com/xiaoji235/airport-free/main/clash/naidounode.txt",
        "https://raw.githubusercontent.com/xiaoji235/airport-free/main/v2ray.txt",
        "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/mix",
        "https://raw.githubusercontent.com/yugogo/clash_config/main/clash.yaml",
        "https://raw.githubusercontent.com/yuandongying/free-nodes/main/v2ray.txt",
        "https://raw.githubusercontent.com/yorkLiu/FreeV2RayNode/main/v2ray.txt",
        "https://raw.githubusercontent.com/zhangkaiitugithub/passcro/main/speednodes.yaml",
        "https://t.me/s/C_137_channel",
        "https://t.me/s/Outline_Vpn",
        "https://t.me/s/V2List",
        "https://t.me/s/daily_free_nodes",
        "https://t.me/s/free_v2ray_config",
        "https://t.me/s/ssrList",
        "https://t.me/s/v2ray_free_conf",
        "https://t.me/s/v2rayfree",
        "https://t.me/s/vmess_vless_ss",
        "https://t.me/s/vpn_v2ray_vpn"
    ]
    
    final_proxies = []
    txt_links = []
    seen_ips = set()

    for url in sources:
        try:
            print(f"🚀 正在处理: {url}")
            res = requests.get(url, timeout=15)
            content = res.text
            
            if ".yaml" in url or ".yml" in url or "clash" in url.lower():
                try:
                    data = yaml.safe_load(content)
                    if isinstance(data, dict) and 'proxies' in data:
                        for p in data['proxies']:
                            fp = f"{p.get('server')}:{p.get('port')}"
                            if fp not in seen_ips:
                                seen_ips.add(fp)
                                final_proxies.append(p)
                except Exception: pass
            else:
                decoded = content
                if "://" not in content[:50]:
                    try:
                        decoded = base64.b64decode(content + "==").decode('utf-8', errors='ignore')
                    except Exception: pass
                for line in decoded.splitlines():
                    if "://" in line:
                        core = line.split('#')[0]
                        if core not in seen_ips:
                            seen_ips.add(core)
                            txt_links.append(line)
        except Exception: pass

    # 核心：必须存成洗货工具能认的文件名
    with open("nodes.yaml", "w", encoding="utf-8") as f:
        yaml.dump({"proxies": final_proxies}, f, allow_unicode=True, sort_keys=False)
    with open("nodes.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(txt_links))
    print(f"✨ 原始进货完成: {len(seen_ips)}")

if __name__ == "__main__":
    universal_mirror_factory()
