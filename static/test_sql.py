import sqlite3
connexion = sqlite3.connect("collect.db")
res = connexion.execute("SELECT * FROM user;")
reslist=list(res)
connexion.commit()
connexion.close()
print(reslist)