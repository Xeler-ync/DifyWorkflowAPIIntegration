# -*- coding: utf-8 -*-
# This script generates ~3000 synthetic Chinese hotel-domain sentences (corpus.txt)
# and 100 FAQ items (faq.csv). Safe to rerun; it overwrites the files.

import os, random, csv

BASE = os.path.dirname(__file__)
DATA = os.path.join(BASE, "..", "data")

random.seed(42)

def ensure_dir(p):
    if not os.path.exists(p):
        os.makedirs(p)

def write_corpus(path, lines):
    with open(path, "w", encoding="utf-8") as f:
        for ln in lines:
            ln = " ".join(ln.split())
            f.write(ln.strip() + "\n")

def write_faq(path, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id","question","answer"])
        for i,(q,a) in enumerate(rows, start=1):
            w.writerow([i,q,a])

def main():
    ensure_dir(DATA)

    times = ["6 点","7 点","8 点","9 点","10 点","12 点","14 点","15 点","22 点"]
    yesno  = ["可以","可以的","可以安排","可根据房态","暂不可以","目前不支持"]
    req    = ["需 提前 预约","需 视 房态","可能 产生 费用","建议 提前 联系 前台","需 提供 证件","请 至 前台 办理"]
    facilities = ["健身房","游泳池","自助早餐","停车场","充电桩","洗衣房","商务中心","前台","餐厅","大堂吧"]
    pos = ["一 楼","二 楼","三 楼","地下一 层","B1 层","B2 层","东侧","西侧","北侧","南侧"]
    policy = ["免费","收费","需 押金","需 预授权","凭 房卡 进入","住客 专享","限 时 段 开放"]
    room = ["标准间","大床房","双床房","亲子房","无烟房","行政房","豪华房","套房"]
    actions = [
        "办理 入住","办理 退房","延迟 退房","提前 入住","加床","开发票","行李 寄存","叫醒 服务",
        "接机 服务","加早餐","免费 取消","变更 预订","升级 房型"
    ]
    who = ["住店 客人","外宾 客人","带 儿童 的 家庭","商务 出行 客人","长住 客人"]
    ask = [
        "是否 可以","怎么 办理","是否 收费","在哪里","开放 时间 是 多少","能否 预约",
        "最早 可以 几点","最晚 可以 几点","是否 需要 押金","是否 可以 退款"
    ]

    corpus = []

    for fac in facilities:
        for p in policy:
            corpus.append(f"本 酒店 {fac} {p}")
        for place in pos:
            corpus.append(f"{fac} 位于 {place}")

    for fac in ["自助早餐","健身房","游泳池"]:
        for t1, t2 in [("6 点","22 点"), ("7 点","10 点"), ("8 点","21 点")]:
            corpus.append(f"{fac} 开放 时间 为 {t1} 至 {t2}")
            corpus.append(f"{fac} 营业 时间 {t1} 到 {t2}")

    for act in actions:
        for r in req:
            corpus.append(f"{act} {r}")
        for y in yesno:
            corpus.append(f"{act} {y}")

    for r in room:
        for y in yesno:
            corpus.append(f"{r} 预订 {y}")
        for p in policy:
            corpus.append(f"{r} {p}")
        for a in actions[:6]:
            corpus.append(f"{r} 可 {a}")

    for w in who:
        for act in actions:
            corpus.append(f"{w} 可 {act}")
        for fac in facilities:
            corpus.append(f"{w} 可 使用 {fac}")

    for a in ask:
        for target in actions + facilities:
            corpus.append(f"{target} {a}")
    for t in times:
        corpus.append(f"标准 入住 时间 为 14 点")
        corpus.append(f"标准 退房 时间 为 12 点")
        corpus.append(f"早餐 时间 为 7 点 至 10 点")
        corpus.append(f"健身房 开放 至 22 点")

    for fac in facilities:
        for place in pos:
            for p in ["免费", "收费"]:
                corpus.append(f"{fac} 位于 {place} 对 住店 客人 {p}")
    for act in ["延迟 退房","提前 入住"]:
        for cond in ["视 房态","可能 收费","需 提前 申请","可 免费"]:
            corpus.append(f"{act} {cond}")

    import random
    extra = []
    for _ in range(1200):
        fac = random.choice(facilities)
        a = random.choice(actions)
        r = random.choice(req)
        extra.append(f"{fac} {a} {r}")
    corpus.extend(extra)

    seen = set()
    corpus_unique = []
    for s in corpus:
        if s not in seen:
            corpus_unique.append(s)
            seen.add(s)

    target = 3000
    if len(corpus_unique) > target:
        corpus_unique = corpus_unique[:target]
    else:
        while len(corpus_unique) < target:
            fac = random.choice(facilities)
            a = random.choice(actions)
            t1, t2 = random.choice([("6 点","22 点"),("7 点","10 点"),("8 点","21 点")])
            corpus_unique.append(f"{fac} {a} 时间 为 {t1} 至 {t2}")

    faq_pairs = [
        ("入住时间是几点","标准入住时间为14:00，如需提前入住请联系前台并视房态而定。"),
        ("最晚几点退房","标准退房时间为12:00，如需延迟请与前台沟通可能产生费用。"),
        ("是否提供早餐","酒店提供自助早餐，时间为07:00-10:00，地点在一楼餐厅。"),
        ("停车是否收费","住店客人可免费停车，离店后按标准收费。"),
        ("可以加床吗","可提供加床服务，需额外收费，请在预订时备注需求。"),
        ("可以开具发票吗","可以开具增值税普通发票，请提供发票抬头与税号。"),
        ("是否有健身房","有，开放时间06:00-22:00。"),
        ("是否有游泳池","当前根据检修安排开放，具体请咨询前台。"),
        ("是否提供接机服务","可提供接机服务，需至少提前一天预约并确认费用。"),
        ("是否可以提前入住","可根据当日房态安排，建议提前联系前台。"),
        ("办理入住需要什么证件","需携带有效身份证件，外宾需提供有效护照。"),
        ("是否有无烟房","有无烟楼层，可在预订时备注。"),
        ("行李可以寄存吗","可在前台免费寄存当日行李，长时寄存请咨询。"),
        ("是否提供叫醒服务","可通过客房电话或前台预约叫醒服务。"),
        ("早餐可以打包吗","可，提前与餐厅说明。"),
        ("是否提供洗衣服务","二楼东侧设有自助洗衣房，另提供付费干洗。"),
        ("是否支持无接触入住","提供线上办理与自助机办理，具体以当日房态为准。"),
        ("是否有亲子房","有亲子主题房，请联系前台确认房态。"),
        ("是否有充电桩","地下车库B2层设有充电桩，住客凭房卡进出。"),
        ("能否接待外宾","可以，按规定登记办理。"),
        ("能否开具专票","可开具增值税专用发票，需提供完整资质。"),
        ("押金如何收取","入住时将进行预授权，退房后自动解除。"),
        ("是否可以免费取消订单","需参考预订条款与套餐规则。"),
        ("发票如何索取","可在退房时至前台或通过邮件获取电子发票。"),
        ("是否提供婴儿床","数量有限，需提前预约。"),
        ("加早餐如何收费","以当日餐价为准，住客可享优惠。"),
        ("是否有商务中心","一楼商务中心提供打印复印与会议室预订。"),
        ("是否提供延迟退房","视房态可申请，可能产生半天或按小时计费。"),
        ("是否可以带宠物","暂不接待宠物入住，敬请谅解。"),
        ("Wi-Fi如何连接","酒店提供免费Wi‑Fi，入住后获取房间专属密码。"),
    ]

    variants_q = [
        "可以提前入住吗","能否延迟退房","早餐时间是几点","停车是否免费",
        "健身房开放到几点","可否加床","能否开具发票","是否提供接机",
        "是否有亲子房","是否有无烟房","能否行李寄存","是否可叫醒服务"
    ]
    variants_a = [
        "需视当日房态安排，建议提前联系前台。",
        "标准时间为上述说明，若需变更请咨询前台。",
        "服务可能产生费用，请以当日价格为准。",
        "相关设施位置与开放时间以酒店公告为准。"
    ]

    while len(faq_pairs) < 100:
        q = random.choice(variants_q)
        a = random.choice(variants_a)
        faq_pairs.append((q,a))

    corpus_path = os.path.join(DATA, "corpus.txt")
    faq_path = os.path.join(DATA, "faq.csv")
    write_corpus(corpus_path, corpus_unique)
    write_faq(faq_path, faq_pairs[:100])

    print(f"Wrote corpus: {corpus_path} ({len(corpus_unique)} lines)")
    print(f"Wrote FAQ:    {faq_path} ({min(100, len(faq_pairs))} rows)")

if __name__ == "__main__":
    main()
