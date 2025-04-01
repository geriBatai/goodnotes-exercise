from locust import HttpUser, LoadTestShape, task
import random
import string

class EndpointTest(HttpUser):
    @task
    def post_random_data(self):
        """
        We generate random data to POST to /
        
        This choice was made to make reports make more sense  for http reporting side
        while complying with exercise params
        """

        alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits
        data = "".join([random.choice(alphabet) for _ in range(64)])
        self.client.post("/", data={ "random_data": data})



class LoadRampUp(LoadTestShape):

    stages = [
            {  "duration": 10, "users": 10 },
            {  "duration": 20, "users": 50 },
            {  "duration": 30, "users": 100 },
            {  "duration": 40, "users": 200 },
    ]
    
    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                # spawn all users at the same time
                return (stage["users"], stage["users"])
        return None
