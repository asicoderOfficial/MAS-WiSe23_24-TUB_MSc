
class PackageCounter:
    
    generated_packages = 0
    delivered_packages = 0
    
    @staticmethod
    def add_generated_package():
        PackageCounter.generated_packages += 1
    
    @staticmethod
    def add_delivered_package():
        PackageCounter.delivered_packages += 1