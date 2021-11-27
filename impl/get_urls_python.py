# from github import Github

# g = Github()
import time
from github import Github
from configparser import ConfigParser
import os
import re
import threading as th

config = ConfigParser()
config.read('config.ini')
token = config.get('auth', 'token')
url = "https://api.github.com"

filename = "serverless"
pattern = "serverless-step-functions"

interval = 20
g = Github(token)

# files = g.search_code(
#     "filename:{}+yml".format(filename), page=1)

files = g.search_code(
    query="serverless -created:2020-10-08")
links = []

keep_going = True


def key_capture_thread():
    global keep_going
    input()
    keep_going = False


def get_repos():
    i = 0
    links = []
    all_links = []
    th.Thread(target=key_capture_thread, args=(),
              name='key_capture_thread', daemon=True).start()

    files = g.search_code(query="filename:serverless+yml created:2020-10-08")

    while keep_going:
        try:
            for i in range(1, 10000000):
                page = files.get_page(i)
                for f in page:
                    all_links.append(f.repository.full_name)
                    print(f.repository.full_name)
                time.sleep(60)
        except Exception as e:
            print(e)
            break
    return links, all_links

    # while keep_going:
    #     try:
    #         txt = files[i].decoded_content.decode("utf-8")
    #         print(files[i])
    #         # txt = files[i].decoded_content.decode("utf-16")
    #         # print(txt)
    #         txt = re.sub("\n", "", txt)
    #         print(i)
    #         all_links.append("https://www.github.com/" +
    #                          files[i].repository.full_name)
    #         if re.search(pattern, txt):
    #             links.append("https://www.github.com/" +
    #                          files[i].repository.full_name)
    #             print(links[-1])
    #         i += 1
    #         time.sleep(2)
    #     except Exception as e:
    #         print(e)
    #         return links, all_links

    # return links, all_links


links, all_links = get_repos()

with open("links.txt", "w") as f:
    for link in links:
        f.write(link+"\n")

with open("all_links.txt", "w") as f:
    for link in all_links:
        f.write(link+"\n")


print("PROCESS SUCCESSFULLY COMPLETED")
# get_repos()
# {
#   for (( i=500; i<=10000; i+=$interval ))
#   do
#     j=$((i+interval-1))
#     last_repo_page=$( curl -s --head -H "$token_cmd" "$url/search/code?q=filename:$keyword+size:$i..$j+extension:yml&per_page=100" | sed -nE 's/^Link:.*per_page=100.page=([0-9]+)>; rel="last".*/\1/p' )

#     if [[ "$last_repo_page" == "" ]]; then
#       echo "Fetching repository list for $keyword filename"
#       all_repos=($( curl -s -H "$token_cmd" "$url/search/code?q=filename:$keyword+size:$i..$j+extension:yml&per_page=100" | jq --raw-output '.items[].html_url' | tr '\n' ' ' ))
#       output_list
#       total_repos=$( echo "${all_repos[@]}" | wc -w | tr -d "[:space:]" )
#       echo
#       echo "Total # of repositories for size:$i..$j: $total_repos"
#       echo "List saved to result-$today.txt"
#     else
#       echo "Fetching repository list for $keyword filename"
#       all_repos=()
#       for (( k=1; k<=$last_repo_page; k++ ))
#       do
#         working
#         paginated_repos=$( curl -s -H "$token_cmd" "$url/search/code?q=filename:$keyword+size:$i..$j+extension:yml&per_page=100&page=$k" | jq --raw-output '.items[].html_url' | tr '\n' ' ' )
#         all_repos=(${all_repos[@]} $paginated_repos)
#       done
#       work_done
#       output_list
#       total_repos=$( echo "${all_repos[@]}" | wc -w | tr -d "[:space:]" )
#       echo "Total # of repositories for size:$i..$j: $total_repos"
#       echo "List saved to result-$today.txt"
#     fi
#   done
# }
