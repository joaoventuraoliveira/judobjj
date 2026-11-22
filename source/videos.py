"""Vídeos oficiais: série KODOKAN × IJF ACADEMY "100 Techniques", publicada no canal
oficial do Kodokan no YouTube (canal UCtF6tu7GuZYkZzht5MIv8UQ). IDs coletados em
22/11/2026 por busca na web; cada título confere com o nome da técnica."""

KODOKAN_CHANNEL = 'https://www.youtube.com/@KODOKANJUDO'

# grupo → [(nome IJF, kanji, id do vídeo)]
GROUPS = [
    ('Te-waza (técnicas de braço)', 'nage', [
        ('Seoi-nage', '背負投', 'zIq0xI0ogxk'), ('Ippon-seoi-nage', '一本背負投', 'FQnOlCxo4oI'),
        ('Seoi-otoshi', '背負落', 'vu1TMVNnq34'), ('Tai-otoshi', '体落', '4x6S3Q-Ktv8'),
        ('Kata-guruma', '肩車', 'cnHRhSy8yi4'), ('Sukui-nage', '掬投', 'vU6aJ2kFxoI'),
        ('Obi-otoshi', '帯落', 'ff8U2TVZIYI'), ('Uki-otoshi', '浮落', '6H5tmncOY4Q'),
        ('Sumi-otoshi', '隅落', 'lLU9wv52ni0'), ('Yama-arashi', '山嵐', 'MGlyKmSuzdc'),
        ('Obi-tori-gaeshi', '帯取返', 'bpc82SrunUU'), ('Morote-gari', '双手刈', 'BHLQS4K85bs'),
        ('Kuchiki-taoshi', '朽木倒', 'ZNL47q1aJNY'), ('Kibisu-gaeshi', '踵返', 'tJylJYfBliA'),
        ('Uchi-mata-sukashi', '内股すかし', 'V-RS3uhtVWM'), ('Ko-uchi-gaeshi', '小内返', '_MWAdYi_LC4')]),
    ('Koshi-waza (técnicas de quadril)', 'nage', [
        ('Uki-goshi', '浮腰', 'bPKwtB4lyOQ'), ('O-goshi', '大腰', 'yhu1mfy2vJ4'),
        ('Koshi-guruma', '腰車', 'SU7Id6uVJ44'), ('Tsurikomi-goshi', '釣込腰', 'McfzA0yRVt4'),
        ('Sode-tsurikomi-goshi', '袖釣込腰', 'QsmAxpmYLOI'), ('Harai-goshi', '払腰', 'qTo8HlAAkOo'),
        ('Tsuri-goshi', '釣腰', '51Htlp7xEvE'), ('Hane-goshi', '跳腰', 'M9_7De6A1kk'),
        ('Utsuri-goshi', '移腰', '4pQd_bEnlf0'), ('Ushiro-goshi', '後腰', 'ORIYstuxYT8')]),
    ('Ashi-waza (técnicas de perna)', 'nage', [
        ('De-ashi-harai', '出足払', '4BUUvqxi_Kk'), ('Hiza-guruma', '膝車', 'JPJx9-oAVns'),
        ('Sasae-tsurikomi-ashi', '支釣込足', '699i--pvYmE'), ('O-soto-gari', '大外刈', 'c-A_nP7mKAc'),
        ('O-uchi-gari', '大内刈', '0itJFhV9pDQ'), ('Ko-soto-gari', '小外刈', 'jeQ541ScLB4'),
        ('Ko-uchi-gari', '小内刈', '3Jb3tZvr9Ng'), ('Okuri-ashi-harai', '送足払', 'nw1ZdRjrdRI'),
        ('Uchi-mata', '内股', 'iUpSu5J-bgw'), ('Ko-soto-gake', '小外掛', '8b6kY4s4zH4'),
        ('Ashi-guruma', '足車', 'ROeayhvom9U'), ('Harai-tsurikomi-ashi', '払釣込足', 'gGPXvWL8VbE'),
        ('O-guruma', '大車', 'SnZciTAY9vc'), ('O-soto-guruma', '大外車', '92KbCm6pQeI'),
        ('O-soto-otoshi', '大外落', '2DsVvDw7b8g'), ('Tsubame-gaeshi', '燕返', 'GwweWqqFB5g'),
        ('O-soto-gaeshi', '大外返', '8ZjM3X_EANo'), ('O-uchi-gaeshi', '大内返', 'dCyZTXyjIXE'),
        ('Hane-goshi-gaeshi', '跳腰返', '9bZAZSBtnGs'), ('Harai-goshi-gaeshi', '払腰返', '4U3It-7PPsc'),
        ('Uchi-mata-gaeshi', '内股返', 'Sy6sLWxkWYw')]),
    ('Ma-sutemi-waza (sacrifício de costas)', 'nage', [
        ('Tomoe-nage', '巴投', '880WbHvHv6A'), ('Sumi-gaeshi', '隅返', '5VhduA5xkbA'),
        ('Hikikomi-gaeshi', '引込返', '92zUYWBp5N8'), ('Tawara-gaeshi', '俵返', 'TmTWgrmViZc'),
        ('Ura-nage', '裏投', 'Fgi9b8DJ5sQ')]),
    ('Yoko-sutemi-waza (sacrifício de lado)', 'nage', [
        ('Yoko-otoshi', '横落', 'MnNG67pF_a0'), ('Tani-otoshi', '谷落', '3b9Me3Fohpk'),
        ('Hane-makikomi', '跳巻込', '6CRBGLGz9j8'), ('Soto-makikomi', '外巻込', 'bWG9O1BVKtQ'),
        ('Uchi-makikomi', '内巻込', '5BowcjduxVc'), ('Uki-waza', '浮技', 'weVOpJ63gII'),
        ('Yoko-wakare', '横分', 'bp1tscHlePI'), ('Yoko-guruma', '横車', 'MehP6I5cY2c'),
        ('Yoko-gake', '横掛', 'tP1Sj1uDfSo'), ('Daki-wakare', '抱分', 'Hr0cOMGBDYo'),
        ('O-soto-makikomi', '大外巻込', 'DGDv2oMwmas'), ('Uchi-mata-makikomi', '内股巻込', 'jZXENTLpJCI'),
        ('Harai-makikomi', '払巻込', 'VBaHzKaCXss'), ('Ko-uchi-makikomi', '小内巻込', '_1eygIXLD_w'),
        ('Kani-basami', '蟹挟', 'OR-HGHnarYc'), ('Kawazu-gake', '河津掛', 'w6G57bWACi0')]),
    ('Osaekomi-waza (imobilizações)', 'katame', [
        ('Kesa-gatame', '袈裟固', 'NDaQuJOFBYk'), ('Kuzure-kesa-gatame', '崩袈裟固', 'Q2fb9jaoUFQ'),
        ('Ushiro-kesa-gatame', '後袈裟固', 'SBapox2M2dE'), ('Kata-gatame', '肩固', 'zQR3IOXxO_Q'),
        ('Kami-shiho-gatame', '上四方固', 'HFuMjOv0WN8'), ('Kuzure-kami-shiho-gatame', '崩上四方固', 'YUrogQWdwiY'),
        ('Yoko-shiho-gatame', '横四方固', 'TT7XJVSEQxA'), ('Tate-shiho-gatame', '縦四方固', '55-rFmBx53g'),
        ('Uki-gatame', '浮固', 'e_lAjik1SUM'), ('Ura-gatame', '裏固', 'eeAHZB0v3XY')]),
    ('Shime-waza (estrangulamentos)', 'katame', [
        ('Nami-juji-jime', '並十字絞', 'k2cHry9HByQ'), ('Gyaku-juji-jime', '逆十字絞', 't3tQriIPdlI'),
        ('Kata-juji-jime', '片十字絞', '3VZVUAmiMD8'), ('Hadaka-jime', '裸絞', '9f0n8jez7iA'),
        ('Okuri-eri-jime', '送襟絞', 'EiqyoVcIAi8'), ('Kataha-jime', '片羽絞', 'yaTGgRjnwB8'),
        ('Katate-jime', '片手絞', 'cHeIs-fSqwE'), ('Ryote-jime', '両手絞', '-RHC4V7TQiY'),
        ('Sode-guruma-jime', '袖車絞', 'E3nvQzClcAU'), ('Tsukkomi-jime', '突込絞', 'dKKpnD3eLcY'),
        ('Sankaku-jime', '三角絞', 'lq1CUBRAm7s'), ('Do-jime', '胴絞', 'D_0fFcoIbvY')]),
    ('Kansetsu-waza (chaves de braço)', 'katame', [
        ('Ude-garami', '腕緘', 'AIlTvZb4RlE'), ('Juji-gatame', '腕挫十字固', 'OWgSOlCuMXw'),
        ('Ude-gatame', '腕挫腕固', 'SBf0aTma1VI'), ('Hiza-gatame', '腕挫膝固', 'H2HtAJdiJcE'),
        ('Waki-gatame', '腕挫腋固', '8F5p1zuJRG0'), ('Hara-gatame', '腕挫腹固', 'ZzEycg8R_9M'),
        ('Ashi-gatame', '腕挫脚固', 'ClY7g_pX-4s'), ('Te-gatame', '腕挫手固', '6DnvhY0tQVM'),
        ('Sankaku-gatame', '腕挫三角固', 'WefAmW4azhk'), ('Ashi-garami', '足緘', 'BWWb0GoAtZw')]),
]

# fundamentos, saídas de imobilização e aulas de mestres (mesmo canal oficial)
EXTRAS = [
    ('Fundamentos', [
        ('Kodomo-no-kata: etiqueta (rei), ukemi e movimentos básicos', '講道館 こどもの形', 'VoktcQAxEPg'),
        ('Apresentação da série 100 Techniques', 'KODOKAN JUDO 100 Techniques PV', '_GxcFx8LZRk'),
        ('Visão geral do Te-waza', '手技', 'z5qYfCEcZOU'),
        ('Visão geral do Ma-sutemi-waza', '真捨身技', 'LnjW67efl00'),
        ('Visão geral do Shime-waza', '絞技', 'bq3cwrcS1-c')]),
    ('Saídas de imobilização (defesa no solo)', [
        ('Saídas do Kuzure-kesa-gatame', '崩袈裟固の逃れ方', '-zFQ6h4yKT4'),
        ('Saídas do Kata-gatame', '肩固の逃れ方', '7hP1-W2yovk'),
        ('Saídas do Uki-gatame', '浮固の逃れ方', 'AMHWDFR4ryo'),
        ('Saídas do Ura-gatame', '裏固の逃れ方', '0aY2Tmchzs8')]),
    ('Do pé ao solo e combinações: série “Waza” com campeões', [
        ('Nakamura Kenzo: uchi-mata e como entrar no katame-waza', '中村兼三「内股」「固技への入り方」', 'QNkxH7WJwmQ'),
        ('Kato Hirotaka: nage-waza', '加藤博剛①「投技」', 'BlYHIKcZl3E'),
        ('Kato Hirotaka: katame-waza', '加藤博剛②「固技」', 'Kg4ugwHjc0A')]),
]

# nomes usados no livro → nome da série (quando diferem)
ALIASES = {
    'ko-uchi-gaeshi': 'Ko-uchi-gaeshi', 'kibishu-gaeshi': 'Kibisu-gaeshi',
    'ude-hishigi-juji-gatame': 'Juji-gatame', 'juji-gatame': 'Juji-gatame',
    'hon-kesa-gatame': 'Kesa-gatame', 'kesa-gatame': 'Kesa-gatame',
}

VID = {}
KANJI = {}
for _, _, items in GROUPS:
    for n, k, v in items:
        VID[n.lower()] = (n, v)
        KANJI[n.lower()] = k
for a, n in ALIASES.items():
    VID[a] = VID[n.lower()]


def ijf_url(name):
    special = {'Kata-guruma': 'Kata-Guruma', 'Kibisu-gaeshi': 'Kibishu-gaeshi'}
    return 'https://judo.ijf.org/techniques/' + special.get(name, name)


def find(name):
    return VID.get(name.lower())
