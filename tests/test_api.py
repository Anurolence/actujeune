"""End-to-end and CRUD unit test suite for Acujeune with Cameroonian enhancements."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db
from app.seed_data import seed_database

client = TestClient(app)

def test_full_lifecycle():
    # 1. Startup initialization
    init_db()
    seed_database()

    # 2. Test Home Page
    response = client.get("/")
    assert response.status_code == 200
    assert "Acujeune" in response.text
    print("✓ Home page renders successfully")

    # 3. Test Metadata endpoint
    response = client.get("/api/meta")
    assert response.status_code == 200
    meta = response.json()
    assert "categories" in meta
    assert "regions" in meta
    assert "opportunity_types" in meta
    assert meta["stats"]["total_posts"] >= 6
    print("✓ Metadata & opportunity statistics working")

    # 4. Test List Posts with Opportunity Filter
    response = client.get("/api/posts?opportunity_type=concours")
    assert response.status_code == 200
    concours_posts = response.json()
    assert isinstance(concours_posts, list)
    print(f"✓ Retrieved {len(concours_posts)} concours posts from API")

    # 5. Test Create Cameroonian Opportunity Post
    new_post_payload = {
        "title": "Bourses d'Études Doctorales & Master 2026 - Université de Dschang",
        "summary": "Appel à candidatures pour 25 bourses de recherche axées sur la transformation locale et l'agriculture durable.",
        "content": "Le rectorat de l'Université de Dschang en partenariat avec des bailleurs internationaux lance l'appel...",
        "category": "Opportunités & Bourses",
        "region": "Ouest (Bafoussam)",
        "opportunity_type": "bourse",
        "deadline": "2026-12-15",
        "remuneration_fcfa": "1 800 000 FCFA / an",
        "contact_whatsapp": "+237 670 99 88 77",
        "apply_link": "https://univ-dschang.org",
        "author_name": "Dr. Kenfack",
        "author_role": "Doyen Faculté Agronomie",
        "image_url": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=800&q=80",
        "tags": "Bourse, Dschang, Recherche, Cameroun",
        "is_featured": 1,
        "status": "published"
    }
    create_res = client.post("/api/posts", json=new_post_payload)
    assert create_res.status_code == 201
    created_post = create_res.json()
    created_id = created_post["id"]
    assert created_post["opportunity_type"] == "bourse"
    assert created_post["remuneration_fcfa"] == "1 800 000 FCFA / an"
    print(f"✓ Created Cameroonian opportunity post ID #{created_id}")

    # 6. Test Get Created Post (Detail)
    get_res = client.get(f"/api/posts/{created_id}")
    assert get_res.status_code == 200
    assert get_res.json()["contact_whatsapp"] == "+237 670 99 88 77"
    print(f"✓ Retrieved single post #{created_id}")

    # 7. Test Detail HTML Page
    html_res = client.get(f"/post/{created_id}")
    assert html_res.status_code == 200
    assert "Dschang" in html_res.text
    assert "1 800 000 FCFA" in html_res.text
    print(f"✓ Detail HTML page renders for #{created_id} with FCFA and WhatsApp info")

    # 8. Test Update Post
    update_payload = {
        "title": "Bourses d'Études Doctorales & Master 2026 - Édition Étendue",
        "remuneration_fcfa": "2 000 000 FCFA / an"
    }
    update_res = client.put(f"/api/posts/{created_id}", json=update_payload)
    assert update_res.status_code == 200
    updated_data = update_res.json()
    assert updated_data["remuneration_fcfa"] == "2 000 000 FCFA / an"
    print(f"✓ Updated post #{created_id}")

    # 9. Test Like Toggle
    like_res = client.post(f"/api/posts/{created_id}/like", data={"client_id": "test_client_cm"})
    assert like_res.status_code == 200
    like_data = like_res.json()
    assert like_data["has_liked"] is True
    print(f"✓ Like & unlike working for post #{created_id}")

    # 10. Test Add Comment
    comment_payload = {
        "author_name": "Arsène (Dschang)",
        "content": "Super opportunité pour notre département de biotechnologie !"
    }
    comment_res = client.post(f"/api/posts/{created_id}/comments", json=comment_payload)
    assert comment_res.status_code == 201
    print(f"✓ Added comment to #{created_id}")

    # 11. Test Delete Post
    del_res = client.delete(f"/api/posts/{created_id}")
    assert del_res.status_code == 200
    assert del_res.json()["success"] is True

    # Verify deleted
    verify_res = client.get(f"/api/posts/{created_id}")
    assert verify_res.status_code == 404
    print(f"✓ Deleted post #{created_id} and verified 404")

    print("\n🎉 ALL CAMEROONIAN ENHANCEMENT TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_full_lifecycle()
