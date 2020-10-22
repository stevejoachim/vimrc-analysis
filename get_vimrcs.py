import pickle
import os
from github import Github
from secrets.secrets import github_api_key
from constants import search_result_file


def get_vimrcs(VERBOSE=False, TEST=True):
    max_per_page = 100
    g = Github(github_api_key, per_page=max_per_page)
    search_results = g.search_code("", filename=".vimrc")

    # Can submit 30 search reqs/min, each returning 100 files
    # All other reqs are subject to 5000 reqs/hr
    i = 0
    vimrcs = []
    for result in search_results:

        # Try to decode content
        try:
            decoded = result.decoded_content
        except:
            continue
        # Save vimrc info
        vimrcs.append({
            "repo": result.repository.name,
            "stars": result.repository.stargazers_count,
            "url": result.download_url,
            "content": result.decoded
        })

        # Break or wait if exceeding rate limit
        rate_limit = g.get_rate_limit()
        i += 1
        if TEST and i > 100:
            break
        if rate_limit.core.remaining == 0:
            break  # wait until rate_limit.core.reset
        if rate_limit.search.remaining == 0:
            break  # wait until rate_limit.search.reset

        # Diagnostics
        if VERBOSE:
            print("-----------------------")
            print("Rate limit search: ", rate_limit.search.remaining)
            print("Rate limit core: ", rate_limit.core)

    # Save results

    with open(search_result_file,'wb') as f:
        pickle.dump(vimrcs, f)
