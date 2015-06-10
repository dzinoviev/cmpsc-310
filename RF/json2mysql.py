import glob, json, pymysql

conn = pymysql.connect (host = 'localhost', port = 3306, user = 'cs310', passwd = 'badpassw0rd', db = 'cs310', charset = "utf8")
cur = conn.cursor ()

for f in glob.glob ('2008-KZ-*.json'):
    with open (f) as infile:
        data = json.load (infile)
        for key in data["entities"]:
            e_type = data["entities"][key]["type"]
            e_name = data["entities"][key]["name"]
            cur.execute ("INSERT IGNORE INTO rf_entities VALUES (NULL, NULL, %s, %s, %s)",
                         (key, e_type, e_name))
            if "category" in data["entities"][key].keys ():
                e_id = cur.lastrowid
                for cat_id in data["entities"][key]["category"]:
                    cur.execute ("INSERT INTO rf_entity_categories VALUES (NULL, NULL, %s, %s)",
                                 (e_id, cat_id))
        conn.commit ()
 
cur.execute ("SELECT type,COUNT(*) AS cnt FROM rf_entities GROUP BY type ORDER BY cnt DESC LIMIT 10")

print ("#Type,Count")
for (t, count) in cur.fetchall ():
    print (t, count, sep = ',')
