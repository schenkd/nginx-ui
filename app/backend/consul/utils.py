def get_instance_id(service_name, user_name):
    return f'{service_name}-{user_name}'


def get_ingress(service_name):
    # wish-user-action-dev.bjs.i.wish.com
    return f'{service_name}-dev.bjs.i.wish.com'


def get_service_name_by_ingress(ingress: str):
    suffix = "-dev.bjs.i.wish.com"
    if ingress.endswith(suffix):
        return True, ingress[:-len(suffix)]
    else:
        return False, ingress
