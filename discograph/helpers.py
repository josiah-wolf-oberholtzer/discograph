# -*- encoding: utf-8 -*-
from discograph.library import DiscographAPI


discograph_api = DiscographAPI()


def parse_request_args(args):
    from discograph.library.mongo import CreditRole
    year = None
    role_names = set()
    for key in args:
        if key == 'year':
            value = args[key]
            try:
                if '-' in year:
                    start, _, stop = year.partition('-')
                    year = tuple(sorted((int(start), int(stop))))
                else:
                    year = int(year)
            except:
                pass
        elif key == 'roles[]':
            value = args.getlist(key)
            for role_name in value:
                if role_name in CreditRole.all_credit_roles:
                    role_names.add(role_name)
    role_names = list(sorted(role_names))
    return role_names, year