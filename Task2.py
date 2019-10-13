from packaging import version 

class Version:
    def __init__(self, version):
        self.version = version
    
    def __ne__(self, other):
        return version.parse(self.version) != version.parse(other.version)
    
    def __eq__(self, other):
        return version.parse(self.version) == version.parse(other.version)    
    
    def __lt__(self, other):
        return version.parse(self.version) < version.parse(other.version)
    
    def __gt__(self, other):
        return version.parse(self.version) > version.parse(other.version)
    
    def __le__(self, other):
        return version.parse(self.version) <= version.parse(other.version)
    
    def __ge__(self, other):
        return version.parse(self.version) >= version.parse(other.version)

def main():
    to_test = [
        ('1.0.0', '2.0.0'),
        ('1.0.0', '1.42.0'),
        ('1.2.0', '1.2.42'),
        ('1.1.0-alpha', '1.2.0-alpha.1'),
        ('1.0.1b', '1.0.10-alpha.beta'),
        ('1.0.0-rc.1', '1.0.0'),
    ]

    assert Version("1.0.0") < Version("2.0.0")
    assert Version("1.0.0") < Version("1.42.0")
    assert Version("1.2.0") < Version("1.2.42")
    print(Version('1.3.42') == Version('42.3.1'))

if __name__ == "__main__":
    main()
