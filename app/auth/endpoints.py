# encoding: utf-8
from app.auth import auth


@auth.route('/login', methods=['POST'])
def login():
    pass


@auth.route('/logout', methods=['POST'])
def logout():
    pass
