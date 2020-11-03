import src.formulators as formulators
import src.stream_receiving as streamr

"""
Хранилище для быстрого доступа к заранее настроенным камерам.

Некоторые конфиги могут нуждаться в детальной индивидуальной настройке, для более оптимальной работы, например
изменения частоты скачивания m3u8 файла и иных.
"""

powernet = []

# Волжский ЦУП ПАУЭРНЕТ ул. Карбышева - ул. 40 лет Победы
cfg0 = streamr.M3u8Watcher.Config()
cfg0.name = "id0"
cfg0.m3u8_url = "https://flussonic.powernet.com.ru:8081/user32003/tracks-v1/mono.m3u8"
cfg0.ts_base_url = "https://flussonic.powernet.com.ru:8081/user32003/tracks-v1/"
cfg0.uTS_duration = 30
cfg0.m3u8_update_delay = 10
cfg0.formulator = formulators.PowernetFormulator(cfg0)
powernet.append(streamr.M3u8Watcher(cfg0))

# Волжский ул. Дружбы в сторону 40 Лет Победы
cfg1 = streamr.M3u8Watcher.Config()
cfg1.name = "id1"
cfg1.m3u8_url = "https://flussonic.powernet.com.ru:8081/user79093/tracks-v1/mono.m3u8"
cfg1.ts_base_url = "https://flussonic.powernet.com.ru:8081/user79093/tracks-v1/"
cfg1.uTS_duration = 30
cfg1.m3u8_update_delay = 24
cfg1.formulator = formulators.PowernetFormulator(cfg1)
powernet.append(streamr.M3u8Watcher(cfg1))

# Волжский ул. Карбышева - ул. Молодогвардейцев
cfg2 = streamr.M3u8Watcher.Config()
cfg2.name = "id2"
cfg2.m3u8_url = "https://flussonic.powernet.com.ru:8081/user60878/tracks-v1/mono.m3u8"
cfg2.ts_base_url = "https://flussonic.powernet.com.ru:8081/user60878/tracks-v1/"
cfg2.uTS_duration = 30
cfg2.m3u8_update_delay = 12
cfg2.formulator = formulators.PowernetFormulator(cfg2)
powernet.append(streamr.M3u8Watcher(cfg2))

# Волжский ул. Александрова - ул. Пушкина
cfg3 = streamr.M3u8Watcher.Config()
cfg3.name = "id3"
cfg3.m3u8_url = "https://flussonic.powernet.com.ru:8081/user68720/tracks-v1/mono.m3u8"
cfg3.ts_base_url = "https://flussonic.powernet.com.ru:8081/user68720/tracks-v1/"
cfg3.uTS_duration = 30
cfg3.formulator = formulators.PowernetFormulator(cfg3)
powernet.append(streamr.M3u8Watcher(cfg3))

# Волжский Площадь перед магазином МАН
cfg4 = streamr.M3u8Watcher.Config()
cfg4.name = "id4"
cfg4.m3u8_url = "https://flussonic.powernet.com.ru:8081/user96368/tracks-v1/mono.m3u8"
cfg4.ts_base_url = "https://flussonic.powernet.com.ru:8081/user96368/tracks-v1/"
cfg4.uTS_duration = 30
cfg4.formulator = formulators.PowernetFormulator(cfg4)
powernet.append(streamr.M3u8Watcher(cfg4))

# Волжский ул. XIX Партсъезда в сторону ул. Коммунистическая
cfg5 = streamr.M3u8Watcher.Config()
cfg5.name = "id5"
cfg5.m3u8_url = "https://flussonic.powernet.com.ru:8081/user70374/tracks-v1/mono.m3u8"
cfg5.ts_base_url = "https://flussonic.powernet.com.ru:8081/user70374/tracks-v1/"
cfg5.uTS_duration = 30
cfg5.formulator = formulators.PowernetFormulator(cfg5)
powernet.append(streamr.M3u8Watcher(cfg5))

# Волжский ул. Коммунистическая - ул. Пушкина
cfg6 = streamr.M3u8Watcher.Config()
cfg6.name = "id6"
cfg6.m3u8_url = "https://flussonic.powernet.com.ru:8081/user87925/tracks-v1/mono.m3u8"
cfg6.ts_base_url = "https://flussonic.powernet.com.ru:8081/user87925/tracks-v1/"
cfg6.uTS_duration = 30
cfg6.formulator = formulators.PowernetFormulator(cfg6)
powernet.append(streamr.M3u8Watcher(cfg6))

# Волжский ул. XIX Партсъезда д. 64
cfg7 = streamr.M3u8Watcher.Config()
cfg7.name = "id7"
cfg7.m3u8_url = "https://flussonic.powernet.com.ru:8081/user73827/tracks-v1/mono.m3u8"
cfg7.ts_base_url = "https://flussonic.powernet.com.ru:8081/user73827/tracks-v1/"
cfg7.uTS_duration = 30
cfg7.formulator = formulators.PowernetFormulator(cfg7)
powernet.append(streamr.M3u8Watcher(cfg7))

# Волжский ул. Комсомольская в сторону Зорге
cfg8 = streamr.M3u8Watcher.Config()
cfg8.name = "id8"
cfg8.m3u8_url = "https://flussonic.powernet.com.ru:8081/user91498/tracks-v1/mono.m3u8"
cfg8.ts_base_url = "https://flussonic.powernet.com.ru:8081/user91498/tracks-v1/"
cfg8.uTS_duration = 30
cfg8.formulator = formulators.PowernetFormulator(cfg8)
powernet.append(streamr.M3u8Watcher(cfg8))

# Волжский ул. Карбышева - ул. Оломоуцкая
cfg9 = streamr.M3u8Watcher.Config()
cfg9.name = "id9"
cfg9.m3u8_url = "https://flussonic.powernet.com.ru:8081/user35932/tracks-v1/mono.m3u8"
cfg9.ts_base_url = "https://flussonic.powernet.com.ru:8081/user35932/tracks-v1/"
cfg9.uTS_duration = 30
cfg9.formulator = formulators.PowernetFormulator(cfg9)
powernet.append(streamr.M3u8Watcher(cfg9))

# Волжский пр. Ленина - ул. Академика Королёва
cfg10 = streamr.M3u8Watcher.Config()
cfg10.name = "id10"
cfg10.m3u8_url = "https://flussonic.powernet.com.ru:8081/user35463/tracks-v1/mono.m3u8"
cfg10.ts_base_url = "https://flussonic.powernet.com.ru:8081/user35463/tracks-v1/"
cfg10.uTS_duration = 30
cfg10.formulator = formulators.PowernetFormulator(cfg10)
powernet.append(streamr.M3u8Watcher(cfg10))

# Волгоград Дзержинский (7 Ветров) (ул. Космонавтов, д. 33)
cfg11 = streamr.M3u8Watcher.Config()
cfg11.name = "id11"
cfg11.m3u8_url = "https://flussonic.powernet.com.ru:8081/user87469/tracks-v1/mono.m3u8"
cfg11.ts_base_url = "https://flussonic.powernet.com.ru:8081/user87469/tracks-v1/"
cfg11.uTS_duration = 30
cfg11.formulator = formulators.PowernetFormulator(cfg11)
powernet.append(streamr.M3u8Watcher(cfg11))

# Волгоград Дзержинский, ул. им. Константина Симонова - ул. 8-й Воздушной Армии
cfg12 = streamr.M3u8Watcher.Config()
cfg12.name = "id12"
cfg12.m3u8_url = "https://flussonic.powernet.com.ru:8081/user89378/tracks-v1/mono.m3u8"
cfg12.ts_base_url = "https://flussonic.powernet.com.ru:8081/user89378/tracks-v1/"
cfg12.uTS_duration = 30
cfg12.formulator = formulators.PowernetFormulator(cfg12)
powernet.append(streamr.M3u8Watcher(cfg12))

# Волгоград ул. 30-летия Победы - ул. Константина Симонова
cfg13 = streamr.M3u8Watcher.Config()
cfg13.name = "id13"
cfg13.m3u8_url = "https://flussonic.powernet.com.ru:8081/user81297/tracks-v1/mono.m3u8"
cfg13.ts_base_url = "https://flussonic.powernet.com.ru:8081/user81297/tracks-v1/"
cfg13.uTS_duration = 30
cfg13.formulator = formulators.PowernetFormulator(cfg13)
powernet.append(streamr.M3u8Watcher(cfg13))
