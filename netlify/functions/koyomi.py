import json
import ephem
import datetime
import pytz

def format_time(dt):
    """時刻をHH:MM形式の文字列にフォーマットするヘルパー関数"""
    if dt is None:
        return "--:--"
    return dt.strftime('%H:%M')

def handler(event, context):
    """
    Netlifyから呼び出されるメインの関数。
    暦の情報を計算し、JSON形式で返す。
    """
    try:
        # --- 基本設定 ---
        locations = [
            {"name": "札幌", "lat": "43.06", "lon": "141.35"},
            {"name": "仙台", "lat": "38.27", "lon": "140.87"},
            {"name": "新潟", "lat": "37.90", "lon": "139.02"},
            {"name": "東京", "lat": "35.69", "lon": "139.69"},
            {"name": "名古屋", "lat": "35.18", "lon": "136.91"},
            {"name": "大阪", "lat": "34.69", "lon": "135.52"},
            {"name": "福岡", "lat": "33.61", "lon": "130.42"},
            {"name": "那覇", "lat": "26.21", "lon": "127.68"},
        ]
        sekki_list = ['春分','清明','穀雨','立夏','小満','芒種','夏至','小暑','大暑','立秋','処暑','白露','秋分','寒露','霜降','立冬','小雪','大雪','冬至','小寒','大寒','立春','雨水','啓蟄']
        kou_data = {
            '雀始巣': 'すずめはじめてすくう', '桜始開': 'さくらはじめてひらく', '雷乃発声': 'かみなりすなわちこえをはっす', '玄鳥至': 'つばめきたる', '鴻鴈北': 'こうがんかえる', '虹始見': 'にじはじめてあらわる', '葭始生': 'あしはじめてしょうず', '霜止出苗': 'しもやんでなえいずる', '牡丹華': 'ぼたんはなさく', '蛙始鳴': 'かわずはじめてなく', '蚯蚓出': 'みみずいずる', '竹笋生': 'たけのこしょうず', '蚕起食桑': 'かいこおきてくわをはむ', '紅花栄': 'べにはなさかう', '麦秋至': 'むぎのときいたる', '螳螂生': 'かまきりしょうず', '腐草為蛍': 'くされたるくさほたるとなる', '梅子黄': 'うめのみきばむ', '乃東枯': 'なつかれくさかるる', '菖蒲華': 'あやめはなさく', '半夏生': 'はんげしょうず', '温風至': 'あつかぜいたる', '蓮始開': 'はすはじめてひらく', '鷹乃学習': 'たかすなわちわざをなす', '桐始結花': 'きりはじめてはなをむすぶ', '土潤溽暑': 'つちうるおうてむしあつし', '大雨時行': 'たいうときどきにふる', '涼風至': 'すずかぜいたる', '寒宙鳴': 'ひぐらしなく', '蒙霧升降': 'ふかききりまとう', '綿析開': 'わたのはなしべひらく', '天地始粛': 'てんちはじめてさむし', '禾乃登': 'こくものすなわちみのる', '草露白': 'くさのつゆしろし', '鶺鴒鳴': 'せきれいなく', '玄鳥去': 'つばめさる', '雷乃収声': 'かみなりすなわちこえをおさむ', '蟄虫培戸': 'むしかくれてとをふさぐ', '水始涸': 'みずはじめてかる', '鴻鴈来': 'こうがんきたる', '菊花開': 'きくのはなひらく', '蟋蟀在戸': 'きりぎりすとにあり', '霜始降': 'しもはじめてふる', '霎時施': 'こさめときどきふる', '楓蔦黄': 'もみじつたきばむ', '山茶始開': 'つばきはじめてひらく', '地始凍': 'ちはじめてこおる', '金盞香': 'きんせんかさく', '虹蔵不見': 'にじかくれてみえず', '朔風払葉': 'きたかぜこのはをはらう', '橘始黄': 'たちばなはじめてきばむ', '閉塞成冬': 'そらさむくふゆとなる', '熊蟄穴': 'くまあなにこもる', '硫魚群': 'さけのうおむらがる', '乃東生': 'なつかれくさしょうず', '麋角解': 'さわしかのつのおつる', '雪下出麦': 'ゆきわたりてむぎいずる', '芹乃栄': 'せりすなわちさかう', '水泉動': 'しみずあたたかをふくむ', '雉始': 'きじはじめてなく', '款冬華': 'ふきのはなさく', '水沢腹堅': 'さわみずこおりつめる', '範始乳': 'にわとりはじめてとやにつく', '東風解凍': 'はるかぜこおりをとく', '黄鶯遵純': 'うぐいすなく', '魚上氷': 'うおこおりをいずる', '土脉潤起': 'つちのしょううるおいおこる', '霞始靆': 'かすみはじめてたなびく', '草木萌動': 'そうもくめばえいずる', '蟄虫啓戸': 'すごもりむしとをひらく', '桃始笑': 'ももはじめてさく', '菜虫化蝶': 'なむしちょうとなる'
        }
        kou_list = list(kou_data.keys())

        # --- 計算処理 ---
        JST = pytz.timezone('Asia/Tokyo')
        now_jst = datetime.datetime.now(JST)
        
        tokyo_loc = locations[3]
        obs = ephem.Observer()
        obs.lon = tokyo_loc['lon']
        obs.lat = tokyo_loc['lat']
        obs.elevation = 0
        obs.date = now_jst

        sun = ephem.Sun(obs)
        sun_hlon_deg = ((sun.hlon + ephem.pi) % (2 * ephem.pi)) * 180 / ephem.pi
        sekki_index = int(sun_hlon_deg / 15)
        kou_index = int(sun_hlon_deg / 5)
        kou_name = kou_list[kou_index]
        kou_reading = kou_data[kou_name]

        time_for_moon_age = now_jst.replace(hour=20, minute=0, second=0, microsecond=0)
        obs.date = time_for_moon_age
        prev_new_moon = ephem.previous_new_moon(obs.date)
        moon_age_delta = obs.date.datetime() - prev_new_moon.datetime()
        moon_age = moon_age_delta.days + float(moon_age_delta.seconds) / 86400

        city_data = []
        start_of_day_jst = now_jst.replace(hour=0, minute=0, second=0, microsecond=0)
        
        for loc in locations:
            obs.lon = loc['lon']
            obs.lat = loc['lat']
            obs.date = start_of_day_jst
            
            obs.horizon = '-0:34' 
            sunrise_utc = obs.next_rising(ephem.Sun(), use_center=True).datetime()
            sunset_utc = obs.next_setting(ephem.Sun(), use_center=True).datetime()

            obs.horizon = '0' 
            try:
                moonrise_utc = obs.next_rising(ephem.Moon()).datetime()
                moonrise_jst = moonrise_utc.astimezone(JST)
            except (ephem.AlwaysUpError, ephem.NeverUpError):
                moonrise_jst = None
            
            try:
                moonset_utc = obs.next_setting(ephem.Moon()).datetime()
                moonset_jst = moonset_utc.astimezone(JST)
            except (ephem.AlwaysUpError, ephem.NeverUpError):
                moonset_jst = None

            city_data.append({
                "name": loc['name'],
                "sunrise": format_time(sunrise_utc.astimezone(JST)),
                "sunset": format_time(sunset_utc.astimezone(JST)),
                "moonrise": format_time(moonrise_jst),
                "moonset": format_time(moonset_jst)
            })

        response_data = {
            "date": now_jst.strftime('%Y年%m月%d日'),
            "sekki": sekki_list[sekki_index],
            "kou": f"{kou_name}（{kou_reading}）",
            "moon_age": f"{moon_age:.1f}",
            "cities": city_data
        }

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*", # どのサイトからのアクセスも許可する設定
            },
            "body": json.dumps(response_data, ensure_ascii=False)
        }

    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "An internal error occurred"})
        }

