from ddgs import DDGS

results = DDGS().text("Focus on Debian 12 and Debian 10, the impact, attacking path and fix solutions for Vulnerability CVE-2024-36971", max_results=5)
print(results)