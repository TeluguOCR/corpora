#! /usr/bin/env python3

import re, sys, os
import urllib.request as url
from bs4 import BeautifulSoup
from collections import Counter 

art_issue_dict = {'1718': '201105', '643': '200105', '597': '200209', '587': '200209', '1004': '200211', '108': '199901', '109': '199901', '100': '200605', '106': '200509', '107': '199901', '104': '200507', '105': '200507', '2046': '201301', '2044': '201301', '2045': '201301', '2042': '201301', '2043': '201301', '2040': '201301', '2041': '201301', '2048': '201301', '2049': '201301', '99': '200605', '98': '200605', '90': '200605', '96': '200001', '1623': '201009', '1622': '201009', '1621': '201009', '1620': '201009', '1627': '201009', '1626': '201009', '1997': '201209', '1624': '201009', '1999': '201209', '1998': '201209', '1629': '201011', '1628': '201011', '559': '200207', '558': '200207', '555': '200207', '554': '200207', '557': '200207', '551': '200205', '550': '200205', '553': '200207', '552': '200205', '1199': '200801', '1198': '200801', '1191': '200801', '1190': '200801', '1193': '200801', '1192': '200801', '1195': '200801', '1194': '200801', '1197': '200801', '1196': '200801', '1177': '200801', '1176': '200711', '1175': '200711', '1174': '200711', '1173': '200711', '1172': '200711', '1171': '200711', '1170': '200711', '1179': '200801', '644': '200105', '1285': '200807', '1284': '200806', '1287': '200806', '1286': '200807', '1281': '200807', '1280': '200807', '1283': '200806', '515': '200203', '879': '199911', '1289': '200806', '1288': '200806', '514': '200203', '1579': '201007', '1578': '201005', '689': '200607', '517': '200203', '1573': '201005', '1572': '201005', '1571': '201005', '1570': '201005', '1577': '201005', '1576': '201005', '1575': '201005', '1574': '201005', '458': '200307', '459': '200307', '621': '200103', '873': '199911', '620': '200103', '627': '200103', '626': '200103', '625': '200103', '624': '200103', '1370': '200811', '1372': '200811', '1377': '200901', '1376': '200811', '1379': '200901', '1378': '200901', '1342': '200311', '1343': '200811', '1344': '200811', '455': '200307', '456': '200307', '1347': '200811', '2038': '201301', '1247': '200805', '245': '200303', '244': '200303', '247': '200303', '241': '200303', '240': '200303', '242': '200303', '248': '200303', '179': '200411', '178': '200411', '177': '200507', '176': '200507', '175': '200507', '174': '200507', '173': '200507', '172': '200507', '171': '200507', '170': '200507', '2051': '201301', '2050': '201301', '2053': '201301', '2052': '201301', '2055': '201301', '2054': '201301', '2057': '201301', '2056': '201301', '654': '200107', '655': '200107', '1506': '200911', '653': '200107', '1367': '200811', '1364': '200811', '1977': '201207', '1976': '201207', '1975': '201207', '1365': '200811', '1974': '201207', '1973': '201207', '1970': '201207', '1968': '201207', '1969': '201207', '1618': '201009', '1619': '201009', '1964': '201207', '1965': '201207', '1966': '201207', '1967': '201207', '1960': '201207', '1961': '201207', '1962': '201207', '1963': '201207', '1363': '200811', '1142': '200709', '1143': '200709', '1140': '200709', '1141': '200709', '1146': '200709', '1144': '200709', '1145': '200709', '1148': '200709', '1149': '200709', '769': '200005', '1546': '201003', '693': '200607', '690': '200607', '691': '200607', '696': '200111', '1543': '201003', '694': '200607', '1541': '201003', '698': '200111', '1548': '201003', '542': '200205', '540': '200205', '541': '200205', '546': '200205', '547': '200205', '544': '200607', '545': '200205', '548': '200205', '549': '200205', '761': '200005', '765': '200005', '417': '200305', '1388': '200901', '1389': '200901', '1384': '200901', '1385': '200901', '1386': '200901', '1387': '200901', '418': '200305', '1381': '200903', '1382': '200811', '1383': '200901', '258': '200305', '259': '200305', '256': '200305', '257': '200305', '901': '200609', '168': '200507', '169': '200507', '164': '200507', '165': '200507', '167': '200507', '1980': '201207', '908': '200609', '909': '200609', '1090': '200705', '609': '200101', '1091': '200705', '1814': '201109', '1815': '201109', '1816': '201109', '1817': '201109', '1810': '201109', '1811': '201109', '1812': '201109', '1813': '201109', '1818': '201109', '1819': '201109', '1098': '200705', '671': '200107', '1609': '201009', '1608': '201009', '1979': '201207', '1978': '201207', '1601': '201007', '1600': '201007', '1603': '201009', '1602': '201009', '1605': '201009', '1604': '201009', '1971': '201207', '1606': '201009', '809': '200011', '808': '200011', '803': '200009', '802': '200009', '801': '200009', '800': '200009', '807': '200011', '806': '200011', '805': '200011', '608': '200101', '1155': '200709', '1157': '200709', '1156': '200709', '1151': '200709', '1150': '200709', '1153': '200709', '1152': '200709', '1555': '201003', '1554': '201003', '1550': '201003', '1552': '201003', '59': '200509', '58': '200605', '1557': '201005', '1556': '201003', '1559': '201005', '1558': '201005', '57': '200511', '56': '200511', '51': '200511', '50': '200511', '53': '200511', '52': '200511', '537': '200205', '536': '200205', '535': '200205', '534': '200205', '533': '200205', '532': '200205', '531': '200205', '54': '200511', '539': '200205', '538': '200205', '1399': '200901', '1398': '200901', '1397': '200901', '1396': '200901', '1395': '200901', '1394': '200901', '1393': '200901', '1392': '200901', '1391': '200901', '1390': '200901', '530': '200205', '229': '200301', '228': '200301', '227': '200301', '226': '200301', '225': '200301', '224': '200301', '223': '200301', '222': '200301', '221': '200301', '220': '200301', '151': '200411', '150': '200411', '153': '200411', '152': '200411', '155': '200411', '154': '200411', '157': '200501', '156': '200411', '158': '200503', '1524': '201001', '1948': '201205', '1544': '201003', '1525': '201001', '1942': '201205', '1943': '201205', '1940': '201205', '1941': '201205', '1946': '201205', '1947': '201205', '1944': '201205', '1945': '201205', '818': '200001', '819': '200011', '1527': '201001', '810': '200011', '1520': '201001', '812': '200011', '813': '200011', '814': '200011', '815': '200011', '816': '200011', '1521': '201001', '1991': '201209', '1522': '201001', '1990': '201209', '1251': '200805', '1993': '201209', '1490': '200911', '1491': '200911', '1492': '200911', '1493': '200911', '1494': '200911', '1495': '200911', '1496': '200911', '1497': '200911', '1498': '200911', '1995': '201209', '1994': '201211', '1700': '201103', '1701': '201103', '1702': '201103', '1703': '201103', '1704': '201103', '1705': '201103', '1706': '201103', '1707': '201103', '1708': '201105', '1996': '201209', '1128': '200707', '1129': '200707', '1120': '200707', '1121': '200707', '1122': '200707', '1123': '200707', '1124': '200707', '1125': '200707', '1126': '200707', '1127': '200707', '524': '200203', '525': '200203', '526': '200203', '527': '200203', '520': '200203', '521': '200203', '528': '200203', '529': '200203', '1234': '200805', '1235': '200805', '1236': '200805', '1237': '200805', '1230': '200805', '1231': '200807', '1232': '200805', '1233': '200805', '1238': '200805', '1239': '200805', '436': '200305', '437': '200305', '238': '200303', '239': '200303', '234': '200303', '235': '200303', '236': '200303', '237': '200303', '230': '200301', '231': '200301', '232': '200303', '233': '200303', '146': '200409', '147': '200409', '144': '200409', '145': '200409', '142': '200407', '143': '200409', '140': '200401', '141': '200403', '148': '200409', '149': '200409', '1832': '201109', '1833': '201109', '1831': '201109', '1836': '201109', '1837': '201109', '1834': '201109', '1835': '201109', '1838': '201111', '1839': '201111', '1955': '201205', '1954': '201205', '1957': '201205', '1956': '201205', '1951': '201207', '1950': '201205', '1953': '201205', '1952': '201205', '1959': '201207', '1958': '201207', '829': '199907', '828': '199907', '825': '199907', '824': '199907', '827': '199907', '826': '199907', '821': '199907', '820': '200011', '822': '199907', '1483': '200911', '1482': '200911', '1481': '200911', '1480': '200911', '1487': '201003', '1486': '200911', '1484': '200911', '1489': '200911', '1488': '200911', '1713': '201105', '1712': '201105', '1711': '201105', '1710': '201103', '1717': '201105', '1716': '201105', '1715': '201105', '1714': '201105', '1719': '201105', '1992': '201209', '799': '200009', '798': '200009', '613': '200101', '610': '200101', '1139': '200709', '1138': '200709', '1133': '200707', '616': '200101', '1131': '200707', '1130': '200707', '1136': '200403', '1135': '200401', '614': '200101', '615': '200101', '519': '200203', '518': '200201', '511': '200203', '510': '200211', '513': '200203', '512': '200203', '1003': '200503', '1002': '200505', '1001': '200505', '1000': '200505', '1227': '200803', '1226': '200803', '1225': '200803', '1224': '200803', '1223': '200803', '1222': '200803', '1221': '200803', '1220': '200803', '629': '200103', '1228': '200803', '1561': '201005', '13': '200603', '12': '200603', '15': '200603', '14': '200603', '17': '200603', '16': '200603', '19': '200603', '18': '200603', '201': '200401', '200': '200401', '203': '200401', '202': '200401', '205': '200401', '204': '200401', '207': '200401', '206': '200401', '209': '200401', '208': '200401', '685': '200111', '684': '200111', '681': '200111', '680': '200111', '683': '200111', '682': '200111', '1829': '201109', '1828': '201109', '1825': '201109', '1824': '201109', '1827': '201109', '1826': '201109', '1821': '201109', '1820': '201109', '1823': '201109', '1822': '201109', '1920': '201203', '1921': '201203', '1922': '201203', '1923': '201203', '1924': '201203', '1929': '201203', '832': '199907', '833': '199907', '830': '199907', '831': '199907', '836': '199907', '837': '199909', '834': '199907', '835': '199907', '838': '199909', '839': '199909', '3': '200603', '1987': '201209', '784': '200007', '785': '200007', '787': '200007', '780': '200005', '1728': '201107', '1729': '201107', '1726': '201105', '1727': '201105', '1724': '201105', '1725': '201105', '1722': '201105', '1723': '201105', '1720': '201105', '1721': '201105', '60': '200509', '61': '200509', '62': '200509', '63': '200509', '64': '200509', '65': '200509', '66': '200509', '67': '200605', '68': '200605', '69': '200509', '1588': '201007', '1589': '201007', '1582': '201007', '1583': '201007', '1580': '201007', '1581': '201007', '1586': '201007', '1587': '201007', '1584': '201007', '1585': '201007', '509': '200201', '506': '200201', '507': '200201', '504': '200201', '505': '200201', '502': '200201', '503': '200201', '500': '200201', '501': '200201', '1212': '200803', '1213': '200803', '632': '200103', '1211': '200803', '1216': '200803', '1217': '200803', '636': '200105', '1215': '200803', '638': '200105', '639': '200105', '1218': '200803', '1219': '200803', '782': '200007', '783': '200007', '1106': '200705', '1455': '200907', '1104': '200705', '1457': '200907', '1450': '200907', '1103': '200705', '1100': '200705', '1101': '200705', '1458': '200907', '1459': '200907', '1108': '200101', '788': '200007', '789': '200007', '1891': '201201', '216': '200401', '217': '200401', '214': '200401', '215': '200401', '212': '200401', '213': '200401', '210': '200401', '211': '200401', '218': '200301', '219': '200301', '4': '200603', '1858': '201111', '1850': '201111', '1851': '201111', '1852': '201111', '1853': '201111', '1856': '201111', '1857': '201111', '918': '200609', '915': '200609', '914': '200609', '917': '200609', '911': '200609', '910': '200609', '913': '200609', '912': '200609', '516': '200203', '1933': '201203', '1932': '201203', '1931': '201203', '1930': '201203', '1937': '201205', '1936': '201205', '1935': '201205', '1934': '201203', '1939': '201205', '1938': '201205', '847': '199909', '846': '199909', '845': '199909', '844': '199909', '843': '199909', '842': '199909', '841': '199909', '840': '199909', '849': '199909', '848': '199909', '663': '200107', '1739': '201107', '1738': '201107', '1731': '201107', '1730': '201107', '1733': '201107', '1732': '201107', '662': '200107', '1734': '201107', '1737': '201107', '1736': '201107', '753': '200003', '752': '200003', '751': '200003', '750': '200003', '757': '200003', '756': '200003', '755': '200003', '754': '200003', '759': '200003', '758': '200003', '1595': '201007', '1594': '201007', '1597': '201007', '1591': '201007', '1592': '201007', '1599': '201007', '605': '200101', '630': '200103', '607': '200101', '606': '200101', '601': '200209', '600': '200209', '603': '200209', '602': '200209', '1205': '200801', '1204': '200801', '1207': '200803', '1201': '200803', '1200': '200801', '1203': '200801', '1202': '200801', '1560': '201005', '634': '200105', '635': '200103', '637': '200105', '1447': '200907', '1353': '200811', '1445': '200907', '1112': '200905', '5': '200007', '1442': '200905', '1117': '200707', '1352': '200811', '1119': '200707', '1118': '200707', '467': '200309', '1448': '200907', '466': '200309', '461': '200307', '450': '200307', '489': '200311', '488': '200311', '487': '200311', '486': '200311', '485': '200311', '484': '200311', '483': '200311', '482': '200311', '481': '200311', '480': '200311', '451': '200307', '199': '200401', '198': '200403', '195': '200403', '194': '200403', '197': '200403', '196': '200403', '191': '200403', '190': '200403', '193': '200403', '192': '200403', '1454': '200907', '1107': '199907', '1456': '200907', '1105': '200705', '1102': '200705', '1451': '200907', '1452': '200907', '1453': '200907', '902': '200609', '903': '200609', '1849': '201111', '1848': '201111', '906': '200609', '907': '200609', '904': '200609', '905': '200609', '1843': '201111', '1842': '201111', '1841': '201111', '1840': '201111', '1847': '201111', '1846': '201111', '1845': '201111', '1844': '201111', '1908': '201203', '1909': '201203', '1906': '201203', '1907': '201203', '1904': '201203', '1905': '201203', '1902': '201201', '1903': '201201', '1900': '201201', '1901': '201201', '857': '200607', '850': '199909', '851': '199909', '852': '199911', '853': '199911', '858': '200607', '859': '200607', '6': '200603', '811': '200011', '611': '200101', '817': '200011', '740': '200001', '741': '200003', '742': '200003', '743': '200003', '744': '200003', '745': '200003', '746': '200003', '747': '200003', '748': '200003', '749': '200003', '1050': '200701', '1051': '200701', '1052': '200701', '1053': '200701', '1054': '200701', '1055': '200701', '1056': '200701', '1057': '200903', '1058': '200701', '1059': '200701', '1696': '201103', '1697': '201103', '1694': '201103', '1695': '201103', '1692': '201103', '1693': '201103', '1690': '201103', '1691': '201103', '1698': '201103', '1699': '201105', '1278': '200807', '1279': '200811', '618': '200101', '619': '200101', '612': '200101', '1271': '200806', '1272': '200806', '1273': '200806', '1274': '200807', '617': '200101', '1276': '200806', '1277': '200806', '1472': '200909', '1470': '200909', '1471': '200909', '1476': '200909', '1477': '200909', '1474': '200909', '1475': '200909', '1478': '200909', '1479': '200911', '1304': '200807', '1305': '200807', '1306': '200807', '1307': '200807', '1300': '200807', '1301': '200807', '1302': '200807', '1303': '200807', '1308': '200807', '1309': '200807', '498': '200201', '499': '200201', '1499': '200911', '494': '200311', '495': '200311', '496': '200311', '497': '200311', '490': '200311', '491': '200311', '492': '200311', '493': '200311', '24': '200603', '25': '200603', '26': '200603', '27': '200603', '20': '200603', '21': '200603', '22': '200603', '23': '200603', '29': '200601', '7': '200603', '1879': '201201', '591': '200209', '1085': '200703', '1876': '201201', '1877': '201201', '1874': '201201', '1875': '201201', '1873': '201201', '1083': '200703', '1878': '201201', '594': '200209', '977': '200407', '976': '200407', '973': '200611', '972': '200611', '971': '200503', '970': '200611', '979': '200407', '978': '200407', '182': '200411', '183': '200411', '180': '200411', '181': '200411', '186': '200403', '187': '200401', '184': '200411', '185': '200403', '188': '200403', '189': '200403', '1919': '201203', '1918': '201203', '1911': '201203', '1910': '201203', '1913': '201203', '1912': '201203', '1915': '201203', '1914': '201203', '1917': '201203', '1916': '201203', '869': '199911', '868': '199911', '861': '200607', '860': '200607', '863': '200607', '862': '200607', '865': '200607', '864': '200607', '867': '199911', '866': '200607', '2024': '201301', '2025': '201301', '2026': '201301', '2027': '201301', '2020': '201211', '2021': '201301', '2022': '201301', '2023': '201301', '2028': '201301', '2029': '201301', '1502': '200911', '883': '199911', '882': '199911', '881': '199911', '880': '199911', '887': '199810', '886': '199810', '885': '199911', '884': '199911', '889': '200607', '888': '199810', '657': '200107', '775': '200005', '774': '200005', '777': '200005', '776': '200005', '771': '200005', '770': '200005', '773': '200005', '772': '200005', '779': '200005', '778': '200005', '77': '200605', '76': '200605', '75': '200605', '74': '200605', '73': '200209', '72': '200509', '71': '200509', '70': '200509', '79': '200605', '78': '200605', '1043': '200701', '1042': '200701', '1047': '200701', '1046': '200701', '1045': '200701', '1044': '200701', '1049': '200701', '1681': '201101', '1680': '201101', '1683': '201101', '1682': '201101', '1685': '201101', '1684': '201101', '1687': '201103', '1686': '201101', '1689': '201103', '1688': '201103', '1268': '200806', '668': '200107', '667': '200107', '1261': '200805', '1260': '200805', '1267': '200806', '1266': '200806', '1265': '200806', '660': '200107', '1469': '200909', '1468': '200909', '1465': '200909', '1464': '200909', '1467': '200909', '1466': '200909', '1461': '200907', '1460': '200907', '1463': '200909', '1462': '200909', '1317': '200809', '1315': '200809', '1314': '200809', '1313': '200809', '1311': '200903', '1310': '200503', '1318': '200811', '443': '200307', '442': '200307', '441': '200307', '447': '200307', '446': '200307', '445': '200307', '444': '200307', '631': '200103', '633': '200105', '1861': '201111', '1860': '201111', '1863': '201111', '1862': '201111', '1865': '201111', '1864': '201111', '1867': '201111', '1866': '201111', '1869': '201111', '1868': '201111', '964': '200611', '965': '200611', '967': '200611', '960': '200611', '961': '200611', '962': '200611', '963': '200611', '968': '200611', '969': '200611', '1241': '200805', '878': '199911', '1240': '200805', '876': '199911', '877': '199911', '874': '200607', '875': '199911', '872': '199911', '1243': '200805', '870': '199911', '871': '199911', '1242': '200805', '2033': '201301', '2032': '201301', '2030': '201301', '9': '200605', '1245': '200805', '2039': '201301', '1244': '200805', '890': '199810', '891': '199810', '892': '199810', '893': '200607', '894': '200607', '647': '200107', '896': '200607', '897': '200607', '898': '200607', '899': '200607', '1246': '200805', '649': '200107', '648': '200107', '641': '200105', '1616': '201009', '1617': '201009', '1614': '201009', '768': '200005', '1615': '201009', '762': '200005', '763': '200005', '640': '200105', '766': '200005', '767': '200005', '764': '200005', '1613': '201009', '1610': '201009', '1611': '201009', '1078': '200703', '1079': '200703', '1076': '200703', '1077': '200703', '1074': '200703', '1075': '200703', '1072': '200703', '1073': '200703', '1070': '200703', '1071': '200703', '1678': '201101', '1679': '201101', '1674': '201103', '1676': '201101', '1677': '201101', '1670': '201101', '1671': '201101', '1672': '201101', '1673': '201101', '1094': '200705', '1095': '200705', '1096': '200705', '1097': '200705', '678': '200111', '679': '200111', '1092': '200705', '642': '200105', '674': '200107', '675': '200107', '676': '200107', '677': '200111', '670': '200107', '1099': '200705', '672': '200107', '673': '200107', '645': '200105', '1418': '200903', '1419': '200903', '1410': '200903', '1411': '200903', '1412': '200903', '1413': '200903', '1414': '200903', '1415': '200903', '1417': '200903', '1322': '200809', '1323': '200211', '1320': '200809', '1321': '200809', '1326': '200811', '1327': '200809', '1324': '200809', '1325': '200809', '1328': '200809', '1329': '200809', '1256': '200807', '1257': '200805', '1254': '200805', '1255': '200805', '1252': '200805', '1253': '200805', '1250': '200805', '1523': '201001', '1528': '201001', '1529': '201001', '1258': '200805', '646': '200105', '308': '200303', '1625': '201009', '623': '200103', '622': '200103', '1898': '201201', '1899': '201201', '1894': '201201', '1895': '201201', '1896': '201201', '1897': '201201', '1890': '201201', '476': '200309', '1892': '201201', '1893': '201201', '959': '200611', '958': '200611', '951': '200501', '950': '200501', '953': '200503', '955': '200611', '954': '200503', '957': '200611', '956': '200611', '2002': '201211', '2003': '201211', '2000': '200211', '2001': '201211', '2006': '201211', '2007': '201211', '2004': '201211', '2005': '201211', '2008': '201211', '2009': '201211', '664': '200107', '719': '200001', '718': '200111', '717': '200111', '716': '200111', '715': '200111', '710': '200111', '661': '200107', '1264': '200806', '1069': '200703', '1068': '200703', '1062': '200701', '1065': '199903', '1067': '200703', '1066': '200703', '1669': '201101', '1668': '201101', '1667': '201101', '1664': '201101', '1663': '201101', '1662': '201101', '1661': '201101', '1660': '200211', '1087': '200705', '590': '200209', '593': '200209', '592': '200209', '595': '200209', '1082': '200703', '1081': '200703', '596': '200209', '599': '200209', '1089': '200705', '1526': '201001', '1409': '200903', '1408': '200903', '1403': '200901', '1402': '200901', '1400': '200901', '1407': '200903', '1406': '200903', '1404': '200509', '692': '200607', '449': '200307', '448': '200307', '1339': '200811', '1338': '200809', '1547': '201003', '1335': '200809', '1334': '200809', '1337': '200809', '1331': '200809', '1330': '200809', '1333': '200809', '1332': '200809', '1545': '201003', '1542': '201003', '39': '200601', '38': '200601', '1540': '201001', '33': '200601', '32': '200601', '31': '200601', '30': '200601', '37': '200601', '36': '200601', '35': '200601', '34': '200601', '1537': '201001', '1536': '201001', '1535': '201001', '1534': '201001', '1533': '201001', '1532': '201001', '1531': '201001', '1530': '201001', '1249': '200805', '1248': '200809', '1539': '201001', '1538': '201001', '1889': '201201', '1888': '201201', '1887': '201201', '1886': '201201', '1885': '201201', '1884': '201201', '1883': '201201', '1882': '201201', '1881': '201201', '1880': '201201', '948': '200501', '949': '200501', '946': '200501', '947': '200501', '944': '200501', '945': '200501', '942': '200609', '943': '200501', '941': '200609', '133': '200211', '131': '200203', '130': '200201', '137': '200307', '136': '200305', '135': '200303', '134': '200301', '139': '200311', '138': '200309', '2019': '201211', '2018': '201211', '2015': '201211', '2014': '201211', '2017': '201211', '2016': '201211', '2011': '201211', '2010': '201211', '2013': '201211', '2012': '201211', '704': '200111', '707': '200111', '700': '200111', '701': '200111', '82': '200605', '83': '200605', '80': '200605', '81': '200605', '87': '200605', '84': '200605', '1658': '201101', '1659': '200211', '1652': '201101', '1653': '201101', '1650': '201101', '1651': '201101', '1656': '201101', '1657': '201101', '1654': '201101', '1655': '201101', '586': '200209', '1986': '201209', '584': '200209', '585': '200209', '582': '200209', '583': '200209', '580': '200209', '581': '200209', '1632': '201011', '588': '200209', '589': '200209', '1633': '201011', '1982': '201209', '1983': '201209', '1436': '200905', '1437': '200905', '1434': '200905', '1435': '200905', '1432': '200905', '1433': '200905', '1430': '200905', '1981': '201209', '1438': '200905', '1439': '200905', '1348': '200811', '1349': '200811', '1340': '200811', '1341': '200811', '452': '200307', '453': '200307', '454': '200307', '1345': '200811', '1346': '200811', '457': '200307', '656': '200107', '1503': '200911', '1500': '200911', '1501': '200911', '652': '200107', '1507': '200911', '650': '200107', '651': '200111', '1508': '200911', '1509': '200911', '658': '200107', '659': '200107', '55': '200511', '995': '200505', '994': '200505', '997': '200505', '996': '200505', '991': '200505', '990': '200505', '993': '200505', '992': '200505', '999': '200505', '998': '200505', '120': '200005', '122': '200009', '123': '200007', '124': '200011', '125': '200101', '126': '200103', '127': '200105', '128': '200107', '129': '200111', '2060': '201301', '722': '200001', '1645': '201011', '1644': '201011', '1647': '201011', '1646': '201011', '1641': '201011', '1640': '201011', '1643': '201011', '1649': '201011', '1648': '201011', '728': '200001', '579': '200209', '578': '200209', '604': '200101', '573': '200207', '572': '200207', '570': '200207', '577': '200209', '576': '200209', '575': '200209', '574': '200207', '1209': '200803', '1421': '200903', '1420': '200903', '1423': '200905', '1424': '200905', '1426': '200905', '1429': '200905', '1428': '200905', '733': '200001', '732': '200001', '735': '200001', '734': '200001', '737': '200001', '736': '200001', '738': '200001', '1359': '200811', '1358': '200811', '469': '200309', '468': '200309', '465': '200309', '464': '200311', '1351': '200811', '1350': '200811', '1357': '200811', '460': '200307', '463': '200311', '462': '200307', '1519': '201001', '1518': '201001', '1515': '201001', '1514': '201001', '1517': '201001', '1516': '201001', '1511': '200911', '1510': '200911', '1513': '201001', '1512': '200911', '1735': '201107', '43': '200511', '1446': '200907', '1113': '201007', '1441': '200907', '1116': '200707', '263': '200305', '262': '200305', '261': '200305', '260': '200305', '267': '200305', '266': '200305', '265': '200305', '264': '200305', '269': '200305', '268': '200305', '1562': '201005', '1564': '201005', '1565': '201005', '1566': '201005', '1567': '201007', '988': '200407', '982': '200407', '983': '200407', '980': '200407', '981': '200407', '986': '200407', '987': '200407', '984': '200407', '985': '200407', '115': '199901', '114': '199901', '117': '199911', '116': '199907', '111': '199901', '110': '199901', '113': '199901', '112': '199901', '118': '199909', '1630': '201011', '1631': '201011', '1984': '201209', '1985': '201209', '1634': '201011', '1635': '201011', '1636': '201011', '1637': '201011', '1638': '201011', '1639': '201011', '1988': '201209', '1989': '201209', '568': '200207', '569': '200207', '560': '200207', '561': '200207', '562': '200207', '563': '200207', '564': '200207', '565': '200207', '566': '200207', '567': '200207', '1188': '200801', '1189': '200801', '1186': '200801', '1187': '200801', '1184': '200801', '1185': '200801', '1183': '200801', '1180': '200801', '727': '200001', '724': '200001', '1748': '201107', '1749': '201107', '1744': '201107', '1745': '201107', '1746': '201107', '1740': '201107', '1742': '201107', '1743': '201107', '1164': '200711', '1165': '200711', '1166': '200711', '1160': '200711', '1161': '200711', '1162': '200711', '1163': '200711', '1169': '200711', '48': '200511', '49': '200511', '46': '200511', '47': '200511', '44': '200511', '45': '200511', '42': '200601', '2034': '201301', '40': '200601', '41': '200601', '1568': '201005', '1569': '201005', '1298': '200807', '1299': '200807', '1292': '200806', '1293': '200807', '1290': '200806', '1563': '201005', '1296': '200807', '1297': '200807', '1294': '200807', '1295': '200807', '797': '200009', '796': '200009', '1361': '200811', '795': '200009', '793': '200007', '792': '200007', '791': '200007', '790': '200007', '472': '200309', '473': '200309', '470': '200309', '471': '200309', '1362': '200901', '477': '200311', '474': '200309', '475': '200309', '478': '200311', '479': '200311', '1368': '200811', '1369': '200811'}
art_ids = sorted(art_issue_dict, key=lambda x:art_issue_dict[x])

# Count articles in each issue
c = Counter()
for k, v in art_issue_dict.items():    c[v] += 1

filelist = os.listdir("articles")
link_head = "http://www.eemaata.com/em/printerfriendly/?id="

# The main function to get every nth article
# n instances of this fn are launched in nthreads for download speed
def onethreadfn(nthreads, ithread):
    for i in range(ithread, len(art_ids), nthreads):
        art_id = art_ids[i]
        issue = art_issue_dict[art_id]
        if art_id+'.html' in filelist:
            print("{2}:Skipping article {0:4} from issue {1}".format(art_id, issue, ithread))
            continue
        print("{2}:Fetching article {0:4} from issue {1}".format(art_id, issue, ithread), end=" ")
        try:
            article = url.urlopen(link_head+art_id)
        except :
            print("ERROR ", sys.exc_info()[0])
        else:
            soup = BeautifulSoup(article.read().decode('utf-8'))
            post = soup.find("div", "post")
            print(len(str(post)), " bytes")
            with open("articles/"+art_id+".html", "w") as f:
                f.write(str(post))

# Launch n threads each getting 1/n of the pages
from threading import Thread
nthreads = 6 
for ithread in range(nthreads):
    th = Thread(target=onethreadfn, args=(nthreads, ithread))
    th.start()