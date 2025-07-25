import utils

def test_all_scrapers():
    query = "Software Engineer"
    print(f"--- Testing all scrapers for query: '{query}' ---")

    print("\n--- Testing LinkedIn ---")
    linkedin_jobs = utils.scrape_linkedin(query)
    print(f"Found {len(linkedin_jobs)} jobs on LinkedIn.")
    # print(linkedin_jobs)

    print("\n--- Testing Upwork ---")
    upwork_jobs = utils.scrape_upwork(query)
    print(f"Found {len(upwork_jobs)} jobs on Upwork.")
    # print(upwork_jobs)

    print("\n--- Testing Fiverr ---")
    fiverr_jobs = utils.scrape_fiverr(query)
    print(f"Found {len(fiverr_jobs)} jobs on Fiverr.")
    # print(fiverr_jobs)

    print("\n--- Testing Indeed ---")
    indeed_jobs = utils.scrape_indeed(query)
    print(f"Found {len(indeed_jobs)} jobs on Indeed.")
    # print(indeed_jobs)

    print("\n--- Testing Naukri.com ---")
    naukri_jobs = utils.scrape_naukri(query)
    print(f"Found {len(naukri_jobs)} jobs on Naukri.com.")
    # print(naukri_jobs)

    print("\n--- Testing Internshala ---")
    internshala_jobs = utils.scrape_internshala(query)
    print(f"Found {len(internshala_jobs)} jobs on Internshala.")
    # print(internshala_jobs)

if __name__ == "__main__":
    test_all_scrapers()