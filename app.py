import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_js_src(URL):
    try:
        print("[+] Fetching script sources")
        response = requests.get(URL)

        soup = BeautifulSoup(response.content, 'html.parser')

        script_srcs = []
        for script in soup.find_all('script'):
            if script.get('src'):
                print(f"[+] Found {script['src']}")
                script_srcs.append(script['src'])
        
        print("[+] Fetching script sources successful")
       
        return script_srcs
    except Exception as e:
        print("[-] Error fetching script sources")
        print(e)

def find_keywords(js_URL, data):
    keywords_file = "keywords.txt"

    try:
        print(f"[+] Searching keywords for {js_URL}")

        with open(keywords_file, 'r') as file:

            js_response = requests.get(js_URL)

            if js_response.status_code == 200:
                js_code = js_response.text

                for keyword in file:

                    indices = []
                    index = js_code.find(keyword.strip())

                    while index != -1:
                        indices.append(index)
                        index = js_code.find(keyword.strip(), index + 1)

                    line_data = {"JS_file": js_URL, "keyword": keyword.strip(), "num": len(indices), "Indices": indices}
                    data.append(line_data)
                    

        return data
                
    
        
    except FileNotFoundError:
        print(f"[-] The file {keywords_file} does not exist.")
    except Exception as e:
        print(f"[-] Error finding keywords for {js_URL}")
        print(e)


if __name__ == "__main__":

    data = []

    try:
        URL = input("[+] Please enter a URL: ")

        script_srcs = get_js_src(URL)

        for src in script_srcs:
            if src[0:1] == "/":
                src = URL + src
            data = find_keywords(src, data)
        
        data_df = pd.DataFrame(data)

        print(data_df)

        output_file = f"output.xlsx"

        data_df.to_excel(output_file, index=False)

        print(f"[+] DataFrame has been exported to {output_file}")
        
    except Exception as e:
        print("[-] Error fetching data")
        print(e)
    
    
        
        



