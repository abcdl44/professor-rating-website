import requests


class Professor(object):
    def __init__(self, planetterp_json, detailed=False):
        if detailed:
            self.name = planetterp_json["name"]
            self.reviews = planetterp_json["reviews"]

        self.name = planetterp_json["name"]
        self.reviews = planetterp_json["reviews"]

    def __repr__(self):
        return self.name


class ProfessorClient(object):
    def __init__(self):
        self.sess = requests.Session()
        self.base_url = f"https://api.planetterp.com/v1/"

    def prof_data(self, prof_name):
        """
        Searches for the professor, and returns
        a list of objects if the professor exists, or an error response
        if the professor doen't exist in the planetterp

        Only use this method if the user is using the search bar on the website.
        """
        search_string = "%20".join(prof_name.split())
        page = 1

        prof_url = f"professor?name={search_string}"

        resp = self.sess.get(self.base_url + prof_url)

        if resp.status_code != 200:
            raise ValueError(
                "Search request failed; professor doesn't exist"
            )

        data = resp.json()

        return data

    def prof_exists(self, prof_name):
        
        search_string = "%20".join(prof_name.split())
        page = 1

        prof_url = f"professor?name={search_string}"

        resp = self.sess.get(self.base_url + prof_url)

        if resp.status_code != 200:
            raise ValueError(
                "Search request failed; professor doesn't exist"
            )

        data = resp.json()

        if data:
            return True

        return False


## -- Example usage -- ###
# if __name__ == "__main__":
#     import os

#     # client = MovieClient(os.environ.get("OMDB_API_KEY"))

#     movies = client.search("guardians")

#     for movie in movies:
#         print(movie)

#     print(len(movies))
