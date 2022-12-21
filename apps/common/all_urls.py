def all_urls_view():
    from api.urls import urlpatterns
    return get_urls(urlpatterns, [])


def get_urls(raw_urls, nice_urls=[]):
    for entry in raw_urls:
        if hasattr(entry, 'url_patterns'):
            get_urls(entry.url_patterns, nice_urls)
        else:
            if hasattr(entry.callback, 'actions'):
                nice_urls.extend([
                    {
                        "pattern": entry.pattern.regex.pattern,
                        "action": _action,
                        'method': _method,
                        'func': entry.lookup_str
                    } for (_method, _action) in entry.callback.actions.items()
                ])
    return nice_urls
