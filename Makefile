backend:
	docker exec -it nginx-ui sudo --preserve-env=PYTHONPATH /home/app/virtualenv/bin/uwsgi --http 0.0.0.0:8000 --wsgi-file /home/app/nginx-ui/app/backend/wsgi.py --callable app --threads 8

frontend-install:
	docker exec -w /home/app/nginx-ui/app/frontend -it nginx-ui npm install

frontend-dev:
	docker exec -w /home/app/nginx-ui/app/frontend -it nginx-ui npm run serve