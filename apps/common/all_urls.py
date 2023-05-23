from drf_yasg.generators import EndpointEnumerator


def all_urls_view():
    from api.urls import urlpatterns
    return get_urls(urlpatterns, {})


def get_urls(raw_urls, nice_urls=None):
    if nice_urls is None:
        nice_urls = {}
    for entry in raw_urls:
        if hasattr(entry, 'url_patterns'):
            get_urls(entry.url_patterns, nice_urls)
        elif hasattr(entry.callback, 'actions'):
            for (_method, _action) in entry.callback.actions.items():
                if f'{entry.lookup_str}_{_action}' not in nice_urls:
                    nice_urls[f'{entry.lookup_str}_{_action}'] = {
                        "pattern": entry.pattern.regex.pattern,
                        "action": _action,
                        'method': _method,
                        'func': entry.lookup_str,
                        'meta': f'{entry.lookup_str}_{_action}'
                    }
    return nice_urls.values()


def get_all_api():
    endpoints = EndpointEnumerator().get_api_endpoints()
    data = []
    for endpoint in endpoints:
        named_path_components = [component for component in endpoint[0].strip('/').split('/')
                                 if '{' not in component]
        action = endpoint[1].lower()
        data.append({
            'path': endpoint[0],
            'name': ('_'.join(named_path_components[1:]) + '__' + action).replace('-', '_')
        })
    return data
