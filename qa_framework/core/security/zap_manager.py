import time
from typing import List, Dict, Any
from zapv2 import ZAPv2
from qa_framework.core.config import settings
from qa_framework.core.logger import get_logger

logger = get_logger("zap_manager")

class ZapManager:
    """
    Manager for OWASP ZAP (Zed Attack Proxy) integration.
    Allows controlling ZAP via API to run spiders and retrieve alerts.
    """

    def __init__(self):
        if not settings.USE_ZAP_PROXY:
            logger.warning("USE_ZAP_PROXY is False. ZapManager might not work if traffic isn't routed.")
        
        self.zap = ZAPv2(proxies={'http': settings.ZAP_BASE_URL, 'https': settings.ZAP_BASE_URL}, 
                         apikey=settings.ZAP_API_KEY)
        self.base_url = settings.ZAP_BASE_URL

    def spider(self, target_url: str):
        """
        Starts the ZAP Spider on the target URL.
        """
        logger.info(f"Starting ZAP Spider on {target_url}")
        scan_id = self.zap.spider.scan(target_url)
        
        # Wait for spider to finish
        while int(self.zap.spider.status(scan_id)) < 100:
            logger.info(f"Spider progress: {self.zap.spider.status(scan_id)}%")
            time.sleep(2)
        
        logger.info("Spider completed")

    def active_scan(self, target_url: str):
        """
        Starts the ZAP Active Scan. 
        WARNING: This is aggressive and takes time.
        """
        logger.info(f"Starting ZAP Active Scan on {target_url}")
        scan_id = self.zap.ascan.scan(target_url)
        
        while int(self.zap.ascan.status(scan_id)) < 100:
            logger.info(f"Active Scan progress: {self.zap.ascan.status(scan_id)}%")
            time.sleep(5)
            
        logger.info("Active Scan completed")

    def get_alerts(self, base_url: str, risk_level: str = None) -> List[Dict[str, Any]]:
        """
        Retrieves alerts from ZAP.
        risk_level: Optional filter ('High', 'Medium', 'Low', 'Informational')
        """
        alerts = self.zap.core.alerts(baseurl=base_url)
        
        if risk_level:
            alerts = [a for a in alerts if a.get('risk') == risk_level]
            
        return alerts

    def generate_report(self):
        """
        Generates HTML report.
        """
        # This is a placeholder as ZAP API for reports varies by version or needs export
        # usually report = self.zap.core.htmlreport()
        # writing to file...
        pass
