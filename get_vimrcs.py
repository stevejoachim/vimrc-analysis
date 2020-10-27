import pickle
import os
from time import sleep
from github import Github
from secrets.secrets import github_api_key
from constants import search_result_file

star_threshold = ">=50"
max_per_page = 50


def save_results(filename, repos_seen, all_vimrcs):
    print(f"Saving {len(all_vimrcs)} vimrc files")
    data = {"repos_seen": repos_seen, "all_vimrcs": all_vimrcs}
    with open(filename, "wb") as f:
        pickle.dump(data, f)


def check_rate_limit(g, repos_seen, all_vimrcs, VERBOSE, TEST):

    rate_limit = g.get_rate_limit()

    if TEST and repos_seen > 3:
        save_results(search_result_file, repos_seen, all_vimrcs)
        exit("Exceeded test limit")

    if rate_limit.core.remaining < 2:
        print("Exceeded core rate limit, waiting one hour")
        save_results(search_result_file, repos_seen, all_vimrcs)
        sleep(3630)

    if rate_limit.search.remaining < 2:
        print("Exceeded search rate limit, waiting one minute")
        save_results(search_result_file, repos_seen, all_vimrcs)
        sleep(65)

    # Diagnostics
    if VERBOSE:
        print("Rate limit search: ", rate_limit.search.remaining)
        print("Rate limit core: ", rate_limit.core.remaining)


def get_vimrcs(VERBOSE=False, TEST=False):

    # Open existing data file if it exists
    if os.path.isfile(search_result_file):
        with open(search_result_file, "rb") as f:
            data = pickle.load(f)
        all_vimrcs = data["all_vimrcs"]
        repos_seen = data["repos_seen"]
    else:
        all_vimrcs = {}
        repos_seen = 0

    g = Github(github_api_key, per_page=max_per_page)

    repos = g.search_repositories(
        "dotfiles OR vimrc",
        sort="stars",
        order="desc",
        **{"in": "name,description", "stars": star_threshold},
    )

    try:
        print(f"Starting at repo {repos_seen}")
        for repo in repos[repos_seen:]:

            # Get .vimrc files in this repo
            vimrcs = g.search_code("", repo=repo.full_name, filename=".vimrc")

            if VERBOSE:
                print("Repo: ", repo.full_name)
                print("Vimrc Count: ", vimrcs.totalCount)

            for vimrc in vimrcs:

                # Try to decode content and save info
                try:
                    decoded = vimrc.decoded_content
                except:
                    print("Couldn't decode ", vimrc.download_url)
                else:
                    # Save vimrc info
                    all_vimrcs[vimrc.download_url] = {
                        "repo": repo.full_name,
                        "stars": repo.stargazers_count,
                        "content": decoded,
                    }

                sleep(1)
                check_rate_limit(g, repos_seen, all_vimrcs, VERBOSE, TEST)

            sleep(1)
            repos_seen += 1
            check_rate_limit(g, repos_seen, all_vimrcs, VERBOSE, TEST)

    except Exception as e:
        print(e)
        save_results(search_result_file, repos_seen, all_vimrcs)
    else:
        print("Made it through all of the results")
        save_results(search_result_file, repos_seen, all_vimrcs)


if __name__ == "__main__":
    get_vimrcs(VERBOSE=True, TEST=False)

