import pickle
import stylegan2_models.dnnlib as dnnlib
import stylegan2_models.dnnlib.tflib as tflib


# def get_path_or_url(path_or_gdrive_path):
#     return gdrive_urls.get(path_or_gdrive_path, path_or_gdrive_path)


_cached_networks = dict()


def load_networks(path_or_gdrive_path):
    # path_or_url = get_path_or_url(path_or_gdrive_path)
    path_or_url = path_or_gdrive_path
    if path_or_url in _cached_networks:
        return _cached_networks[path_or_url]

    if dnnlib.util.is_url(path_or_url):
        stream = dnnlib.util.open_url(path_or_url, cache_dir='.stylegan2-cache')
    else:
        stream = open(path_or_url, 'rb')

    tflib.init_tf()
    with stream:
        G, D, Gs = pickle.load(stream, encoding='latin1')
    _cached_networks[path_or_url] = G, D, Gs
    return G, D, Gs