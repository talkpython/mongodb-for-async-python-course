import locust


class ApiTest(locust.HttpUser):
    host = "http://127.0.0.1:8000"
    wait_time = locust.between(5, 30)

    @locust.task(weight=1)
    def home_page(self):
        self.client.get('/')

    @locust.task(weight=5)
    def stats(self):
        self.client.get('/api/stats')

    @locust.task(weight=15)
    def recent(self):
        self.client.get('/api/packages/recent/5')
