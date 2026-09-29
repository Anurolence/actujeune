from fastapi import FastAPI
app = FastAPI()

DEMO_POSTS = [
    {"id":1,"title":"Concours ENS Yaoundé 2026 - Inscriptions ouvertes","content":"Le concours ENS Yaoundé est ouvert. Date limite 15 Octobre 2026.","category":"Concours","region":"Centre","author":"MINESUP","created_at":"2026-09-29"},
    {"id":2,"title":"Bourse MoMo 2026 pour jeunes entrepreneurs","content":"MTN Cameroon lance bourse 5M FCFA pour startups.","category":"Bourse","region":"Littoral","author":"MTN","created_at":"2026-09-29"},
    {"id":3,"title":"Formation digitale gratuite à Buea","content":"Formation gratuite en dev web à Buea, SW Region.","category":"Formation","region":"Sud-Ouest","author":"ActuJeune","created_at":"2026-09-29"},
]

@app.get("/api/posts")
def get_posts():
    return DEMO_POSTS
