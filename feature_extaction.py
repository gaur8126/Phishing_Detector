import re
import socket
import whois
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from datetime import datetime
import ssl
import tldextract
import time

class URLFeatureExtractor:
    def __init__(self, url):
        self.url = url
        self.parsed_url = urlparse(url)
        self.domain = self.parsed_url.netloc
        self.soup = None
        self.response = None
        self.final_url = None
        self.redirect_count = 0
        self.external_objects = 0
        self.external_anchors = 0
        self.external_tags = 0
        self.favicon_source = None
        self.iframe_count = 0
        self.mouseover_scripts = 0
        self.right_click_disabled = False
        self.popups_detected = False
        self.form_handlers = []
        self.email_submissions = False
        self.page_rank = None
        self.google_indexed = None
        self.dns_records = None
        self.traffic_estimate = None
        self.statistical_report = None

        # Initialize with default values
        self.features = {
            'having_IP_Address': 1,
            'URL_Length': 1,
            'Shortining_Service': 1,
            'having_At_Symbol': 1,
            'double_slash_redirecting': 1,
            'Prefix_Suffix': 1,
            'having_Sub_Domain': 0,
            'SSLfinal_State': -1,
            'Domain_registeration_length': -1,
            'Favicon': 1,
            'port': 1,
            'HTTPS_token': 1,
            'Request_URL': 1,
            'URL_of_Anchor': 1,
            'Links_in_tags': 1,
            'SFH': 1,
            'Submitting_to_email': 1,
            'Abnormal_URL': 1,
            'Redirect': 1,
            'on_mouseover': 1,
            'RightClick': 1,
            'popUpWidnow': 1,
            'Iframe': 1,
            'age_of_domain': -1,
            'DNSRecord': -1,
            'web_traffic': -1,
            'Page_Rank': -1,
            'Google_Index': -1,
            'Links_pointing_to_page': -1,
            'Statistical_report': 1
        }

        try:
            self._fetch_url()
            self._analyze_features()
        except Exception as e:
            print(f"Error analyzing URL: {e}")

    def _fetch_url(self):
        """Fetch the URL content and handle redirects"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        try:
            self.response = requests.get(self.url, headers=headers, timeout=10, allow_redirects=True)
            self.final_url = self.response.url
            self.redirect_count = len(self.response.history)
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
        except requests.exceptions.RequestException:
            pass

    def _analyze_features(self):
        """Analyze all requested features"""
        # 1. IP Address check
        self._check_ip_address()

        # 2. URL Length
        self._check_url_length()

        # 3. Shortening Service
        self._check_shortening_service()

        # 4. @ Symbol
        self._check_at_symbol()

        # 5. Double slash redirecting
        self._check_double_slash()

        # 6. Prefix/Suffix (hyphen in domain)
        self._check_hyphen()

        # 7. Subdomains
        self._check_subdomains()

        # 8. SSL State
        self._check_ssl()

        # 9. Domain registration length
        self._check_domain_registration()

        # 10. Favicon
        self._check_favicon()

        # 11. Port
        self._check_port()

        # 12. HTTPS token
        self._check_https_token()

        # 13-16. External resources
        self._analyze_external_resources()

        # 17. Form submission
        self._check_forms()

        # 18. Abnormal URL
        self._check_abnormal_url()

        # 19. Redirects
        self._check_redirects()

        # 20-22. JavaScript behaviors
        self._check_javascript()

        # 23. Iframes
        self._check_iframes()

        # 24. Domain age
        self._check_domain_age()

        # 25. DNS Records
        self._check_dns()

        # 26. Web traffic (simulated)
        self._estimate_traffic()

        # 27. Page Rank (simulated)
        self._estimate_page_rank()

        # 28. Google Index
        self._check_google_index()

        # 29. Backlinks
        self._estimate_backlinks()

        # 30. Statistical reports
        self._check_statistical_reports()

    # Feature-specific methods
    def _check_ip_address(self):
        """Check if URL contains IP address"""
        ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        if re.search(ip_pattern, self.domain):
            self.features['having_IP_Address'] = -1

    def _check_url_length(self):
        """Check URL length"""
        if len(self.url) > 54:  # Threshold for suspicious length
            self.features['URL_Length'] = -1

    def _check_shortening_service(self):
        """Check for URL shortening services"""
        shorteners = ['bit.ly', 'goo.gl', 'tinyurl.com', 't.co', 'ow.ly']
        if any(s in self.domain for s in shorteners):
            self.features['Shortining_Service'] = -1

    def _check_at_symbol(self):
        """Check for @ symbol in URL"""
        if '@' in self.url:
            self.features['having_At_Symbol'] = -1

    def _check_double_slash(self):
        """Check for double slash redirecting"""
        if '//' in self.url.split('://')[1]:
            self.features['double_slash_redirecting'] = -1

    def _check_hyphen(self):
        """Check for hyphen in domain"""
        if '-' in self.domain.split('.')[0]:
            self.features['Prefix_Suffix'] = -1

    def _check_subdomains(self):
        """Count subdomains"""
        ext = tldextract.extract(self.url)
        subdomains = ext.subdomain.split('.')
        count = len([s for s in subdomains if s])

        if count == 0:
            self.features['having_Sub_Domain'] = 1
        elif count > 2:
            self.features['having_Sub_Domain'] = -1

    def _check_ssl(self):
        """Check SSL certificate"""
        try:
            hostname = self.parsed_url.hostname
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    if cert:
                        self.features['SSLfinal_State'] = 1
        except:
            pass

    def _check_domain_registration(self):
        """Check domain registration length"""
        try:
            domain_info = whois.whois(self.domain)
            if domain_info.creation_date:
                if isinstance(domain_info.creation_date, list):
                    creation_date = domain_info.creation_date[0]
                else:
                    creation_date = domain_info.creation_date

                expiry_date = domain_info.expiration_date
                if isinstance(expiry_date, list):
                    expiry_date = expiry_date[0]

                if creation_date and expiry_date:
                    reg_length = (expiry_date - creation_date).days
                    if reg_length > 365:  # More than 1 year
                        self.features['Domain_registeration_length'] = 1
            return domain_info
        except:
            pass

    def _check_favicon(self):
        """Check favicon source"""
        if not self.soup:
            return

        favicon = self.soup.find('link', rel='icon') or self.soup.find('link', rel='shortcut icon')
        if favicon and favicon.get('href'):
            favicon_url = urljoin(self.url, favicon['href'])
            if self.domain not in favicon_url:
                self.features['Favicon'] = -1

    def _check_port(self):
        """Check for non-standard ports"""
        if self.parsed_url.port and self.parsed_url.port not in [80, 443]:
            self.features['port'] = -1

    def _check_https_token(self):
        """Check for misleading HTTPS in path"""
        path = self.parsed_url.path.lower()
        if 'https' in path and not self.parsed_url.scheme == 'https':
            self.features['HTTPS_token'] = -1

    def _analyze_external_resources(self):
        """Analyze external resources, anchors, and tags"""
        if not self.soup:
            return

        base_domain = self.parsed_url.netloc
        tags = self.soup.find_all(['img', 'script', 'link', 'iframe'])

        for tag in tags:
            src = tag.get('src') or tag.get('href')
            if src:
                parsed_src = urlparse(src)
                if parsed_src.netloc and base_domain not in parsed_src.netloc:
                    self.external_objects += 1

        # Anchors
        anchors = self.soup.find_all('a', href=True)
        for a in anchors:
            href = a['href']
            parsed_href = urlparse(href)
            if parsed_href.netloc and base_domain not in parsed_href.netloc:
                self.external_anchors += 1

        # Meta, script, link tags
        meta_tags = self.soup.find_all(['meta', 'script', 'link'])
        for tag in meta_tags:
            src = tag.get('src') or tag.get('href') or tag.get('content')
            if src:
                parsed_src = urlparse(src)
                if parsed_src.netloc and base_domain not in parsed_src.netloc:
                    self.external_tags += 1

        # Set features based on thresholds
        if self.external_objects > 5:
            self.features['Request_URL'] = -1
        if self.external_anchors / len(anchors) > 0.5 if anchors else False:
            self.features['URL_of_Anchor'] = -1
        if self.external_tags > 5:
            self.features['Links_in_tags'] = -1

    def _check_forms(self):
        """Check form handlers and email submissions"""
        if not self.soup:
            return

        forms = self.soup.find_all('form')
        for form in forms:
            action = form.get('action', '').lower()
            if action:
                if 'mailto:' in action or 'email' in action:
                    self.email_submissions = True

                if self.domain not in action and action.startswith('http'):
                    self.form_handlers.append(action)

        if self.email_submissions:
            self.features['Submitting_to_email'] = -1
        if any(h for h in self.form_handlers if self.domain not in h):
            self.features['SFH'] = -1

    def _check_abnormal_url(self):
        """Check for abnormal URL structure"""
        # Check for excessive special characters
        special_chars = re.findall(r'[^\w\-\.\/\:]', self.url)
        if len(special_chars) > 5:  # Threshold
            self.features['Abnormal_URL'] = -1

        # Check for encoding
        if '%' in self.url:
            self.features['Abnormal_URL'] = -1

    def _check_redirects(self):
        """Check redirect count"""
        if self.redirect_count > 2:
            self.features['Redirect'] = -1

    def _check_javascript(self):
        """Check JavaScript behaviors"""
        if not self.soup:
            return

        scripts = self.soup.find_all('script')
        for script in scripts:
            if script.string and 'onmouseover' in script.string.lower():
                self.mouseover_scripts += 1
            if script.string and 'event.button==2' in script.string.lower():
                self.right_click_disabled = True
            if script.string and 'window.open' in script.string.lower():
                self.popups_detected = True

        if self.mouseover_scripts > 0:
            self.features['on_mouseover'] = -1
        if self.right_click_disabled:
            self.features['RightClick'] = -1
        if self.popups_detected:
            self.features['popUpWidnow'] = -1

    def _check_iframes(self):
        """Check for iframes"""
        if not self.soup:
            return

        iframes = self.soup.find_all('iframe')
        self.iframe_count = len(iframes)
        if self.iframe_count > 0:
            self.features['Iframe'] = -1

    def _check_domain_age(self):
        """Check domain age"""
        try:
            domain_info = whois.whois(self.domain)
            if domain_info.creation_date:
                if isinstance(domain_info.creation_date, list):
                    creation_date = domain_info.creation_date[0]
                else:
                    creation_date = domain_info.creation_date

                age = (datetime.now() - creation_date).days
                if age > 365:  # Older than 1 year
                    self.features['age_of_domain'] = 1
        except:
            pass

    def _check_dns(self):
        """Check DNS records (simplified)"""
        try:
            # Try to resolve domain
            socket.gethostbyname(self.domain)
            self.features['DNSRecord'] = 1
        except:
            pass

    def _estimate_traffic(self):
        """Simulate traffic estimation (would use API in real implementation)"""
        # In a real implementation, use SimilarWeb API or similar
        self.features['web_traffic'] = -1  # Default to low traffic

    def _estimate_page_rank(self):
        """Simulate page rank (would use API in real implementation)"""
        # In a real implementation, use Moz API or similar
        self.features['Page_Rank'] = -1  # Default to low rank

    def _check_google_index(self):
        """Check if site is indexed by Google (simplified)"""
        # In a real implementation, use Google Search Console API
        self.features['Google_Index'] = -1  # Default to not indexed

    def _estimate_backlinks(self):
        """Estimate backlinks (simplified)"""
        # In a real implementation, use Ahrefs/Moz API
        self.features['Links_pointing_to_page'] = -1  # Default to few links

    def _check_statistical_reports(self):
        """Check statistical reports (simplified)"""
        # In a real implementation, check phishing databases
        self.features['Statistical_report'] = 1  # Default to not reported

    def get_features(self):
        """Return all features as a dictionary"""
        return self.features

# Example usage
if __name__ == "__main__":
    test_url = "https://github.com"#"http://sub1.sub2.sub3.218.184.94.129:8080//xq5i8/ulztqrnheddl2ypvb5ltw48sv3x4fsvftx3txa6ggx3ocoipcomo4fy7l36v7jy8ew3za1fdu34/%20%3F%236eky2/https-secure?u=http%3A%2F%2Fexternal-site.com&l=mailto%3Aadmin%40k8vv4x.com&a=http%3A%2F%2Fcdn-service.net%2Fform&s=http%3A%2F%2Fthird-party.org%2Fscript.js&r=4&m=onmouseover%3Dalert%281%29&rc=disabled&p=popup%3D1&i=iframe%3D1&f=http%3A%2F%2Fexternal-site.com%2Ffavicon.ico"  # Replace with your URL
    extractor = URLFeatureExtractor(test_url)
    features = extractor.get_features()

    print(f"Analysis for: {test_url}")
    # for feature, value in features.items():
    #     print(f"{feature}: {value}")
    print(list(features.values()))
    print(len(features))