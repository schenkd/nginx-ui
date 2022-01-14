backend:
	docker exec -it nginx-ui uwsgi --http 0.0.0.0:8080 --wsgi-file ./app/backend/wsgi.py --callable app --threads 8

frontend:
	docker exec -it