dev_run:
	docker exec -it nginx-ui uwsgi --http 0.0.0.0:8080 --wsgi-file wsgi.py --callable app --processes 1 --threads 8