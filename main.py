import requests
from wox import Wox

icons_dir = './icons/'
class Main(Wox):
    def request(self, url):
        if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
            proxies = {
                "http": "http://{}:{}".format(self.proxy.get("server"), self.proxy.get("port")),
                "https": "http://{}:{}".format(self.proxy.get("server"), self.proxy.get("port"))}
            return requests.get(url, proxies=proxies)
        else:
            return requests.get(url)

    def query(self, query):
        results = []
        url = "http://suggestqueries.google.com/complete/search?client=firefox&q=" + query
        r = requests.get(url).json()
        for item in r[1]:
            results.append({
                "Title": item,
                "SubTitle": "Click to replace",
                "IcoPath": icons_dir + "spell.png",
                "JsonRPCAction": {
                    "method": "Wox.ChangeQuery",
                    "parameters": [item, False],
                    # hide the query wox or not
                    "dontHideAfterAction": True
                }
            })
        if not results:
            results.append({
                "Title": 'No suggestions',
                "SubTitle": '',
                "IcoPath": icons_dir + "spell.png"
            })
        return results

if __name__ == "__main__":
    Main()
