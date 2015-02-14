class ErudiPublisher:
    def __init__(self, config): 
        self.url_resolver = self.select_component('urlpublisher')

    def select_component(self, cid, *args, **kwargs):
        try:
            return self.select(self.registry_objects('components', cid), *args, **kwargs)
        except NoSelectableObject:
            return

    def main_publish(self, path, req):
        ctrlid = self.url_resolver.process(req, path)
