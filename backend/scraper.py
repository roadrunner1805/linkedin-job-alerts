import asyncio
import random
import logging
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from urllib.parse import quote

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LinkedInScraper:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        ]

    async def scrape_jobs(self, keyword, location):
        logger.info(f"Scraping jobs for keyword='{keyword}' in location='{location}'")
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=random.choice(self.user_agents)
            )
            page = await context.new_page()
            await Stealth().apply_stealth_async(page)

            # Construct the search URL for public jobs
            encoded_keyword = quote(keyword)
            encoded_location = quote(location)
            # f-constant to search for past 24 hours (f_TPR=r86400) or past week
            url = f"https://www.linkedin.com/jobs/search/?keywords={encoded_keyword}&location={encoded_location}&f_TPR=r604800"
            
            logger.info(f"Navigating to {url}")
            try:
                await page.goto(url, wait_until="load", timeout=60000)
                
                # Wait for results or "no results" indicator
                try:
                    await page.wait_for_selector(".jobs-search__results-list", timeout=10000)
                except:
                    logger.warning("Results list not found. Maybe no jobs or blocked.")
                    await browser.close()
                    return []

                # Scroll down to load more
                for _ in range(3):
                    await page.mouse.wheel(0, 1000)
                    await asyncio.sleep(random.uniform(1, 2))

                job_cards = await page.query_selector_all(".jobs-search__results-list li")
                jobs = []

                for card in job_cards:
                    try:
                        title_elem = await card.query_selector(".base-search-card__title")
                        company_elem = await card.query_selector(".base-search-card__subtitle")
                        location_elem = await card.query_selector(".job-search-card__location")
                        link_elem = await card.query_selector(".base-card__full-link")
                        
                        if title_elem and company_elem and link_elem:
                            title = (await title_elem.inner_text()).strip()
                            company = (await company_elem.inner_text()).strip()
                            location_str = (await location_elem.inner_text()).strip() if location_elem else ""
                            link = await link_elem.get_attribute("href")
                            
                            # Clean up link (remove tracking params)
                            link = link.split("?")[0] if link else ""
                            
                            # Extract ID from link or card
                            # Example: https://www.linkedin.com/jobs/view/software-engineer-at-company-3882938472
                            job_id = link.split("-")[-1] if "-" in link else link.split("/")[-1]
                            
                            jobs.append({
                                "linkedin_id": job_id,
                                "title": title,
                                "company": company,
                                "location": location_str,
                                "link": link
                            })
                    except Exception as e:
                        logger.error(f"Error parsing job card: {e}")
                        continue

                logger.info(f"Found {len(jobs)} jobs for '{keyword}'")
                await browser.close()
                return jobs

            except Exception as e:
                logger.error(f"Error during scraping: {e}")
                await browser.close()
                return []
